#!/usr/bin/env python3
"""Produce owner-only offline contact sheets/crops, never upload or replace art."""
import argparse,csv,hashlib,html,io,json,os,re,shutil,zipfile
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
import visual_ip as audit
LOOKS=['classic','hero','alien','astronaut','scientist']
def frame_image(raw,frame=None,mask_runs=None):
    if frame and 'frame_index' in frame:
        image=Image.open(io.BytesIO(raw));image.seek(frame['frame_index']);image=image.convert('RGBA')
    else:image=audit.decoded(raw)
    if frame is None:return image
    if mask_runs and frame['label'].split('-')[-1] in LOOKS[1:]:
        owner=LOOKS.index(frame['label'].split('-')[-1]);mask=Image.new('L',image.size);draw=ImageDraw.Draw(mask)
        for y,left,length,value in mask_runs:
            if value==owner:draw.rectangle((left,y,left+length-1,y),fill=255)
        image.putalpha(ImageChops.multiply(image.getchannel('A'),mask))
    x,y,w,h=frame['rect']
    if min(x,y)<0 or min(w,h)<=0 or x+w>image.width or y+h>image.height:raise ValueError('Frame outside source')
    return image.crop((x,y,x+w,y+h))

def masks(row,frame,root):
    if not frame or not frame.get('mask_available'):return None
    if frame.get('mask_git_blob'):
        data=json.loads(audit.git(root,'cat-file','blob',frame['mask_git_blob']));heroes=list(data.get('heroes',{}).values()) if 'heroes' in data else [data];return heroes[frame['mask_hero_index']].get('mask_runs')
    if frame['label'].startswith('cast-'):
        heroes=list(json.loads((root/'art/public/characters/frames.json').read_text())['heroes'].values());return heroes[int(frame['label'].split('-')[1])-1]['mask_runs']
    if frame['label'].startswith('squirrel-'):return json.loads((root/'art/shared/squirrel-looks.json').read_text()).get('mask_runs')
    if frame['label'].startswith('private-'):
        heroes=list(json.loads((root/'.private/characters/looks.json').read_text())['heroes'].values());return heroes[int(frame['label'].split('-')[1])-1].get('mask_runs')
    return None

def source(row):
    return min(row['occurrences'],key=lambda o:(not o['tracked'],not o['path'].startswith(('assets/','art/','historical/')),len(o['path'])))

def contact_sheets(folder,entries):
    paths=[]
    for page in range((len(entries)+19)//20):
        items=entries[page*20:page*20+20];sheet=Image.new('RGB',(1000,1400),'#edf1f5');draw=ImageDraw.Draw(sheet)
        for offset,item in enumerate(items):
            x=(offset%4)*250;y=(offset//4)*280;path=folder/item['candidate']
            if path.suffix=='.svg':draw.text((x+15,y+80),'SVG: inspect original locally',fill='#172c3e')
            else:
                image=Image.open(path).convert('RGBA');image.thumbnail((232,215));sheet.paste(image,(x+(250-image.width)//2,y+5),image)
            draw.text((x+8,y+222),f"{page*20+offset+1:02d}  {item['risk']}",fill='#172c3e')
            label=item['id'];draw.text((x+8,y+240),label[:33],fill='#172c3e');draw.text((x+8,y+254),label[33:66],fill='#172c3e')
        name=f'contact_sheet_{page+1:02d}.png';sheet.save(folder/name);paths.append(name)
    return paths

def prepare(report,output,root=audit.ROOT,limit=40):
    root=root.resolve();output=output.resolve()
    if output==root or root in output.parents:raise ValueError('Review pack must remain outside the repository')
    if output.exists():raise ValueError('Refusing to overwrite an existing review pack')
    output.mkdir(parents=True,mode=0o700);os.chmod(output,0o700)
    audit.redacted(report) # allocate stable opaque local aliases before export
    pool=[]
    for row in report['images']:
        if row['format'] in ['Font','GodotResource','GodotTexture','SVG']:continue
        primary=any(o['tracked'] and o['path'].startswith(('assets/quest/','art/public/')) for o in row['occurrences'])
        if row['sensitivity']=='non_sensitive' and (primary or row.get('historical_unestablished')):
            priority=0 if row.get('historical_unestablished') else 1 if any(o['path']=='assets/quest/appicon.png' for o in row['occurrences']) else 2
            # Original app-icon source remains inventoried; one search candidate
            # is enough for this explicitly linked runtime/source image pair.
            if any(o['path']=='art/public/app-icon/original.png' for o in row['occurrences']):continue
            pool.append((priority,row,None))
            for f in row['frames']:
                if f['label'].startswith(('cast-','squirrel-')):pool.append((3 if f['label'].endswith(('hero','astronaut')) else 4,row,f))
    pool.sort(key=lambda item:(item[0],item[1]['id'],item[2]['id'] if item[2] else ''))
    private=[]
    for row in report['images']:
        local_source=any(o['path'].startswith(('.private/','external-generated/','git-retained/')) for o in row['occurrences'])
        if row['sensitivity']!='non_sensitive' and local_source and row['format'] in ['PNG','JPEG','WEBP','GIF']:
            private.append((0,row,None))
            for f in row['frames']:private.append((1,row,f))
    summaries={}
    for label,items in [('public-candidates',pool[:limit]),('restricted-family',private)]:
        folder=output/label;folder.mkdir(mode=0o700);(folder/'candidates').mkdir(mode=0o700);entries=[]
        for index,(_,row,f) in enumerate(items,1):
            original=source(row);raw=audit.load_bytes(original['locator'],root)
            if audit.sha(raw)!=row['sha256']:raise ValueError('Source changed since inventory')
            id=row['id'] if f is None else f['id'];name=re.sub('[^a-zA-Z0-9_.-]','_',id)
            if label=='restricted-family':
                name=report['private_ids'][row['sha256']]
                if f:name+='-frame-'+audit.sha(json.dumps([f['rect'],f.get('frame_index')]).encode())[:10]
                id=name
            if row['format']=='SVG' and f is None:
                if row.get('external_resources'):continue
                candidate='candidates/'+name+'.svg';(folder/candidate).write_bytes(raw);transform='Byte-for-byte SVG copy; no external resources fetched'
            elif f is None and row['format'] in ['PNG','JPEG','WEBP','GIF']:
                extension={'PNG':'.png','JPEG':'.jpg','WEBP':'.webp','GIF':'.gif'}[row['format']];candidate='candidates/'+name+extension;(folder/candidate).write_bytes(raw);transform='Byte-for-byte original review copy; source metadata retained'
            else:
                candidate='candidates/'+name+'.png';image=frame_image(raw,f,masks(row,f,root));image.save(folder/candidate)
                transform='Lossless PNG review copy' if f is None else 'Lossless atlas crop; authoritative runtime ownership mask applied when available'
            entries.append({'rank':len(entries)+1,'id':id,'risk':row['risk']['overall'],'candidate':candidate,'candidate_sha256':audit.sha((folder/candidate).read_bytes()),'source_path':original['path'],'source_sha256':row['sha256'],'frame_coordinates':f.get('rect') if f else None,'reason':row['recommended_action'],'provenance_issue':row['declared_license'],'lineage':transform,'online_upload_permitted':False,'reverse_search_status':'not_searched','owner_decision':'','result_urls':'','access_date':'','evidence_note_paths':'','search_notes':'','follow_up_action':''})
        sheets=contact_sheets(folder,entries)
        keys=['rank','id','risk','source_path','source_sha256','frame_coordinates','reason','provenance_issue','online_upload_permitted','reverse_search_status','owner_decision','result_urls','access_date','evidence_note_paths','search_notes','follow_up_action','candidate','candidate_sha256','lineage']
        with (folder/'review_queue.csv').open('w',newline='') as stream:
            writer=csv.DictWriter(stream,fieldnames=keys);writer.writeheader();writer.writerows(entries)
        (folder/'manifest.json').write_text(json.dumps({'scope':'Private/local owner triage; not a legal clearance or upload permission','entries':entries},ensure_ascii=False,indent=2)+'\n')
        intro='Non-sensitive candidates for a SPECIFIC owner upload decision. No online search has been performed and permission is not granted by this pack.' if label=='public-candidates' else 'RESTRICTED FAMILY/UNCLASSIFIED SOURCE MATERIAL. Offline owner review only. Do not upload to image-search, vision services, PR attachments, CI artifacts or releases.'
        rows=''.join('<article><h2>'+str(i+1)+' · '+html.escape(e['id'])+' · '+e['risk']+'</h2><a href="'+e['candidate']+'"><img src="'+e['candidate']+'" alt="Local audit candidate" width="240"></a><p>'+html.escape(e['reason'])+'</p><p>Source SHA-256: '+e['source_sha256']+'</p><p>'+html.escape(e['lineage'])+'</p><label><input type="checkbox">Original source/author/license reviewed</label> <label><input type="checkbox">Specific resemblance checked</label><p>Reverse search: not_searched. Record your decision in review_queue.csv; boxes here are not saved.</p></article>' for i,e in enumerate(entries))
        page='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src \'none\'; img-src \'self\' file:; style-src \'unsafe-inline\'; connect-src \'none\'"><title>Private visual IP review</title><style>body{font:17px system-ui;max-width:1000px;margin:2rem auto;padding:1rem}article{border-top:1px solid #aaa;padding:1rem}img{object-fit:contain;max-height:260px}p{overflow-wrap:anywhere}</style><h1>Private visual IP review</h1><p>'+intro+'</p><p>Resemblance is not proof of infringement; no match is not proof of originality or rights.</p>'+rows+'</html>'
        (folder/'index.html').write_text(page)
        if label=='public-candidates':
            readme='''# Private owner review: non-sensitive candidates

Nothing has been submitted to an image-search or external vision service.
Every queue row starts `not_searched` and `online_upload_permitted=false`.
The owner must approve a specific non-sensitive candidate before any upload.
This pack does not authorize uploading family/private or unclassified material.

After your specific approval, manual Google Lens / Google Images steps:
1. Open images.google.com in your own browser and select the camera/Lens control.
2. Upload only the approved file from this folder's candidates directory.
   Use the individual atlas crop when the full sheet hides the element.
3. Inspect visually similar results and open the original publication pages.
   A repost, stock aggregator or AI gallery is not sufficient source evidence.
4. Trace the earliest credible author/source; check dates, original files,
   license version and attribution/share-alike/non-commercial/no-derivatives
   restrictions. Copyright, trademark and personality rights are separate.
5. Record URLs, access date, screenshots/notes and your decision in the local
   queue. Keep any newly discovered private information out of Git/CI.
6. A search with no hits is not clearance. Resemblance alone is not proof of
   infringement. Obtain the missing rights/evidence or seek qualified advice
   before deciding whether a specific asset needs replacement.

Do not publish this pack, its contact sheets or its ZIP as a repository artifact.
'''
        else:readme='''# Restricted local review

Family-derived and unclassified retained source images. Owner-only offline
inspection. No permission for external image-search or vision uploads. Do not
publish these images, names, paths, contact sheets or the ZIP in Git, PRs, CI or
releases. Review consent and distribution scope separately from copyright.

The full inventory remains in the parent private audit directory. It also lists
unclassified screenshots/derived material that was not duplicated into this
pack. Original family reference photos were not downloaded or opened; generated
illustrations do not prove consent or the rights in those original photos.
'''
        (folder/'README.md').write_text(readme)
        archive=output/(label+'.zip')
        with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
            for p in sorted(folder.rglob('*')):
                if p.is_file():z.write(p,p.relative_to(folder))
        os.chmod(archive,0o600)
        with zipfile.ZipFile(archive) as z:
            if z.testzip() is not None:raise ValueError('Review ZIP CRC failure')
        summaries[label]={'candidates':len(entries),'contact_sheets':len(sheets),'zip':str(archive),'bytes':archive.stat().st_size,'sha256':audit.sha(archive.read_bytes())}
    (output/'delivery.json').write_text(json.dumps(summaries,indent=2)+'\n')
    return summaries
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--inventory',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--root',type=Path,default=audit.ROOT);a=p.parse_args();print(json.dumps(prepare(json.loads(a.inventory.read_text()),a.output,a.root),indent=2))
