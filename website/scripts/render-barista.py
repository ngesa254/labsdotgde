from pathlib import Path
import re, html, textwrap
PROJECT=Path(__file__).resolve().parents[1]
p=PROJECT/'dist/barista/index.html'
p.parent.mkdir(parents=True,exist_ok=True)
LAB=Path('developers-day-nairobi-2026/01-ai-barista-cloud-run')
s=(PROJECT.parent/LAB/'BARISTA_CLOUD_RUN_ARCHITECTURE.html').read_text()
def guide_link(match):
 target=match[1]
 if target.startswith(('#','https://','http://','mailto:')):return match[0]
 relative=(PROJECT.parent/LAB/target).resolve().relative_to(PROJECT.parent)
 return 'href="https://github.com/ngesa254/labsdotgde/blob/main/'+relative.as_posix()+'"'
s=re.sub(r'href="([^"]+)"',guide_link,s)
blocks=re.findall(r'<div class="mermaid">(.*?)</div>',s,re.S)
assert len(blocks)==4
assets=p.parent/'assets';assets.mkdir(exist_ok=True)
def esc(t):return html.escape(t,quote=True)
def text(x,y,lines,anchor='middle',size=14,color='#172b4d'):
 if isinstance(lines,str):lines=textwrap.wrap(lines,36) or ['']
 return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Arial,sans-serif" font-size="{size}" fill="{color}">'+''.join(f'<tspan x="{x}" dy="{0 if j==0 else 18}">{esc(t)}</tspan>' for j,t in enumerate(lines))+'</text>'
def base(w,h,title):return [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}"><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0 8 4 0 8Z" fill="#4285f4"/></marker></defs><rect width="100%" height="100%" fill="white"/>']
for i,encoded in enumerate(blocks,1):
 source=html.unescape(encoded)
 if source.startswith('sequenceDiagram'):
  participants={}
  edges=[]
  for line in source.splitlines():
   line=line.strip()
   m=re.match(r'(?:actor|participant) (\w+)(?: as (.*))?$',line)
   if m:participants[m[1]]=m[2] or m[1]
   m=re.match(r'(\w+)(--?>>)(\w+):\s*(.*)',line)
   if m:edges.append((m[1],m[3],m[4],m[2].startswith('--')))
  names=list(participants);w=max(1000,len(names)*190);height=150+len(edges)*86
  svg=base(w,height,'AI Barista chat and tool-call sequence')
  xs={name:100+j*(w-200)/(len(names)-1) for j,name in enumerate(names)}
  for name in names:
   x=xs[name];svg.append(f'<rect x="{x-82}" y="20" width="164" height="62" rx="8" fill="#e8f0fe" stroke="#4285f4"/>');svg.append(text(x,44,textwrap.wrap(participants[name],20)));svg.append(f'<path d="M{x} 82V{height-20}" stroke="#cbd5e1" stroke-dasharray="5 5"/>')
  for j,(a,b,label,dashed) in enumerate(edges):
   y=130+j*86;x1,x2=xs[a],xs[b]
   svg.append(f'<path d="M{x1} {y}H{x2}" stroke="#4285f4" fill="none" stroke-width="1.7" marker-end="url(#arrow)"'+(' stroke-dasharray="5 4"' if dashed else '')+'/>')
   lines=textwrap.wrap(label,max(22,int(abs(x2-x1)/8)))
   svg.append(text((x1+x2)/2,y-14-18*(len(lines)-1),lines,size=12))
  assert len(edges)==12,len(edges)
 else:
  labels={};edges=[]
  for line in source.splitlines():
   line=line.strip()
   if line.startswith(('subgraph','style','flowchart')):continue
   m=re.match(r'(\w+)\[\(?"([^"]+)"\)?\]',line)
   if m:labels[m[1]]=m[2]
   if '-->' in line or '-.->' in line:
    # Remove quoted edge labels before splitting chained links.
    parts=re.split(r'(-->|-\.->)(?:\|"([^"]*)"\|)?',line)
    previous=parts[0].strip()
    for k in range(1,len(parts),3):
     arrow,label,target=parts[k:k+3];target=target.strip();edges.append((previous,target,label or '',arrow=='-.->'));previous=target
  assert edges and all(a in labels and b in labels for a,b,_,_ in edges),(labels,edges)
  height=40+len(edges)*100;svg=base(1100,height,'AI Barista component relationships')
  for j,(a,b,label,dashed) in enumerate(edges):
   y=20+j*100
   for x,name in [(20,a),(730,b)]:
    svg.append(f'<rect x="{x}" y="{y}" width="350" height="76" rx="8" fill="#eef5ff" stroke="#4285f4"/>')
    lines=textwrap.wrap(labels[name],35);svg.append(text(x+175,y+32-(len(lines)-1)*8,lines))
   svg.append(f'<path d="M370 {y+52}H725" fill="none" stroke="#4285f4" stroke-width="1.8" marker-end="url(#arrow)"'+(' stroke-dasharray="5 4"' if dashed else '')+'/>')
   if label:svg.append(text(550,y+20,textwrap.wrap(label,36),size=12,color='#475569'))
 svg.append('</svg>');(assets/f'diagram-{i}.svg').write_text(''.join(svg))
 replacement=f'<div class="mermaid" data-processed="true"><img src="assets/diagram-{i}.svg" alt="'+['Serverless agent component relationships','Chat and tool-call sequence','Firestore vector retrieval relationships','Build and deployment relationships'][i-1]+'" style="display:block;width:100%;min-width:760px;height:auto"></div>'
 s=s.replace('<div class="mermaid">'+encoded+'</div>',replacement,1)
# Keep the original expand/print/navigation script, removing only remote rendering.
a=s.index('try {\n  const {default: mermaid}')
s=s[:a]+s[s.index('</script>',a):]
p.write_text(s)
import shutil
shutil.copytree(p.parent, PROJECT/'dist/decode', dirs_exist_ok=True)
print('Rendered all four diagrams locally; editable source and guide content retained.')
