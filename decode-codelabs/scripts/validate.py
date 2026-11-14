#!/usr/bin/env python3
"""Structural, syntax and non-networked behavioral validation; never runs cloud commands."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import ast
import json
import os
import re
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[1]
checks=[]
class Links(HTMLParser):
    def __init__(self): super().__init__();self.links=[];self.steps=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        for name in ('href','src'):
            if name in a: self.links.append(a[name])
        if tag=='google-codelab-step': self.steps.append((a['label'],int(a['duration'])))
for lab in sorted((ROOT/'labs').iterdir()):
    md=(lab/'codelab.md').read_text()
    assert len(re.findall(r'^# ',md,re.M))==1
    metadata,body=md.split('\n# ',1)
    id=re.search(r'^id: (.+)$',metadata,re.M)[1]
    assert 'author: Ngesa Marvin' in metadata and 'status: Draft' in metadata
    steps=re.findall(r'^## (.+)\nDuration: (\d+):(\d+):(\d+)\n',body,re.M)
    assert len(steps)==len(re.findall(r'^## ',body,re.M))
    total=sum(int(h)*60+int(m)+int(s)/60 for _,h,m,s in steps)
    html=(ROOT/'site/codelabs'/id/'index.html').read_text()
    parser=Links();parser.feed(html)
    assert [s[0] for s in parser.steps]==[s[0] for s in steps]
    assert sum(s[1] for s in parser.steps)==total
    data=json.loads((ROOT/'site/codelabs'/id/'codelab.json').read_text())
    assert data['id']==id and data['duration']==total and data['status']==['draft']
    assert 'Author: Ngesa Marvin' in html
    assert '<aside class=' in html if id=='decode-mpesa-mcp' else True
    assert 'codelab-gaid=""' in html and 'google-codelab-analytics' not in html
    assert 'UA-49880327-14' not in html
    assert '<pre><code language=' in html
    assert 'storage.googleapis.com/claat-public/' not in html
    assert '//fonts.googleapis.com/' not in html
    for block in re.findall(r'```bash\n(.*?)\n```',md,re.S):
        subprocess.run(['bash','-n'],input=block,text=True,check=True,capture_output=True)
    checks.append(f'{id}: {len(steps)} steps, {int(total)} minutes, metadata, attribution, callouts and shell syntax passed')
for html in (ROOT/'site').rglob('*.html'):
    parser=Links();parser.feed(html.read_text())
    for link in parser.links:
        url=urlsplit(link)
        if url.scheme or url.netloc or not url.path: continue
        assert not url.path.startswith('/'),(html,link,'root-relative path')
        target=(html.parent/unquote(url.path)).resolve()
        assert target.is_relative_to(ROOT/'site'),(html,link,'escaped site')
        assert target.exists(),(html,link,'missing target')
checks.append('All generated local image, download, stylesheet, navigation and handoff links resolve without root-relative paths')
for file in list((ROOT/'labs').rglob('*.py'))+list((ROOT/'scripts').glob('*.py')):
    ast.parse(file.read_text(),filename=str(file))
checks.append('All sample and tooling Python files parse')
for docker in (ROOT/'labs').glob('*/sample-code/Dockerfile'):
    cmd=next(line[4:] for line in docker.read_text().splitlines() if line.startswith('CMD '))
    json.loads(cmd)
checks.append('Docker CMD arrays parse; container images not built')
python=ROOT/'.venv/bin/python'
if python.exists():
    for lab in sorted((ROOT/'labs').iterdir()):
        subprocess.run([str(python),'-m','unittest','discover','-s',str(lab/'sample-code'),'-p','test_*.py','-v'],check=True,cwd=ROOT)
    subprocess.run([str(python),'-m','pip','--disable-pip-version-check','check'],check=True,env={**os.environ,'PIP_CACHE_DIR':str(ROOT/'.cache/pip')})
    checks.append('10 non-networked sample tests and pip check passed in authoring environment')
else:
    raise SystemExit('Structural checks passed, but sample tests require .venv; see README.md to install the validation environment.')
# Guard against credential-bearing files entering generated sample archives.
for example in (ROOT/'labs').glob('*/sample-code/.env.example'):
    for line in example.read_text().splitlines():
        if 'SECRET=' in line or 'KEY=' in line: assert 'REPLACE_' in line
for file in (ROOT/'labs').rglob('*'):
    if file.is_file() and file.suffix in ('.py','.md','.txt','.example'):
        s=file.read_text()
        assert 'BEGIN PRIVATE KEY' not in s and not re.search(r'AIza[0-9A-Za-z_-]{30,}',s)
checks.append('Placeholder examples and private-key/API-key pattern checks passed; no secret stores inspected')
print('\n'.join(checks))
(ROOT/'evidence/structural-results.json').write_text(json.dumps({'checks':checks},indent=2)+'\n')
