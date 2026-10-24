"""Credential claims stay distinct from authenticated origin and owner findings."""
import base64
import csv
import hashlib
import io
import json
import struct
import sys
import tempfile
import unittest
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts/qa'))
import visual_c2pa as credentials

PNG = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+aA1sAAAAASUVORK5CYII=')


def cbor(value):
    def length(major, size):
        return bytes([major * 32 + size]) if size < 24 else bytes([major * 32 + 24, size])
    if isinstance(value, str):
        data = value.encode()
        return length(3, len(data)) + data
    if isinstance(value, list):
        return length(4, len(value)) + b''.join(cbor(v) for v in value)
    if isinstance(value, dict):
        return length(5, len(value)) + b''.join(cbor(k) + cbor(v) for k, v in value.items())
    raise TypeError('Unsupported synthetic CBOR value')


def box(kind, data):
    return struct.pack('>I4s', len(data) + 8, kind) + data


def jumb(label, data):
    return box(b'jumb', box(b'jumd', bytes(16) + b'\x03' + label.encode() + b'\0') + data)


def chunk(kind, data):
    return struct.pack('>I4s', len(data), kind) + data + struct.pack('>I', zlib.crc32(kind + data) & 0xffffffff)


def credential_png():
    action = {'actions': [{'action': 'c2pa.created', 'when': '2026-10-20T18:12:20Z',
                          'softwareAgent': {'name': 'ChatGPT', 'version': 'gpt-image'},
                          'digitalSourceType': 'trainedAlgorithmicMedia'}]}
    claim = {'claim_generator_info': {'name': 'OpenAI Media Service API'}}
    data = jumb('c2pa', jumb('c2pa.actions.v2', box(b'cbor', cbor(action))) +
                jumb('c2pa.claim.v2', box(b'cbor', cbor(claim))) +
                jumb('c2pa.signature', box(b'cbor', b'not an authentic signature')))
    return PNG[:-12] + chunk(b'caBX', data) + PNG[-12:]


class ContentCredentialsTests(unittest.TestCase):
    def test_embedded_claims_are_read_without_asserting_authenticity(self):
        result = credentials.png_credentials(credential_png())
        self.assertEqual(result['status'], 'metadata_read')
        self.assertEqual(result['claim_generators'][0]['name'], 'OpenAI Media Service API')
        self.assertEqual(result['actions'][0]['when'], '2026-10-20T18:12:20Z')
        self.assertTrue(result['signature_box_present'])
        self.assertEqual(result['cryptographic_validation'], 'not_performed')
        self.assertFalse(any(result[k] for k in ('signature_verified', 'certificate_trust_verified', 'asset_binding_verified')))

    def test_plain_text_or_post_iend_bytes_do_not_become_credentials(self):
        self.assertEqual(credentials.png_credentials(PNG + credential_png()[8:])['status'], 'absent')
        raw = PNG[:-12] + chunk(b'tEXt', b'OpenAI Media Service; ChatGPT / gpt-image') + PNG[-12:]
        self.assertEqual(credentials.png_credentials(raw)['status'], 'absent')

    def test_corrupt_or_malformed_credentials_are_not_reported_as_read(self):
        raw = bytearray(credential_png())
        raw[-13] ^= 1
        for data in (bytes(raw), PNG[:-12] + chunk(b'caBX', b'not JUMBF') + PNG[-12:], PNG[:20]):
            with self.subTest(data=data[:20]):
                result = credentials.png_credentials(data)
                self.assertEqual(result['status'], 'malformed_or_unsupported')
                self.assertNotIn('claim_generators', result)

    def test_truncated_reserved_and_duplicate_cbor_is_rejected(self):
        for raw in (b'\xbf', b'\xa1', b'\xa2axayaxaz', b'\x81' * 20 + b'\x00'):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                credentials._decode_cbor(raw)

    def test_current_source_evidence_matches_actual_png_chunks(self):
        ledger = json.loads((ROOT / 'scripts/qa/visual-ip-owner-review.json').read_text())
        checked = 0
        for row in ledger['sources']:
            if row['source_path'].startswith('historical/'):
                continue
            raw = (ROOT / row['source_path']).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), row['source_sha256'])
            self.assertEqual(credentials.png_credentials(raw), row['file_credentials'])
            checked += 1
        self.assertEqual(checked, 14)
        self.assertEqual(ledger['summary']['embedded_manifest_sources'], 11)
        self.assertEqual(ledger['summary']['metadata_absent_derivatives_linked_to_credentialed_originals'], 7)
        self.assertTrue(all(not r['retained_original']['credentials']['signature_verified'] for r in ledger['sources']))
        icon = next(r for r in ledger['sources'] if r['source_path'] == 'assets/quest/appicon.png')
        raw = (ROOT / 'art/public/app-icon/original.png').read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), icon['retained_original']['sha256'])
        self.assertEqual(credentials.png_credentials(raw), icon['retained_original']['credentials'])

    def review_fixture(self, changed=None, duplicate=False):
        candidate = {'id': 'image-test/frame-1', 'source_path': 'assets/test.png',
                     'source_sha256': '1' * 64, 'frame_coordinates': [0, 1, 2, 3]}
        row = dict(candidate, frame_coordinates='[0, 1, 2, 3]', owner_decision='similar ',
                   result_urls='https://example.invalid/owner-result', access_date='24.10.2026',
                   reverse_search_status='', online_upload_permitted='true')
        row.update(changed or {})
        stream = io.StringIO()
        writer = csv.DictWriter(stream, fieldnames=list(row), delimiter=';')
        writer.writeheader()
        writer.writerows([row, row] if duplicate else [row])
        return candidate, '\ufeff' + stream.getvalue()

    def test_owner_semicolon_csv_is_bound_to_delivered_source_without_inventing_search(self):
        candidate, csv_text = self.review_fixture()
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'review.csv'
            path.write_text(csv_text)
            review = credentials.read_owner_review(path, [candidate])
        self.assertEqual(review['rows'][0]['owner_decision'], 'similar')
        self.assertEqual(review['rows'][0]['reverse_search_status'], '')
        self.assertEqual(review['assistant_external_image_uploads'], 0)
        self.assertEqual(review['source_csv_sha256'], hashlib.sha256(csv_text.encode()).hexdigest())

    def test_unknown_changed_duplicate_or_wrong_frame_reviews_are_rejected(self):
        changes = ({'id': 'unknown'}, {'source_sha256': '2' * 64},
                   {'source_path': 'assets/another.png'}, {'frame_coordinates': '[0, 0, 2, 3]'})
        cases = [self.review_fixture(changed) for changed in changes] + [self.review_fixture(duplicate=True)]
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'review.csv'
            for candidate, text in cases:
                with self.subTest(text=text), self.assertRaises(ValueError):
                    path.write_text(text)
                    credentials.read_owner_review(path, [candidate])


if __name__ == '__main__':
    unittest.main()
