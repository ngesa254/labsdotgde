#!/usr/bin/env python3
"""Install the exact tested official release asset locally; never installs globally."""
from pathlib import Path
import hashlib
import platform
import urllib.request
ROOT=Path(__file__).resolve().parents[1]
SHA='3ba3eebec664076123626c2c77674f7779d5fc5647c53d180399183a3ba31695'
URL='https://github.com/googlecodelabs/tools/releases/download/v2.2.6/claat-darwin-amd64'
if platform.system()!='Darwin':
    raise SystemExit('This installer pins the tested macOS release asset. See TOOLCHAIN.md for other hosts.')
target=ROOT/'.tools/claat'
target.parent.mkdir(parents=True,exist_ok=True)
if not target.exists():
    content=urllib.request.urlopen(URL,timeout=60).read()
    if hashlib.sha256(content).hexdigest()!=SHA: raise SystemExit('Downloaded claat checksum mismatch.')
    target.write_bytes(content)
if hashlib.sha256(target.read_bytes()).hexdigest()!=SHA: raise SystemExit('Existing claat checksum mismatch.')
target.chmod(0o755)
print('Verified project-local claat v2.2.6 release asset. Apple Silicon requires x86 compatibility support.')
