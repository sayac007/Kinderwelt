#!/usr/bin/env python3
"""Check local documentation and CI references; keep run output outside docs.

Archive identity is checked offline against the reviewed one-time index. The
optional GitHub check verifies every original blob at its pinned remote commit.
External non-archive HTTP links are listed, not silently certified as reachable.
"""
import argparse,csv,hashlib,json,re,subprocess
from pathlib import Path
from urllib.parse import unquote,urlsplit
ROOT=Path(__file__).resolve().parents[2]
SOURCE='a55e9e0a3bfda0128d2a1aeba94e5dd1b300981e'
COMMAND='GODOT=/pfad/zu/Godot_v4.7.2-stable_linux.x86_64 KINDERWELT_VARIANT=public bash tests/run.sh'

def check(root=ROOT,remote=False):
    root=Path(root);findings=[];external=set();local_count=0;ci_count=0
    index=root/'docs/qa/ARCHIVE_INDEX.tsv'
    with index.open() as f:rows=list(csv.DictReader(f,delimiter='\t'))
    assert len(rows)==139 and sum(int(r['bytes']) for r in rows)==7383943,'Archive inventory changed'
    for row in rows:
        assert re.fullmatch('[0-9a-f]{64}',row['sha256'])
        assert row['archive_url']==f'https://github.com/sayac007/Kinderwelt/blob/{SOURCE}/'+row['original_path']
    docs=[root/'README.md',*([root/'ASSETS_LICENSE.md'] if (root/'ASSETS_LICENSE.md').is_file() else []),*sorted((root/'docs').rglob('*.md'))]
    for doc in docs:
        if 'internal' in doc.relative_to(root).parts:continue
        text=re.sub(r'^```[^\n]*\n.*?^```\s*$', '',doc.read_text(),flags=re.M|re.S)
        targets=[m[1] for m in re.finditer(r'!?\[[^\]]*\]\((<[^>]*>|[^)\s]+)(?:\s+"[^"]*")?\)',text)]
        targets.extend(m[1] for m in re.finditer(r'^\[[^\]]+\]:\s*(\S+)',text,re.M))
        external.update(u.rstrip('.,;') for u in re.findall(r'https?://[^\s<>"`)]+',text))
        for target in targets:
            target=target.strip('<>');url=urlsplit(target)
            if url.scheme in ('http','https'):
                external.add(target);continue
            if url.scheme:continue
            path=(doc.parent/unquote(url.path)).resolve() if url.path else doc;local_count+=1
            if not path.exists():findings.append(f'{doc.relative_to(root)}: missing {target}')
            elif url.fragment and path.suffix=='.md':
                headings=re.findall(r'^#+\s+(.+?)\s*#*$',path.read_text(),re.M)
                anchors={re.sub(r'[^\w -]','',h.casefold()).replace(' ','-') for h in headings}
                if unquote(url.fragment) not in anchors:findings.append(f'{doc.relative_to(root)}: missing anchor {target}')
    assert COMMAND in (root/'README.md').read_text() and COMMAND in (root/'docs/QUALITY_ASSURANCE.md').read_text(),'Entry commands differ'
    for workflow in sorted((root/'.github/workflows').glob('*.yml')):
        for target in set(re.findall(r'\b(?:scripts|tests)/[\w./-]+\.(?:py|sh|gd|json)\b',workflow.read_text())):
            ci_count+=1
            if not (root/target).is_file():findings.append(f'{workflow.relative_to(root)}: missing {target}')
    for file in (root/'docs/qa').iterdir():
        if file.name not in ['README.md','ARCHIVE_INDEX.tsv','VISUAL_IP_AUDIT.md','visual-ip-manifest.json']:findings.append('Unexpected new QA run file: '+file.name)
    archive_urls={row['archive_url'] for row in rows}
    for url in external:
        prefix=f'https://github.com/sayac007/Kinderwelt/blob/{SOURCE}/docs/qa/'
        if url.startswith(prefix) and url not in archive_urls:findings.append('Unknown archive link: '+url)
    verified=0
    if remote:
        data=json.loads(subprocess.check_output(['gh','api',f'repos/sayac007/Kinderwelt/git/trees/{SOURCE}?recursive=1']))
        assert not data['truncated'],'Incomplete GitHub tree'
        blobs={r['path']:r for r in data['tree'] if r['type']=='blob'}
        for row in rows:
            actual=blobs[row['original_path']]
            assert actual['sha']==row['git_blob'] and actual['size']==int(row['bytes'])
            raw=subprocess.check_output(['git','show',SOURCE+':'+row['original_path']],cwd=root)
            assert hashlib.sha256(raw).hexdigest()==row['sha256'];verified+=1
        tag=json.loads(subprocess.check_output(['gh','api','repos/sayac007/Kinderwelt/git/ref/tags/qa-evidence/2026-10-23-v091']))
        obj=json.loads(subprocess.check_output(['gh','api','repos/sayac007/Kinderwelt/git/tags/'+tag['object']['sha']]))
        assert obj['object']['sha']==SOURCE,'Archive tag moved'
    return {'status':'FAIL' if findings else 'PASS','findings':findings,'local_markdown_targets':local_count,
            'ci_file_references':ci_count,'archive_files':len(rows),'archive_source':SOURCE,
            'github_archive_files_verified':verified,'external_http':'Not certified by the offline check; archive verified separately when requested',
            'external_links':sorted(external)}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true');p.add_argument('--verify-archive',action='store_true');p.add_argument('--output',type=Path,default=ROOT/'qa-results/documentation.json');a=p.parse_args()
    result=check(remote=a.verify_archive);a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('Documentation:',result['status'],';',result['local_markdown_targets'],'local links;',result['ci_file_references'],'CI references;',result['github_archive_files_verified'],'remote archive files verified')
    for issue in result['findings']:print(issue)
    raise SystemExit(1 if result['findings'] else 0)
if __name__=='__main__':main()
