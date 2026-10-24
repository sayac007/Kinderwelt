"""Offline audit boundaries: coverage, correct crops, privacy and no uploads."""
import ast,hashlib,importlib.util,io,json,subprocess,sys,tempfile,unittest,zipfile
from pathlib import Path
from unittest.mock import patch
try:
    from PIL import Image
    PILLOW_AVAILABLE=True
except ModuleNotFoundError:
    PILLOW_AVAILABLE=False
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts/qa'))
if PILLOW_AVAILABLE:
    import visual_ip as audit
    import visual_ip_pack as pack
@unittest.skipUnless(PILLOW_AVAILABLE,'Pillow is required for the optional visual audit; install it to execute these checks')
class VisualAuditTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)/'repo';self.root.mkdir()
        (self.root/'assets/quest').mkdir(parents=True);(self.root/'build').mkdir();(self.root/'.private').mkdir()
        (self.root/'project.godot').write_text('[application]\nconfig/name="Audit test"\n')
        image=Image.new('RGBA',(12,8),'red');stream=io.BytesIO();image.save(stream,format='PNG');self.raw=stream.getvalue()
        (self.root/'assets/quest/test.png').write_bytes(self.raw);(self.root/'build/mislabeled.data').write_bytes(self.raw)
        Image.new('RGB',(10,10),'blue').save(self.root/'.private/SECRET_PERSON_REFERENCE.png')
        (self.root/'embedded.tscn').write_text('[resource]\nsvg_data="<svg xmlns=\\"http://www.w3.org/2000/svg\\" width=\\"3\\" height=\\"4\\"></svg>"')
        with zipfile.ZipFile(self.root/'build/sample.apk','w') as z:
            z.writestr('assets/assets/quest/test.png.import','[remap]\npath="res://.godot/imported/test.ctex"\n\0')
            z.writestr('assets/.godot/imported/test.ctex',b'GST2'+bytes(36)+self.raw)
            z.writestr('../never-extract.png',self.raw)
        subprocess.run(['git','init','-q',str(self.root)],check=True)
        subprocess.run(['git','-C',str(self.root),'add','assets','project.godot','embedded.tscn'],check=True)
        subprocess.run(['git','-C',str(self.root),'-c','user.name=Audit Test','-c','user.email=audit@example.invalid','commit','-qm','Synthetic audit fixture'],check=True)
    def scan(self):return audit.scan(self.root,history=False)
    def test_signature_inventory_includes_untracked_and_archive_duplicates(self):
        report=self.scan();row=next(r for r in report['images'] if r['sha256']==hashlib.sha256(self.raw).hexdigest())
        self.assertEqual(row['format'],'PNG');self.assertEqual(row['dimensions'],[12,8])
        self.assertEqual(len(row['occurrences']),3)
        self.assertIn('build/mislabeled.data',{o['path'] for o in row['occurrences']})
        self.assertFalse((self.root.parent/'never-extract.png').exists())
    def test_exported_import_without_deps_has_a_source_hint(self):
        report=self.scan();row=next(r for r in report['images'] if r['format']=='GodotTexture')
        self.assertEqual(row['occurrences'][0]['source_hint'],'assets/quest/test.png')
        self.assertEqual(audit.decoded(audit.load_bytes(row['occurrences'][0]['locator'])).size,(12,8))
        audit.enrich(report,self.root)
        self.assertTrue(row['lineage_sources'])
    def test_embedded_svg_is_extracted_instead_of_misclassifying_the_document(self):
        self.assertIsNone(audit.kind(b'[resource]\nsvg_data="<svg></svg>"'))
        report=self.scan();rows=[r for r in report['images'] if r['format']=='SVG']
        self.assertEqual(len(rows),1);self.assertEqual(rows[0]['dimensions'],[3,4])
        self.assertIn('embedded_svg_file',rows[0]['occurrences'][0]['locator'])
    def test_private_paths_hashes_and_ids_are_redacted(self):
        report=self.scan();private=next(r for r in report['images'] if any('.private/' in o['path'] for o in r['occurrences']))
        text=json.dumps(audit.redacted(report))
        self.assertNotIn('SECRET_PERSON_REFERENCE',text);self.assertNotIn(private['sha256'],text);self.assertNotIn(private['sha256'][:20],text)
        self.assertNotIn(str(self.root),text)
    def test_lossless_crop_and_mask_do_not_modify_the_source(self):
        image=Image.new('RGBA',(8,4),'red');image.paste('blue',(4,0,8,4));stream=io.BytesIO();image.save(stream,format='PNG');raw=stream.getvalue();before=hashlib.sha256(raw).hexdigest()
        crop=pack.frame_image(raw,{'rect':[0,0,4,4],'label':'hero'})
        self.assertEqual(crop.size,(4,4));self.assertEqual(crop.getpixel((2,2)),(255,0,0,255))
        masked=pack.frame_image(raw,{'rect':[0,0,8,4],'label':'hero'},[[y,0,4,1] for y in range(4)])
        self.assertEqual(masked.getpixel((6,2))[3],0);self.assertEqual(hashlib.sha256(raw).hexdigest(),before)
        with self.assertRaises(ValueError):pack.frame_image(raw,{'rect':[0,0,100,4],'label':'hero'})
    def test_alpha_is_part_of_the_visible_pixel_identity(self):
        a=Image.new('RGBA',(4,4),(255,255,255,255));b=Image.new('RGBA',(4,4),(255,255,255,0))
        self.assertNotEqual(audit.fingerprints(a)[0],audit.fingerprints(b)[0])
    def test_animated_and_atlas_frames_are_enumerated(self):
        a=Image.new('RGB',(5,6),'green');b=Image.new('RGB',(5,6),'orange');a.save(self.root/'animated.gif',save_all=True,append_images=[b],duration=100,loop=0)
        (self.root/'atlas.tres').write_text('[gd_resource type="AtlasTexture"]\n[ext_resource path="res://assets/quest/test.png" type="Texture2D" id="1"]\n[resource]\nregion = Rect2(0, 0, 4, 3)')
        report=self.scan();audit.add_frames(report,self.root)
        self.assertEqual(sum(len(r['frames']) for r in report['images']),3)
    def test_pack_is_outside_git_and_keeps_sensitive_material_separate(self):
        report=self.scan()
        with self.assertRaises(ValueError):pack.prepare(report,self.root/'unsafe-review',self.root)
        out=self.root.parent/'owner-only';result=pack.prepare(report,out,self.root)
        self.assertTrue(Path(result['public-candidates']['zip']).exists())
        public=(out/'public-candidates/manifest.json').read_text();self.assertNotIn('SECRET_PERSON_REFERENCE',public)
        self.assertIn('SECRET_PERSON_REFERENCE',(out/'restricted-family/manifest.json').read_text())
        self.assertEqual(result['restricted-family']['candidates'],1)
        self.assertTrue(all(not e['online_upload_permitted'] for e in json.loads(public)['entries']))
        with zipfile.ZipFile(result['public-candidates']['zip']) as z:self.assertIsNone(z.testzip())
    def test_nested_archive_images_are_loaded_without_extraction(self):
        data=io.BytesIO();Image.new('RGBA',(7,9),'purple').save(data,format='PNG');raw=data.getvalue();inner=io.BytesIO()
        with zipfile.ZipFile(inner,'w') as z:z.writestr('deep/image.bin',raw)
        with zipfile.ZipFile(self.root/'build/sample.apk','a') as z:z.writestr('library.aar',inner.getvalue())
        report=self.scan();audit.nested_containers(report)
        row=next(r for r in report['images'] if r['sha256']==hashlib.sha256(raw).hexdigest())
        self.assertEqual(audit.load_bytes(row['occurrences'][0]['locator']),raw)
        self.assertEqual(row['dimensions'],[7,9]);self.assertFalse((self.root/'deep/image.bin').exists())
    def test_native_drawable_definitions_are_counted_without_claiming_visual_review(self):
        with zipfile.ZipFile(self.root/'build/sample.apk','a') as archive:
            archive.writestr('res/mipmap-anydpi-v26/icon.xml',b'\x03\x00\x08\x00'+b'compiled fixture')
        report=self.scan();audit.native_drawables(report)
        rows=[r for r in report['images'] if r['format']=='AndroidDrawableXML']
        self.assertEqual(len(rows),1);self.assertEqual(rows[0]['visual_review'],'not_reviewed')
        self.assertEqual(rows[0]['decode_status'],'native_definition_not_rasterized')
    def test_retained_git_visuals_include_deleted_private_source_safely(self):
        path=self.root/'.private/HISTORICAL_SECRET.png';Image.new('RGB',(3,3),'cyan').save(path);digest=hashlib.sha256(path.read_bytes()).hexdigest()
        subprocess.run(['git','-C',str(self.root),'add','-f',str(path)],check=True)
        subprocess.run(['git','-C',str(self.root),'-c','user.name=Audit Test','-c','user.email=audit@example.invalid','commit','-qm','Synthetic private history'],check=True);path.unlink()
        report=self.scan();audit.retained_git_visuals(report,self.root)
        row=next(r for r in report['images'] if r['sha256']==digest)
        self.assertEqual(row['sensitivity'],'family_private')
        exported=json.dumps(audit.redacted(report));self.assertNotIn('HISTORICAL_SECRET',exported);self.assertNotIn(digest[:20],exported)
    def test_repeated_scan_is_deterministic_and_review_is_bound_to_sha256(self):
        first=self.scan();second=self.scan();self.assertEqual(audit.redacted(first),audit.redacted(second))
        row=next(r for r in first['images'] if r['sha256']==hashlib.sha256(self.raw).hexdigest())
        ledger={'source_reviews':[{'sha256':'0'*64,'resemblance':'low','observation':'Must not apply'}]}
        audit.apply_reviews(first,self.root,ledger);self.assertEqual(row['visual_review'],'not_reviewed')
    def test_owner_findings_cannot_leak_private_evidence_or_apply_to_stale_hashes(self):
        report=self.scan();private=next(r for r in report['images'] if any(o['path'].startswith('.private/') for o in r['occurrences']))
        folder=self.root/'scripts/qa';folder.mkdir(parents=True)
        owner={'review_date':'2026-10-24','base_commit':'fixture','scope':'fixture','summary':{},'legacy_chronology':{},
               'sources':[{'source_sha256':private['sha256'],'file_credentials':{'secret':'PRIVATE_CREDENTIAL'},'retained_original':{'secret':'PRIVATE_ORIGINAL'}},
                          {'source_sha256':'0'*64,'file_credentials':{'secret':'STALE_OWNER_FINDING'},'retained_original':{}}],
               'manual_review':{'rows':[{'source_sha256':private['sha256'],'owner_decision':'PRIVATE_DECISION'}]}}
        (folder/'visual-ip-owner-review.json').write_text(json.dumps(owner))
        audit.apply_reviews(report,self.root,{})
        self.assertNotIn('owner_manual_reviews',private)
        exported=json.dumps(audit.redacted(report))
        for secret in ['PRIVATE_CREDENTIAL','PRIVATE_ORIGINAL','PRIVATE_DECISION','STALE_OWNER_FINDING']:
            self.assertNotIn(secret,exported)
    def test_tools_have_no_network_or_shell_upload_implementation(self):
        for name in ['visual_ip.py','visual_ip_pack.py','visual_c2pa.py']:
            tree=ast.parse((ROOT/'scripts/qa'/name).read_text())
            for node in ast.walk(tree):
                if isinstance(node,(ast.Import,ast.ImportFrom)):
                    modules=[n.name for n in node.names] if isinstance(node,ast.Import) else [node.module or '']
                    self.assertFalse(any(m.split('.')[0] in ['socket','requests','urllib','http','ftplib','webbrowser'] for m in modules))
                if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute) and isinstance(node.func.value,ast.Name) and node.func.value.id=='subprocess':
                    self.assertEqual(node.func.attr,'check_output');self.assertIsInstance(node.args[0],ast.List);self.assertEqual(node.args[0].elts[0].value,'git')
if __name__=='__main__':unittest.main()
