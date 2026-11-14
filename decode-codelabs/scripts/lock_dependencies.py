"""Resolve installed distributions into per-lab exact-version closure locks.
Run only after intentionally reviewing/installing requirements.txt. No network calls.
"""
from importlib.metadata import distribution
from packaging.requirements import Requirement
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
for lab in sorted((ROOT/'labs').iterdir()):
    source=lab/'sample-code'
    pending=[Requirement(line) for line in (source/'requirements.txt').read_text().splitlines() if line and not line.startswith('#')]
    selected={}; extras={}; visited=set()
    while pending:
        req=pending.pop()
        key=req.name.lower().replace('_','-')
        extras.setdefault(key,set()).update(req.extras)
        signature=(key,tuple(sorted(extras[key])))
        if signature in visited: continue
        visited.add(signature)
        dist=distribution(req.name)
        if req.specifier and not req.specifier.contains(dist.version):
            raise ValueError(f'{req} does not match installed {dist.version}')
        selected[dist.metadata['Name']]=dist.version
        for line in dist.requires or []:
            dep=Requirement(line)
            if not dep.marker or any(dep.marker.evaluate({'extra':extra}) for extra in extras[key] | {''}):
                pending.append(dep)
    (source/'requirements.lock').write_text('# Exact installed dependency closure; CPython 3.11, macOS arm64 authoring host.\n# No hashes: re-resolve/retest deliberately for another platform.\n'+'\n'.join(f'{n}=={v}' for n,v in sorted(selected.items(),key=lambda pair:pair[0].lower()))+'\n')
    print(lab.name,len(selected),'locked distributions')
