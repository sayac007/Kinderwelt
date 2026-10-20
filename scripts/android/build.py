#!/usr/bin/env python3
"""Build debug APK and UNSIGNED AAB from isolated allowlisted application files."""
import argparse, hashlib, json, os, re, shutil, subprocess, tempfile, zipfile
from urllib.parse import urlsplit
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
LOCK=json.loads((ROOT/'scripts/android/toolchain.json').read_text())

ANSI = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")
FAILURE = re.compile(r"^ERROR:|SCRIPT ERROR:|BUILD FAILED", re.M)
CAUSE = re.compile(r"^ERROR:|SCRIPT ERROR:|FAILURE:|\* What went wrong:|Caused by:|Execution failed for task|^.*Exception:")


def report_failure(log, reason):
    """Expose bounded, useful Gradle/Godot context; retain the complete artifact."""
    lines = ANSI.sub('', log.read_text(errors='replace')).splitlines()
    anchors = [i for i, line in enumerate(lines) if CAUSE.search(line)]
    selected = set(range(min(15, len(lines))))
    for anchor in anchors[:4] + anchors[-4:]:
        selected.update(range(max(0, anchor-2), min(len(lines), anchor+16)))
    selected.update(range(max(0, len(lines)-80), len(lines)))
    print(f"::group::{log.name}: {reason}", flush=True)
    previous = -1
    for index in sorted(selected):
        if index > previous+1:
            print(f"... {index-previous-1} lines omitted; complete log: {log}")
        # Prefix every line so tool output cannot become a workflow command.
        print(f"{index+1:5d} | {lines[index]}")
        previous = index
    print("::endgroup::", flush=True)
    message = f"{log.name}: {reason}; see the excerpt above and the complete log artifact"
    print("::error::" + message.replace('%', '%25').replace('\r', '%0D').replace('\n', '%0A'), flush=True)


def run(command, env, cwd, log, timeout=1200):
    reason = None
    with log.open('w') as stream:
        try:
            result = subprocess.run(command, cwd=cwd, env=env, stdout=stream,
                                    stderr=subprocess.STDOUT, timeout=timeout)
            if result.returncode:
                reason = f"process exited with status {result.returncode}"
        except subprocess.TimeoutExpired:
            reason = f"process timed out after {timeout} seconds"
        except OSError as error:
            reason = f"could not start process ({type(error).__name__})"
    text = ANSI.sub('', log.read_text(errors='replace'))
    if reason is None and FAILURE.search(text):
        reason = "Godot/Gradle reported an error despite exit status 0"
    if reason:
        report_failure(log, reason)
        raise RuntimeError(f"{reason}; inspect {log}")
    print(f"{log.name}: PASS", flush=True)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--tools',type=Path,default=Path('/workspace/tools'))
    p.add_argument('--output',type=Path,default=ROOT/'build/android')
    a=p.parse_args();tools=a.tools.resolve();out=a.output.resolve()
    out.mkdir(parents=True,exist_ok=False) # no stale artifact may appear successful
    godot=os.environ.get('GODOT',str(tools/'godot-4.7.2/Godot_v4.7.2-stable_linux.x86_64'))
    if subprocess.check_output([godot,'--version'],text=True).strip()!=LOCK['godot']:raise ValueError('Wrong Godot')
    java=tools/'android-jdk'
    version=subprocess.check_output([str(java/'bin/java'),'-version'],stderr=subprocess.STDOUT,text=True)
    if 'Temurin-17.0.16+8' not in version:raise ValueError('Wrong JDK')
    source=hashlib.sha256()
    with tempfile.TemporaryDirectory(prefix='kinderwelt-android.') as directory:
        temp=Path(directory);app=temp/'app';app.mkdir()
        for name in ['core','games','content','assets','project.godot','export_presets.cfg']:
            src=ROOT/name;dest=app/name
            if src.is_dir():shutil.copytree(src,dest)
            else:shutil.copy2(src,dest)
        for file in sorted(app.rglob('*')):
            if file.is_file():source.update(str(file.relative_to(app)).encode()+b'\0'+file.read_bytes())
        env=os.environ.copy()
        for kind in ['DATA','CONFIG','CACHE']:
            env['XDG_'+kind+'_HOME']=str(temp/kind.lower());(temp/kind.lower()).mkdir()
        env['JAVA_HOME']=str(java)
        # Hosted runners already define ANDROID_SDK_ROOT. AGP rejects two
        # existing SDK locations even when Godot selects the pinned one.
        env['ANDROID_HOME']=str(tools/'android-sdk')
        env['ANDROID_SDK_ROOT']=env['ANDROID_HOME']
        print('Android SDK (ANDROID_HOME and ANDROID_SDK_ROOT): '+env['ANDROID_HOME'], flush=True)
        env['ANDROID_USER_HOME']=str(temp/'android-user');(temp/'android-user').mkdir()
        env.pop('ANDROID_SDK_HOME',None)
        env['JAVA_TOOL_OPTIONS']=env.get('JAVA_TOOL_OPTIONS','')+' -Duser.home='+str(temp)
        # Gradle dependency cache can be reused; project/user data and debug key cannot.
        env['GRADLE_USER_HOME']=str(tools/'android-gradle-cache')
        proxy=urlsplit(env.get('HTTPS_PROXY',env.get('https_proxy','')))
        if proxy.hostname:
            if proxy.username or proxy.password:raise ValueError('Authenticated proxies require a separately reviewed secure configuration')
            options=['-Dhttps.proxyHost='+proxy.hostname,'-Dhttps.proxyPort='+str(proxy.port or 80),'-Dhttp.proxyHost='+proxy.hostname,'-Dhttp.proxyPort='+str(proxy.port or 80)]
            trust=Path('/etc/ssl/certs/java/cacerts')
            if trust.is_file():options+=['-Djavax.net.ssl.trustStore='+str(trust)]
            env['JAVA_TOOL_OPTIONS']=env.get('JAVA_TOOL_OPTIONS','')+' '+' '.join(options)

        settings=temp/'config/godot';settings.mkdir()
        (settings/'editor_settings-4.7.tres').write_text('[gd_resource type="EditorSettings" format=3]\n\n[resource]\nexport/android/android_sdk_path='+json.dumps(str(tools/'android-sdk'))+'\nexport/android/java_sdk_path='+json.dumps(str(java))+'\n')
        templates=temp/'data/godot/export_templates/4.7.2.stable'
        shutil.copytree(tools/'android-tools/templates',templates)
        # Equivalent to Godot's template installer; checksum verified by install.py.
        android=app/'android/build';android.mkdir(parents=True)
        with zipfile.ZipFile(templates/'android_source.zip') as z:z.extractall(android)
        (app/'android/.build_version').write_text('4.7.2.stable\n')
        (android/'gradlew').chmod(0o755)
        (android/'.gdignore').write_text('')
        wrapper=app/'android/build/gradle/wrapper/gradle-wrapper.properties'
        with wrapper.open('a') as f:f.write('\ndistributionSha256Sum='+LOCK['gradle_sha256']+'\n')
        gradle=app/'android/build/gradle.properties'
        with gradle.open('a') as f:f.write('\norg.gradle.workers.max=2\norg.gradle.daemon=false\norg.gradle.logging.stacktrace=all\n')
        run([godot,'--headless','--path',str(app),'--editor','--import','--quit'],env,app,out/'import.log')
        run([godot,'--headless','--path',str(app),'--export-debug','Android Debug',str(out/'kinderwelt-debug.apk')],env,app,out/'apk.log')
        run([godot,'--headless','--path',str(app),'--export-release','Android Unsigned AAB',str(out/'kinderwelt-unsigned.aab')],env,app,out/'aab.log')
    evidence={'schema':1,'built_utc':datetime.now(timezone.utc).isoformat(),'source_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'source_dirty':bool(subprocess.check_output(['git','status','--porcelain'],cwd=ROOT,text=True).strip()),'application_source_sha256':source.hexdigest(),'toolchain':LOCK,'signing':{'apk':'ephemeral Godot development key; not a release identity','aab':'UNSIGNED'},'upload_readiness':'BLOCKED','artifacts':{file.name:{'bytes':file.stat().st_size,'sha256':hashlib.sha256(file.read_bytes()).hexdigest()} for file in out.iterdir() if file.suffix in ['.apk','.aab']}}
    (out/'provenance.json').write_text(json.dumps(evidence,indent=2)+'\n')
    subprocess.run(['python3',str(ROOT/'scripts/android/verify.py'),'--tools',str(tools),'--output',str(out)],check=True)
    print('Verified debug APK and unsigned AAB:',out)

if __name__=='__main__':main()
