#!/usr/bin/env python3
"""Export the operator-supplied German policy without Word markup or active content."""
import argparse,html,json,re
from html.parser import HTMLParser
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
SOURCE='Datenschutzerklärung für die App.htm'
GOOGLE='https://policies.google.com/privacy'
class PolicyParser(HTMLParser):
    def __init__(self):
        super().__init__();self.skip=0;self.paragraph=None;self.block_tag=None;self.blocks=[];self.links=[]
    def handle_starttag(self,tag,attrs):
        if tag in ['head','style','script']:self.skip+=1
        if self.skip:return
        if tag in ['p','li'] and self.paragraph is None:self.paragraph=[];self.block_tag=tag
        if tag=='br' and self.paragraph is not None:self.paragraph.append(' ')
        if tag=='a':
            href=dict(attrs).get('href','')
            if href:self.links.append(href)
    def handle_endtag(self,tag):
        if tag in ['head','style','script']:self.skip-=1
        if tag==self.block_tag and self.paragraph is not None:
            text=' '.join(''.join(self.paragraph).split())
            if text:self.blocks.append(text)
            self.paragraph=None;self.block_tag=None
    def handle_data(self,data):
        if not self.skip and self.paragraph is not None:self.paragraph.append(data)
def parse(raw):
    charset=re.search(rb'charset[=\s]+[\"\x27]?([A-Za-z0-9_-]+)',raw[:6000],re.I)
    parser=PolicyParser();parser.feed(raw.decode(charset[1].decode() if charset else 'utf-8'))
    text='\n'.join(parser.blocks)
    if re.search(r'\{\{[^}]+\}\}',text):raise ValueError('Approved privacy source still contains placeholders')
    if [int(m[1]) for p in parser.blocks if (m:=re.match(r'^(\d+)\.\s',p)) and 1<=int(m[1])<=10]!=list(range(1,11)):
        raise ValueError('Expected all ten numbered sections of the operator policy')
    for link in parser.links:
        if link!=GOOGLE and not link.startswith('mailto:'):raise ValueError('Unexpected external policy link; review the source')
    if GOOGLE not in parser.links:raise ValueError('Expected original Google privacy reference')
    return parser.blocks
def texts(root=ROOT):
    root=Path(root);result={'de':parse((root/SOURCE).read_bytes())}
    for locale in ['en','ru']:
        raw=(root/'docs/privacy'/('privacy.'+locale+'.md')).read_text()
        if re.search(r'\{\{[^}]+\}\}',raw):raise ValueError('Unresolved translated privacy field')
        result[locale]=[re.sub(r'^#{1,2} ', '',p).replace('\n',' ') for p in raw.strip().split('\n\n')]
        if len([p for p in result[locale] if re.match(r'^(?:[1-9]|10)\. ',p)])!=10:raise ValueError('Incomplete translated privacy policy')
    return result
def app_data(root=ROOT):
    return json.dumps({'schema':1,'google_privacy_url':GOOGLE,'texts':texts(root)},ensure_ascii=False,indent=2)+'\n'
def pages(root=ROOT):
    policies=texts(root);result={}
    for locale,blocks in policies.items():
        body=[]
        for index,text in enumerate(blocks):
            heading=re.match(r'^(\d+)\.\s',text)
            tag='h1' if index==0 else 'h2' if heading and 1<=int(heading[1])<=10 else 'p'
            escaped=html.escape(text)
            phrases={'de':'Datenschutzerklärung von Google','en':"Google's privacy policy",'ru':'политике конфиденциальности Google'}
            phrase=phrases[locale]
            escaped=escaped.replace(html.escape(phrase),f'<a href="{GOOGLE}">{html.escape(phrase)}</a>')
            body.append(f'<{tag}>{escaped}</{tag}>')
        links=' · '.join(f'<a href="{lang}.html" lang="{lang}">{lang.upper()}</a>' for lang in policies)
        result[locale+'.html']=f'<!doctype html>\n<html lang="{locale}"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kinderwelt – Privacy</title><style>body{{font:1.1rem/1.65 system-ui;max-width:52rem;margin:2rem auto;padding:0 1rem;color:#19384f}}h1,h2{{line-height:1.3}}a{{color:#194e72}}</style><nav>{links}</nav><main>\n'+'\n'.join(body)+'</main></html>\n'
    result['index.html']=result['de.html']
    return result
def build(output,root=ROOT):
    rendered=pages(root);output=Path(output);output.mkdir(parents=True,exist_ok=False)
    for name,page in rendered.items():(output/name).write_text(page)
    return output
def check(output,root=ROOT):
    for name,page in pages(root).items():
        if (Path(output)/name).read_text()!=page:raise ValueError('Stale approved privacy page: '+name)
    if (Path(root)/'assets/privacy/policy.json').read_text()!=app_data(root):raise ValueError('Stale bundled privacy policy')
    return Path(output)
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,default=ROOT/'build/privacy-approved');p.add_argument('--check',action='store_true');p.add_argument('--write-app',action='store_true');a=p.parse_args()
    try:
        if a.write_app:
            target=ROOT/'assets/privacy/policy.json';target.parent.mkdir(parents=True,exist_ok=True);target.write_text(app_data())
        print(check(a.output) if a.check else build(a.output))
    except (ValueError,UnicodeError) as error:p.error(str(error))
