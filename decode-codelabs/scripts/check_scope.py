"""Compare all pre-existing repository file hashes without modifying Git state."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT.parent
parser=argparse.ArgumentParser()
parser.add_argument('--publication',action='store_true',help='Allow authorized docs/codelabs output and commits')
args=parser.parse_args()
before=json.loads((ROOT/'evidence/initial-state.json').read_text())
def check(item):
    name,expected=item;p=REPO/name
    if not p.is_file():return name+' (missing)'
    return name if hashlib.sha256(p.read_bytes()).hexdigest()!=expected else None
with ThreadPoolExecutor(max_workers=8) as pool:
    changed=[v for v in pool.map(check,before['sha256'].items()) if v]
new=[]
for p in REPO.rglob('*'):
    if '.git' in p.parts or p.is_relative_to(ROOT):continue
    if args.publication and p.is_relative_to(REPO/'docs/codelabs'):continue
    if p.is_file() and str(p.relative_to(REPO)) not in before['sha256']:new.append(str(p.relative_to(REPO)))
branch=subprocess.check_output(['git','-C',str(REPO),'branch','--show-current'],text=True).strip()
commit=subprocess.check_output(['git','-C',str(REPO),'rev-parse','HEAD'],text=True).strip()
result={'pre_existing_files_checked':len(before['sha256']),'changed_outside_destination':changed,
        'new_outside_destination':new,'branch_unchanged':branch==before['branch'],
        'commit_unchanged':commit==before['commit'],
        'publication_scope':args.publication,
        'git_status':subprocess.check_output(['git','-C',str(REPO),'status','--short'],text=True)}
(ROOT/'evidence/scope-results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
assert not changed and not new and result['branch_unchanged'] and (args.publication or result['commit_unchanged'])
