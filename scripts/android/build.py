#!/usr/bin/env python3
"""Build development APK/unsigned AAB, or an explicitly configured neutral release AAB."""
import sys
from contextlib import ExitStack
import argparse, hashlib, json, os, re, shutil, subprocess, tempfile, zipfile
from urllib.parse import urlsplit
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
import variants
sys.path.insert(0,str(ROOT/'scripts/android'))
import identity
import debug_key
import backup_policy
import asset_notices
import upload_signing
LOCK=json.loads((ROOT/'scripts/android/toolchain.json').read_text())

ANSI = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")
FAILURE = re.compile(r"^ERROR:|SCRIPT ERROR:|BUILD FAILED", re.M)
CAUSE = re.compile(r"^ERROR:|SCRIPT ERROR:|FAILURE:|\* What went wrong:|Caused by:|Execution failed for task|^.*Exception:")


def git_provenance(root):
    """Do not borrow a parent repository's clean status for an ignored capsule."""
    def git(*args):
        try:
            return subprocess.run(['git','-C',str(root),*args],text=True,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,check=False)
        except FileNotFoundError:return None
    top=git('rev-parse','--show-toplevel')
    if top is None or top.returncode or Path(top.stdout.strip()).resolve()!=root.resolve():
        return {'source_tracking':'unversioned-snapshot','source_commit':None,'source_dirty':None}
    commit=git('rev-parse','HEAD');status=git('status','--porcelain')
    if commit.returncode or status.returncode:
        return {'source_tracking':'git-unresolved','source_commit':None,'source_dirty':None}
    return {'source_tracking':'git-worktree','source_commit':commit.stdout.strip(),'source_dirty':bool(status.stdout.strip())}


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
    p.add_argument('--variant',choices=['family','public'],help='Default: family for development, public for release')
    p.add_argument('--release',action='store_true',help='Build only a signed neutral release AAB; requires operator-owned upload credentials')
    p.add_argument('--preview',action='store_true',help='Use a separate variant/version test identity and local save')
    p.add_argument('--package-id',help='Explicit identity; release also accepts KINDERWELT_PACKAGE_ID')
    a=p.parse_args();tools=a.tools.resolve();out=a.output.resolve()
    a.variant=a.variant or ('public' if a.release else 'family')
    values=None
    try:
        if a.release:
            if a.variant!='public' or a.preview:raise ValueError('Release requires the neutral/public variant without --preview')
            a.package_id=identity.validate_configured_release_package(a.package_id or os.environ.get('KINDERWELT_PACKAGE_ID'))
            values=upload_signing.credentials()
            upload_signing.metadata()
        elif a.package_id:
            identity.validate_package(a.package_id)
    except ValueError as error:
        p.error(str(error))
    out.mkdir(parents=True,exist_ok=False) # no stale artifact may appear successful
    godot=os.environ.get('GODOT',str(tools/'godot-4.7.2/Godot_v4.7.2-stable_linux.x86_64'))
    with tempfile.TemporaryDirectory(prefix='kinderwelt-version.') as version_cache:
        probe_env=upload_signing.export_environment()
        probe_env['XDG_CACHE_HOME']=version_cache
        if subprocess.check_output([godot,'--version'],text=True,env=probe_env).strip()!=LOCK['godot']:raise ValueError('Wrong Godot')
    java=tools/'android-jdk'
    version=subprocess.check_output([str(java/'bin/java'),'-version'],stderr=subprocess.STDOUT,text=True)
    if 'Temurin-17.0.16+8' not in version:raise ValueError('Wrong JDK')
    source=hashlib.sha256()
    tracking=git_provenance(ROOT)
    # A character file must have reviewed generation provenance before export.
    sys.path.insert(0,str(ROOT/'scripts/qa'))
    import character_origins
    character_origins.audit(ROOT)
    sys.path.insert(0,str(ROOT/'scripts/store'))
    import approved_privacy
    approved_privacy.check(ROOT/'docs/privacy/site')
    with tempfile.TemporaryDirectory(prefix='kinderwelt-android.') as directory, ExitStack() as signing_context:
        temp=Path(directory);app=temp/'app'
        upload_key=None
        if a.release:
            upload_key=signing_context.enter_context(upload_signing.materialize(values,temp))
            upload_fingerprint=upload_signing.certificate(upload_key,java,values)
        variants.snapshot(app,a.variant)
        package=identity.configure(app,a.package_id,a.preview,a.variant)
        asset_notices.check_filters(app)
        for file in sorted(app.rglob('*')):
            if file.is_file():source.update(str(file.relative_to(app)).encode()+b'\0'+file.read_bytes())
        env=upload_signing.export_environment()
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
        # Gradle dependencies and the development certificate are reused outside source.
        # Project/user data remain isolated; no release key is loaded.
        env['GRADLE_USER_HOME']=str(tools/'android-gradle-cache')
        proxy=urlsplit(env.get('HTTPS_PROXY',env.get('https_proxy','')))
        if proxy.hostname:
            if proxy.username or proxy.password:raise ValueError('Authenticated proxies require a separately reviewed secure configuration')
            options=['-Dhttps.proxyHost='+proxy.hostname,'-Dhttps.proxyPort='+str(proxy.port or 80),'-Dhttp.proxyHost='+proxy.hostname,'-Dhttp.proxyPort='+str(proxy.port or 80)]
            trust=Path('/etc/ssl/certs/java/cacerts')
            if trust.is_file():options+=['-Djavax.net.ssl.trustStore='+str(trust)]
            env['JAVA_TOOL_OPTIONS']=env.get('JAVA_TOOL_OPTIONS','')+' '+' '.join(options)

        key=None if a.release else debug_key.ensure(tools,java)
        settings=temp/'config/godot';settings.mkdir()
        editor='[gd_resource type="EditorSettings" format=3]\n\n[resource]\nexport/android/android_sdk_path='+json.dumps(str(tools/'android-sdk'))+'\nexport/android/java_sdk_path='+json.dumps(str(java))+'\n'
        if key:editor+='export/android/debug_keystore='+json.dumps(str(key))+'\nexport/android/debug_keystore_user="androiddebugkey"\nexport/android/debug_keystore_pass="android"\n'
        (settings/'editor_settings-4.7.tres').write_text(editor)
        templates=temp/'data/godot/export_templates/4.7.2.stable'
        shutil.copytree(tools/'android-tools/templates',templates)
        # Equivalent to Godot's template installer; checksum verified by install.py.
        android=app/'android/build';android.mkdir(parents=True)
        with zipfile.ZipFile(templates/'android_source.zip') as z:z.extractall(android)
        (app/'android/.build_version').write_text('4.7.2.stable\n')
        (android/'gradlew').chmod(0o755)
        backup_policy.install(android)
        (android/'.gdignore').write_text('')
        wrapper=app/'android/build/gradle/wrapper/gradle-wrapper.properties'
        with wrapper.open('a') as f:f.write('\ndistributionSha256Sum='+LOCK['gradle_sha256']+'\n')
        gradle=app/'android/build/gradle.properties'
        with gradle.open('a') as f:f.write('\norg.gradle.workers.max=2\norg.gradle.daemon=false\norg.gradle.logging.stacktrace=all\n')
        run([godot,'--headless','--path',str(app),'--editor','--import','--quit'],env,app,out/'import.log')
        if not a.release:
            run([godot,'--headless','--path',str(app),'--export-debug','Android Debug',str(out/'kinderwelt-debug.apk')],env,app,out/'apk.log')
        run([godot,'--headless','--path',str(app),'--export-release','Android Unsigned AAB',str(out/'kinderwelt-unsigned.aab')],env,app,out/'aab.log')
        if a.release:
            upload_signing.sign(out/'kinderwelt-unsigned.aab',out/'kinderwelt-release-neutral.aab',upload_key,java,values)
            upload_signing.verify(out/'kinderwelt-release-neutral.aab',java,upload_fingerprint)
            (out/'kinderwelt-unsigned.aab').unlink()
        evidence={'schema':2,'built_utc':datetime.now(timezone.utc).isoformat(),**tracking,'git_state_changed_during_build':(git_provenance(ROOT)!=tracking) if tracking['source_tracking']=='git-worktree' else None,'application_source_sha256':source.hexdigest(),'toolchain':LOCK,'variant':a.variant,'package':package,'identity_status':identity.CONFIG['identity_status'] if not a.package_id else 'EXPLICIT_OVERRIDE; no Play approval','version_name':identity.CONFIG['version_name'],'version_code':identity.CONFIG['version_code'],'signing':({'aab':'UPLOAD_SIGNED','upload_certificate_sha256':upload_fingerprint} if a.release else {'apk':'cached development-only Godot key; not a release identity','aab':'UNSIGNED','development_certificate_sha256':debug_key.fingerprint(key,java)}),'upload_readiness':'BLOCKED','artifacts':{file.name:{'bytes':file.stat().st_size,'sha256':hashlib.sha256(file.read_bytes()).hexdigest()} for file in out.iterdir() if file.suffix in ['.apk','.aab']}}
        (out/'provenance.json').write_text(json.dumps(evidence,indent=2)+'\n')
        verify=['python3',str(ROOT/'scripts/android/verify.py'),'--tools',str(tools),'--output',str(out),'--package',evidence['package'],'--source',str(app)]
        if a.release:verify+=['--release','--upload-certificate-sha256',upload_fingerprint]
        subprocess.run(verify,env=env,check=True)
        if not a.release:
            subprocess.run(['python3',str(ROOT/'scripts/android/analyze_size.py'),str(out/'kinderwelt-debug.apk'),str(out/'kinderwelt-unsigned.aab'),'--output',str(out/'size-analysis.json')],env=env,check=True)
        print('Verified neutral upload-signed AAB; Play approval remains BLOCKED:' if a.release else 'Verified debug APK and unsigned AAB:',out)


if __name__=='__main__':main()
