"""A missing hosted decoder must not depend on stalled apt repositories."""
import hashlib,importlib.util,os,subprocess,tempfile,unittest,zipfile
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('ci_decoder_tests',ROOT/'scripts/ci/audio_decoder.py');decoder=importlib.util.module_from_spec(spec);spec.loader.exec_module(decoder)
class DecoderBootstrapTests(unittest.TestCase):
 def fixture(self,folder):
  wheel=folder/'decoder.whl';binary=b'fixture executable bytes'
  with zipfile.ZipFile(wheel,'w') as z:z.writestr('bin/ffmpeg',binary);z.writestr('LICENSE','Original package notice')
  config={'url':'https://example.invalid/no-network-in-tests','sha256':hashlib.sha256(wheel.read_bytes()).hexdigest(),'binary':'bin/ffmpeg','binary_sha256':hashlib.sha256(binary).hexdigest(),'notice':'LICENSE'}
  return wheel,config
 def test_verified_binary_notices_and_offline_cache(self):
  with tempfile.TemporaryDirectory() as d:
   folder=Path(d);wheel,config=self.fixture(folder);dest=folder/'installed'
   exe=decoder.install(config,dest,wheel)
   self.assertEqual(exe.read_bytes(),b'fixture executable bytes');self.assertTrue(exe.stat().st_mode&0o111)
   self.assertEqual((dest/'IMAGEIO-LICENSE.txt').read_text(),'Original package notice')
   self.assertIn('GNU GENERAL PUBLIC LICENSE',(dest/'FFMPEG-COPYING.txt').read_text())
   with patch.object(decoder,'download',side_effect=AssertionError('Cache must work offline')):self.assertEqual(decoder.install(config,dest),exe)
 def test_changed_archive_is_rejected_without_installing(self):
  with tempfile.TemporaryDirectory() as d:
   folder=Path(d);wheel,config=self.fixture(folder);wheel.write_bytes(wheel.read_bytes()+b'tampered')
   with self.assertRaisesRegex(ValueError,'archive SHA-256'):decoder.install(config,folder/'out',wheel)
   self.assertFalse((folder/'out/ffmpeg').exists())
 def test_changed_binary_is_rejected_even_with_a_valid_archive_hash(self):
  with tempfile.TemporaryDirectory() as d:
   folder=Path(d);wheel,config=self.fixture(folder);config['binary_sha256']='0'*64
   with self.assertRaisesRegex(ValueError,'binary SHA-256'):decoder.install(config,folder/'out',wheel)
   self.assertFalse((folder/'out/ffmpeg').exists())
 def script(self,path,text):path.write_text('#!/bin/sh\n'+text);path.chmod(0o755)
 def test_missing_system_decoder_uses_pinned_fallback_without_apt(self):
  with tempfile.TemporaryDirectory() as d:
   folder=Path(d);bin=folder/'bin';bin.mkdir();ready=folder/'ready'
   self.script(ready,"echo 'ffmpeg version fixture'\n")
   self.script(bin/'ffmpeg',"echo 'forced missing decoder' >&2\nexit 127\n")
   self.script(bin/'sudo','exit 99\n')
   self.script(bin/'python3','while [ "$#" -gt 0 ]; do\n if [ "$1" = "--destination" ]; then shift; dest="$1"; fi\n shift\ndone\n/bin/mkdir -p "$dest"\n/bin/cp "$TEST_READY_DECODER" "$dest/ffmpeg"\nprintf "%s\\n" "$dest" >> "$GITHUB_PATH"\n')
   env=dict(os.environ,PATH=str(bin)+':'+os.environ['PATH'],RUNNER_TEMP=str(folder/'runner'),GITHUB_PATH=str(folder/'github-path'),TEST_READY_DECODER=str(ready))
   result=subprocess.run(['bash',str(ROOT/'scripts/ci/install-audio-decoder.sh')],env=env,cwd=folder,capture_output=True,text=True,timeout=10)
   self.assertEqual(result.returncode,0,result.stdout+result.stderr)
   self.assertIn('ffmpeg version fixture',result.stdout)
   self.assertEqual((folder/'github-path').read_text().strip(),str(folder/'runner/kinderwelt-ffmpeg'))
 def test_working_system_decoder_needs_no_download(self):
  with tempfile.TemporaryDirectory() as d:
   folder=Path(d);bin=folder/'bin';bin.mkdir()
   self.script(bin/'ffmpeg',"echo 'ffmpeg version existing'\n")
   self.script(bin/'python3','exit 99\n')
   env=dict(os.environ,PATH=str(bin)+':'+os.environ['PATH'],RUNNER_TEMP=str(folder/'runner'))
   result=subprocess.run(['bash',str(ROOT/'scripts/ci/install-audio-decoder.sh')],env=env,cwd=folder,capture_output=True,text=True,timeout=10)
   self.assertEqual(result.returncode,0,result.stdout+result.stderr);self.assertIn('ffmpeg version existing',result.stdout)
   self.assertFalse((folder/'runner').exists())
