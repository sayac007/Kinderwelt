import importlib.util,json,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
identity=load('identity_test','scripts/android/identity.py')
class ReleaseConfigTests(unittest.TestCase):
    def test_preview_channel_stays_stable_when_the_display_version_changes(self):
        original=identity.CONFIG['version_name']
        try:
            packages=[]
            for version in ['0.9.0','0.9.1']:
                identity.CONFIG['version_name']=version
                with tempfile.TemporaryDirectory() as d:
                    app=Path(d)
                    for n in ['export_presets.cfg','project.godot']:(app/n).write_bytes((ROOT/n).read_bytes())
                    packages.append(identity.configure(app,preview=True,variant='family'))
            self.assertEqual(packages[0],packages[1])
        finally:identity.CONFIG['version_name']=original
    def test_explicit_package_override_and_isolated_previews(self):
        for variant in ['family','public']:
            with tempfile.TemporaryDirectory() as d:
                app=Path(d)
                for n in ['export_presets.cfg','project.godot']:(app/n).write_bytes((ROOT/n).read_bytes())
                chosen=identity.configure(app,'de.kinderwelt.test',True,variant)
                self.assertEqual(chosen,'de.kinderwelt.test.preview.'+('family' if variant=='family' else 'neutral')+'.v090')
                text=(app/'export_presets.cfg').read_text()
                self.assertNotIn(identity.TOKEN,text)
                self.assertEqual(text.count('package/unique_name="'+chosen+'"'),2)
                self.assertIn('version/code=13',text)
    def test_invalid_package_ids_rejected_before_export(self):
        for value in ['','single','com..app','com.App','com.1app','com.public.app','com.test-app','com.app;echo','com.app\nother','a.'+'a'*180]:
            with self.subTest(value=value),self.assertRaises(ValueError):identity.validate_package(value)
    def test_music_arrangements_match_sources_and_preserve_licences(self):
        m=load('notice_test','scripts/music/notices.py');text=m.render_notices()
        self.assertEqual(text,(ROOT/'assets/music/NOTICES.txt').read_text())
        self.assertEqual([l for l in text.splitlines() if l.startswith('Lizenz:')],json.loads((ROOT/'scripts/music/notice-license-fixtures.json').read_text()))
        tracks=json.loads((ROOT/'scripts/music/catalog.json').read_text())['tracks'];notes={t['id']:m.arrangement(t) for t in tracks}
        self.assertEqual(len(set(notes.values())),20)
        self.assertIn('Faktor 1.65',notes['babbino'])
        self.assertIn('keine LilyPond-Konvertierung',notes['babbino'])
        self.assertIn('200 auf 180',notes['wiener_blut'])
        self.assertIn('Historically attributed to Bach in the source; now attributed to Christian Petzold.',text)
    def test_repo_review_assets_are_not_duplicated(self):
        for folder in ['docs/character-proposals','docs/music-previews','docs/voice-previews']:
            self.assertFalse([p for p in (ROOT/folder).glob('*') if p.suffix in ['.zip','.mp3']])
