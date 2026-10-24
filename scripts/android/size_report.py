#!/usr/bin/env python3
"""Measure a neutral AAB's arm64/de download using pinned bundletool.

Category figures are measured marginal gzip-download contributions: run
bundletool get-size again on disposable diagnostic APK sets with each category
removed. Surviving compressed ZIP entry bytes are preserved, not re-encoded.
These contributions are not additive. Diagnostic sets are never installable or
uploaded; the original bundle is never changed. No signing key is used/created.
"""
import argparse
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import upload_signing
from build import git_provenance

MB = 1_000_000
# Internal budget; adapt to the applicable Play limit, not a claimed Play limit.
BASE_WARNING_BYTES = 190 * MB
DEVICE = {'supportedAbis': ['arm64-v8a'], 'supportedLocales': ['de'],
          'screenDensity': 480, 'sdkVersion': 36}
CATEGORIES = ('speech', 'music', 'graphics', 'engine', 'other')


def parse_size(text):
    rows = list(csv.DictReader(io.StringIO(text.strip())))
    if len(rows) != 1 or set(rows[0]) != {'MIN', 'MAX'}:
        raise ValueError('Expected one numeric MIN,MAX row from bundletool')
    row = rows[0]
    if any(not re.fullmatch(r'[0-9]+', row[k] or '') for k in ['MIN', 'MAX']):
        raise ValueError('bundletool must report raw integer bytes, not formatted estimates')
    result = {'min_bytes': int(row['MIN']), 'max_bytes': int(row['MAX'])}
    if result['min_bytes'] > result['max_bytes']:
        raise ValueError('Reversed bundletool size interval')
    return result


def difference(whole, part):
    return {'min_bytes': whole['min_bytes'] - part['max_bytes'],
            'max_bytes': whole['max_bytes'] - part['min_bytes']}


def base_budget(base):
    return {'warning_bytes': BASE_WARNING_BYTES,
            'status': 'WARN' if base['max_bytes'] > BASE_WARNING_BYTES else 'PASS'}


def category(name):
    name = name.replace('\\', '/')
    leaf = name.rsplit('/', 1)[-1]
    if 'assets/voice/' in name or leaf.startswith('voice_'):
        return 'speech'
    if 'assets/music/' in name or leaf.endswith('.oggvorbisstr'):
        return 'music'
    if leaf.endswith(('.ctex', '.png', '.webp', '.svg')):
        return 'graphics'
    if re.search(r'(^|/)lib/[^/]+/[^/]+\.so$', name) or re.fullmatch(r'classes[0-9]*\.dex', leaf):
        return 'engine'
    return 'other'


def _copy_bytes(source, destination, count):
    while count:
        data = source.read(min(count, 1024 * 1024))
        if not data:
            raise ValueError('Truncated diagnostic APK')
        destination.write(data)
        count -= len(data)


def _central_directory_offset(stream):
    stream.seek(0, os.SEEK_END)
    length = stream.tell()
    stream.seek(max(0, length - 65557))
    tail = stream.read()
    for offset in range(len(tail) - 22, -1, -1):
        if tail[offset:offset + 4] != b'PK\x05\x06':
            continue
        end = struct.unpack_from('<4s4H2IH', tail, offset)
        if offset + 22 + end[7] != len(tail):
            continue
        if end[1] or end[2] or end[3] != end[4] or end[4] == 65535 or end[6] == 0xffffffff:
            raise ValueError('Diagnostic ZIP32 APK required; multi-disk/ZIP64 is unsupported')
        return end[6]
    raise ValueError('Missing APK ZIP end record')


def filter_apk(source, destination, excluded):
    """Remove one category with raw ZIP copies, preserving compression exactly.

    Rebuild only the ZIP central directory/offsets according to the ZIP32 spec.
    Retained local headers, compressed data, descriptors and padding are copied
    verbatim. This is a measurement probe, deliberately not an installable APK.
    """
    with zipfile.ZipFile(source) as archive, open(source, 'rb') as raw:
        infos = archive.infolist()
        if len({i.filename for i in infos}) != len(infos):
            raise ValueError('Duplicate APK entries')
        removed = {i.filename for i in infos if not i.is_dir() and category(i.filename) == excluded}
        if not removed:
            shutil.copyfile(source, destination)
            return 0
        central = _central_directory_offset(raw)
        ordered = sorted(infos, key=lambda i: i.header_offset)
        offsets = {}
        with open(destination, 'wb') as target:
            if ordered:
                raw.seek(0)
                _copy_bytes(raw, target, ordered[0].header_offset)
            for index, entry in enumerate(ordered):
                end = ordered[index + 1].header_offset if index + 1 < len(ordered) else central
                if end < entry.header_offset:
                    raise ValueError('Invalid diagnostic APK offsets')
                if entry.filename in removed:
                    continue
                offsets[entry.filename] = target.tell()
                raw.seek(entry.header_offset)
                _copy_bytes(raw, target, end - entry.header_offset)
            start = target.tell()
            for entry in infos:
                if entry.filename not in offsets:
                    continue
                name = entry.filename.encode('utf-8' if entry.flag_bits & 0x800 else 'cp437')
                year, month, day, hour, minute, second = entry.date_time
                dos_time = (hour << 11) | (minute << 5) | (second // 2)
                dos_date = ((year - 1980) << 9) | (month << 5) | day
                target.write(struct.pack('<4s6H3I5H2I', b'PK\x01\x02', entry.create_version | (entry.create_system << 8),
                    entry.extract_version, entry.flag_bits, entry.compress_type, dos_time, dos_date,
                    entry.CRC, entry.compress_size, entry.file_size, len(name), len(entry.extra),
                    len(entry.comment), 0, entry.internal_attr, entry.external_attr, offsets[entry.filename]))
                target.write(name + entry.extra + entry.comment)
            end = target.tell()
            target.write(struct.pack('<4s4H2IH', b'PK\x05\x06', 0, 0, len(offsets), len(offsets),
                                     end - start, start, len(archive.comment)))
            target.write(archive.comment)
    return len(removed)


def diagnostic_set(original, target, excluded, work):
    removed = 0
    with zipfile.ZipFile(original) as source, zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_STORED) as dest:
        for info in source.infolist():
            if not info.filename.endswith('.apk'):
                with source.open(info) as reader, dest.open(info.filename, 'w') as writer:
                    shutil.copyfileobj(reader, writer)
                continue
            apk, filtered = work / 'source.apk', work / 'filtered.apk'
            with source.open(info) as reader, apk.open('wb') as writer:
                shutil.copyfileobj(reader, writer)
            removed += filter_apk(apk, filtered, excluded)
            dest.write(filtered, info.filename, compress_type=zipfile.ZIP_STORED)
            apk.unlink()
            filtered.unlink()
    return removed


def run(command, env, log):
    result = subprocess.run([str(x) for x in command], env=env, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True, timeout=600, check=False)
    log.write_text(result.stdout + '\n' + result.stderr)
    if result.returncode:
        print('::error::bundletool size measurement failed: ' + log.name)
        for line in (result.stdout + '\n' + result.stderr).splitlines()[-20:]:
            print('  | ' + line)
        raise ValueError('bundletool failed; inspect ' + log.name)
    return result.stdout


def render(report):
    def value(interval):
        low, high = interval['min_bytes'] / MB, interval['max_bytes'] / MB
        return f'{low:.3f}' if low == high else f'{low:.3f}–{high:.3f}'
    lines = ['# Neutral Android download measurement', '',
             'Device: arm64-v8a, German, API 36, 480 dpi. MB = 1,000,000 bytes.', '',
             '| bundletool download estimate | MB |', '|---|---:|',
             f'| Initial download, including install-time assets | {value(report["initial_download"])} |',
             f'| Base module | {value(report["base_module"])} |',
             f'| Additional install-time assets (difference) | {value(report["install_time_assets"])} |', '',
             '| Category: marginal bundletool download contribution | MB |', '|---|---:|']
    lines += [f'| {name} | {value(data["marginal_download"])} |' for name, data in report['categories'].items()]
    lines += ['', 'Category figures come from bundletool runs on diagnostic copies with each category removed.',
              'Surviving compressed entries are copied verbatim. Marginals include ZIP/gzip interactions,',
              'are not additive and are not independent installable downloads.', '',
              'Internal base budget: ' + str(report['base_budget']['warning_bytes'] // MB) + ' MB. Status: ' + report['base_budget']['status'] + '.',
              'This budget is not the current Play limit. Play Console uses a similar, non-identical calculation.',
              'Measurement APK sets are unsigned, ephemeral and not installable; no signing key is used.',
              'No audio/graphics were transcoded. No Play upload/readiness approval is implied.', '']
    return '\n'.join(lines)


def measure(bundle, tools, output):
    bundle, tools, output = bundle.resolve(), tools.resolve(), output.resolve()
    if not bundle.is_file():
        raise ValueError('Input AAB does not exist')
    with zipfile.ZipFile(bundle) as archive:
        casts = [n for n in archive.namelist() if n.endswith('/assets/quest/cast.json')]
        if len(casts) != 1 or json.loads(archive.read(casts[0]))['variant'] != 'public':
            raise ValueError('Size report accepts only the neutral/public cast')
    lock = json.loads((ROOT / 'scripts/android/toolchain.json').read_text())
    tool = tools / ('android-tools/bundletool-' + lock['bundletool_version'] + '.jar')
    if hashlib.sha256(tool.read_bytes()).hexdigest() != lock['bundletool_sha256']:
        raise ValueError('Pinned bundletool checksum mismatch')
    original_hash = hashlib.sha256(bundle.read_bytes()).hexdigest()
    output.mkdir(parents=True, exist_ok=False)
    spec = output / 'device.json'
    spec.write_text(json.dumps(DEVICE, indent=2) + '\n')
    with tempfile.TemporaryDirectory(prefix='kinderwelt-size.') as temporary:
        work = Path(temporary)
        home = work / 'jvm-home'
        home.mkdir()
        env = upload_signing.export_environment()
        env['ANDROID_USER_HOME'] = str(home / 'android')
        env.pop('ANDROID_SDK_HOME', None)
        env.pop('JAVA_TOOL_OPTIONS', None)
        env.pop('_JAVA_OPTIONS', None)
        java = [tools / 'android-jdk/bin/java', '-Xmx1024m', '-Duser.home=' + str(home), '-jar', tool]
        apks = work / 'reference.apks'
        run(java + ['build-apks', '--bundle=' + str(bundle), '--output=' + str(apks),
                    '--device-spec=' + str(spec), '--aapt2=' + str(tools / 'android-sdk/build-tools/36.1.0/aapt2'),
                    '--max-threads=2'], env, output / 'build-apks.log')
        if list(home.rglob('*.keystore')) or list(home.rglob('*.jks')):
            raise ValueError('Size measurement unexpectedly created signing material')

        def size(path, label, module=None):
            args = ['get-size', 'total', '--apks=' + str(path), '--device-spec=' + str(spec)]
            if module:
                args.append('--modules=' + module)
            text = run(java + args, env, output / (label + '.log'))
            result = parse_size(text)
            (output / (label + '.csv')).write_text(text)
            return result

        total, base = size(apks, 'total'), size(apks, 'base', 'base')
        categories = {}
        for name in CATEGORIES:
            probe = work / 'diagnostic.apks'
            removed = diagnostic_set(apks, probe, name, work)
            without = size(probe, 'without-' + name)
            categories[name] = {'removed_entries': removed, 'without_category': without,
                                'marginal_download': difference(total, without)}
            probe.unlink()
    if hashlib.sha256(bundle.read_bytes()).hexdigest() != original_hash:
        raise ValueError('Source bundle changed during measurement')
    budget = base_budget(base)
    report = {'schema': 1, 'bundle': bundle.name, 'bundle_sha256': original_hash,
              'bundletool': lock['bundletool_version'], 'jdk': lock['java'], 'device': DEVICE,
              'measurement_source': git_provenance(ROOT),
              'initial_download': total, 'base_module': base,
              'install_time_assets': difference(total, base), 'categories': categories,
              'category_method': 'Marginal bundletool get-size on raw-copy filtered, non-installable diagnostic APK sets; not additive',
              'measurement_signing': 'UNSIGNED; isolated JVM home, no keystore used or created',
              'source_bundle_unchanged': True, 'base_budget': budget, 'play_readiness': 'NOT VERIFIED'}
    (output / 'size-report.json').write_text(json.dumps(report, indent=2) + '\n')
    (output / 'SIZE_REPORT.md').write_text(render(report))
    print('::notice title=Neutral arm64/de download::bundletool initial=' + str(total['max_bytes'])
          + ' bytes; base=' + str(base['max_bytes']) + ' bytes; install-time assets='
          + str(report['install_time_assets']['max_bytes']) + ' bytes')
    print('::notice title=Marginal download contributions::' + '; '.join(
        name + '=' + str(data['marginal_download']['max_bytes']) + ' bytes' for name, data in categories.items()))
    if os.environ.get('GITHUB_STEP_SUMMARY'):
        with open(os.environ['GITHUB_STEP_SUMMARY'], 'a') as summary:
            summary.write(render(report) + '\n')
    if budget['status'] == 'WARN':
        print('::warning::Base module exceeds the internal ' + str(BASE_WARNING_BYTES // MB) + ' MB budget; inspect the size report. This is not the current Play limit.')
    print(render(report))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle', type=Path, required=True)
    parser.add_argument('--tools', type=Path, default=Path('/workspace/tools'))
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        measure(args.bundle, args.tools, args.output)
    except (ValueError, OSError, zipfile.BadZipFile, subprocess.TimeoutExpired) as error:
        parser.exit(1, 'Size report failed: ' + str(error) + '\n')


if __name__ == '__main__':
    main()
