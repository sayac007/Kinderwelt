"""Read the only editable Android/display version from project.godot."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def read(root=ROOT):
    text = (Path(root) / 'project.godot').read_text()
    names = re.findall(r'^config/version=("[^"\n]+")$', text, re.M)
    codes = re.findall(r'^config/version_code=([0-9]+)$', text, re.M)
    if len(names) != 1 or len(codes) != 1:
        raise ValueError('project.godot must define one config/version and config/version_code')
    name, code = json.loads(names[0]), int(codes[0])
    if not re.fullmatch(r'[0-9]+\.[0-9]+\.[0-9]+(?:[.-][A-Za-z0-9.-]+)?', name) or not 1 <= code <= 2100000000:
        raise ValueError('Invalid Android version in project.godot')
    return {'version_name': name, 'version_code': code}
