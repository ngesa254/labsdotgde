"""Publish the homepage at the Pages root, retaining historical entry points."""
from pathlib import Path
import hashlib
import runpy
import shutil

WEBSITE = Path(__file__).resolve().parents[1]
SOURCE = WEBSITE / 'dist'
DOCS = WEBSITE.parent / 'docs'
runpy.run_path(str(WEBSITE / 'scripts/render-barista.py'), run_name='__main__')
# Root is the main site; /website remains an alias for existing shared links.
for destination in [DOCS, DOCS / 'website']:
    if destination.is_symlink():
        raise SystemExit('Unsafe staging destination')
    shutil.copytree(SOURCE, destination, dirs_exist_ok=True)
    count = 0
    for source in SOURCE.rglob('*'):
        if source.is_file():
            target = destination / source.relative_to(SOURCE)
            assert hashlib.sha256(source.read_bytes()).digest() == hashlib.sha256(target.read_bytes()).digest(), target
            count += 1
    print(f'Staged and verified {count} files in {destination.relative_to(WEBSITE.parent)}')
(DOCS / '.nojekyll').touch()
