#!/usr/bin/env python3
"""Deliver a verified neutral upload-signed AAB to a PRIVATE GitHub DRAFT release.

No Play upload and no release publication. This delivery uses GitHub Releases
storage rather than the Actions artifact quota. Never accepts a family/debug build.
"""
import argparse,hashlib,json,os,re,subprocess,sys,zipfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import identity,upload_signing
ROOT=Path(__file__).resolve().parents[2]
BUNDLE='kinderwelt-release-neutral.aab'
def validate(directory,tools):
    directory=Path(directory)
    for name in [BUNDLE,'provenance.json','verification.json']:
        if (directory/name).is_symlink():raise ValueError('Symlink in release review inputs')
    proof=json.loads((directory/'provenance.json').read_text());verification=json.loads((directory/'verification.json').read_text())
    if proof.get('variant')!='public' or proof.get('signing',{}).get('aab')!='UPLOAD_SIGNED':raise ValueError('Only neutral upload-signed bundles may be delivered')
    if proof.get('source_tracking')!='git-worktree' or proof.get('source_dirty') is not False or proof.get('git_state_changed_during_build') is not False:raise ValueError('A clean, unchanged source checkout is required')
    if not re.fullmatch('[0-9a-f]{40}',proof.get('source_commit','')):raise ValueError('Missing release source commit')
    identity.validate_configured_release_package(proof.get('package'))
    if verification.get('status')!='PASS':raise ValueError('Release verification did not pass')
    bundled=verification.get('artifacts',{}).get(BUNDLE,{})
    if bundled.get('package')!=proof['package'] or bundled.get('version_name')!=proof.get('version_name') or bundled.get('version_code')!=proof.get('version_code'):raise ValueError('Verification/provenance identity mismatch')
    bundle=directory/BUNDLE;metadata=proof.get('artifacts',{}).get(BUNDLE,{})
    if bundle.stat().st_size!=metadata.get('bytes') or hashlib.sha256(bundle.read_bytes()).hexdigest()!=metadata.get('sha256'):raise ValueError('Bundle changed after export verification')
    if bundled.get('bytes')!=metadata['bytes'] or bundled.get('sha256')!=metadata['sha256'] or bundled.get('permissions')!=[] or bundled.get('allow_backup') is not False:raise ValueError('Verification report does not describe this bundle')
    if proof.get('version_name')!=identity.CONFIG['version_name'] or proof.get('version_code')!=identity.CONFIG['version_code']:raise ValueError('Release version differs from the reviewed source')
    with zipfile.ZipFile(bundle) as archive:
        names=archive.namelist();casts=[n for n in names if n.endswith('/assets/quest/cast.json')]
        if len(casts)!=1 or json.loads(archive.read(casts[0])).get('variant')!='public' or any(re.search(r'(?:actor|outfits)-[1-6]\.png',n) for n in names):raise ValueError('Family or unknown cast in review bundle')
    upload_signing.verify(bundle,Path(tools)/'android-jdk',proof['signing'].get('upload_certificate_sha256'))
    files=[bundle,directory/'provenance.json',directory/'verification.json']
    for name in ['aab-manifest.xml','aab-validation.txt','aab-signature.txt','size/SIZE_REPORT.md','size/size-report.json']:
        file=directory/name
        if file.is_file() and not file.is_symlink():files.append(file)
    # No keystores, raw export logs, source archives or family inputs.
    return proof,files
def gh(*args):
    result=subprocess.run(['gh',*map(str,args)],text=True,capture_output=True,env=upload_signing.export_environment())
    if result.returncode:raise ValueError('GitHub draft delivery failed; check repository access (tool diagnostics withheld)')
    return result.stdout
def deliver(directory,tools,repo,run_id):
    if not re.fullmatch('[A-Za-z0-9_-]+/[A-Za-z0-9_.-]+',repo) or not re.fullmatch(r'[0-9]+(?:\.[0-9]+)?',run_id):raise ValueError('Invalid repository/run identifier')
    proof,files=validate(directory,tools)
    repository=json.loads(gh('api','repos/'+repo))
    if repository.get('private') is not True:raise ValueError('Draft delivery is restricted to the private repository')
    tag='upload-review-v'+proof['version_name']+'-c'+str(proof['version_code'])+'-'+run_id
    notes=Path(directory)/'draft-notes.md'
    notes.write_text('Neutral upload-signed Android bundle for operator review.\n\nSource: '+proof['source_commit']+'\nPackage: '+proof['package']+'\n\nThis is a private GitHub draft, not a Google Play upload or approval. Device, listening, rights, privacy hosting and Play Console acceptance remain operator responsibilities. No family graphics or source photos included.\n')
    gh('release','create',tag,*files,'--repo',repo,'--target',proof['source_commit'],'--draft','--title','Kinderwelt '+proof['version_name']+' — neutral upload review','--notes-file',notes)
    return json.loads(gh('release','view',tag,'--repo',repo,'--json','url,isDraft'))
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);p.add_argument('--tools',type=Path,required=True);p.add_argument('--repo',required=True);p.add_argument('--run-id',required=True);a=p.parse_args()
    try:
        result=deliver(a.output,a.tools,a.repo,a.run_id)
        if result.get('isDraft') is not True:raise ValueError('Delivery did not remain a draft')
        print('Private draft review:',result['url'])
    except (ValueError,KeyError,FileNotFoundError) as error:p.error(str(error))
