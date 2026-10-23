#!/usr/bin/env python3
"""Verify pinned voice provenance. This cannot certify intelligibility."""
import argparse,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def check(models=None):
    contract=json.loads((ROOT/'scripts/qa/voice-models.json').read_text());report={}
    for locale,expected in contract['selected'].items():
        folder=ROOT/'assets/voice/quest'/locale;manifest=json.loads((folder/'manifest.json').read_text())
        for key in ['model','model_sha256','model_source','dataset_license','voice_gender']:
            assert manifest[key]==expected[key],f'Voice provenance drift: {locale}/{key}'
        assert hashlib.sha256((folder/'MODEL_CARD.txt').read_bytes()).hexdigest()==expected['model_card_sha256'],'Model card changed'
        assert expected['dataset_license'] in ['CC0','Public Domain']
        if models:
            path=models/('vits-piper-'+expected['model'])/(expected['model']+'.onnx')
            assert hashlib.sha256(path.read_bytes()).hexdigest()==expected['model_sha256']
            config=json.loads(Path(str(path)+'.json').read_text())
            assert config['audio']['sample_rate']==expected['sample_rate']
            if locale=='de':assert config['audio']['quality']=='high'
        clips=manifest['clips'];unique={c['file']:c for c in clips}
        report[locale]={'model':expected['model'],'mappings':len(clips),'unique_files':len(unique),'generated_seconds':round(sum(c['seconds'] for c in unique.values()),3),'model_and_card_provenance':'PASS','human_intelligibility':'OPEN'}
    return report
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--models',type=Path);p.add_argument('--output',type=Path);a=p.parse_args();report=check(a.models)
    if a.output:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
