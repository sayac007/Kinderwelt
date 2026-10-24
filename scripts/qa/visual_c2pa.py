#!/usr/bin/env python3
"""Read bounded local PNG Content Credentials and owner CSV; never verify rights.

This is a metadata reader, NOT a C2PA validator. No signature, certificate trust,
timestamp authority, assertion hash or asset binding is authenticated. No network
client is used. PNG chunk CRC checks detect corruption, not forged credentials.
"""
import argparse
import csv
import hashlib
import json
import struct
import zlib
from pathlib import Path


class _CBOR:
    """Bounded definite-length CBOR subset used by claim/action assertions."""

    def __init__(self, raw):
        self.raw, self.pos, self.items = raw, 0, 0

    def take(self, size):
        if size < 0 or self.pos + size > len(self.raw):
            raise ValueError('Truncated CBOR')
        value = self.raw[self.pos:self.pos + size]
        self.pos += size
        return value

    def item(self, depth=0):
        self.items += 1
        if depth > 16 or self.items > 4096:
            raise ValueError('CBOR bounds exceeded')
        first = self.take(1)[0]
        major, extra = first >> 5, first & 31
        if extra < 24:
            value = extra
        elif extra in (24, 25, 26, 27):
            value = int.from_bytes(self.take(1 << (extra - 24)), 'big')
        else:
            raise ValueError('Indefinite/reserved CBOR is not supported')
        if major == 0:
            return value
        if major == 1:
            return -1 - value
        if major in (2, 3):
            data = self.take(value)
            return data if major == 2 else data.decode('utf-8')
        if major == 4:
            if value > 4096:
                raise ValueError('CBOR array too large')
            return [self.item(depth + 1) for _ in range(value)]
        if major == 5:
            if value > 4096:
                raise ValueError('CBOR map too large')
            result = {}
            for _ in range(value):
                key = self.item(depth + 1)
                if not isinstance(key, (str, int, bytes)) or key in result:
                    raise ValueError('Unsupported/duplicate CBOR key')
                result[key] = self.item(depth + 1)
            return result
        if major == 6:
            # Preserve the date value without treating its tag as authentication.
            return self.item(depth + 1)
        if major == 7 and extra in (20, 21, 22):
            return {20: False, 21: True, 22: None}[extra]
        raise ValueError('Unsupported CBOR value')


def _decode_cbor(raw):
    decoder = _CBOR(raw)
    value = decoder.item()
    if decoder.pos != len(raw):
        raise ValueError('Trailing CBOR data')
    return value


def _boxes(raw, depth=0):
    if depth > 8:
        raise ValueError('JUMBF nesting too deep')
    pos, label = 0, ''
    while pos < len(raw):
        if len(raw) - pos < 8:
            raise ValueError('Truncated JUMBF box')
        size, kind = struct.unpack_from('>I4s', raw, pos)
        header = 8
        if size == 1:
            if len(raw) - pos < 16:
                raise ValueError('Truncated extended JUMBF box')
            size = struct.unpack_from('>Q', raw, pos + 8)[0]
            header = 16
        elif size == 0:
            size = len(raw) - pos
        if size < header or pos + size > len(raw):
            raise ValueError('Invalid JUMBF box length')
        payload = raw[pos + header:pos + size]
        if kind == b'jumd':
            if len(payload) < 17:
                raise ValueError('Truncated JUMBF descriptor')
            label = payload[17:].split(b'\0', 1)[0].decode('utf-8') if payload[16] & 2 else ''
        yield label, kind, payload
        if kind == b'jumb':
            yield from _boxes(payload, depth + 1)
        pos += size


def png_credentials(raw):
    result = {'status': 'absent', 'cryptographic_validation': 'not_performed',
              'signature_verified': False, 'certificate_trust_verified': False,
              'asset_binding_verified': False}
    if not raw.startswith(b'\x89PNG\r\n\x1a\n'):
        return dict(result, status='not_png')
    pos, chunks = 8, []
    try:
        while pos < len(raw):
            if len(raw) - pos < 12:
                raise ValueError('Truncated PNG chunk')
            size, kind = struct.unpack_from('>I4s', raw, pos)
            if pos + size + 12 > len(raw):
                raise ValueError('Invalid PNG chunk length')
            if kind == b'caBX':
                if size > 1_000_000 or len(chunks) >= 8:
                    raise ValueError('Credential bounds exceeded')
                payload = raw[pos + 8:pos + 8 + size]
                crc = struct.unpack_from('>I', raw, pos + 8 + size)[0]
                if zlib.crc32(kind + payload) & 0xffffffff != crc:
                    raise ValueError('Credential chunk CRC mismatch')
                chunks.append(payload)
            pos += size + 12
            if kind == b'IEND':
                break
        if not chunks:
            return result
        boxes = [entry for chunk in chunks for entry in _boxes(chunk)]
        if not any(label == 'c2pa' and kind == b'jumd' for label, kind, _ in boxes):
            return dict(result, status='container_without_c2pa_descriptor')
        generators, actions = [], []
        for label, kind, payload in boxes:
            if kind != b'cbor' or not label.startswith(('c2pa.claim', 'c2pa.actions')):
                continue
            data = _decode_cbor(payload)
            if not isinstance(data, dict):
                raise ValueError('Expected claim/action map')
            if label.startswith('c2pa.claim'):
                info = data.get('claim_generator_info', [])
                info = [info] if isinstance(info, dict) else info
                generators.extend({k: row[k] for k in ('name', 'version') if isinstance(row.get(k), str)} for row in info if isinstance(row, dict))
            if label.startswith('c2pa.actions'):
                for action in data.get('actions', []):
                    if not isinstance(action, dict):
                        raise ValueError('Expected action map')
                    agent = action.get('softwareAgent')
                    actions.append({k: action[k] for k in ('action', 'when', 'digitalSourceType') if isinstance(action.get(k), str)} | {'softwareAgent': agent if isinstance(agent, (str, dict)) else None})
        return result | {'status': 'metadata_read', 'png_credential_crc_valid': True,
                         'credential_sha256': [hashlib.sha256(chunk).hexdigest() for chunk in chunks],
                         'claim_generators': generators, 'actions': actions,
                         'signature_box_present': any(label == 'c2pa.signature' for label, _, _ in boxes),
                         'certificate_name_text_seen': 'OpenAI Media Service' if any(b'OpenAI Media Service' in chunk for chunk in chunks) else None,
                         'embedded_metadata_image_boxes': sum(kind == b'bidb' for _, kind, _ in boxes)}
    except (ValueError, UnicodeError, struct.error, TypeError) as error:
        return dict(result, status='malformed_or_unsupported', error=str(error))


def read_owner_review(path, candidates):
    """Bind submitted findings to the delivered IDs/hashes; never invent a search."""
    raw = Path(path).read_bytes()
    text = raw.decode('utf-8-sig')
    dialect = csv.Sniffer().sniff(text[:4096], delimiters=',;\t')
    rows = list(csv.DictReader(text.splitlines(), dialect=dialect))
    known = {row['id']: row for row in candidates}
    seen, normalized = set(), []
    for row in rows:
        key = row['id'].strip()
        expected = known.get(key)
        if key in seen or expected is None:
            raise ValueError('Unknown or duplicate review candidate')
        if any(row[field].strip() != str(expected[field]) for field in ('source_sha256', 'source_path')):
            raise ValueError('Review source identity does not match delivered candidate')
        original_frame = expected.get('frame_coordinates')
        actual_frame = json.loads(row['frame_coordinates']) if row['frame_coordinates'].strip() else None
        if original_frame != actual_frame:
            raise ValueError('Review frame does not match delivered candidate')
        seen.add(key)
        finding = {field: row.get(field, '').strip() for field in (
            'id', 'source_path', 'source_sha256', 'owner_decision', 'result_urls',
            'access_date', 'reverse_search_status', 'online_upload_permitted',
            'search_notes', 'follow_up_action')}
        finding.update(delivered_rank=expected.get('rank'), frame_coordinates=actual_frame,
                       delivered_candidate_sha256=expected.get('candidate_sha256'))
        normalized.append(finding)
    return {'source_csv_sha256': hashlib.sha256(raw).hexdigest(),
            'evidence_type': 'owner_supplied_manual_review_not_independently_reproduced',
            'assistant_external_image_uploads': 0, 'rows': normalized}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--image', type=Path, required=True)
    arguments = parser.parse_args()
    print(json.dumps(png_credentials(arguments.image.read_bytes()), indent=2))
