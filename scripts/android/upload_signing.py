"""Operator-owned upload signing; never create keys or expose tool diagnostics.

Godot/Gradle never receive upload credentials. jarsigner reads passwords from
environment variables; no password occurs in an argument or retained log.
"""
import base64
import binascii
import hashlib
import json
import os
import re
import subprocess
from contextlib import contextmanager
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PREFIX = 'KINDERWELT_UPLOAD_'
REQUIRED = tuple(PREFIX + n for n in ['KEYSTORE', 'ALIAS', 'STORE_PASSWORD', 'KEY_PASSWORD'])
MAX_KEYSTORE_BYTES = 1024 * 1024
METADATA_ENV = {k: 'KINDERWELT_' + k.upper() for k in ['publisher', 'support_email', 'asset_license']}


def credentials(env=None):
    env = os.environ if env is None else env
    missing = [n for n in REQUIRED if not env.get(n)]
    if missing:
        raise ValueError('Release signing requires environment variables: ' + ', '.join(missing))
    if any(c in env[PREFIX + 'ALIAS'] for c in '\r\n\0') or env[PREFIX + 'ALIAS'].startswith('-'):
        raise ValueError('Invalid upload key alias')
    return {n: env[n] for n in REQUIRED}


def metadata(env=None, root=ROOT):
    env = os.environ if env is None else env
    values = json.loads((Path(root) / 'scripts/android/release-metadata.json').read_text())
    for key, variable in METADATA_ENV.items():
        value = env.get(variable, values.get(key, '')).strip()
        if not value or '{{' in value or '}}' in value:
            raise ValueError('Release operator information is missing: ' + variable)
        values[key] = value
    if not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', values['support_email']):
        raise ValueError('Invalid KINDERWELT_SUPPORT_EMAIL')
    return values


def export_environment(env=None):
    """Do not pass signing secrets or operator information to Godot/Gradle."""
    return {k: v for k, v in (os.environ if env is None else env).items()
            if not k.startswith(PREFIX) and k not in METADATA_ENV.values()}


def _tool(command, env, message, binary=False):
    try:
        result = subprocess.run([str(x) for x in command], env=env,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                timeout=120, check=False)
    except (OSError, subprocess.TimeoutExpired):
        raise ValueError(message) from None
    if result.returncode:
        # Tool errors may contain paths, aliases or credential material.
        raise ValueError(message)
    return result.stdout if binary else result.stdout.decode('utf-8', errors='replace')


@contextmanager
def materialize(values, directory, root=ROOT):
    if Path(directory).resolve().is_relative_to(Path(root).resolve()):
        raise ValueError('Temporary upload keystore storage must remain outside the repository')
    value = values[PREFIX + 'KEYSTORE']
    temporary = None
    if value.startswith('base64:'):
        encoded = value.removeprefix('base64:')
        if len(encoded) > MAX_KEYSTORE_BYTES * 2:
            raise ValueError('Upload keystore exceeds 1 MiB')
        try:
            data = base64.b64decode(encoded, validate=True)
        except (ValueError, binascii.Error):
            raise ValueError('Invalid base64 upload keystore') from None
        if not data or len(data) > MAX_KEYSTORE_BYTES:
            raise ValueError('Upload keystore must contain 1 byte to 1 MiB')
        temporary = Path(directory) / 'upload.keystore'
        with temporary.open('xb') as stream:
            temporary.chmod(0o600)
            stream.write(data)
        key = temporary
    else:
        key = Path(value).expanduser().resolve()
        if key.is_relative_to(Path(root).resolve()):
            raise ValueError('Upload keystore must remain outside the repository')
        if not key.is_file() or not 0 < key.stat().st_size <= MAX_KEYSTORE_BYTES:
            raise ValueError('Upload keystore path is missing, empty or exceeds 1 MiB')
    try:
        yield key
    finally:
        if temporary:
            temporary.unlink(missing_ok=True)


def certificate(key, java, values):
    env = export_environment()
    env.update(values)
    data = _tool([java / 'bin/keytool', '-exportcert', '-keystore', key,
                  '-storepass:env', PREFIX + 'STORE_PASSWORD',
                  '-alias', values[PREFIX + 'ALIAS']], env,
                 'Upload keystore cannot be opened with the supplied alias and store password', binary=True)
    return hashlib.sha256(data).hexdigest()


def sign(source, target, key, java, values):
    if target.exists():
        raise ValueError('Refusing to replace an existing release bundle')
    env = export_environment()
    env.update(values)
    _tool([java / 'bin/jarsigner', '-keystore', key,
           '-storepass:env', PREFIX + 'STORE_PASSWORD',
           '-keypass:env', PREFIX + 'KEY_PASSWORD', '-digestalg', 'SHA-256',
           '-signedjar', target, source, values[PREFIX + 'ALIAS']], env,
          'Upload signing failed; check keystore, alias and passwords (tool output intentionally withheld)')


def verify(bundle, java, expected):
    if not re.fullmatch('[0-9a-fA-F]{64}', expected or ''):
        raise ValueError('Release verification requires the expected upload certificate SHA-256')
    output = _tool([java / 'bin/java', ROOT / 'scripts/android/VerifyBundle.java', bundle, expected.lower()],
                   export_environment(), 'Release signature verification failed (unsigned, modified, expired or wrong signer)')
    return json.loads(output)
