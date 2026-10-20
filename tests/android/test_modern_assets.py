"""Inspect delivered audio and the size analyzer, not just asset names."""
import hashlib,importlib.util,json,math,struct,subprocess,tempfile,unittest,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('size',ROOT/'scripts/android/analyze_size.py');size=importlib.util.module_from_spec(spec);spec.loader.exec_module(size)
class ModernAssets(unittest.TestCase):
    def decode(self,path):
        return subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-f','f32le','-ac','1','-ar','22050','-'])
    def test_eight_new_scores_are_distinct_and_playable(self):
        manifest=json.loads((ROOT/'assets/music/modern/manifest.json').read_text())
        self.assertEqual(len(manifest['tracks']),8)
        pcm_hashes=set();scores=set()
        for track in manifest['tracks']:
            path=ROOT/'assets/music/modern'/(track['id']+'.ogg')
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),track['sha256'])
            pcm=self.decode(path);pcm_hashes.add(hashlib.sha256(pcm).hexdigest());scores.add(tuple(track['melody']))
            values=struct.unpack('<'+'f'*(len(pcm)//4),pcm)
            self.assertGreater(len(values)/22050,20)
            self.assertLessEqual(max(abs(v) for v in values),1.0)
            self.assertGreater(math.sqrt(sum(v*v for v in values)/len(values)),.05)
            self.assertLess(abs(values[-1]-values[0]),.015)
        self.assertEqual(len(pcm_hashes),8);self.assertEqual(len(scores),8)
    def test_german_voice_clips_have_real_audio(self):
        manifest=json.loads((ROOT/'assets/voice/manifest.json').read_text())
        self.assertEqual(manifest['language'],'de')
        self.assertIn('PROTOTYPE',manifest['quality'])
        ids=set()
        for clip in manifest['clips']:
            path=ROOT/'assets/voice'/clip['file'];ids.add(clip['id'])
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),clip['sha256'])
            pcm=self.decode(path)
            self.assertGreater(len(pcm),10000)
            self.assertTrue(any(pcm[1000:]))
        self.assertTrue({'water_0','water_1','water_2','water_help','water_success'}<=ids)
    def test_size_report_accounts_for_compression_and_all_categories(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'fixture.apk'
            with zipfile.ZipFile(path,'w') as z:
                z.writestr('lib/arm64-v8a/libfake.so',b'a'*4096,compress_type=zipfile.ZIP_DEFLATED)
                z.writestr('assets/.godot/imported/music.sample',b'music'*200)
                z.writestr('assets/font.ttf',b'font')
                z.writestr('assets/hero.ctex',b'image')
                z.writestr('assets/game.gdc',b'code')
                z.writestr('classes.dex',b'android')
            report=size.analyze(path)
            self.assertEqual(report['bytes'],path.stat().st_size)
            self.assertEqual(report['groups']['native/arm64-v8a']['raw_bytes'],4096)
            self.assertLess(report['groups']['native/arm64-v8a']['stored_bytes'],4096)
            self.assertIn('audio',report['groups']);self.assertIn('fonts',report['groups']);self.assertIn('graphics',report['groups'])
            self.assertEqual(sum(g['stored_bytes'] for g in report['groups'].values())+report['zip_alignment_signing_overhead_bytes'],path.stat().st_size)
if __name__=='__main__':unittest.main()
