"""Stage the public website for GitHub Pages without replacing other guides."""
from pathlib import Path
import hashlib
import shutil

WEBSITE = Path(__file__).resolve().parents[1]
SOURCE = WEBSITE / 'dist'
DESTINATION = WEBSITE.parent / 'docs/website'
if DESTINATION.is_symlink() or not DESTINATION.resolve().is_relative_to((WEBSITE.parent / 'docs').resolve()):
    raise SystemExit('Unsafe staging destination')
shutil.copytree(SOURCE, DESTINATION, dirs_exist_ok=True)
count = 0
for source in SOURCE.rglob('*'):
    if source.is_file():
        target = DESTINATION / source.relative_to(SOURCE)
        assert hashlib.sha256(source.read_bytes()).digest() == hashlib.sha256(target.read_bytes()).digest(), target
        count += 1
print(f'Staged and verified {count} files in docs/website/')
