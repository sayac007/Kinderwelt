"""Use a real Vorbis encode to guard codec overshoot and complete duration."""
import array,hashlib,importlib.util,math,subprocess,tempfile,unittest,wave
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('speech_encode',ROOT/'scripts/generate-quest-voice.py');voice=importlib.util.module_from_spec(spec);spec.loader.exec_module(voice)
class SpeechEncodingTests(unittest.TestCase):
    def test_real_encoder_leaves_headroom_without_shortening_the_recording(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d);rate=22050
            pcm=array.array('h',[0]*4410+[round(32700*math.sin(2*math.pi*880*i/rate)) for i in range(rate)]+[0]*8820)
            with wave.open(str(path/'input.wav'),'wb') as w:
                w.setnchannels(1);w.setsampwidth(2);w.setframerate(rate);w.writeframes(pcm.tobytes())
            subprocess.run(['ffmpeg','-nostdin','-v','error','-i',str(path/'input.wav'),'-c:a','libvorbis','-q:a','4',str(path/'unsafe.ogg')],check=True)
            unsafe=path/'unsafe.ogg'
            self.assertFalse(voice.valid_cached_audio(unsafe,hashlib.sha256(unsafe.read_bytes()).hexdigest()))
            result=voice.encode_speech(path/'input.wav',path/'output.ogg')
            # Decode independently, rather than trusting the returned peak metadata.
            actual=array.array('f',subprocess.check_output(['ffmpeg','-nostdin','-v','error','-i',str(path/'output.ogg'),'-ac','1','-ar',str(rate),'-f','f32le','-']))
            self.assertLessEqual(max(abs(v) for v in actual),.95001)
            self.assertAlmostEqual(len(actual)/rate,len(pcm)/rate,delta=.06)
            self.assertLess(result['uniform_gain'],1)
            self.assertGreaterEqual(result['encodes'],2)
            safe=path/'output.ogg'
            self.assertTrue(voice.valid_cached_audio(safe,hashlib.sha256(safe.read_bytes()).hexdigest()))
            self.assertFalse(voice.valid_cached_audio(safe,'0'*64))
