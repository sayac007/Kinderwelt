"""Decode delivered neural clips, and check the authored task/asset contract."""
import array
import hashlib
import json
import math
import struct
import subprocess
import unittest
import importlib.util
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

class QuestAssetsTests(unittest.TestCase):
    def test_classical_tracks_are_real_playable_audio(self):
        folder=ROOT/'assets/music'
        tracks=json.loads((folder/'manifest.json').read_text())['tracks']
        self.assertEqual(len(tracks),4)
        self.assertEqual(len({t['sha256'] for t in tracks}),4)
        for track in tracks:
            path=folder/track['file']
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),track['sha256'])
            pcm=array.array('f',subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-ar','22050','-ac','1','-f','f32le','-']))
            self.assertGreater(len(pcm)/22050,10)
            self.assertGreater(math.sqrt(sum(v*v for v in pcm)/len(pcm)),.005)
            self.assertLess(max(abs(v) for v in pcm),1)
    def test_task_contract(self):
        tasks=json.loads((ROOT/'games/quest/tasks.json').read_text())['tasks']
        self.assertEqual(len(tasks),320)
        self.assertEqual(len({t['id'] for t in tasks}),320)
        for subject in ['math','german','logic','physics','biology','chemistry','body','geography']:
            self.assertEqual(sum(t['subject']==subject for t in tasks),40)
        for task in tasks:
            self.assertIn(task['answer'],task['options'])
            self.assertEqual(len(task['options']),len(set(task['options'])))
            self.assertTrue(task['prompt'] and task['tip'])
    def test_neural_voice_content_hashes_and_actual_decoding(self):
        spec=importlib.util.spec_from_file_location('speech_source',ROOT/'scripts/generate-quest-voice.py')
        source=importlib.util.module_from_spec(spec);spec.loader.exec_module(source)
        decoded=[]
        def decode(item):
            path,clip=item
            pcm=array.array('f',subprocess.check_output(['ffmpeg','-nostdin','-v','error','-threads','1','-i',str(path),'-ar','22050','-ac','1','-f','f32le','-']))
            self.assertAlmostEqual(len(pcm)/22050,clip['seconds'],delta=.06,msg=str(path))
            self.assertGreater(math.sqrt(sum(v*v for v in pcm)/len(pcm)),.005,msg=str(path))
            self.assertLess(max(abs(v) for v in pcm),1.001,msg=str(path))
        for locale,model in [('de','de_DE-kerstin-low'),('en','en_US-ljspeech-medium'),('ru','ru_RU-denis-medium')]:
            folder=ROOT/'assets/voice/quest'/locale
            manifest=json.loads((folder/'manifest.json').read_text())
            self.assertEqual(manifest['model'],model)
            self.assertIn(manifest['dataset_license'],['CC0','Public Domain'])
            self.assertEqual(manifest['voice_gender'],'male' if locale=='ru' else 'female')
            self.assertEqual(manifest['human_listening_review'].split(';')[0],'OPEN')
            expected=source.narration_texts(locale)
            self.assertEqual(len(expected),652)
            self.assertEqual({c['id']:c['text'] for c in manifest['clips']},expected)
            unique={c['file']:c for c in manifest['clips']}
            self.assertEqual({p.name for p in folder.glob('*.ogg')},set(unique))
            for filename,clip in unique.items():
                path=folder/filename
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),clip['sha256'])
                decoded.append((path,clip))
        # Decode each delivered recording once, even if several exercises share it.
        with ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(decode,decoded))
        print('Decoded all',len(decoded),'unique localized voice recordings')
    def test_translations_images_and_original_content_remain_complete(self):
        tasks=json.loads((ROOT/'games/quest/tasks.json').read_text())['tasks']
        languages=json.loads((ROOT/'games/quest/languages.json').read_text())
        for section in ['ui','objects']:
            for key,values in languages[section].items():
                self.assertEqual(set(values),{'de','en','ru'})
                self.assertTrue(all(isinstance(v,str) and v.strip() for v in values.values()),key)
        for task in tasks:
            self.assertEqual(set(task['texts']),{'de','en','ru'})
            for locale in ['de','en','ru']:
                self.assertTrue(task['texts'][locale]['prompt'] and task['texts'][locale]['tip'])
            self.assertIn(task.get('object','star'),languages['objects'])
            if task['kind']=='discovery':
                for option in task['options']:self.assertIn(option,languages['objects'])
        originals=json.loads((ROOT/'scripts/content/foundation-tasks.json').read_text())['tasks']
        current={t['id']:t for t in tasks}
        for task in originals:
            for key,value in task.items():self.assertEqual(current[task['id']][key],value)
    def test_content_generator_is_reproducible(self):
        paths=[ROOT/'games/quest/tasks.json',ROOT/'games/quest/languages.json']
        before=[p.read_bytes() for p in paths]
        subprocess.run(['python3',str(ROOT/'scripts/content/generate.py')],check=True,capture_output=True)
        self.assertEqual(before,[p.read_bytes() for p in paths])
    def test_graphics_are_real_png_and_individual_heroes_differ(self):
        hashes=set()
        for name in ['wanja','mischa','du','mama','katze','icons','objects','landscape','science-a','science-b']:
            raw=(ROOT/'assets/quest'/f'{name}.png').read_bytes()
            self.assertEqual(raw[:8],b'\x89PNG\r\n\x1a\n')
            width,height=struct.unpack('>II',raw[16:24])
            self.assertGreaterEqual(width,1024)
            self.assertGreaterEqual(height,1024)
            hashes.add(hashlib.sha256(raw).hexdigest())
        self.assertEqual(len(hashes),10)
    def test_approved_family_art_is_used_without_changes(self):
        for name in ['wanja','mischa','du','mama','katze']:
            self.assertEqual((ROOT/'assets/quest'/f'{name}.png').read_bytes(),(ROOT/'docs/character-proposals'/f'{name}.png').read_bytes())
        for name in ['mina','leo','sam','jule']:
            self.assertFalse((ROOT/'assets/quest'/f'{name}.png').exists())
    def test_classical_sources_and_notices_are_present(self):
        data=json.loads((ROOT/'assets/music/manifest.json').read_text())
        composers={'wiener_blut':'Johann Strauss II','babbino':'Giacomo Puccini','french_song':'P. I. Tschaikowski','consolation':'Franz Liszt'}
        self.assertEqual({t['id']:t['composer'] for t in data['tracks']},composers)
        for track in data['tracks']:
            source=ROOT/'scripts/music/scores'/track['source']['file']
            self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),track['source']['sha256'])
            self.assertTrue(track['license'] and track['arranger'])
            self.assertGreater(track['midi_notes'],40)
        for name in ['CC-BY-SA-4.0.txt','tnm-MIT.txt','GeneralUser-GS.txt']:
            self.assertGreater((ROOT/'assets/music/licenses'/name).stat().st_size,500)

if __name__=='__main__':unittest.main()
