"""Build the paper-grid lab catalogue from website/labs.json."""
from pathlib import Path
import html
import json

ROOT = Path(__file__).resolve().parents[1]
labs = json.loads((ROOT / 'labs.json').read_text())
e = html.escape
assert len({lab['id'] for lab in labs}) == len(labs), 'Duplicate lab IDs'

def card(lab, index):
    external = lab.get('source') == 'google-gear'
    tags = ''.join('<li>' + e(tag) + '</li>' for tag in lab['tags'])
    attributes = ' target="_blank" rel="noopener noreferrer"' if external else ''
    kind = '{Google codelab}' if external else ('{Architecture guide}' if lab['id'] == 'ai-barista' else '{Codelab}')
    return f'''<article class="lab-card" id="{e(lab['id'])}" data-tags="{e('|'.join(lab['tags']))}">
<div class="lab-card__top"><span class="lab-card__kind mono">{kind}</span><span class="lab-card__number mono">{index:02}</span></div>
<p class="lab-card__track mono">{e(lab['track'])}</p>
<h3>{e(lab['title'])}</h3><p class="lab-card__description">{e(lab['description'])}</p>
<ul class="lab-tags" aria-label="Technologies">{tags}</ul>
<a class="lab-card__open" href="{e(lab['href'])}"{attributes} aria-label="{e(lab['label'])}: {e(lab['title'])}"><span class="lab-card__arrow" aria-hidden="true">{'↗' if external else '→'}</span><span>{e(lab['label']).rstrip('→↗ ').strip()}</span></a></article>'''

def panel(id, title, description, items, theme, note):
    cards = '\n'.join(card(lab, index) for index, lab in enumerate(items, 1))
    plain_title = title.replace('<br>', ' ')
    title = title.replace('<br>', '<br> ')
    return f'''<section class="guide-panel guide-panel--{theme}" data-guide-panel aria-labelledby="{id}-title">
<div class="guide-ticker mono" aria-hidden="true"><span>// — codelabs &nbsp; * &nbsp; code samples &nbsp; * &nbsp; tutorials — // &nbsp; — codelabs &nbsp; * &nbsp; code samples &nbsp; * &nbsp; tutorials — // &nbsp; — codelabs &nbsp; * &nbsp; code samples &nbsp; * &nbsp; tutorials — //</span></div>
<div class="guide-body"><div class="guide-intro"><div><p class="guide-eyebrow mono">{'FROM GOOGLE GEAR' if theme == 'violet' else 'BUILT AT LABSDOTGDE'}</p><h2 id="{id}-title"><span>{title}</span></h2><p class="guide-description">{description}</p><p class="guide-source">{note}</p></div>
<div class="guide-navigation"><div class="guide-controls" hidden><button type="button" data-direction="-1" aria-label="Previous {id} guides" aria-controls="{id}-track">←</button><button type="button" data-direction="1" aria-label="Next {id} guides" aria-controls="{id}-track">→</button></div><span class="guide-count mono">{len(items)} guides</span></div></div>
<div class="guide-viewport" id="{id}-track" tabindex="0" role="region" aria-label="{e(plain_title)} cards"><div class="lab-grid">{cards}</div></div></div></section>'''

local = [lab for lab in labs if lab.get('source') != 'google-gear']
google = [lab for lab in labs if lab.get('source') == 'google-gear']
assert local and google
panels = panel('workshop', 'Start.<br>Build. Grow.', 'Our hands-on workshops. Build the tool layer, connect an agent, or trace a request from question to answer.', local, 'paper', 'Start with DECODE Lab 1, then continue to Lab 2. The Barista guide is a separate starting point.')
panels += panel('google', 'Step-by-step<br>guides', 'Keep building with official Google codelabs covering agents, tools, evaluation, and deployment.', google, 'violet', 'External resources curated from <a href="https://developers.google.com/program/gear/" target="_blank" rel="noopener noreferrer">Google GEAR ↗</a>. These guides open on Google’s sites.')
options = ''.join(f'<option value="{e(tag)}">{e(tag)}</option>' for tag in sorted({tag for lab in labs for tag in lab['tags']}))
page = '''<!doctype html>
<html lang="en" data-theme="light"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Hands-on LabsDotGDE workshops and official Google GEAR codelabs in agents, MCP, and cloud engineering.">
<title>Labs · labsdotgde.afrika</title><link rel="icon" href="../assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="../assets/fonts.css"><link rel="stylesheet" href="../styles.css"><link rel="stylesheet" href="../assets/labs-catalogue.css">
<script type="module" src="../assets/labs-catalogue.js"></script></head>
<body class="catalogue-page"><a class="catalogue-skip" href="#catalogue">Skip to labs</a>
<header class="catalogue-header"><div class="catalogue-wrap"><a class="wordmark mono" href="../index.html">labsdotgde<span class="wordmark__dot">.</span>afrika</a>
<nav aria-label="Main navigation"><a href="../index.html">← Home</a><a href="../index.html#invite">Request a Lab ↗</a></nav></div></header>
<main class="catalogue-wrap" id="catalogue"><div class="catalogue-intro"><div><p class="section-eyebrow mono">THE ENGINEER’S WORKBENCH</p><h1>Less watching.<br><span>More building.</span></h1></div><p>Pick a guide. Open your terminal. Leave with something you can run.<br><a href="#workshop-title">Our workshops ↓</a> <a href="#google-title">Google GEAR guides ↓</a></p></div>
<form class="catalogue-filters" role="search"><div><label for="lab-search">Find your next lab</label><input id="lab-search" type="search" placeholder="Try MCP, agents, or Cloud Run" autocomplete="off"></div>
<div><label for="lab-topic">Technology</label><select id="lab-topic"><option value="">All technologies</option>OPTIONS</select></div><button type="button" id="clear-filters">Clear filters ↺</button></form>
<p id="lab-count" class="mono catalogue-count" role="status" aria-live="polite">COUNT guides</p>
PANELS
<p id="lab-empty" hidden>No guides match those filters. Try another topic or clear the filters.</p>
<div class="labs-bottom"><a href="../codelabs/index.html">Browse the DECODE workshop →</a><a href="https://github.com/ngesa254/labsdotgde" target="_blank" rel="noopener noreferrer">Explore the full lab repository ↗</a></div>
</main><footer class="catalogue-footer catalogue-wrap"><a href="../index.html">← Back to labsdotgde.afrika</a><span>Build. Learn. Share.</span></footer></body></html>
'''
page = page.replace('OPTIONS', options).replace('COUNT guides', str(len(labs)) + ' guides').replace('PANELS', panels)
output = ROOT / 'dist/labs/index.html'
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(page)
print(f'Built catalogue: {len(local)} local labs and {len(google)} official Google guides')
