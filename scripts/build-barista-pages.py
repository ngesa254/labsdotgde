"""Build the GitHub Pages entry point from the canonical Barista HTML guide."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
LAB = Path('developers-day-nairobi-2026/01-ai-barista-cloud-run')
SOURCE = ROOT / LAB / 'BARISTA_CLOUD_RUN_ARCHITECTURE.html'
REPOSITORY = 'https://github.com/ngesa254/labsdotgde/blob/release/devfest_2026/'


def github_link(match):
    target = match.group(1)
    if target.startswith(('#', 'https://', 'http://', 'mailto:')):
        return match.group(0)
    relative = (ROOT / LAB / target).resolve().relative_to(ROOT)
    return f'href="{REPOSITORY}{relative.as_posix()}"'


page = re.sub(r'href="([^"]+)"', github_link, SOURCE.read_text())
output = ROOT / 'docs'
output.mkdir(exist_ok=True)
(output / 'index.html').write_text(page)
(output / '.nojekyll').touch()
print('Built docs/index.html from the canonical architecture guide.')
