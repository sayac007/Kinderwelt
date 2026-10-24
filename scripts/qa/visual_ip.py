#!/usr/bin/env python3
"""Offline visual provenance/similarity triage. Never a rights clearance.

No network client, upload, asset modification or automatic replacement. Pillow
is already used by the repository's art tools. Review output must stay outside
the repository; only the explicitly redacted manifest may be versioned.
"""
import argparse,base64,collections,hashlib,html,io,json,os,re,stat,struct,subprocess,zipfile
from pathlib import Path
from xml.etree import ElementTree
from PIL import Image,ImageDraw,ImageOps,ImageChops,ImageStat
from visual_c2pa import png_credentials
ROOT=Path(__file__).resolve().parents[2]
VISUAL_EXT={'.png','.jpg','.jpeg','.webp','.svg','.gif','.bmp','.tif','.tiff','.ico','.avif','.ctex','.ttf','.otf','.fontdata'}
ARCHIVE_EXT={'.zip','.apk','.aab','.docx','.pptx','.xlsx','.odt'}
LEVEL={'low':0,'medium':1,'high':2,'critical':3,'unreviewed':-1}
def sha(data):return hashlib.sha256(data).hexdigest()
def git(root,*args):
    return subprocess.check_output(['git','-C',str(root),*args],stderr=subprocess.DEVNULL)
def kind(raw):
    if raw.startswith(b'\x89PNG\r\n\x1a\n'):return 'PNG'
    if raw.startswith(b'\xff\xd8\xff'):return 'JPEG'
    if raw[:6] in (b'GIF87a',b'GIF89a'):return 'GIF'
    if raw.startswith(b'RIFF') and raw[8:12]==b'WEBP':return 'WEBP'
    if raw.startswith(b'GST2'):return 'GodotTexture'
    if raw.startswith(b'BM'):return 'BMP'
    if raw[:4] in (b'II*\x00',b'MM\x00*'):return 'TIFF'
    if raw[:4]==b'\x00\x00\x01\x00':return 'ICO'
    if re.match(rb'(?:\xef\xbb\xbf)?\s*(?:<\?xml[^>]*>\s*)?(?:<!--.*?-->\s*)*<svg\b',raw[:2048],re.I|re.S):return 'SVG'
    if raw.startswith(b'OTTO') or (raw.startswith(b'\x00\x01\x00\x00') and len(raw)>=12):return 'Font'
    if raw[:4] in (b'RSRC',b'RSCC'):return 'GodotResource'
    if raw.startswith(b'%PDF-'):return 'PDF'
    if raw.startswith(b'PK\x03\x04'):return 'ZIP'
    return None

def decoded(raw,fmt=None):
    fmt=fmt or kind(raw)
    if fmt=='GodotTexture':
        # Godot GST2 lossless imports contain a standard WebP or PNG base mip.
        starts=[(raw.find(b'RIFF'), 'WEBP'),(raw.find(b'\x89PNG\r\n\x1a\n'),'PNG')]
        starts=[(n,k) for n,k in starts if n>=32]
        if not starts:raise ValueError('Opaque GPU texture; visual content not decoded')
        start,codec=min(starts)
        end=start+8+struct.unpack_from('<I',raw,start+4)[0] if codec=='WEBP' else len(raw)
        raw=raw[start:end]
    image=Image.open(io.BytesIO(raw));image.load()
    if image.width*image.height>32_000_000:raise ValueError('Oversize image; not visually decoded')
    return image.convert('RGBA')

def fingerprints(image):
    # White-matte equality is a transformation clue, not a licensing judgement.
    matte=Image.new('RGBA',image.size,'white');matte.alpha_composite(image);rgb=matte.convert('RGB')
    pixels=sha(struct.pack('>II',*rgb.size)+rgb.tobytes()+image.getchannel('A').tobytes())
    contrast=Image.new('RGBA',image.size,'#888888');contrast.alpha_composite(image)
    tiny=contrast.convert('RGB').resize((9,8),Image.Resampling.LANCZOS).convert('L');values=list(tiny.tobytes());bits=0
    for y in range(8):
        for x in range(8):bits=(bits<<1)|(values[y*9+x]>values[y*9+x+1])
    return pixels,f'{bits:016x}'

def inspect_bytes(raw,path):
    fmt=kind(raw[:2048]);result={'format':fmt or 'unrecognized','bytes':len(raw),'dimensions':None,'pixel_sha256':None,'dhash':None,'decode_status':'not_applicable'}
    if fmt=='PNG':result['content_credentials']=png_credentials(raw)
    if fmt=='SVG':
        try:
            node=ElementTree.fromstring(raw);box=node.get('viewBox','').split();size=[node.get('width'),node.get('height')]
            if all(size):result['dimensions']=[float(re.sub('[^0-9.]','',n)) for n in size]
            elif len(box)==4:result['dimensions']=list(map(float,box[2:]))
            result['decode_status']='xml_inspected_not_rasterized'
            result['external_resources']=bool(re.search(rb'(?:href|url)\s*[=(]\s*["\x27]?https?://',raw))
        except (ValueError,ElementTree.ParseError):result['decode_status']='unreviewed_invalid_svg'
    elif fmt in ['Font','GodotResource']:
        result['decode_status']='support_resource_not_raster'
    elif fmt not in [None,'ZIP','PDF']:
        try:
            im=decoded(raw,fmt);result['dimensions']=list(im.size);result['pixel_sha256'],result['dhash']=fingerprints(im);result['decode_status']='decoded'
        except Exception as error:result['decode_status']='unreviewed_'+type(error).__name__
    elif Path(path).suffix.lower() in VISUAL_EXT:result['decode_status']='unreviewed_unknown_format'
    return result

def evidence(root,generated):
    """Read claims and verify locally available originals; do not adopt verdicts."""
    registry={};private=set();originals={}
    path=root/'art/character-origins.json'
    if path.exists():
        for entry in json.loads(path.read_text())['sources']:
            row=dict(entry);row['record']='art/character-origins.json';registry[row['sha256']]=row
            if row['path'].startswith('.private/'):
                private.add(row['sha256']);private.add(row.get('generation_output_sha256',''))
            if row.get('generation_output_sha256'):originals[row['generation_output_sha256']]=row
    for p in [root/'art/public/headgear.json']:
        if p.exists():
            for entry in json.loads(p.read_text())['images']:registry[entry['sha256']]=dict(entry,record=str(p.relative_to(root)))
    p=root/'art/public/characters/catalog.json'
    if p.exists():
        d=json.loads(p.read_text());registry[d['sha256']]={'path':'art/public/characters/'+d['source'],'origin':d['authorship'],'record':str(p.relative_to(root))}
    for p in [root/'art/public/app-icon/generation.json',root/'art/adventure-worlds.json']:
        if not p.exists():continue
        d=json.loads(p.read_text())
        for key in ['source_sha256','runtime_sha256','sha256']:
            if key in d:registry.setdefault(d[key],{'path':d.get('runtime_image',d.get('asset','art/public/app-icon/original.png')),'origin':d.get('origin',d.get('brief','Documented generation claim')),'record':str(p.relative_to(root))})
    available={}
    if generated and generated.is_dir():
        for p in sorted(generated.iterdir()):
            if p.is_file() and p.suffix.lower() in VISUAL_EXT:
                digest=sha(p.read_bytes());available[digest]=p
    for digest,row in registry.items():
        expected=row.get('generation_output_sha256');source=available.get(expected)
        row['original_hash_verified']=bool(source)
        if source and (root/row['path']).is_file():
            try:
                before=decoded(source.read_bytes());after=decoded((root/row['path']).read_bytes())
                if before.size!=after.size:before=before.resize(after.size,Image.Resampling.LANCZOS)
                row['resize_pixels_verified']=before.tobytes()==after.tobytes()
            except Exception:row['resize_pixels_verified']=False
    return registry,private,originals

def scan(root=ROOT,generated=None,history=True,templates=None):
    root=root.resolve();tracked=set(git(root,'ls-files','-z').decode().split('\0'))
    registry,private_hashes,originals=evidence(root,generated)
    records={};containers=[];gaps=[];references=collections.defaultdict(list);procedural=[];files=[];archives=[];inspected_files=0
    def add(raw,locator,path,sensitive=False,source_hint=None):
        digest=sha(raw);fmt=kind(raw[:2048])
        if fmt not in ['PNG','JPEG','GIF','WEBP','BMP','TIFF','ICO','SVG','GodotTexture','Font','GodotResource'] and Path(path).suffix.lower() not in VISUAL_EXT:return
        if fmt=='GodotResource' and Path(path).suffix!='.fontdata':return
        if digest not in records:
            records[digest]={'id':'image-'+digest[:20],'sha256':digest,**inspect_bytes(raw,path),'occurrences':[],'frames':[]}
        row=records[digest];occ={'locator':locator,'path':path,'tracked':path in tracked,'sensitive_path':sensitive,'source_hint':source_hint}
        if occ not in row['occurrences']:row['occurrences'].append(occ)
    for directory,dirs,names in os.walk(root,followlinks=False):
        dirs[:]=sorted(d for d in dirs if d not in ['.git','__pycache__'] and not (Path(directory)/d).is_symlink())
        for name in sorted(names):
            p=Path(directory)/name
            if p.is_symlink():gaps.append({'kind':'symlink_not_followed','path':str(p.relative_to(root))});continue
            if p.is_file():files.append(p)
    # Inspect signatures even for extensionless/mislabeled files. Audio/model
    # bodies are never loaded; only a short header is needed to rule them out.
    for p in files:
        path=p.relative_to(root).as_posix();inspected_files+=1
        try:
            with p.open('rb') as stream:head=stream.read(2048)
        except OSError:gaps.append({'kind':'unreadable_file','path':path});continue
        fmt=kind(head)
        sensitive=path.startswith('.private/') or 'family' in path.casefold() or 'familie' in path.casefold() or path.startswith(('docs/screenshots/','qa-results/','docs/internal/'))
        if fmt=='ZIP' or p.suffix.lower() in ARCHIVE_EXT:archives.append((p,path,sensitive));continue
        if fmt=='PDF':gaps.append({'kind':'pdf_embedded_images_not_decoded','path':path});continue
        if fmt in ['PNG','JPEG','GIF','WEBP','BMP','TIFF','ICO','SVG','GodotTexture','Font'] or p.suffix.lower() in VISUAL_EXT:
            add(p.read_bytes(),{'file':str(p)},path,sensitive)
        if p.suffix.lower() in ['.gd','.tscn','.tres','.cfg','.godot','.gdshader','.import','.md','.html','.py','.json','.css'] and p.stat().st_size<8_000_000:
            text=p.read_text(errors='replace')
            if p.suffix in ['.gd','.tscn','.tres','.cfg','.godot','.gdshader','.import']:
                for match in re.findall(r'res://([^"\x27\s\]]+)',text):references[match].append(path)
            if p.suffix=='.gd' and re.search(r'\bdraw_(?:circle|polygon|rect|line|polyline|colored_polygon)\(',text) and p.parts[len(root.parts)] in ['core','games']:
                procedural.append({'path':path,'sha256':sha(p.read_bytes()),'role':'Procedural geometry/UI; bitmap-free code is not a third-party similarity clearance','license':'Repository MIT claim (LICENSE)'})
            for index,m in enumerate(re.finditer(r'data:image/[\w.+-]+;base64,([A-Za-z0-9+/=]+)',text)):
                try:add(base64.b64decode(m[1],validate=True),{'embedded_file':str(p),'index':index},path+f'#embedded-{index}',sensitive)
                except ValueError:gaps.append({'kind':'invalid_embedded_image','path':path})
            if fmt!='SVG':
                for index,m in enumerate(re.finditer(r'<svg(?=[\s>]).*?</svg>',text,re.S)):
                    raw=m[0].replace('\\"','"').replace('\\n','\n').encode()
                    add(raw,{'embedded_svg_file':str(p),'index':index},path+f'#embedded-svg-{index}',sensitive)
    if generated and generated.is_dir():
        for p in sorted(generated.iterdir()):
            if p.is_file() and kind(p.read_bytes()[:2048]) in ['PNG','JPEG','WEBP','GIF','SVG']:
                raw=p.read_bytes();digest=sha(raw)
                is_known=digest in registry or digest in originals
                add(raw,{'file':str(p)},'external-generated/'+p.name,not is_known or digest in private_hashes)
    if history:
        p=root/'art/character-origins.json'
        for index,entry in enumerate(json.loads(p.read_text()).get('historical_excluded',[]) if p.exists() else [],1):
            ref=entry['last_examined_commit'];path='assets/quest/'+entry['id']+'.png'
            try:
                if not re.fullmatch('[0-9a-f]{7,40}',ref):raise ValueError('Invalid historical commit')
                raw=git(root,'show',ref+':'+path)
                if sha(raw)!=entry['sha256']:raise ValueError('Historical hash mismatch')
                add(raw,{'git_ref':ref,'git_path':path},'historical/'+ref+'/legacy-'+str(index)+'.png')
                records[sha(raw)]['historical_unestablished']=True
            except Exception:gaps.append({'kind':'historical_image_unavailable','path':'historical/legacy-'+str(index)})
    if templates:
        for p in sorted(templates.iterdir()):
            if p.is_file() and p.name in ['android_debug.apk','android_release.apk','android_source.zip']:archives.append((p,'toolchain/'+p.name,False))
    # All readable ZIP/Office/source/APK/AAB containers, no extraction to disk.
    for p,path,sensitive in archives:
        try:
            with zipfile.ZipFile(p) as z:
                count=0;imports={};texture_sources={}
                if len(z.infolist())>200000:raise ValueError('Too many archive members')
                for info in z.infolist():
                    if info.is_dir():continue
                    name=info.filename
                    if name.endswith('.png.import') or name.endswith('.svg.import') or name.endswith('.ttf.import'):
                        text=z.read(info).decode(errors='replace');source=re.search(r'source_file="res://([^"]+)"',text)
                        source_path=source[1] if source else name.split('assets/',1)[1].removesuffix('.import') if p.suffix in ['.apk','.aab'] and 'assets/' in name else None
                        if source_path:
                            for dest in re.findall(r'res://([^"\]]+\.(?:ctex|fontdata))',text):texture_sources[dest]=source_path
                for info in z.infolist():
                    if info.is_dir():continue
                    name=info.filename
                    with z.open(info) as stream:head=stream.read(2048)
                    fmt=kind(head)
                    if fmt not in ['PNG','JPEG','GIF','WEBP','BMP','TIFF','ICO','SVG','GodotTexture','Font'] and Path(name).suffix.lower() not in VISUAL_EXT:continue
                    if info.file_size>64_000_000 or info.file_size/max(1,info.compress_size)>1000:
                        gaps.append({'kind':'bounded_archive_member_not_decoded','path':path+'!'+name});continue
                    raw=z.read(info);hint=None
                    for dest,source in texture_sources.items():
                        if name.endswith('/'+dest):hint=source;break
                    if name.startswith('res/') and name.endswith(('.png','.webp')):hint='android-monochrome-derived' if 'monochrome' in name else 'android-launcher-derived'
                    add(raw,{'archive':str(p),'member':name},path+'!'+name,sensitive or '.private/' in name or '/docs/screenshots/' in name,hint);count+=1
                containers.append({'path':path,'sha256':sha(p.read_bytes()),'visual_entries':count,'kind':p.suffix.lower(),'variant':None,'provenance':None,'local_file':str(p)})
                for name in z.namelist():
                    if name.endswith('/assets/quest/cast.json'):
                        try:containers[-1]['variant']=json.loads(z.read(name)).get('variant')
                        except (ValueError,KeyError):pass
        except (zipfile.BadZipFile,OSError,ValueError) as error:gaps.append({'kind':'archive_'+type(error).__name__,'path':path,'bytes':p.stat().st_size})
    rows=list(records.values());pixels=collections.defaultdict(list)
    for r in rows:
        if r['pixel_sha256']:pixels[r['pixel_sha256']].append(r)
    # Propagate explicit family-source privacy through exact/pixel derivatives.
    for r in rows:
        r['family_source']=r['sha256'] in private_hashes
    for group in pixels.values():
        if any(r['family_source'] for r in group):
            for r in group:r['family_source']=True
    for r in rows:
        aliases=r['occurrences'];claim=registry.get(r['sha256']) or originals.get(r['sha256'])
        public_primary=any(o['path'].startswith(('assets/quest/','art/public/')) and not o['sensitive_path'] for o in aliases)
        matched_primary=any(any(o['path'].startswith(('assets/quest/','art/public/')) and not o['sensitive_path'] for o in other['occurrences']) for other in pixels.get(r['pixel_sha256'],[]) if other is not r)
        r['sensitivity']='family_private' if r['family_source'] else 'non_sensitive' if public_primary or matched_primary or (claim and r['sha256'] not in private_hashes) or r.get('historical_unestablished') else 'restricted_unclassified'
        r['evidence']={'record':claim.get('record') if claim else None,'claim':claim.get('origin','Generation claim, not authenticated provider/rights evidence') if claim else None,'original_hash_verified':claim.get('original_hash_verified',False) if claim else False,'resize_pixels_verified':claim.get('resize_pixels_verified',False) if claim else False}
        r['references']=sorted({ref for o in aliases for ref in references.get(o.get('source_hint') or o['path'],[])})
        r['runtime_inclusion']='observed_in_package' if any('archive' in o['locator'] and Path(o['locator']['archive']).suffix in ['.apk','.aab'] for o in aliases) else 'referenced_source' if r['references'] else 'retained_source_or_derived_only'
        r['role']='font_support' if r['format'] in ['Font','GodotResource'] else 'imported_texture' if r['format']=='GodotTexture' else 'screenshot_or_render' if any(o['path'].startswith(('docs/screenshots/','qa-results/')) for o in aliases) else 'visual_source'
        r['declared_license']='SIL OFL 1.1; assets/quest/OFL.txt; keep copyright/license notices' if r['role']=='font_support' else 'Repository MIT claim for software/docs; no separately authenticated visual-asset rights grant located'
        similarity='unreviewed';provenance='low' if r['role']=='font_support' else 'high' if r.get('historical_unestablished') and r['runtime_inclusion']=='observed_in_package' else 'medium'
        overall='high' if provenance=='high' and r['sensitivity']=='non_sensitive' else 'medium' if r['sensitivity']=='non_sensitive' else 'unreviewed'
        r['risk']={'overall':overall,'resemblance':similarity,'provenance_license':provenance,'exposure':'high' if r['runtime_inclusion']=='observed_in_package' else 'medium' if public_primary else 'low','private_sensitivity':'high' if r['sensitivity']!='non_sensitive' else 'low','confidence':'high for file facts; visual/legal review pending'}
        r['visual_review']='not_reviewed';r['recommended_action']='Owner review of provenance and any specific resemblance; no clearance inferred'
        r['duplicate_occurrences']=len(aliases)-1;r['same_visible_pixels']=[p['id'] for p in pixels.get(r['pixel_sha256'],[]) if p is not r]
    return {'schema':1,'base_commit':git(root,'rev-parse','HEAD').decode().strip(),'scope':'Current tracked files plus retained local inputs/caches/archives and pinned historical exclusions; not full Git-history enumeration','files_signature_checked':inspected_files,'images':sorted(rows,key=lambda r:r['id']),'procedural':procedural,'containers':containers,'coverage_gaps':gaps,'network_uploads':0}

def load_bytes(locator,root=ROOT):
    if 'file' in locator:return Path(locator['file']).read_bytes()
    if 'archive' in locator:
        if locator.get('chain'):
            value=Path(locator['archive']).read_bytes()
            for member in locator['chain']:
                with zipfile.ZipFile(io.BytesIO(value)) as z:value=z.read(member)
            with zipfile.ZipFile(io.BytesIO(value)) as z:return z.read(locator['member'])
        with zipfile.ZipFile(locator['archive']) as z:return z.read(locator['member'])
    if 'git_blob' in locator:return git(root,'cat-file','blob',locator['git_blob'])
    if 'git_ref' in locator:return git(root,'show',locator['git_ref']+':'+locator['git_path'])
    if 'embedded_svg_file' in locator:
        text=Path(locator['embedded_svg_file']).read_text();value=list(re.finditer(r'<svg(?=[\s>]).*?</svg>',text,re.S))[locator['index']][0]
        return value.replace('\\"','"').replace('\\n','\n').encode()
    if 'embedded_file' in locator:
        matches=list(re.finditer(r'data:image/[\w.+-]+;base64,([A-Za-z0-9+/=]+)',Path(locator['embedded_file']).read_text()))
        return base64.b64decode(matches[locator['index']][1])
    raise ValueError('Unknown offline locator')

def nested_containers(report):
    """Bounded recursive archive inspection, with no filesystem extraction."""
    rows={r['sha256']:r for r in report['images']};added=[];seen=set()
    def visit(z,outer,path,chain,depth):
        if depth>3:report['coverage_gaps'].append({'kind':'nested_archive_depth_limit','path':path});return
        for info in z.infolist():
            if info.is_dir():continue
            with z.open(info) as stream:head=stream.read(2048)
            if kind(head)!='ZIP':continue
            if info.file_size>256_000_000 or info.file_size/max(1,info.compress_size)>1000:
                report['coverage_gaps'].append({'kind':'nested_archive_size_limit','path':path+'!'+info.filename});continue
            raw=z.read(info);key=(outer,tuple(chain+[info.filename]))
            if key in seen:continue
            seen.add(key);location=path+'!'+info.filename;child_chain=chain+[info.filename];count=0
            try:
                with zipfile.ZipFile(io.BytesIO(raw)) as inner:
                    for item in inner.infolist():
                        if item.is_dir():continue
                        with inner.open(item) as stream:prefix=stream.read(2048)
                        fmt=kind(prefix);native=bool(re.search(r'(?:^|/)res/(?:drawable|mipmap)[^/]*/[^/]+\.xml$',item.filename))
                        if not native and fmt not in ['PNG','JPEG','GIF','WEBP','BMP','TIFF','ICO','SVG','GodotTexture','Font'] and Path(item.filename).suffix.lower() not in VISUAL_EXT:continue
                        if item.file_size>64_000_000:report['coverage_gaps'].append({'kind':'nested_visual_size_limit','path':location});continue
                        data=inner.read(item);digest=sha(data);count+=1
                        if digest not in rows:
                            meta=inspect_bytes(data,item.filename)
                            if native:meta.update(format='AndroidDrawableXML',decode_status='native_definition_not_rasterized')
                            rows[digest]={'id':'image-'+digest[:20],'sha256':digest,**meta,'occurrences':[],'frames':[],'family_source':False,'sensitivity':'restricted_unclassified','evidence':{'record':None,'claim':None,'original_hash_verified':False,'resize_pixels_verified':False},'references':[],'runtime_inclusion':'retained_source_or_derived_only','role':'retained_nested_visual','declared_license':'Nested build/library input; per-resource author/license requires review','risk':{'overall':'unreviewed','resemblance':'unreviewed','provenance_license':'unreviewed','exposure':'low','private_sensitivity':'high','confidence':'Nested file identity only'},'visual_review':'not_reviewed','recommended_action':'Review retained library/source provenance; do not infer a new independent license','duplicate_occurrences':0,'same_visible_pixels':[]}
                        row=rows[digest];occ={'locator':{'archive':outer,'chain':child_chain,'member':item.filename},'path':location+'!'+item.filename,'tracked':False,'sensitive_path':True,'source_hint':None}
                        if occ not in row['occurrences']:row['occurrences'].append(occ)
                        row['duplicate_occurrences']=len(row['occurrences'])-1
                    visit(inner,outer,location,child_chain,depth+1)
                added.append({'path':location,'sha256':sha(raw),'visual_entries':count,'kind':Path(info.filename).suffix.lower(),'variant':None,'provenance':None,'local_file':outer,'archive_chain':child_chain})
            except zipfile.BadZipFile:report['coverage_gaps'].append({'kind':'invalid_nested_archive','path':location})
    existing={(c['local_file'],tuple(c.get('archive_chain',[]))) for c in report['containers']};seen.update(k for k in existing if k[1])
    for c in report['containers']:
        if c.get('archive_chain'):continue
        with zipfile.ZipFile(c['local_file']) as z:visit(z,c['local_file'],c['path'],[],1)
    report['containers'].extend(added);report['images']=sorted(rows.values(),key=lambda r:r['id'])

def native_drawables(report):
    """Inventory native compiled drawables separately from decoded image art."""
    rows={r['sha256']:r for r in report['images']}
    for container in report['containers']:
        if container.get('archive_chain'):continue
        native_count=0
        with zipfile.ZipFile(container['local_file']) as z:
            for name in z.namelist():
                if not re.search(r'(?:^|/)res/(?:drawable|mipmap)[^/]*/[^/]+\.xml$',name):continue
                raw=z.read(name);digest=sha(raw);native_count+=1
                if digest not in rows:
                    rows[digest]={'id':'image-'+digest[:20],'sha256':digest,'format':'AndroidDrawableXML','bytes':len(raw),'dimensions':None,'pixel_sha256':None,'dhash':None,'decode_status':'native_definition_not_rasterized','occurrences':[],'frames':[],'family_source':False,'sensitivity':'restricted_unclassified','evidence':{'record':None,'claim':None,'original_hash_verified':False,'resize_pixels_verified':False},'references':[],'runtime_inclusion':'observed_in_package','role':'native_drawable_definition','declared_license':'Native template/generated drawable; exact or semantic vendor attribution needs review','risk':{'overall':'unreviewed','resemblance':'unreviewed','provenance_license':'unreviewed','exposure':'high','private_sensitivity':'high','confidence':'Compiled definition inventoried; semantic review incomplete'},'visual_review':'not_reviewed','recommended_action':'Compare native drawable definition with its template/generated source; this is not an unrecognized game illustration','duplicate_occurrences':0,'same_visible_pixels':[]}
                row=rows[digest];occ={'locator':{'archive':container['local_file'],'member':name},'path':container['path']+'!'+name,'tracked':False,'sensitive_path':False,'source_hint':None}
                if occ not in row['occurrences']:row['occurrences'].append(occ)
                row['duplicate_occurrences']=len(row['occurrences'])-1
        container.setdefault('image_font_entries',container['visual_entries']);container['native_drawable_entries']=native_count;container['visual_entries']=container['image_font_entries']+native_count
    report['images']=sorted(rows.values(),key=lambda r:r['id'])

def retained_git_visuals(report,root=ROOT):
    """Include visual blobs reachable from all local refs, without checkout."""
    rows={r['sha256']:r for r in report['images']};registry,private_hashes,_=evidence(root,None)
    family_stems={Path(v['path']).stem for v in registry.values() if v['path'].startswith('.private/')}
    count=0
    for line in git(root,'rev-list','--objects','--all').decode().splitlines():
        parts=line.split(' ',1)
        if len(parts)!=2 or Path(parts[1]).suffix.lower() not in VISUAL_EXT:continue
        object_id,path=parts
        raw=git(root,'cat-file','blob',object_id);digest=sha(raw);count+=1
        private=('.private/' in path or '/private/' in path or Path(path).stem in family_stems)
        if digest not in rows:
            meta=inspect_bytes(raw,path)
            rows[digest]={'id':'image-'+digest[:20],'sha256':digest,**meta,'occurrences':[],'frames':[],'family_source':private,'sensitivity':'family_private' if private else 'restricted_unclassified','evidence':{'record':None,'claim':None,'original_hash_verified':False,'resize_pixels_verified':False},'references':[],'runtime_inclusion':'retained_source_or_derived_only','role':'retained_git_visual','declared_license':'Historical retained visual: source/author/license require version-specific review','risk':{'overall':'unreviewed','resemblance':'unreviewed','provenance_license':'unreviewed','exposure':'low','private_sensitivity':'high','confidence':'File identity verified; content/rights not reviewed'},'visual_review':'not_reviewed','recommended_action':'Owner-only offline review of historical material; do not upload until sensitivity and specific permission are established','duplicate_occurrences':0,'same_visible_pixels':[]}
        row=rows[digest];occ={'locator':{'git_blob':object_id},'path':'git-retained/'+object_id+'/'+path,'tracked':False,'sensitive_path':private or path.startswith('docs/screenshots/'),'source_hint':None}
        if occ not in row['occurrences']:row['occurrences'].append(occ)
        if private:row['family_source']=True;row['sensitivity']='family_private'
        row['duplicate_occurrences']=len(row['occurrences'])-1
    report['images']=sorted(rows.values(),key=lambda r:r['id']);report['retained_git_visual_blobs']=count;report['git_history_is_shallow']=git(root,'rev-parse','--is-shallow-repository').decode().strip()=='true'
    report['scope']='Signature inventory of current tracked/untracked files and retained build inputs, plus visual-path blobs reachable from all local Git refs; not signature scanning of every non-visual historical Git blob'

def add_frames(report,root=ROOT):
    """Use actual runtime rectangles/masks; preserve atlas/source hashes."""
    for row in report['images']:row['frames']=[]
    by_path={o['path']:r for r in report['images'] for o in r['occurrences'] if '!' not in o['path']}
    def frame(path,label,rect,ref,mask=None):
        source=by_path.get(path)
        if source is None:return
        image=decoded(load_bytes(source['occurrences'][0]['locator'],root))
        x,y,w,h=map(int,rect)
        if min(x,y)<0 or w<=0 or h<=0 or x+w>image.width or y+h>image.height:raise ValueError('Invalid atlas frame')
        crop=image.crop((x,y,x+w,y+h));pixel,dh=fingerprints(crop)
        if any(f.get('rect')==[x,y,w,h] for f in source['frames']):return
        source['frames'].append({'id':source['id']+'/frame-'+label,'label':label,'rect':[x,y,w,h],'pixel_sha256':pixel,'dhash':dh,'reference':ref,'mask_available':mask is not None,'mask_runs':mask})
    catalog=root/'art/public/characters/frames.json'
    if catalog.exists():
        data=json.loads(catalog.read_text())
        for index,(id,hero) in enumerate(data['heroes'].items(),1):
            for look,rect in hero['frames'].items():frame('art/public/characters/neutral-cast.png',f'cast-{index:02d}-{look}',rect,'core/quest/wardrobe.gd',hero.get('mask_runs'))
    p=root/'art/shared/squirrel-looks.json'
    if p.exists():
        d=json.loads(p.read_text())
        for look,rect in d['frames'].items():frame('assets/quest/looks-squirrel.png','squirrel-'+look,rect,'core/quest/wardrobe.gd',d.get('mask_runs'))
    text=(root/'core/quest/art.gd').read_text() if (root/'core/quest/art.gd').exists() else ''
    for name,values in re.findall(r'"(\w+)":Rect2\(([^)]+)\)',text):frame('assets/quest/objects.png',name,values.split(','),'core/quest/art.gd')
    ids=re.search(r'const SCIENCE_IDS := (\[[^\n]+\])',text)
    if ids:
        for index,label in enumerate(json.loads(ids[1])):
            path='assets/quest/science-'+('a' if index<30 else 'b')+'.png';source=by_path.get(path)
            if source:
                width,height=source['dimensions'];cellx=width/6;celly=height/5;n=index%30
                frame(path,label,[int(n%6*cellx+3),int(n//6*celly+3),int(cellx-6),int(celly-6)],'core/quest/art.gd')
    p=root/'assets/quest/icons.png'
    if p.exists():
        text=(root/'core/quest/icon.gd').read_text()
        for index,rect in enumerate(re.findall(r'Rect2\(([^)]+)\)',text.split('var cell')[0])):frame('assets/quest/icons.png','menu-'+str(index+1),rect.split(','),'core/quest/icon.gd')
    for label,index in [('tree',0),('seabed',1),('city',2),('moon',3)]:
        source=by_path.get('assets/quest/adventure-worlds.png')
        if source:
            w,h=source['dimensions'];frame('assets/quest/adventure-worlds.png',label,[index%2*w//2,index//2*h//2,w//2,h//2],'core/quest/scenery.gd')
    # Private frames are inventoried locally and redacted before publication.
    p=root/'.private/characters/looks.json'
    if p.exists():
        for index,(person,data) in enumerate(json.loads(p.read_text())['heroes'].items(),1):
            base='.private/characters/'+person+'.png'
            if base in by_path:frame(base,f'private-{index:02d}-classic',[0,0,*by_path[base]['dimensions']],'core/quest/hero.gd')
            for look,rect in data['frames'].items():frame('.private/characters/looks-'+person+'.png',f'private-{index:02d}-{look}',rect,'core/quest/wardrobe.gd',data.get('mask_runs'))
    for resource in [*root.rglob('*.tres'),*root.rglob('*.tscn')]:
        if '.git' in resource.parts or resource.is_symlink():continue
        text=resource.read_text(errors='replace')
        if 'AtlasTexture' not in text:continue
        region=re.search(r'region\s*=\s*Rect2\(([^)]+)\)',text)
        atlas=re.search(r'path="res://([^"]+\.(?:png|webp|jpg))"',text)
        if not region or not atlas:continue
        anchor=next((p for p in resource.parents if (p/'project.godot').exists()),root)
        path=(anchor/atlas[1]).relative_to(root).as_posix()
        frame(path,'resource-'+sha(str(resource.relative_to(root)).encode())[:12],region[1].split(','),str(resource.relative_to(root)))
    # Historical wardrobe metadata is applied only to its exact source SHA.
    by_sha={r['sha256']:r for r in report['images']}
    for line in git(root,'rev-list','--objects','--all').decode().splitlines():
        parts=line.split(' ',1)
        if len(parts)!=2 or Path(parts[1]).name not in ['looks.json','frames.json','squirrel-looks.json']:continue
        try:metadata=json.loads(git(root,'cat-file','blob',parts[0]))
        except (ValueError,subprocess.CalledProcessError):continue
        heroes=list(metadata.get('heroes',{}).values()) if 'heroes' in metadata else [metadata]
        for index,data in enumerate(heroes):
            source=by_sha.get(data.get('sha256'))
            if not source:continue
            for look,rect in data.get('frames',{}).items():
                before=len(source['frames']);frame(source['occurrences'][0]['path'],f'retained-{index:02d}-{parts[0][:8]}-{look}',rect,'Retained Git frame metadata '+parts[0],data.get('mask_runs'))
                if len(source['frames'])>before:source['frames'][-1].update(mask_git_blob=parts[0],mask_hero_index=index)
    for r in report['images']:
        if r['format']=='GIF':
            image=Image.open(io.BytesIO(load_bytes(r['occurrences'][0]['locator'],root)))
            for index in range(min(500,getattr(image,'n_frames',1))):
                image.seek(index);px,dh=fingerprints(image.convert('RGBA'));r['frames'].append({'id':r['id']+'/frame-animated-'+str(index),'label':'animated-'+str(index),'frame_index':index,'rect':[0,0,*image.size],'pixel_sha256':px,'dhash':dh,'reference':'Animated source image','mask_available':False})
        for f in r['frames']:f.pop('mask_runs',None) # crop pack accesses authoritative source metadata separately

def enrich(report,root=ROOT):
    """Verify import/source/template relationships independently of AI claims."""
    rows=report['images'];by_hash={r['sha256']:r for r in rows};by_path={o['path']:r for r in rows for o in r['occurrences']}
    templates={r['sha256'] for r in rows if any(o['path'].startswith('toolchain/') for o in r['occurrences'])}
    casts={};raw_cache={};proofs={}
    for c in report['containers']:
        p=Path(c['local_file'])
        if c['kind'] not in ['.apk','.aab']:continue
        with zipfile.ZipFile(p) as z:
            source_hashes={}
            for name in z.namelist():
                if name.endswith('/assets/quest/cast.json'):
                    try:source_hashes=json.loads(z.read(name)).get('resource_sha256',{})
                    except ValueError:pass
            casts[str(p)]=source_hashes
        candidates=[p.parent/'provenance.json',*[p.parent/label/'provenance.json' for label in ['family','neutral']]]
        for candidate in candidates:
            if not candidate.exists():continue
            proof=json.loads(candidate.read_text())
            if any(v.get('sha256')==c['sha256'] for v in proof.get('artifacts',{}).values()):
                c['provenance']={'source_commit':proof.get('source_commit'),'version':proof.get('version_name'),'source_dirty':proof.get('source_dirty')};break
    for r in rows:
        r['lineage_sources']=[]
        if r['sha256'] in templates:
            r['sensitivity']='non_sensitive';r['evidence']['template_bytes_verified']=True
            r['declared_license']='Godot/Android export-template resource; exact installed-template bytes verified; per-resource upstream notices need review'
        for o in r['occurrences']:
            hint=o['source_hint'];source=None;basis=None
            if not hint:continue
            if hint.startswith('android-'):
                monochrome=hint=='android-monochrome-derived'
                source=by_path.get('assets/quest/monochrome.svg' if monochrome else 'assets/quest/appicon.png')
                before=None
                if source and monochrome:
                    stamp=root/'assets/quest/monochrome.svg.import'
                    target=re.search(r'path="res://([^"]+\.ctex)"',stamp.read_text()) if stamp.exists() else None
                    if target and (root/target[1]).exists():before=decoded((root/target[1]).read_bytes())
                elif source:before=decoded(load_bytes(source['occurrences'][0]['locator'],root))
                if source and before is not None and r['dimensions'] and 'icon' in o['path']:
                    after=decoded(load_bytes(o['locator'],root))
                    if monochrome:
                        a=Image.new('RGBA',before.size,'black');a.alpha_composite(before);before=a
                        a=Image.new('RGBA',after.size,'black');a.alpha_composite(after);after=a
                    before=before.convert('RGB').resize(after.size,Image.Resampling.LANCZOS);after=after.convert('RGB')
                    error=sum(ImageStat.Stat(ImageChops.difference(before,after)).mean)/3
                    if error<12:basis='Native-size launcher pixel comparison; mean RGB error '+str(round(error,4))
                    else:source=None
                else:source=None
            else:
                expected=casts.get(o['locator'].get('archive',''),{}).get(hint)
                if expected in by_hash:source=by_hash[expected];basis='Packaged cast source SHA-256 and Godot import remap'
                elif hint in by_path:
                    possible=by_path[hint]
                    exact=r['pixel_sha256'] and r['pixel_sha256']==possible['pixel_sha256']
                    near=r['dhash'] and possible['dhash'] and (int(r['dhash'],16)^int(possible['dhash'],16)).bit_count()<=3 and r['dimensions']==possible['dimensions']
                    if exact or near or possible['format']=='SVG' or r['format']=='GodotResource':source=possible;basis='Godot import source reference; '+('identical visible pixels' if exact else 'local derivative comparison; not a rights proof')
            if source and source['id']!=r['id']:
                relation={'id':source['id'],'basis':basis}
                if relation not in r['lineage_sources']:r['lineage_sources'].append(relation)
                if source['family_source']:r['family_source']=True;r['sensitivity']='family_private'
                elif source['sensitivity']=='non_sensitive':r['sensitivity']='non_sensitive'
                if source['evidence'].get('record'):r['evidence']['inherited_record']=source['evidence']['record']
        # Old font caches are not automatically covered by Nunito's OFL notice.
        if r['role']=='font_support':
            nunito=any('Nunito.ttf' in o['path'] for o in r['occurrences'])
            r['declared_license']='SIL OFL 1.1; exact Nunito source/import identified; assets/quest/OFL.txt' if nunito else 'Retained font/support cache; individual font license not yet verified'
            r['risk']['provenance_license']='low' if nunito else 'unreviewed'
        if r.get('historical_unestablished'):
            retained=[Path(o['path']).name for o in r['occurrences'] if o['path'].startswith('external-generated/')]
            r['evidence']['retained_output_hash_verified']=bool(retained)
            r['evidence']['retained_output_filenames']=retained
            r['risk']['provenance_license']='medium' if retained else 'high'
            r['recommended_action']='Verify legacy authorship, generation context and rights before redistribution; exact retained output bytes are an evidence anchor, not legal approval'
            r['evidence']['claim']='Exact bytes also found in retained local output files; embedded credential claims are separate evidence and require authentication' if retained else None
        if r['family_source']:r['sensitivity']='family_private'
        r['risk']['overall']='high' if r.get('historical_unestablished') and r['risk']['provenance_license']=='high' else 'medium' if r['sensitivity']=='non_sensitive' else 'unreviewed'
        r['risk']['private_sensitivity']='low' if r['sensitivity']=='non_sensitive' else 'high'
    # Related normalized hashes prioritize inspection, never prove a common
    # license. This deliberately does not grant public sensitivity to a match.
    groups=collections.defaultdict(list)
    for r in rows:
        if r['dhash']:groups[r['dhash']].append(r['id'])
    report['normalized_similarity_groups']=[{'dhash':key,'ids':ids,'scope':'Local thumbnail similarity only; no copying or license inference'} for key,ids in sorted(groups.items()) if len(ids)>1]
    current=json.loads((root/'scripts/android/app-config.json').read_text())['version_name'] if (root/'scripts/android/app-config.json').exists() else None
    report['current_package_coverage']=[]
    for c in report['containers']:
        if not c['provenance'] or c['provenance']['version']!=current:continue
        packaged=[r for r in rows if any(o['locator'].get('archive')==c['local_file'] for o in r['occurrences'])]
        unmatched=[r['id'] for r in packaged if not r['lineage_sources'] and not r['sha256'] in templates and not any(o['locator'].get('file') for o in r['occurrences'])]
        report['current_package_coverage'].append({'artifact':Path(c['local_file']).name,'sha256':c['sha256'],'version':current,'visual_files':len(packaged),'image_font_files':sum(r['format']!='AndroidDrawableXML' for r in packaged),'native_drawable_definitions':sum(r['format']=='AndroidDrawableXML' for r in packaged),'unmatched_image_font_ids':[id for id in unmatched if next(r for r in packaged if r['id']==id)['format']!='AndroidDrawableXML'],'unmatched_visual_ids':unmatched,'source_commit':c['provenance']['source_commit'],'source_dirty':c['provenance']['source_dirty']})
    report['unavailable_inputs']=[{'id':'family-reference-photo-corpus','count':None,'status':'not_available_not_reviewed','scope':'Original user reference-photo corpus was not downloaded or opened for this audit; count/consent cannot be inferred from generated illustrations'}]

def apply_reviews(report,root=ROOT,ledger=None):
    """A local assistant screen is not an owner, expert or legal approval."""
    if ledger is None:
        path=root/'scripts/qa/visual-ip-review.json';ledger=json.loads(path.read_text()) if path.exists() else {}
    reviews={r['sha256']:r for r in ledger.get('source_reviews',[])}
    owner_path=root/'scripts/qa/visual-ip-owner-review.json'
    owner=json.loads(owner_path.read_text()) if owner_path.exists() else {}
    credentials={r['source_sha256']:r for r in owner.get('sources',[])}
    originals={r['retained_original'].get('sha256'):r['retained_original'].get('credentials') for r in owner.get('sources',[])}
    for row in report['images']:
        review=reviews.get(row['sha256'])
        if review and row['sensitivity']=='non_sensitive':
            row['visual_review']='assistant_local_visual_triage';row['risk']['resemblance']=review['resemblance'];row['review_note']=review['observation'];row['risk']['confidence']='Local visual triage only; no reverse search or legal clearance'
            for f in row['frames']:f['review']='assistant_atlas_visual_triage'
        paths={o['path'] for o in row['occurrences']}
        if paths & set(ledger.get('geometry_reviewed_paths',[])):
            row['visual_review']='source_geometry_inspected';row['risk']['overall']='low';row['risk']['resemblance']='low'
        if row['role']=='font_support' and any('Nunito.ttf' in o['path'] for o in row['occurrences']):
            row['visual_review']='license_metadata_inspected';row['risk']['overall']='low';row['risk']['resemblance']='low'
        if row['sensitivity']=='non_sensitive':
            if row.get('content_credentials'):row['evidence']['content_credentials']=row['content_credentials']
            if originals.get(row['sha256']):row['evidence']['content_credentials']=originals[row['sha256']]
            proof=credentials.get(row['sha256'])
            if proof:
                row['evidence']['content_credentials']=proof['file_credentials']
                row['evidence']['retained_original']=proof['retained_original']
                row['owner_manual_reviews']=[review for review in owner['manual_review']['rows'] if review['source_sha256']==row['sha256']]
    current_paths={c['local_file'] for c in report['containers'] if c.get('provenance') and c['provenance'].get('version') in {p['version'] for p in report.get('current_package_coverage',[])}}
    current=[r for r in report['images'] if any(o['locator'].get('archive') in current_paths for o in r['occurrences'])]
    source_ids={link['id'] for r in current for link in r.get('lineage_sources',[])}
    for r in current:
        if any(o['path'].startswith(('assets/quest/','art/public/','.private/characters/')) for o in r['occurrences']):source_ids.add(r['id'])
    for row in report['images']:
        row['current_distribution']='observed_current_package' if row in current else 'current_package_source' if row['id'] in source_ids else 'retained_or_earlier_only'
    report['current_project_source_ids']=sorted(source_ids)
    report['review_scope']='Assistant local triage of the ledger-listed originals/atlases; family and unclassified images not visually reviewed; owner-supplied findings tracked separately; no expert/legal approval'
    if owner:report['owner_review_follow_up']={k:owner[k] for k in ['review_date','base_commit','scope','summary','legacy_chronology']} | {'source_csv_sha256':owner['manual_review'].get('source_csv_sha256')}

def redacted(report):
    """No private paths, names, hashes, pixels, coordinates or local locators."""
    out={'schema':1,'tool':{'script':'scripts/qa/visual_ip.py','sha256':sha(Path(__file__).read_bytes()),'content_credentials_reader_sha256':sha(Path(__file__).with_name('visual_c2pa.py').read_bytes()),'pillow_version':getattr(Image,'__version__','unknown')},'base_commit':report['base_commit'],'scope':report['scope'],'network_uploads':0,'files_signature_checked':report['files_signature_checked'],'assets':[],'procedural':report['procedural'],'containers':[],'coverage_gaps':[]}
    private_ids=report.setdefault('private_ids',{})
    next_id=max([int(v.split('-')[-1]) for v in private_ids.values()]+[0])+1
    for index,r in enumerate(report['images'],1):
        hidden=r['sensitivity']!='non_sensitive'
        r.setdefault('current_distribution','not_evaluated')
        if hidden and r['sha256'] not in private_ids:
            private_ids[r['sha256']]=f'restricted-{next_id:05d}';next_id+=1
        entry={k:r[k] for k in ['id','format','bytes','dimensions','sha256','role','sensitivity','runtime_inclusion','current_distribution','declared_license','risk','visual_review','recommended_action','duplicate_occurrences']}
        entry['sources']=[{'path':o['path'] if not hidden and not o['sensitive_path'] and (o['tracked'] or o['path'].startswith(('historical/','external-generated/'))) else '<restricted-or-local>','source_hint':o['source_hint'] if not hidden and not o['sensitive_path'] else None,'tracked':o['tracked']} for o in r['occurrences']]
        entry['review_note']=r.get('review_note','Not independently visually reviewed') if not hidden else 'Restricted material not visually reviewed'
        entry['lineage_sources']=[{'id':ids_placeholder['id'],'basis':ids_placeholder['basis']} for ids_placeholder in r.get('lineage_sources',[]) if not hidden]
        entry['references']=[p for p in r['references'] if p.startswith(('core/','games/'))] if not hidden else []
        entry['evidence']=r['evidence'] if not hidden else {'status':'Restricted evidence retained only in local pack'}
        if not hidden and r.get('owner_manual_reviews'):entry['owner_manual_reviews']=r['owner_manual_reviews']
        entry['frames']=[{k:v for k,v in f.items() if k not in ['mask_runs','mask_git_blob','mask_hero_index']} for f in r['frames']] if not hidden else [{'id':private_ids[r['sha256']]+f'/frame-{i+1:03d}','review':'unreviewed'} for i,_ in enumerate(r['frames'])]
        if hidden:entry.update(id=private_ids[r['sha256']],sha256=None,bytes=None,dimensions=None)
        out['assets'].append(entry)
    ids={r['id']:entry['id'] for r,entry in zip(report['images'],out['assets'])}
    for entry in out['assets']:
        entry['lineage_sources']=[dict(link,id=ids.get(link['id'],'<restricted>')) for link in entry['lineage_sources']]
    out['current_project_source_ids']=[ids[id] for id in report.get('current_project_source_ids',[])]
    for i,c in enumerate(report['containers'],1):out['containers'].append({'id':f'container-{i:03d}','kind':c['kind'],'visual_entries':c['visual_entries'],'path':'<local-container>','sha256':None,'variant':c['variant']})
    out['similarity_groups']=[{'ids':[ids[id] for id in group['ids'] if ids[id].startswith('image-')],'scope':group['scope']} for group in report.get('normalized_similarity_groups',[]) if len([id for id in group['ids'] if ids[id].startswith('image-')])>1]
    out['package_coverage']=[dict(c,unmatched_visual_ids=[ids.get(id,'<restricted>') for id in c['unmatched_visual_ids']],unmatched_image_font_ids=[ids.get(id,'<restricted>') for id in c.get('unmatched_image_font_ids',[])]) for c in report.get('current_package_coverage',[])]
    out['retained_git_visual_blobs']=report.get('retained_git_visual_blobs',0)
    out['git_history_is_shallow']=report.get('git_history_is_shallow')
    out['unavailable_inputs']=report.get('unavailable_inputs',[])
    if report.get('owner_review_follow_up'):out['owner_review_follow_up']=report['owner_review_follow_up']
    out['coverage_gaps']=[{'kind':g['kind'],'path':'<restricted-or-local>'} for g in report['coverage_gaps']]
    out['totals']={'unique_visual_files':len(report['images']),'logical_frames':sum(len(r['frames']) for r in report['images']),'current_project_sources':len(report.get('current_project_source_ids',[])),'atlas_frames_locally_screened':sum(f.get('review')=='assistant_atlas_visual_triage' for r in report['images'] for f in r['frames']),'occurrences':sum(len(r['occurrences']) for r in report['images']),'risk_counts':dict(collections.Counter(r['risk']['overall'] for r in report['images'])),'sensitivity_counts':dict(collections.Counter(r['sensitivity'] for r in report['images'])),'unreviewed_visual_files':sum(r['visual_review']=='not_reviewed' for r in report['images']),'containers':len(report['containers']),'procedural_sources':len(report['procedural']),'coverage_gaps':len(report['coverage_gaps'])}
    return out

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=ROOT);p.add_argument('--output',required=True,type=Path);p.add_argument('--generated-root',type=Path);p.add_argument('--redacted-output',type=Path);p.add_argument('--templates-root',type=Path);a=p.parse_args()
    root=a.root.resolve();output=a.output.resolve()
    if output==root or root in output.parents:raise SystemExit('Full audit output must be outside the repository')
    output.parent.mkdir(parents=True,exist_ok=True,mode=0o700);os.chmod(output.parent,0o700)
    previous_ids=json.loads(output.read_text()).get('private_ids',{}) if output.exists() else {}
    report=scan(root,a.generated_root,True,a.templates_root)
    checkpoint=output.with_suffix('.scan-checkpoint.json');checkpoint.write_text(json.dumps(report,ensure_ascii=False));os.chmod(checkpoint,0o600)
    report['private_ids']=previous_ids
    nested_containers(report);native_drawables(report);retained_git_visuals(report,root);add_frames(report,root);enrich(report,root);apply_reviews(report,root)
    public=redacted(report)
    output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');os.chmod(output,0o600)
    if a.redacted_output:
        target=a.redacted_output.resolve()
        if root in target.parents and target!=root/'docs/qa/visual-ip-manifest.json':raise SystemExit('Only the named redacted QA manifest may be written inside the repository')
        target.parent.mkdir(parents=True,exist_ok=True);target.write_text(json.dumps(public,separators=(',',':'))+'\n')
    print(json.dumps(public['totals'],indent=2))
if __name__=='__main__':main()
