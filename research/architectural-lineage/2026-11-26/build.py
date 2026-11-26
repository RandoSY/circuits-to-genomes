"""Build three expanded photographic review editions from immutable baselines.
Run from repository root: python research/architectural-lineage/2026-11-26/build.py
Dependencies: pymupdf, reportlab, pillow; Linux DejaVu fonts.
"""
from pathlib import Path
import re, json, hashlib, urllib.request, time, io, html
import fitz
from PIL import Image as PIL
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

root=Path(__file__).resolve().parent
repo=root.parents[2]
raw=(root/'README.md').read_text()
photos=root/'photos'; photos.mkdir(exist_ok=True)
urls=[
('pdp8','https://upload.wikimedia.org/wikipedia/commons/6/6d/PDP-8.jpg'),
('h100','https://upload.wikimedia.org/wikipedia/commons/2/2f/NVIDIA_H100_%28%E6%9E%81%E5%AE%A2%E6%B9%BEGeekerwan%29_010.png'),
('system','https://upload.wikimedia.org/wikipedia/commons/d/d0/TSUBAME4.0_P5160984.jpg')]
for name,url in urls:
    dest=photos/(name+'.jpg')
    if not dest.exists():
        last=None
        for attempt in range(3):
            try:
                req=urllib.request.Request(url,headers={'User-Agent':'C2G scholarly figure archive (https://github.com/RandoSY/circuits-to-genomes)'})
                with urllib.request.urlopen(req,timeout=45) as r: data=r.read()
                im=PIL.open(io.BytesIO(data)).convert('RGB'); im.thumbnail((1800,1800)); im.save(dest,quality=94)
                break
            except Exception as e:
                last=e; time.sleep(5*(attempt+1))
        if not dest.exists(): raise RuntimeError(f'Photo download failed {url}: {last}')
for name,file in [('D','DejaVuSans.ttf'),('DB','DejaVuSans-Bold.ttf'),('DI','DejaVuSans-Oblique.ttf')]:
    pdfmetrics.registerFont(TTFont(name,'/usr/share/fonts/truetype/dejavu/'+file))
pdfmetrics.registerFontFamily('D',normal='D',bold='DB',italic='DI',boldItalic='DB')
ink=colors.HexColor('#24383e'); teal=colors.HexColor('#17695f')
style=lambda name,font,size,leading,**kw:ParagraphStyle(name,fontName=font,fontSize=size,leading=leading,textColor=ink,spaceAfter=8,**kw)
body=style('body','D',10.5,15)
head=style('head','DB',16,21,keepWithNext=True)
title=style('title','DB',22,27)
cap=style('caption','DI',8.4,12)
cell=style('cell','D',8.3,12)
ref=style('ref','D',8.4,12)
W=492
def clean(s):
    s=re.sub(r'\[([^\]]+)\]\((https?://[^ ]+)\)',r'\1 (\2)',s)
    return html.escape(s.replace('**','').strip('*'))
def para(s,st=body): return Paragraph(clean(s),st)
photo_caps=[
'Plate A. DEC PDP-8, National Museum of American History. Alkivar, public domain. Source: commons.wikimedia.org/wiki/File:PDP-8.jpg. Resized.',
'Plate B. NVIDIA H100 PCIe accelerator, Geekerwan (2023 video still), CC BY 3.0, creativecommons.org/licenses/by/3.0/. Source: Wikimedia Commons, File:NVIDIA H100 (极客湾Geekerwan) 010.png. Resized.',
'Plate C. Four NVIDIA H100 GPUs, TSUBAME 4.0 node. Fukumoto, 16 May 2026, CC BY-SA 4.0, creativecommons.org/licenses/by-sa/4.0/. Source: commons.wikimedia.org/wiki/File:TSUBAME4.0_P5160984.jpg. Resized.']
def plate(i):
    path=photos/(urls[i][0]+'.jpg')
    with PIL.open(path) as im: w,h=im.size
    scale=min(W/w,250/h)
    return KeepTogether([Image(str(path),width=w*scale,height=h*scale),Spacer(1,5),para(photo_caps[i],cap)])
sections=re.split(r'^## Paper [123] — ',raw,flags=re.M)
p1=sections[1].split('\n',1)[1]; p2=sections[2].split('\n',1)[1]; p3=sections[3].split('\n',1)[1].split('## Sources')[0]
sources=raw.split('## Sources\n',1)[1].split('## Release status')[0]
def content(text,photo_indices):
    story=[]; table=[]; pi=iter(photo_indices)
    def flush():
        if not table:return
        rows=[[para(x,cell) for x in row] for row in table]
        t=Table(rows,colWidths=[112,190,190],repeatRows=1,hAlign='LEFT')
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#dcebe6')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f0f5f4')]),('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,-1),(-1,-1),.5,teal)]))
        story.extend([t,Spacer(1,8)]);table.clear()
    for line in text.splitlines():
        line=line.strip()
        if line.startswith('|'):
            parts=[x.strip() for x in line.strip('|').split('|')]
            if not all(re.fullmatch(r'[-: ]+',x) for x in parts):table.append(parts)
            continue
        flush()
        if not line:continue
        if line.startswith('!['):story.append(plate(next(pi)));continue
        if line.startswith('*Plate '):continue
        if line.startswith('### '):story.append(para(line[4:],head));continue
        story.append(para(line))
    flush();return story
def page(c,d):
    c.setFont('D',8); c.setFillColor(teal);c.drawString(60,760,'C2G / DOCUMENTARY ARCHITECTURAL LINEAGE')
    c.setStrokeColor(teal);c.line(60,749,552,749);c.line(60,43,552,43)
    c.drawString(60,29,'26 November 2026 | Expanded review edition');c.drawRightString(552,29,str(d.page))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
specs=[
('01-architectural-economy','Architectural_Economy_v11.pdf','Architectural_Economy_v12_review.pdf','Architectural Economy','v12',p1,[0,1,2]),
('02-primate-enhancer-fem','Primate_Enhancer_FEM_v1.2.pdf','Primate_Enhancer_FEM_v1.3_review.pdf','Functional Equivalence Mapping','v1.3',p2,[]),
('03-augmented-investigator','The_Augmented_Investigator_v0.5.pdf','The_Augmented_Investigator_v0.6_review.pdf','The Augmented Investigator','v0.6',p3,[])]
manifest={'status':'expanded review editions; previous PDFs reproduced without textual modification; not integrated journal layouts','photos':{},'papers':[]}
for name,url in urls:manifest['photos'][name]={'sha256':sha(photos/(name+'.jpg')),'source':url}
for j,(folder,old,new,ttl,version,txt,indices) in enumerate(specs):
    directory=repo/'papers'/folder; baseline=directory/old; out=directory/new; insert=root/(version+'_insert.pdf')
    story=[para(ttl,title),para(version+' | Architectural lineage revision',head),para('Randall S. Young, Ed.S. | ORCID 0009-0003-1657-0243'),para('Expanded review edition. The following new editorial material precedes the complete preserved baseline; journal integration and independent review remain outstanding. No new empirical results are reported.')]
    story+=content(txt,indices)
    if j>0:story.append(plate(j))
    story.append(para('Technical sources',head));story.extend(para(line,ref) for line in sources.splitlines() if line.strip())
    SimpleDocTemplate(str(insert),pagesize=(612,792),leftMargin=60,rightMargin=60,topMargin=55,bottomMargin=56,title=ttl+' '+version,author='Randall S. Young').build(story,onFirstPage=page,onLaterPages=page)
    with fitz.open(insert) as add,fitz.open(baseline) as original,fitz.open() as result:
        n=len(add); m=len(original); result.insert_pdf(add);result.insert_pdf(original);result.set_metadata({'title':ttl+' '+version+' expanded review edition','author':'Randall S. Young'});result.save(out,garbage=4,deflate=True)
        with fitz.open(out) as check:
            assert len(check)==n+m
            for i in range(m):
                assert original[i].get_text()==check[n+i].get_text()
            # render all new pages, verify text exists and the expected images are embedded
            for i in range(n):
                assert check[i].get_text().strip()
                pix=check[i].get_pixmap(matrix=fitz.Matrix(.75,.75))
                assert pix.width>0 and pix.height>0
            count=sum(len(check[i].get_images()) for i in range(n))
            assert count >= (3 if j==0 else 1)
        manifest['papers'].append({'path':str(out.relative_to(repo)),'sha256':sha(out),'baseline':str(baseline.relative_to(repo)),'baseline_sha256':sha(baseline),'new_pages':n,'preserved_pages':m,'embedded_images':count})
    insert.unlink()
(root/'BUILD_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(manifest,indent=2))
