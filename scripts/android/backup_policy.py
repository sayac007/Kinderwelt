"""Exclude app data from cloud backup and device transfer, without permissions."""
import re
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

DOMAINS = {'root', 'file', 'database', 'sharedpref', 'external'}
FILES = {'fullBackupContent': 'kinderwelt_backup_rules',
         'dataExtractionRules': 'kinderwelt_data_extraction_rules'}


def install(android):
    android = Path(android)
    main = android / 'src/main/AndroidManifest.xml'
    text = main.read_text()
    application = ET.fromstring(text).find('application')
    if application is None or text.count('<application') != 1:
        raise ValueError('Expected one application in the pinned main manifest')
    namespace = '{http://schemas.android.com/apk/res/android}'
    if any(application.get(namespace + attribute) is not None for attribute in FILES):
        raise ValueError('Refusing to overwrite existing main-manifest backup policy')
    exclusions = ''.join(f'<exclude domain="{domain}" path="."/>' for domain in sorted(DOMAINS))
    rules = {
        'kinderwelt_backup_rules': '<full-backup-content>' + exclusions + '</full-backup-content>',
        'kinderwelt_data_extraction_rules': '<data-extraction-rules><cloud-backup>' + exclusions +
        '</cloud-backup><device-transfer>' + exclusions + '</device-transfer></data-extraction-rules>',
    }
    for name, content in rules.items():
        path = android / 'res/xml' / (name + '.xml')
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('<?xml version="1.0" encoding="utf-8"?>\n' + content + '\n')
    # Godot REGENERATES src/debug and src/release manifests on each export.
    # The pinned src/main manifest is retained and merged into both variants.
    attributes = ' '.join(f'android:{attr}="@xml/{name}"' for attr, name in FILES.items())
    main.write_text(re.sub(r'<application\b', '<application ' + attributes + ' ', text, count=1))


def xmltree(text):
    """Read aapt2's plain resource-tree output, preserving element nesting."""
    stack, root = [], None
    for line in text.splitlines():
        element = re.match(r'^(\s*)E: ([\w-]+)', line)
        if element:
            depth = len(element[1])
            while stack and stack[-1][0] >= depth:
                stack.pop()
            node = ET.Element(element[2])
            if stack:
                stack[-1][1].append(node)
            else:
                root = node
            stack.append((depth, node))
        attribute = re.match(r'^\s*A: ([\w-]+)(?:\([^)]*\))?="([^"]*)"', line)
        if attribute and stack:
            stack[-1][1].set(attribute[1], attribute[2])
    if root is None:
        raise ValueError('No decoded backup rule tree')
    return root


def validate_rules(root, modern=False):
    assert root.tag == ('data-extraction-rules' if modern else 'full-backup-content'), 'Wrong backup rule root'
    groups = [root.find('cloud-backup'), root.find('device-transfer')] if modern else [root]
    if modern:
        assert len(root) == 2, 'Unexpected backup rule section'
    for group in groups:
        assert group is not None, 'Missing cloud/device-transfer backup policy'
        assert len(group) == 5 and all(node.tag == 'exclude' for node in group), 'Backup must contain only exclusions'
        assert {(node.get('domain'), node.get('path')) for node in group} == {(domain, '.') for domain in DOMAINS}, 'Incomplete backup exclusion'


def verify_apk(aapt, apk, manifest_text):
    def run(*args):
        return subprocess.check_output([str(aapt), *map(str, args)], text=True, stderr=subprocess.STDOUT)
    resources = run('dump', 'resources', apk)
    for attribute, name in FILES.items():
        resource = re.search(r'\bresource (0x[\da-f]+)\s+xml/' + name + r'\b', resources, re.I)
        assert resource, 'Missing compiled backup resource: ' + name
        assert re.search(r'android:' + attribute + r'[^\n]*=@' + resource[1] + r'\b', manifest_text, re.I), 'Manifest does not reference verified backup rules: ' + attribute
        tree = run('dump', 'xmltree', apk, '--file', 'res/xml/' + name + '.xml')
        validate_rules(xmltree(tree), attribute == 'dataExtractionRules')
    return {'cloud_backup': 'excluded', 'device_transfer': 'excluded',
            'compiled_rule_resources_and_manifest_references': 'PASS'}
