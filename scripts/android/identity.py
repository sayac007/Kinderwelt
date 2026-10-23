"""Explicit provisional Android identity, shared by builder and verifier."""
import json,re
from pathlib import Path
CONFIG=json.loads((Path(__file__).parent/'app-config.json').read_text())
TOKEN='@KINDERWELT_PACKAGE_ID@'
def validate_package(value):
    if len(value)>180 or not re.fullmatch(r'[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)+',value):
        raise ValueError('Android package must contain at least two lowercase identifier segments, max 180 characters')
    reserved={'abstract','assert','boolean','break','byte','case','catch','char','class','const','continue','default','do','double','else','enum','extends','final','finally','float','for','goto','if','implements','import','instanceof','int','interface','long','native','new','package','private','protected','public','return','short','static','strictfp','super','switch','synchronized','this','throw','throws','transient','try','void','volatile','while','true','false','null'}
    if set(value.split('.'))&reserved:raise ValueError('Java reserved word in package identifier')
    return value

def configure(app,package=None,preview=False,variant='family'):
    base=validate_package(package or CONFIG['test_package'])
    chosen=validate_package(base+f'.preview.{"family" if variant=="family" else "neutral"}.'+CONFIG['preview_channel'] if preview else base)
    preset=app/'export_presets.cfg';text=preset.read_text()
    if text.count('package/unique_name="'+TOKEN+'"')!=2:raise ValueError('Missing package placeholders in Android presets')
    text=text.replace(TOKEN,chosen)
    if preview:
        label='Kinderwelt '+CONFIG['version_name']+' '+('Privat' if variant=='family' else 'Public')+' Test'
        text=text.replace('package/name="Kinderwelt"','package/name='+json.dumps(label))
        project=app/'project.godot';project.write_text(project.read_text().replace('config/name="Kinderwelt"','config/name='+json.dumps(label)))
    preset.write_text(text)
    return chosen
