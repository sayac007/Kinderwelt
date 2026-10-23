"""Decode delivered neural clips, and check the authored task/asset contract."""
import array
import configparser
import fnmatch
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
        self.assertEqual(len(tracks),20)
        self.assertEqual(len({t['sha256'] for t in tracks}),20)
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
            self.assertLess(max(abs(v) for v in pcm[:2205]),.001,msg='Speech has a complete quiet lead-in: '+str(path))
            self.assertLess(max(abs(v) for v in pcm[-3307:]),.001,msg='Speech has a complete quiet ending: '+str(path))
        for locale,model in [('de','de_DE-thorsten-high'),('en','en_US-ljspeech-medium'),('ru','ru_RU-denis-medium')]:
            folder=ROOT/'assets/voice/quest'/locale
            manifest=json.loads((folder/'manifest.json').read_text())
            self.assertEqual(manifest['model'],model)
            self.assertEqual(manifest['synthesis'],source.synthesis_profile(locale))
            self.assertGreaterEqual(manifest['synthesis']['sentence_pause_seconds'],.25)
            self.assertIn(manifest['dataset_license'],['CC0','Public Domain'])
            self.assertEqual(manifest['voice_gender'],'female' if locale=='en' else 'male')
            self.assertEqual(manifest['human_listening_review'].split(';')[0],'OPEN')
            expected=source.narration_texts(locale)
            self.assertEqual(len(expected),1947)
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
    def test_german_phonetic_word_durations_are_measured_not_padding(self):
        manifest=json.loads((ROOT/'assets/voice/quest/de/manifest.json').read_text())
        self.assertEqual(manifest['synthesis']['duration_alignment'],'vits-ceil-frames')
        by_id={c['id']:c for c in manifest['clips']}
        for clip in manifest['clips']:
            units=clip['phonetic_units']
            self.assertTrue(units,clip['id'])
            previous=.17
            for unit in units:
                self.assertGreaterEqual(unit['start'],previous-.00001,clip['id'])
                self.assertGreater(unit['seconds'],0,clip['id'])
                self.assertAlmostEqual(unit['end']-unit['start'],unit['seconds'],places=5)
                self.assertLessEqual(unit['end'],clip['seconds']-.30,clip['id'])
                previous=unit['end']
        # Independent bounds for short, previously swallowed subject words.
        # These compare actual model speech allocation, excluding inserted silence.
        for subject in ['math','german','logic','physics','biology','chemistry','body','geography']:
            clip=by_id['area_'+subject]
            # Some subjects now have a short spoken introduction; the subject
            # itself is the last phonetic unit, not the added context or silence.
            self.assertGreaterEqual(clip['phonetic_units'][-1]['seconds'],.35,subject)
        self.assertGreaterEqual(by_id['area_physics']['phonetic_units'][0]['seconds'],.65)
    def test_phoneme_normalization_keeps_the_german_ich_sound_and_rejects_unknowns(self):
        spec=importlib.util.spec_from_file_location('speech_source',ROOT/'scripts/generate-quest-voice.py')
        source=importlib.util.module_from_spec(spec);spec.loader.exec_module(source)
        self.assertEqual(source.normalized_phonemes(list('ɪc\u0327'),{'ɪ':[1],'ç':[2]}),['ɪ','ç'])
        self.assertEqual(''.join(source.pronunciation_phonemes(list('diː çeːmˈiː.'),'Die Chemie.','de')),'diː çeˈmiː.')
        with self.assertRaises(ValueError):source.normalized_phonemes(['?'],{'ɪ':[1]})
        model=json.loads((ROOT/'assets/voice/quest/de/manifest.json').read_text())
        self.assertEqual(model['synthesis']['phoneme_normalization'],'supported-nfc')
    def test_short_subject_clips_have_stable_measured_articulation_in_all_languages(self):
        for locale in ['de','en','ru']:
            manifest=json.loads((ROOT/'assets/voice/quest'/locale/'manifest.json').read_text())
            clips={c['id']:c for c in manifest['clips']}
            for subject in ['math','german','logic','physics','biology','chemistry','body','geography']:
                clip=clips['area_'+subject]
                profile=clip.get('generation_profile',manifest['synthesis'])
                self.assertEqual(profile['noise_w_scale'],0)
                self.assertGreaterEqual(clip['phonetic_units'][-1]['seconds'],.35,(locale,subject))
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
        for name in ['squirrel','icons','objects','landscape','science-a','science-b','home','castle','adventure-worlds']:
            raw=(ROOT/'assets/quest'/f'{name}.png').read_bytes()
            self.assertEqual(raw[:8],b'\x89PNG\r\n\x1a\n')
            width,height=struct.unpack('>II',raw[16:24])
            self.assertGreaterEqual(width,512 if name=='squirrel' else 1024)
            self.assertGreaterEqual(height,768)
            hashes.add(hashlib.sha256(raw).hexdigest())
        self.assertEqual(len(hashes),9)
    def test_shared_world_atlas_has_provenance_and_bounded_source_size(self):
        metadata=json.loads((ROOT/'art/adventure-worlds.json').read_text())
        data=(ROOT/metadata['asset']).read_bytes()
        self.assertEqual(hashlib.sha256(data).hexdigest(),metadata['sha256'])
        self.assertEqual(metadata['layout'],[['tree','seabed'],['city','moon']])
        self.assertLessEqual(len(data),metadata['source_budget_bytes'])
        self.assertEqual(metadata['source_budget_bytes'],4*1024*1024)

    def test_costume_atlases_and_visible_frames(self):
        # Metadata must match the optimized source pixels and visible crops.
        data=json.loads((ROOT/'assets/quest/looks.json').read_text())
        self.assertEqual(set(data['heroes']),{'wanja','mischa','du','mama','katze','george','squirrel'})
        for id,hero in data['heroes'].items():
            raw=(ROOT/'assets/quest'/hero['file']).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(),hero['sha256'])
            width,height=struct.unpack('>II',raw[16:24])
            self.assertEqual(raw[25],6)
            self.assertTrue({'hero','alien','astronaut','scientist'}<=set(hero['frames']))
            self.assertTrue({'hero','alien','astronaut','scientist'}<=set(hero['probes']))
            self.assertGreater(len(hero['mask_runs']),height)
            for row,left,length,owner in hero['mask_runs']:
                self.assertTrue(0<=row<height and 0<=left<left+length<=width and owner in [1,2,3,4])
            for look,rect in hero['frames'].items():
                x,y,w,h=rect
                self.assertGreater(w,80);self.assertGreater(h,160)
                self.assertTrue(0<=x<x+w<=width and 0<=y<y+h<=height)
        for name in ['home','castle']:
            raw=(ROOT/'assets/quest'/(name+'.png')).read_bytes()
            self.assertEqual(raw[:8],b'\x89PNG\r\n\x1a\n')
            self.assertGreater(len(raw),100000)
    def test_active_cast_resources_match_the_materialized_variant(self):
        cast=json.loads((ROOT/'assets/quest/cast.json').read_text())
        self.assertIn(cast['variant'],['family','public'])
        for path,digest in cast['resource_sha256'].items():
            self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),digest)
        self.assertEqual(len(cast['names']),7)
        if cast['variant']=='public':
            self.assertEqual(cast['names']['wanja'],'Nova')
            self.assertFalse(list((ROOT/'assets/quest/characters').glob('outfits-*.png')))
        else:
            pack=ROOT/'.private/characters'
            for index,id in enumerate(['wanja','mischa','du','mama','george','katze'],1):
                self.assertEqual((ROOT/'assets/quest/characters'/f'actor-{index}.png').read_bytes(),(pack/(id+'.png')).read_bytes())
        for name in ['mina','leo','sam','jule']:
            self.assertFalse((ROOT/'assets/quest'/f'{name}.png').exists())
    def test_android_presets_include_all_nonresource_licence_texts(self):
        presets=configparser.ConfigParser(interpolation=None)
        presets.read(ROOT/'export_presets.cfg')
        notices=['assets/quest/OFL.txt','assets/music/NOTICES.txt']
        notices += [str(p.relative_to(ROOT)) for p in (ROOT/'assets/music/licenses').glob('*.txt')]
        notices += ['assets/voice/quest/'+locale+'/MODEL_CARD.txt' for locale in ['de','en','ru']]
        for preset in ['preset.0','preset.1']:
            patterns=json.loads(presets[preset]['include_filter']).split(',')
            for name in notices:
                self.assertTrue(any(fnmatch.fnmatchcase(name,pattern) for pattern in patterns),(preset,name))
    def test_classical_sources_and_notices_are_present(self):
        data=json.loads((ROOT/'assets/music/manifest.json').read_text())
        composers={'wiener_blut':'Johann Strauss II','babbino':'Giacomo Puccini','french_song':'P. I. Tschaikowski','consolation':'Franz Liszt'}
        self.assertEqual({t['id']:t['composer'] for t in data['tracks'] if t['id'] in composers},composers)
        self.assertEqual(len(data['tracks']),20)
        self.assertTrue(data['complete'])
        for track in data['tracks']:
            source=ROOT/'scripts/music/scores'/track['source']['file']
            self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),track['source']['sha256'])
            self.assertTrue(track['license'] and track['arranger'])
            self.assertGreater(track['midi_notes'],40)
            for dependency in track.get('dependencies',[]):
                self.assertEqual(hashlib.sha256((ROOT/'scripts/music/scores'/dependency['file']).read_bytes()).hexdigest(),dependency['sha256'])
        for name in ['CC-BY-SA-4.0.txt','tnm-MIT.txt','GeneralUser-GS.txt']:
            self.assertGreater((ROOT/'assets/music/licenses'/name).stat().st_size,500)

if __name__=='__main__':unittest.main()
