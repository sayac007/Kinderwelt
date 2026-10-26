"""The clean policy preserves the operator text and never executes Word content."""
import importlib.util,tempfile,unittest,hashlib
from html.parser import HTMLParser
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('approved_privacy',ROOT/'scripts/store/approved_privacy.py')
policy=importlib.util.module_from_spec(spec);spec.loader.exec_module(policy)
class Visible(HTMLParser):
    def __init__(self):super().__init__();self.parts=[];self.skip=0
    def handle_starttag(self,t,a):
        if t in ['head','style','script','title','nav']:self.skip+=1
        if t in ['p','h1','h2','li','br']:self.parts.append(' ')
    def handle_endtag(self,t):
        if t in ['head','style','script','title','nav']:self.skip-=1
    def handle_data(self,d):
        if not self.skip:self.parts.append(d)
class ApprovedPrivacyTests(unittest.TestCase):
    def test_generated_page_preserves_every_operator_paragraph_and_original_bytes(self):
        source=ROOT/policy.SOURCE;before=hashlib.sha256(source.read_bytes()).digest()
        original=Visible();original.feed(source.read_bytes().decode('cp1252'))
        expected=' '.join(''.join(original.parts).split())
        with tempfile.TemporaryDirectory() as d:
            out=policy.build(Path(d)/'site')
            for filename in ['index.html','de.html']:
                text=(out/filename).read_text();parsed=Visible();parsed.feed(text)
                self.assertEqual(' '.join(''.join(parsed.parts).split()),expected)
                self.assertNotIn('<script',text);self.assertNotIn('mso-',text);self.assertNotIn('<img',text)
                self.assertIn('a.w.kulikov@gmail.com',text)
                self.assertIn('href="'+policy.GOOGLE+'"',text)
        self.assertEqual(hashlib.sha256(source.read_bytes()).digest(),before)
    def test_source_placeholders_and_unexpected_links_are_rejected(self):
        raw=(ROOT/policy.SOURCE).read_bytes()
        with self.assertRaisesRegex(ValueError,'placeholders'):policy.parse(raw.replace(b'Kinderwelt',b'{{NAME}}',1))
        with self.assertRaisesRegex(ValueError,'Unexpected external'):
            policy.parse(raw.replace(policy.GOOGLE.encode(),b'https://unreviewed.invalid/'))
    def test_active_markup_is_removed_without_evaluating_it(self):
        raw=(ROOT/policy.SOURCE).read_bytes()
        # The added active element is not a legal-policy paragraph.
        raw=raw.replace(b'</body>',b'<script>privateMarker()</script></body>')
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/policy.SOURCE).write_bytes(raw)
            (root/'docs/privacy').mkdir(parents=True)
            for locale in ['en','ru']:(root/'docs/privacy'/('privacy.'+locale+'.md')).write_bytes((ROOT/'docs/privacy'/('privacy.'+locale+'.md')).read_bytes())
            out=policy.build(root/'site',root)
            self.assertNotIn('privateMarker',(out/'index.html').read_text())
