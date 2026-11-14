"""Stage the workshop without replacing the existing GitHub Pages landing page."""
from pathlib import Path
import hashlib,json,shutil
ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT.parent/'docs/codelabs'
if DEST.is_symlink() or not DEST.resolve().is_relative_to((ROOT.parent/'docs').resolve()):
    raise SystemExit('Unsafe Pages staging destination')
shutil.copytree(ROOT/'site',DEST,dirs_exist_ok=True)
files={str(p.relative_to(ROOT/'site')):hashlib.sha256(p.read_bytes()).hexdigest()
       for p in (ROOT/'site').rglob('*') if p.is_file()}
for name,checksum in files.items():
    if hashlib.sha256((DEST/name).read_bytes()).hexdigest()!=checksum:
        raise SystemExit('Staged asset differs: '+name)
(ROOT/'evidence/pages-artifact.json').write_text(json.dumps({'destination':'docs/codelabs','file_count':len(files),'sha256':files},indent=2)+'\n')
print(f'Staged and verified {len(files)} identical files at docs/codelabs/')
