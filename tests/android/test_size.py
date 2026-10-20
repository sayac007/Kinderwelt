"""Classify real Godot export suffixes, including imported font resources."""
import importlib.util,tempfile,unittest,zipfile
from pathlib import Path
spec=importlib.util.spec_from_file_location('size',Path(__file__).resolve().parents[2]/'scripts/android/analyze_size.py')
size=importlib.util.module_from_spec(spec);spec.loader.exec_module(size)
class SizeTests(unittest.TestCase):
    def test_imported_godot_resource_formats_are_counted(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'app.apk'
            with zipfile.ZipFile(path,'w') as z:
                z.writestr('assets/.godot/imported/Nunito.ttf-example.fontdata',b'font payload')
                z.writestr('assets/.godot/imported/icon.png-example.ctex',b'image payload')
                z.writestr('assets/.godot/imported/music.ogg-example.oggvorbisstr',b'audio payload')
            groups=size.analyze(path)['groups']
            self.assertEqual(groups['fonts']['raw_bytes'],12)
            self.assertEqual(groups['graphics']['raw_bytes'],13)
            self.assertEqual(groups['audio']['raw_bytes'],13)
