"""Required upstream notices, shared by filter checks and actual APK/AAB checks."""
import configparser
import fnmatch
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MUSIC_LICENSES = ['CC-BY-SA-4.0.txt', 'CC-BY-3.0.txt', 'CC-BY-SA-3.0.txt',
                  'CC-BY-SA-2.5.txt', 'tnm-MIT.txt', 'GeneralUser-GS.txt']


def required():
    return ['assets/music/NOTICES.txt', 'assets/quest/OFL.txt', 'assets/licenses/Kinderwelt-MIT.txt'] + [
        'assets/music/licenses/' + name for name in MUSIC_LICENSES] + [
        'assets/voice/quest/' + locale + '/' + name
        for locale in ['de', 'en', 'ru'] for name in ['MODEL_CARD.txt', 'LICENSE.txt']]


def check_filters(root=ROOT):
    root = Path(root)
    config = configparser.ConfigParser(interpolation=None)
    config.read(root / 'export_presets.cfg')
    presets = [s for s in config.sections() if s.startswith('preset.') and not s.endswith('.options')]
    if len(presets) != 2:
        raise ValueError('Expected both Android export presets for notice verification')
    for preset in presets:
        includes = config[preset]['include_filter'].strip('"').split(',')
        excludes = config[preset]['exclude_filter'].strip('"').split(',')
        for name in required():
            if not (root / name).is_file():
                raise ValueError('Required source notice is missing: ' + name)
            if not any(fnmatch.fnmatchcase(name, p) for p in includes) or any(fnmatch.fnmatchcase(name, p) for p in excludes):
                raise ValueError('Notice is excluded from ' + preset + ': ' + name)
    return len(required())


def check_archive(archive, root=ROOT):
    root = Path(root)
    names = archive.namelist()
    for name in required():
        matches = [n for n in names if 'assets/' in n and n.split('assets/', 1)[1] == name]
        if len(matches) != 1:
            raise AssertionError('Missing or duplicate bundled notice: ' + name)
        if archive.read(matches[0]) != (root / name).read_bytes():
            raise AssertionError('Bundled notice differs from tested source: ' + name)
    return {'status': 'PASS', 'files_checked': len(required())}
