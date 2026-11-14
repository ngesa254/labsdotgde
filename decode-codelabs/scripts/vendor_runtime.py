"""Fetch official runtime/font assets for a deliberate, reviewed vendor update."""
from pathlib import Path
from urllib.request import urlopen
from concurrent.futures import ThreadPoolExecutor
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/'site/vendor/claat';DEST.mkdir(parents=True,exist_ok=True)
assets=[(name,'https://storage.googleapis.com/claat-public/'+name) for name in ['codelab-elements.css','native-shim.js','custom-elements.min.js','codelab-elements.js']]
assets += [
('prettify.js','https://raw.githubusercontent.com/google/code-prettify/master/src/prettify.js'),
('Roboto.ttf','https://raw.githubusercontent.com/google/fonts/main/ofl/roboto/Roboto%5Bwdth,wght%5D.ttf'),
('Roboto-Italic.ttf','https://raw.githubusercontent.com/google/fonts/main/ofl/roboto/Roboto-Italic%5Bwdth,wght%5D.ttf'),
('RobotoMono.ttf','https://raw.githubusercontent.com/google/fonts/main/ofl/robotomono/RobotoMono%5Bwght%5D.ttf'),
('SourceCodePro.ttf','https://raw.githubusercontent.com/google/fonts/main/ofl/sourcecodepro/SourceCodePro%5Bwght%5D.ttf'),
('MaterialIcons.ttf','https://raw.githubusercontent.com/google/material-design-icons/master/font/MaterialIcons-Regular.ttf')]
def fetch(item):
 name,url=item
 # Retain completed downloads across an interrupted initial vendor operation.
 file=DEST/name
 data=file.read_bytes() if file.exists() else urlopen(url,timeout=35).read()
 file.write_bytes(data)
 return {'file':name,'url':url,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)}
with ThreadPoolExecutor(max_workers=4) as pool:records=list(pool.map(fetch,assets))
fonts="""/* Local Google Fonts; upstream SIL Open Font License notices are alongside. */
@font-face{font-family:'Roboto';font-style:normal;font-weight:100 900;font-display:swap;src:url('Roboto.ttf') format('truetype')}
@font-face{font-family:'Roboto';font-style:italic;font-weight:100 900;font-display:swap;src:url('Roboto-Italic.ttf') format('truetype')}
@font-face{font-family:'Roboto Mono';font-style:normal;font-weight:100 700;font-display:swap;src:url('RobotoMono.ttf') format('truetype')}
@font-face{font-family:'Source Code Pro';font-style:normal;font-weight:200 900;font-display:swap;src:url('SourceCodePro.ttf') format('truetype')}
"""
icons="""/* Local Material Icons font; upstream Apache-2.0 notice is alongside. */
@font-face{font-family:'Material Icons';font-style:normal;font-weight:400;font-display:block;src:url('MaterialIcons.ttf') format('truetype')}
.material-icons{font-family:'Material Icons';font-weight:normal;font-style:normal;font-size:24px;line-height:1;letter-spacing:normal;text-transform:none;display:inline-block;white-space:nowrap;word-wrap:normal;direction:ltr;font-feature-settings:'liga';-webkit-font-smoothing:antialiased}
"""
for name,content in [('fonts.css',fonts),('icons.css',icons)]:
 (DEST/name).write_text(content)
 records.append({'file':name,'sha256':hashlib.sha256(content.encode()).hexdigest(),'note':'Local font-face declarations for upstream fonts'})
(DEST/'manifest.json').write_text(json.dumps({'retrieved':'2026-11-14','assets':records},indent=2)+'\n')
print('Vendored',len(records),'runtime/font assets inside site/vendor/claat')
