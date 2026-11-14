#!/usr/bin/env python3
"""Export both authoritative Markdown sources with the pinned claat binary."""
from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess
import zipfile
ROOT=Path(__file__).resolve().parents[1]
CLAAT=Path(os.environ.get('CLAAT',ROOT/'.tools/claat')).resolve()
EXPECTED='3ba3eebec664076123626c2c77674f7779d5fc5647c53d180399183a3ba31695'
if not CLAAT.is_file(): raise SystemExit('Install claat first: python3 scripts/install_claat.py')
if hashlib.sha256(CLAAT.read_bytes()).hexdigest()!=EXPECTED:
    raise SystemExit('Unexpected claat binary; inspect scripts/install_claat.py and toolchain provenance.')
runtime=ROOT/'site/vendor/claat'
manifest=json.loads((runtime/'manifest.json').read_text())
for asset in manifest['assets']:
    file=runtime/asset['file']
    if not file.is_file() or hashlib.sha256(file.read_bytes()).hexdigest()!=asset['sha256']:
        raise SystemExit(f'Missing or changed vendored runtime asset: {file}')
subprocess.run(['python3',str(ROOT/'scripts/diagrams.py')],check=True)
for lab in sorted((ROOT/'labs').iterdir()):
    # v2.2.6 release binary ends metadata at the first blank paragraph.
    # Normalize metadata ONLY; preserve requested blank-separated editable sources.
    source=(lab/'codelab.md').read_text()
    metadata,body=source.split('\n# ',1)
    stage=ROOT/'.cache/export'/lab.name
    stage.mkdir(parents=True,exist_ok=True)
    shutil.copytree(lab/'assets',stage/'assets',dirs_exist_ok=True)
    md=stage/'codelab.md'
    md.write_text('\n'.join(line for line in metadata.splitlines() if line.strip())+'\n\n# '+body)
    subprocess.run([str(CLAAT),'export','-ga=','-o',str(ROOT/'site/codelabs'),str(md)],check=True,cwd=ROOT)
    id=next(line.split(': ',1)[1] for line in metadata.splitlines() if line.startswith('id:'))
    out=ROOT/'site/codelabs'/id
    shutil.copytree(lab/'assets',out/'assets',dirs_exist_ok=True)
    html=(out/'index.html').read_text()
    # Remove default global Analytics component after export (no personal tracking).
    import re
    html=re.sub(r'<google-codelab-analytics\b[^>]*>\s*</google-codelab-analytics>','',html)
    html=re.sub(r'<script src="//support.google.com/inapp/api.js"></script>', '', html)
    # Serve the original runtime/fonts locally; remote CSS can block script startup.
    html=re.sub(r'//fonts.googleapis.com/css\?[^\"]+', '../../vendor/claat/fonts.css', html)
    html=html.replace('//fonts.googleapis.com/icon?family=Material+Icons','../../vendor/claat/icons.css')
    html=html.replace('https://storage.googleapis.com/claat-public/','../../vendor/claat/')
    # Keep internal workshop navigation in the same tab.
    html=re.sub(r'(<a href="(?!https?:|mailto:)[^"]+") target="_blank"', r'\1', html)
    # Keep lab styling separate from the landing page trainer biography.
    html=html.replace('</head>','<link rel="stylesheet" href="../../codelab-overrides.css">\n</head>')
    html=html.replace('</body>', '<script src="../../codelab-navigation.js"></script>\n</body>')
    (out/'index.html').write_text(html)
    # Remove only unused renderer-owned image files inside this new output.
    used_images=set(re.findall(r'img/([^\"<> ]+)',html))
    for stale in (out/'img').glob('*'):
        if stale.is_file() and stale.name not in used_images:
            stale.unlink()
    data=json.loads((out/'codelab.json').read_text())
    # Generated provenance must not depend on this machine's absolute staging path.
    data['source']=str((lab/'codelab.md').relative_to(ROOT))
    (out/'codelab.json').write_text(json.dumps(data,indent=2)+'\n')
    downloads=ROOT/'site/downloads';downloads.mkdir(exist_ok=True)
    number='1' if lab.name.startswith('01') else '2'
    with zipfile.ZipFile(downloads/f'lab{number}.zip','w',zipfile.ZIP_DEFLATED) as archive:
        for file in sorted((lab/'sample-code').rglob('*')):
            if file.is_file() and '__pycache__' not in file.parts and '.venv' not in file.parts:
                info=zipfile.ZipInfo(str(file.relative_to(lab)),date_time=(2026,1,1,0,0,0))
                info.compress_type=zipfile.ZIP_DEFLATED
                archive.writestr(info,file.read_bytes())
print('Built site/index.html and both guided codelabs; no cloud actions.')
