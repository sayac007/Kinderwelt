#!/usr/bin/env python3
"""Render checked-in classical scores into real, offline-playable piano audio.

Development dependencies: LilyPond 2.24.4, mido 1.3.3, pyfluidsynth 1.4.0,
libfluidsynth 2.4.4, FFmpeg; no external recording or runtime synthesizer.
"""
import argparse
import ctypes
import hashlib
import importlib.metadata
import json
import re
from pathlib import Path
import subprocess
import tempfile
import wave

import fluidsynth
import mido
import numpy as np
from notices import render_notices

ROOT = Path(__file__).resolve().parents[2]
FONT_SHA = '9575028c7a1f589f5770fccc8cff2734566af40cd26ed836944e9a5152688cfe'
RATE = 44100


def render_midi(path, soundfont, destination, scale=1.0):
    synth = fluidsynth.Synth(samplerate=RATE, gain=0.65)
    try:
        sfid = synth.sfload(str(soundfont))
        assert sfid >= 0, 'Could not load piano SoundFont'
        for channel in range(16):
            synth.program_select(channel, sfid, 0, 0)
        chunks = []
        midi = mido.MidiFile(path)
        note_count = 0
        for msg in midi:
            frames = round(msg.time * scale * RATE)
            if frames:
                chunks.append(synth.get_samples(frames))
            if msg.type == 'note_on' and msg.velocity:
                synth.noteon(msg.channel, msg.note, min(msg.velocity, 104))
                note_count += 1
            elif msg.type in ('note_off', 'note_on'):
                synth.noteoff(msg.channel, msg.note)
            elif msg.type == 'control_change':
                synth.cc(msg.channel, msg.control, msg.value)
        assert note_count >= 40, 'Score is unexpectedly empty'
        for channel in range(16):
            synth.cc(channel, 64, 0)
            synth.cc(channel, 123, 0)
        chunks.append(synth.get_samples(3 * RATE))
        pcm = np.concatenate(chunks).astype(np.float64)
        # Leave headroom for lossy encoding; never saturate to int16.
        peak = np.max(np.abs(pcm))
        assert peak > 100, 'Silent rendering'
        pcm *= min(1.0, 25000.0 / peak)
        # Very short endpoint fades suppress clicks without cutting musical phrases.
        stereo = pcm.reshape(-1, 2)
        fade = min(RATE // 20, len(stereo))
        stereo[:fade] *= np.linspace(0, 1, fade)[:, None]
        fade = min(RATE, len(stereo))
        stereo[-fade:] *= np.linspace(1, 0, fade)[:, None]
        with wave.open(str(destination), 'wb') as wav:
            wav.setnchannels(2)
            wav.setsampwidth(2)
            wav.setframerate(RATE)
            wav.writeframes(stereo.astype('<i2').tobytes())
        return {'midi_notes': note_count, 'seconds': len(stereo) / RATE}
    finally:
        synth.delete()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lilypond-root', type=Path, default=Path('/workspace/tools/classical/lilypond-2.24.4'))
    parser.add_argument('--soundfont', type=Path, default=Path('/workspace/tools/classical/generaluser/GeneralUser-GS.sf2'))
    args = parser.parse_args()
    lily = args.lilypond_root / 'bin/lilypond'
    version = subprocess.check_output([lily, '--version'], text=True).splitlines()[0]
    assert version.startswith('GNU LilyPond 2.24.4'), 'Use pinned LilyPond 2.24.4'
    assert hashlib.sha256(args.soundfont.read_bytes()).hexdigest() == FONT_SHA, 'Wrong SoundFont'
    fluid_major, fluid_minor, fluid_micro = ctypes.c_int(), ctypes.c_int(), ctypes.c_int()
    fluidsynth.fluid_version(ctypes.byref(fluid_major), ctypes.byref(fluid_minor), ctypes.byref(fluid_micro))
    fluid_library_version = f'{fluid_major.value}.{fluid_minor.value}.{fluid_micro.value}'
    catalog = json.loads((ROOT / 'scripts/music/catalog.json').read_text())
    prior=json.loads((ROOT/'assets/music/manifest.json').read_text())
    cached={t['id']:t for t in prior.get('tracks',[])}
    manifest = {'schema': 3, 'complete':False, 'authorship': 'Own instrumental renderings of named public-domain compositions; score and arrangement licences are listed per track.',
                'renderer': {'lilypond': version, 'fluidsynth': fluid_library_version, 'ffmpeg': subprocess.check_output(['ffmpeg','-version'],text=True).splitlines()[0], 'mido': importlib.metadata.version('mido'), 'pyfluidsynth': importlib.metadata.version('pyfluidsynth'), 'soundfont_sha256': FONT_SHA}, 'tracks': []}
    with tempfile.TemporaryDirectory(prefix='kinderwelt-classical.') as directory:
        temp = Path(directory)
        for track in catalog['tracks']:
            original = ROOT / 'scripts/music/scores' / track['source']['file']
            assert hashlib.sha256(original.read_bytes()).hexdigest() == track['source']['sha256']
            old=cached.get(track['id'],{})
            audio=ROOT/'assets/music'/(track['id']+'.ogg')
            if old.get('render_profile')=='score-modernization-1' and old.get('source')==track['source'] and audio.exists() and hashlib.sha256(audio.read_bytes()).hexdigest()==old.get('sha256'):
                manifest['tracks'].append(old)
                print('Cached:',track['title'],flush=True)
                continue
            source = temp / original.name
            source.write_bytes(re.sub(rb"(?m)^%[^\n]*old-relative[^\n]*\n",b"",original.read_bytes()))
            for dependency in track.get('dependencies',[]):
                raw=(ROOT/'scripts/music/scores'/dependency['file']).read_bytes()
                assert hashlib.sha256(raw).hexdigest()==dependency['sha256']
                dep=temp/dependency['file'];dep.write_bytes(raw)
                converted=subprocess.check_output([args.lilypond_root/'bin/convert-ly',str(dep)],stderr=subprocess.PIPE)
                dep.write_bytes(converted)
            midi = source
            if track['kind'].startswith('lilypond'):
                if track['kind'] == 'lilypond_wiener':
                    source.write_text(source.read_text().replace('4 = 200', '4 = 180'))
                    wrapper = '\\version "2.24.4"\n\\include "wiener_blut.ly"\n\\score { << '
                    for voice in ['melody_wiener_blut', 'second_melody_wiener_blut', 'left_wiener_blue', 'pedal_wiener_blut']:
                        wrapper += '\\new Staff { \\' + voice + ' } '
                    source = temp / 'wiener-wrapper.ly'
                    source.write_text(wrapper + ' >> \\midi {} }\n')
                else:
                    converted = subprocess.check_output([args.lilypond_root / 'bin/convert-ly', str(source)], stderr=subprocess.PIPE)
                    converted=re.sub(rb"#\s*\(set-octavation\s+(-?\d+)\)",lambda m:b"\\ottava #"+m.group(1),converted)
                    # Obsolete beam-engraving settings affect notation only, not sound.
                    converted=re.sub(rb"#\s*\(override-auto-beam-setting[^\n]*\n",b"",converted)
                    source.write_bytes(converted)
                result = subprocess.run([lily, '-dno-print-pages', '-o', str(temp / track['id']), str(source)], cwd=temp, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                (temp / (track['id']+'.log')).write_text(result.stdout)
                if result.returncode:
                    raise RuntimeError(result.stdout)
                candidates = sorted(temp.glob(track['id']+'*.midi'))
                assert len(candidates) == 1, 'Expected one MIDI score per track'
                midi = candidates[0]
            wav = temp / (track['id']+'.wav')
            data = render_midi(midi, args.soundfont, wav, track.get('time_scale', 1.0))
            output = ROOT / 'assets/music' / (track['id']+'.ogg')
            subprocess.run(['ffmpeg', '-nostdin', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(wav), '-c:a', 'libvorbis', '-q:a', '5', '-metadata', 'title='+track['title'], '-metadata', 'artist='+track['composer'], str(output)], check=True)
            data.update(track)
            data["render_profile"]="score-modernization-1"
            data.update(file=output.name, bytes=output.stat().st_size, sha256=hashlib.sha256(output.read_bytes()).hexdigest())
            manifest['tracks'].append(data)
            (ROOT/'assets/music/manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
            print(track['title'], round(data['seconds'], 2), 'seconds', flush=True)
    manifest['complete']=len(manifest['tracks'])==len(catalog['tracks'])
    (ROOT / 'assets/music/manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n')
    (ROOT / 'assets/music/NOTICES.txt').write_text(render_notices())


if __name__ == '__main__':
    main()
