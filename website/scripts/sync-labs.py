"""Refresh the local published lab copies without network access."""
from pathlib import Path
import runpy
import shutil

project = Path(__file__).resolve().parents[1]
shutil.copytree(project.parent / 'docs/codelabs', project / 'dist/codelabs', dirs_exist_ok=True)
runpy.run_path(str(project / 'scripts/render-barista.py'), run_name='__main__')
print('Local lab copies refreshed.')
