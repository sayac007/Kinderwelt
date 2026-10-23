"""Exercise Android launcher verification with real WebP decoding."""
import importlib.util,io,subprocess,unittest,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('launcher_verify',ROOT/'scripts/android/verify.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class LauncherIconTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.generated=subprocess.check_output(['ffmpeg','-nostdin','-v','error','-threads','1','-filter_threads','1','-i',str(ROOT/'assets/quest/appicon.png'),'-vf','scale=192:192','-frames:v','1','-c:v','libwebp','-lossless','1','-f','webp','-'])
        cls.different=subprocess.check_output(['ffmpeg','-nostdin','-v','error','-threads','1','-filter_threads','1','-i',str(ROOT/'assets/quest/home.png'),'-vf','scale=192:192','-frames:v','1','-c:v','libwebp','-lossless','1','-f','webp','-'])
    def archive(self,aab=False,change=None):
        output=io.BytesIO();prefix='base/' if aab else ''
        names=['res/mipmap-xxxhdpi-v4/icon.webp','res/mipmap-xxxhdpi-v4/icon_foreground.webp','res/drawable/splash_icon.webp']
        with zipfile.ZipFile(output,'w') as z:
            for index,name in enumerate(names):
                if change=='missing' and index==1:continue
                z.writestr(prefix+name,self.different if change=='stale' and index==1 else (b'broken' if change=='invalid' and index==2 else self.generated))
        output.seek(0);return zipfile.ZipFile(output)
    def test_decoded_launcher_adaptive_foreground_and_splash_match_generated_source(self):
        for aab in [False,True]:
            with self.subTest(aab=aab),self.archive(aab) as z:
                self.assertEqual(len(v.check_launcher_images(z,aab=aab)),3)
    def test_stale_missing_and_invalid_resources_are_rejected(self):
        for aab in [False,True]:
            for change in ['stale','missing','invalid']:
                with self.subTest(aab=aab,change=change),self.archive(aab,change) as z,self.assertRaises(AssertionError):
                    v.check_launcher_images(z,aab=aab)
