"""Generate the dedicated lab catalogue from website/labs.json."""
from pathlib import Path
import html
import json

ROOT = Path(__file__).resolve().parents[1]
labs = json.loads((ROOT / 'labs.json').read_text())
escape = html.escape
assert len({lab['id'] for lab in labs}) == len(labs), 'Duplicate lab IDs'
cards = []
for index, lab in enumerate(labs, 1):
    tags = ''.join('<li>' + escape(tag) + '</li>' for tag in lab['tags'])
    cards.append(f'''<article class="lab-card" id="{escape(lab['id'])}" data-tags="{escape('|'.join(lab['tags']))}">
<span class="lab-card__number mono">{index:02} · {escape(lab['track'])}</span>
<h2>{escape(lab['title'])}</h2><p>{escape(lab['description'])}</p>
<ul class="lab-tags" aria-label="Technologies">{tags}</ul>
<a href="{escape(lab['href'])}">{escape(lab['label'])}</a></article>''')
options = ''.join(f'<option value="{escape(tag)}">{escape(tag)}</option>' for tag in sorted({tag for lab in labs for tag in lab['tags']}))
page = '''<!doctype html>
<html lang="en" data-theme="light"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Browse hands-on labs in AI, agents, MCP, and Google Cloud from LabsDotGDE.">
<title>Labs · labsdotgde.afrika</title><link rel="icon" href="../assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="../assets/fonts.css"><link rel="stylesheet" href="../styles.css">
<link rel="stylesheet" href="../assets/labs-catalogue.css"><script type="module" src="../assets/labs-catalogue.js"></script></head>
<body class="catalogue-page"><a class="catalogue-skip" href="#catalogue">Skip to labs</a>
<header class="catalogue-header"><div class="catalogue-wrap"><a class="wordmark mono" href="../index.html">labsdotgde<span class="wordmark__dot">.</span>afrika</a>
<nav aria-label="Main navigation"><a href="../index.html">← Home</a><a href="../index.html#invite">Request a Lab</a></nav></div></header>
<main class="catalogue-wrap" id="catalogue"><div class="catalogue-intro"><p class="section-eyebrow mono">PICK A STARTING POINT</p>
<h1>Start. Build. Grow.</h1><p>Practical guides for engineers who learn by building. Find your next lab, follow the steps, and get your hands on the code.</p></div>
<form class="catalogue-filters" role="search" onsubmit="return false"><div><label for="lab-search">Find a lab</label><input id="lab-search" type="search" placeholder="Search topics, tools, or workshops" autocomplete="off"></div>
<div><label for="lab-topic">Technology</label><select id="lab-topic"><option value="">All technologies</option>OPTIONS</select></div><button type="button" id="clear-filters">Clear filters</button></form>
<p id="lab-count" class="mono catalogue-count" role="status" aria-live="polite">COUNT labs</p>
<div class="lab-grid">CARDS</div><p id="lab-empty" hidden>No matching labs. Try another topic or clear the filters.</p>
<div class="labs-bottom"><a href="../codelabs/index.html">Browse the DECODE workshop →</a><a href="https://github.com/ngesa254/labsdotgde" target="_blank" rel="noopener noreferrer">Explore the full lab repository ↗</a></div>
</main><footer class="catalogue-footer catalogue-wrap"><a href="../index.html">← Back to labsdotgde.afrika</a><span>Build. Learn. Share.</span></footer></body></html>
'''
page = page.replace('OPTIONS', options).replace('COUNT labs', str(len(labs)) + ' labs').replace('CARDS', '\n'.join(cards))
output = ROOT / 'dist/labs/index.html'
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(page)
print(f'Built catalogue with {len(labs)} labs from website/labs.json')
