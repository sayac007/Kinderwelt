"""Decode delivered neural clips, and check the authored task/asset contract."""
import array
import hashlib
import json
import math
import struct
import subprocess
import unittest
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
        self.assertEqual(len(tasks),24)
        self.assertEqual(len({t['id'] for t in tasks}),24)
        for subject in ['math','german','logic']:
            self.assertEqual(sum(t['subject']==subject for t in tasks),8)
        for task in tasks:
            self.assertIn(task['answer'],task['options'])
            self.assertEqual(len(task['options']),len(set(task['options'])))
            self.assertTrue(task['prompt'] and task['tip'])
    def test_neural_voice_content_hashes_and_actual_decoding(self):
        folder=ROOT/'assets/voice/quest'
        manifest=json.loads((folder/'manifest.json').read_text())
        self.assertEqual(manifest['engine'],'Piper 1.4.2 (development tool only)')
        self.assertEqual(manifest['model_sha256'],'2d98b40baac55e4206f64114110a3474807e26440b80d465cd202af1e95be5e0')
        tasks=json.loads((ROOT/'games/quest/tasks.json').read_text())['tasks']
        expected={'choose','walk','success','again'}|{t['id'] for t in tasks}|{t['id']+'_hint' for t in tasks}
        self.assertEqual({c['id'] for c in manifest['clips']},expected)
        for clip in manifest['clips']:
            with self.subTest(clip=clip['id']):
                path=folder/(clip['id']+'.ogg')
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),clip['sha256'])
                pcm=array.array('f',subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-ar','22050','-ac','1','-f','f32le','-']))
                self.assertAlmostEqual(len(pcm)/22050,clip['seconds'],delta=.06)
                self.assertGreater(math.sqrt(sum(v*v for v in pcm)/len(pcm)),.005)
                self.assertLess(max(abs(v) for v in pcm),1.001)
        for task in tasks:
            actual={c['id']:c['text'] for c in manifest['clips']}
            self.assertEqual(actual[task['id']],task['prompt'])
            self.assertEqual(actual[task['id']+'_hint'],task['tip'])
    def test_graphics_are_real_png_and_individual_heroes_differ(self):
        hashes=set()
        for name in ['mischa','du','mama','katze','icons','objects','landscape']:
            raw=(ROOT/'assets/quest'/f'{name}.png').read_bytes()
            self.assertEqual(raw[:8],b'\x89PNG\r\n\x1a\n')
            width,height=struct.unpack('>II',raw[16:24])
            self.assertGreaterEqual(width,1024)
            self.assertGreaterEqual(height,1024)
            hashes.add(hashlib.sha256(raw).hexdigest())
        self.assertEqual(len(hashes),7)
    def test_approved_family_art_is_used_without_changes(self):
        for name in ['mischa','du','mama','katze']:
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
