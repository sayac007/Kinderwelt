"""Explicit provisional Android identity, shared by builder and verifier."""
import json,re
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import release_version
CONFIG=json.loads((Path(__file__).parent/'app-config.json').read_text())
CONFIG.update(release_version.read())
TOKEN='@KINDERWELT_PACKAGE_ID@'
def validate_package(value):
    if len(value)>180 or not re.fullmatch(r'[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)+',value):
        raise ValueError('Android package must contain at least two lowercase identifier segments, max 180 characters')
    reserved={'abstract','assert','boolean','break','byte','case','catch','char','class','const','continue','default','do','double','else','enum','extends','final','finally','float','for','goto','if','implements','import','instanceof','int','interface','long','native','new','package','private','protected','public','return','short','static','strictfp','super','switch','synchronized','this','throw','throws','transient','try','void','volatile','while','true','false','null'}
    if set(value.split('.'))&reserved:raise ValueError('Java reserved word in package identifier')
    return value

def validate_release_package(value):
    if not value:
        raise ValueError('Release requires --package-id or KINDERWELT_PACKAGE_ID; no provisional identity is used')
    if value == TOKEN or re.search(r'example|test|debug', value, re.I):
        raise ValueError('Release package must be final: placeholders and example/test/debug identifiers are forbidden')
    return validate_package(value)

def configure(app,package=None,preview=False,variant='family'):
    base=validate_package(package or CONFIG['test_package'])
    chosen=validate_package(base+f'.preview.{"family" if variant=="family" else "neutral"}.'+CONFIG['preview_channel'] if preview else base)
    preset=app/'export_presets.cfg';text=preset.read_text()
    if text.count('package/unique_name="'+TOKEN+'"')!=2:raise ValueError('Missing package placeholders in Android presets')
    text=text.replace(TOKEN,chosen)
    for token, value in [('"@KINDERWELT_VERSION_CODE@"',str(CONFIG['version_code'])),
                         ('"@KINDERWELT_VERSION_NAME@"',json.dumps(CONFIG['version_name']))]:
        if text.count(token)!=2:raise ValueError('Missing version placeholders in Android presets')
        text=text.replace(token,value)
    if preview:
        label='Kinderwelt '+CONFIG['version_name']+' '+('Privat' if variant=='family' else 'Public')+' Test'
        text=text.replace('package/name="Kinderwelt"','package/name='+json.dumps(label))
        project=app/'project.godot';project.write_text(project.read_text().replace('config/name="Kinderwelt"','config/name='+json.dumps(label)))
    preset.write_text(text)
    return chosen
