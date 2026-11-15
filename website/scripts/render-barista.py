"""Copy the original interactive Mermaid guide without altering diagrams."""
from pathlib import Path
import re

PROJECT = Path(__file__).resolve().parents[1]
LAB = Path('developers-day-nairobi-2026/01-ai-barista-cloud-run')
source = (PROJECT.parent / LAB / 'BARISTA_CLOUD_RUN_ARCHITECTURE.html').read_text()

def guide_link(match):
    target = match[1]
    if target.startswith(('#', 'https://', 'http://', 'mailto:')):
        return match[0]
    relative = (PROJECT.parent / LAB / target).resolve().relative_to(PROJECT.parent)
    return 'href="https://github.com/ngesa254/labsdotgde/blob/main/' + relative.as_posix() + '"'

page = re.sub(r'href="([^"]+)"', guide_link, source)
assert page.count('class="mermaid"') == 4
assert 'await mermaid.run' in page
for entry in ['barista', 'decode']:
    output = PROJECT / 'dist' / entry / 'index.html'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(page)
print('Copied original four Mermaid diagrams and interactive renderer unchanged.')
