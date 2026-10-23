"""Reusable development certificate outside source; never a release key.

Android requires the same certificate and package to update a test installation
without losing its local state. Do not use this public-password key for releases.
"""
import os
import hashlib
import subprocess
from pathlib import Path


def ensure(tools, java):
    key = Path(os.environ.get('KINDERWELT_DEBUG_KEYSTORE', str(tools / 'preview-signing' / 'debug.keystore'))).resolve()
    root = Path(__file__).resolve().parents[2]
    if key.is_relative_to(root):
        raise ValueError('Development signing key must be outside the repository')
    key.parent.mkdir(parents=True, exist_ok=True)
    if not key.exists():
        subprocess.run([str(java / 'bin/keytool'), '-genkeypair', '-keystore', str(key),
                        '-storepass', 'android', '-keypass', 'android', '-alias', 'androiddebugkey',
                        '-keyalg', 'RSA', '-keysize', '2048', '-validity', '10000',
                        '-dname', 'CN=Godot,OU=Development Only,O=Kinderwelt,C=DE',
                        '-storetype', 'JKS', '-noprompt'], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        key.chmod(0o600)
    # Fail before a long export if the cached development key is unusable.
    subprocess.run([str(java / 'bin/keytool'), '-list', '-keystore', str(key),
                    '-storepass', 'android', '-alias', 'androiddebugkey'],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    return key


def fingerprint(key, java):
    certificate = subprocess.check_output([str(java / 'bin/keytool'), '-exportcert',
        '-keystore', str(key), '-storepass', 'android', '-alias', 'androiddebugkey'],
        stderr=subprocess.PIPE)
    return hashlib.sha256(certificate).hexdigest()
