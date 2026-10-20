"""Verify real offline music payloads, not just the audio manager API."""
import hashlib
import json
import math
from pathlib import Path
import struct
import unittest
import wave
ROOT=Path(__file__).resolve().parents[2]

class MusicAssetTests(unittest.TestCase):
    def test_every_playable_world_has_a_distinct_recording(self):
        manifest=json.loads((ROOT/'assets/music/manifest.json').read_text())
        worlds={entry['id'] for entry in json.loads((ROOT/'content/modules.json').read_text())}
        self.assertEqual(set(manifest['themes']),worlds)
        hashes=set()
        for world,theme in manifest['themes'].items():
            with self.subTest(world=world):
                path=ROOT/theme['file']
                digest=hashlib.sha256(path.read_bytes()).hexdigest()
                self.assertEqual(digest,theme['sha256'])
                hashes.add(digest)
        self.assertEqual(len(hashes),5)

    def test_recordings_are_audible_pcm_without_clipping(self):
        for path in (ROOT/'assets/music').glob('*.wav'):
            with self.subTest(track=path.name),wave.open(str(path)) as stream:
                self.assertEqual(stream.getsampwidth(),2)
                self.assertEqual(stream.getnchannels(),1)
                self.assertEqual(stream.getframerate(),22050)
                duration=stream.getnframes()/stream.getframerate()
                self.assertGreater(duration,15)
                self.assertLess(duration,32)
                values=struct.unpack('<'+'h'*stream.getnframes(),stream.readframes(stream.getnframes()))
                peak=max(abs(n) for n in values)/32768
                rms=math.sqrt(sum(n*n for n in values)/len(values))/32768
                self.assertGreater(rms,0.02)
                self.assertLess(peak,0.95)
                self.assertEqual(values[0],0)
                self.assertEqual(values[-1],0)

if __name__=='__main__':unittest.main()
