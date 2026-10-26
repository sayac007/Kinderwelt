#!/usr/bin/env python3
"""Report missing release configuration by name only; never expose values."""
import json,os,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import identity,upload_signing
ROOT=Path(__file__).resolve().parents[2]
def missing(env,root=ROOT):
    metadata=json.loads((Path(root)/'scripts/android/release-metadata.json').read_text())
    absent=[name for name in upload_signing.REQUIRED if not env.get(name)]
    for key,name in upload_signing.METADATA_ENV.items():
        value=(env.get(name) or metadata.get(key,'')).strip()
        if not value or '{{' in value or '}}' in value:absent.append(name)
    return absent
def main():
    absent=missing(os.environ)
    ready=not absent
    if ready:
        # These errors name fields, never supplied values.
        try:
            identity.validate_configured_release_package(os.environ.get('KINDERWELT_PACKAGE_ID'))
            upload_signing.metadata()
        except ValueError as error:
            print('::error::'+str(error));return 2
    with open(os.environ['GITHUB_OUTPUT'],'a') as f:f.write('ready='+str(ready).lower()+'\n')
    if absent:print('::notice::Release signing SKIPPED; operator must configure: '+', '.join(absent))
    return 0
if __name__=='__main__':raise SystemExit(main())
