"""Check actual delivered PCM rather than the generator's intention."""
import hashlib,json,math,struct,unittest,wave
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]/'assets/music/adventure'
class AdventureMusic(unittest.TestCase):
    def test_two_distinct_full_length_original_pcm_tracks(self):
        manifest=json.loads((ROOT/'manifest.json').read_text())
        tracks=manifest['tracks'];self.assertEqual(len(tracks),2)
        digests=set()
        for entry in tracks:
            raw=(ROOT/entry['file']).read_bytes()
            digest=hashlib.sha256(raw).hexdigest();digests.add(digest)
            self.assertEqual(digest,entry['sha256'])
            with wave.open(str(ROOT/entry['file'])) as wav:
                self.assertEqual((wav.getnchannels(),wav.getsampwidth(),wav.getframerate()),(1,2,22050))
                self.assertGreater(wav.getnframes()/22050,25)
                values=struct.unpack('<'+'h'*wav.getnframes(),wav.readframes(wav.getnframes()))
            self.assertGreater(math.sqrt(sum(v*v for v in values)/len(values))/32768,.08)
            self.assertLess(max(abs(v) for v in values),30000)
            self.assertLess(abs(values[-1]-values[0]),30)
            # No full second of silence hidden in the middle of a track.
            for i in range(0,len(values)-22050,22050):
                self.assertGreater(max(abs(v) for v in values[i:i+22050]),1000)
        self.assertEqual(len(digests),2)
if __name__=='__main__':unittest.main()
