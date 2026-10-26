#!/usr/bin/env python3
"""Render neutral Store drafts in isolated app/user storage, never real photos."""
import argparse,json,os,re,shutil,struct,subprocess,sys,tempfile,xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
import variants
sys.path.insert(0,str(ROOT/'scripts/android'))
from build import git_provenance
import upload_signing
sys.path.insert(0,str(ROOT/'scripts/qa'))
import character_origins

def validate_placeholder(path):
    text=Path(path).read_text()
    if '<!' in text:raise ValueError('No document entities in store placeholder')
    svg=ET.fromstring(text)
    for element in svg.iter():
        if element.tag.split('}')[-1] not in {'svg','circle','path','rect','ellipse'}:raise ValueError('Store placeholder must contain only geometric shapes, never photos')
        if set(element.attrib)-{'width','height','viewBox','cx','cy','r','d','fill','x','y','rx','ry'}:raise ValueError('External resources and active attributes are forbidden')
        if any(re.search(r'url\(|https?:|data:|file:',v,re.I) for v in element.attrib.values()):raise ValueError('No external or embedded image input')
    if svg.tag.split('}')[-1]!='svg':raise ValueError('Expected a geometric SVG')

def validate_cast(app):
    cast=json.loads((app/'assets/quest/cast.json').read_text())
    if cast['variant']!='public':raise ValueError('Store screenshots must use the neutral cast')
    resources=set(cast['sprites'].values())|set(cast['atlases'].values())
    allowed={'assets/quest/characters/neutral-cast.png','assets/quest/squirrel.png','assets/quest/looks-squirrel.png',*[f'assets/quest/characters/actor-{i}.tres' for i in range(1,7)]}
    if resources!=allowed:raise ValueError('Unexpected or family illustration in store inputs')
    expected={'neutral-cast.png',*[f'actor-{i}.tres' for i in range(1,7)]}
    if {p.name for p in (app/'assets/quest/characters').iterdir()}!=expected:raise ValueError('Unexpected character input')
    if '.private' in (app/'core/quest/cast.gd').read_text():raise ValueError('Private source in cast')

def verify_output(output):
    captures=json.loads((output/'captures.json').read_text())
    expected={'icon-512.png':(512,512),'feature-1024x500.png':(1024,500)}
    for locale in ['de','en','ru']:
        for index,name in enumerate(['characters','own-character','world','maths','reward'],1):expected[f'{locale}-{index:02}-{name}.png']=(1080,1920)
    if {c['file'] for c in captures}!=set(expected) or len(captures)!=17:raise ValueError('Incomplete/duplicate store captures')
    for name,size in expected.items():
        data=(output/name).read_bytes()
        if data[:8]!=b'\x89PNG\r\n\x1a\n' or struct.unpack('>II',data[16:24])!=size:raise ValueError('Wrong PNG dimensions: '+name)
    return expected

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,default=ROOT/'build/store');parser.add_argument('--godot',default=os.environ.get('GODOT','godot'));args=parser.parse_args()
    output=args.output.resolve();validate_placeholder(ROOT/'art/store/silhouette.svg')
    character_origins.audit(ROOT)
    output.mkdir(parents=True,exist_ok=False)
    with tempfile.TemporaryDirectory(prefix='kinderwelt-store.') as directory:
        temp=Path(directory);app=temp/'app'
        variants.snapshot(app,'public');validate_cast(app)
        (app/'store').mkdir()
        for name in ['capture.gd','feature.gd']:shutil.copy2(ROOT/'scripts/store'/name,app/'store'/name)
        shutil.copy2(ROOT/'art/store/silhouette.svg',app/'store/silhouette.svg')
        env=upload_signing.export_environment()
        for kind in ['DATA','CONFIG','CACHE']:
            env['XDG_'+kind+'_HOME']=str(temp/kind.lower());(temp/kind.lower()).mkdir()
        env['KINDERWELT_STORE_OUTPUT']=str(output)
        for name,command in [('import',[args.godot,'--headless','--path',str(app),'--editor','--import','--quit']),('render',[args.godot,'--path',str(app),'--audio-driver','Dummy','-s','res://store/capture.gd'])]:
            with (output/(name+'.log')).open('w') as stream:result=subprocess.run(command,env=env,stdout=stream,stderr=subprocess.STDOUT,timeout=180)
            log=(output/(name+'.log')).read_text()
            if result.returncode or re.search(r'ERROR:|SCRIPT ERROR:|Parse Error',log):raise RuntimeError('Store '+name+' failed; inspect '+str(output/(name+'.log')))
        verify_output(output)
    (output/'provenance.json').write_text(json.dumps({**git_provenance(ROOT),'variant':'public','own_image':'original geometric silhouette; no person/photo','images':17,'phone_dpi':420,'publication':'DRAFT; operator approval and rights required'},indent=2)+'\n')
    print('Store render: PASS; 17 PNGs:',output)
if __name__=='__main__':main()
