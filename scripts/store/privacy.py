#!/usr/bin/env python3
"""Build static, script-free privacy drafts; --final rejects unresolved placeholders."""
import argparse,html,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
FILES={'de':'datenschutz.de.md','en':'privacy.en.md','ru':'privacy.ru.md'}
def build(output,final=False,root=ROOT):
    sources={locale:(root/'docs/privacy'/name).read_text() for locale,name in FILES.items()}
    if final and any(re.search(r'\{\{[^}]+\}\}',s) for s in sources.values()):
        raise ValueError('Replace and approve all privacy placeholders before publication')
    output=Path(output)
    output.mkdir(parents=True,exist_ok=False)
    for locale,source in sources.items():
        blocks=[]
        for paragraph in source.strip().split('\n\n'):
            text=html.escape(paragraph)
            if paragraph.startswith('# '):blocks.append('<h1>'+html.escape(paragraph[2:])+'</h1>')
            elif paragraph.startswith('## '):blocks.append('<h2>'+html.escape(paragraph[3:])+'</h2>')
            else:blocks.append('<p>'+text.replace('\n',' ')+'</p>')
        links=' · '.join(f'<a href="{lang}.html" lang="{lang}">{lang.upper()}</a>' for lang in FILES)
        page=f'<!doctype html><html lang="{locale}"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kinderwelt — {locale}</title><style>body{{font:1.1rem/1.6 system-ui;max-width:52rem;margin:2rem auto;padding:0 1rem;color:#19384f}}a{{color:#194e72}}p{{white-space:normal}}</style><nav>{links}</nav><main>'+''.join(blocks)+'</main></html>\n'
        (output/(locale+'.html')).write_text(page)
    (output/'index.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><title>Kinderwelt privacy</title><h1>Kinderwelt</h1>'+links+'</html>\n')
    return output
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,default=ROOT/'build/privacy');p.add_argument('--final',action='store_true');a=p.parse_args()
    try:print(build(a.output,a.final))
    except ValueError as error:p.error(str(error))
