from pathlib import Path
import re, shutil, hashlib, json
from xml.sax.saxutils import escape
import fitz
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Polygon
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

root=Path(__file__).parent
source=root/'revisions.md'
text=source.read_text()
fontdir=Path('/usr/share/fonts/truetype/lato')
for n,fn in [('Lato','Lato-Regular.ttf'),('LatoBold','Lato-Bold.ttf'),('LatoItalic','Lato-Italic.ttf')]: pdfmetrics.registerFont(TTFont(n,str(fontdir/fn)))
ink=colors.HexColor('#18333d'); teal=colors.HexColor('#176b66'); pale=colors.HexColor('#e9f3f1'); muted=colors.HexColor('#4c636b'); rule=colors.HexColor('#cbd9d8'); amber=colors.HexColor('#a16a24'); gold=colors.HexColor('#f7eddd')
style={
 'title':ParagraphStyle('title',fontName='LatoBold',fontSize=23,leading=27,textColor=ink,spaceAfter=10),
 'sub':ParagraphStyle('sub',fontName='LatoBold',fontSize=12,leading=16,textColor=teal,spaceAfter=8),
 'meta':ParagraphStyle('meta',fontName='Lato',fontSize=9,leading=13,textColor=muted,spaceAfter=8),
 'h':ParagraphStyle('h',fontName='LatoBold',fontSize=14,leading=18,textColor=teal,spaceAfter=7,spaceBefore=9,keepWithNext=True),
 'p':ParagraphStyle('p',fontName='Lato',fontSize=10.4,leading=14.2,textColor=ink,spaceAfter=8),
 'caption':ParagraphStyle('caption',fontName='LatoItalic',fontSize=8.8,leading=11.5,textColor=muted,spaceAfter=8),
 'small':ParagraphStyle('small',fontName='Lato',fontSize=8.3,leading=11,textColor=muted,spaceAfter=4),
 'table':ParagraphStyle('table',fontName='Lato',fontSize=9.2,leading=12,textColor=ink),
 'th':ParagraphStyle('th',fontName='LatoBold',fontSize=9,leading=12,textColor=colors.white),
}
def para(s,st='p'):return Paragraph(escape(s),style[st])
def table(rows,widths):
 t=Table([[para(str(x),'th' if i==0 else 'table') for x in r] for i,r in enumerate(rows)],colWidths=widths,repeatRows=1,hAlign='LEFT')
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),teal),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,pale]),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),('LINEBELOW',(0,-1),(-1,-1),0.6,rule)]));return t

def diagram(kind):
 d=Drawing(504,134)
 def box(x,y,w,h,label,fill=pale):
  d.add(Rect(x,y,w,h,rx=4,ry=4,fillColor=fill,strokeColor=rule)); lines=label.split('|');
  for i,l in enumerate(lines):d.add(String(x+w/2,y+h/2+(len(lines)-1)*6-i*12-3,l,fontName='LatoBold',fontSize=10,textAnchor='middle',fillColor=ink))
 def arrow(x,y,X,Y):
  d.add(Line(x,y,X,Y,strokeColor=muted,strokeWidth=1.4));import math
  a=math.atan2(Y-y,X-x);d.add(Polygon([X,Y,X-7*math.cos(a-.5),Y-7*math.sin(a-.5),X-7*math.cos(a+.5),Y-7*math.sin(a+.5)],fillColor=muted,strokeColor=None))
 if kind=='return':
  box(0,80,148,44,'PDP-8|Architectural economy');box(178,80,148,44,'Genomes|Functional continuity');box(356,80,148,44,'Parallel computing|Hopper-inspired models');arrow(148,102,178,102);arrow(326,102,356,102)
  box(111,7,282,43,'New questions: dependency diversity,|coordination and verification');arrow(430,80,390,50);arrow(111,29,74,29);arrow(74,29,74,80)
 elif kind=='bio':
  for offset,label in [(0,'Shared dependency'),(264,'Diverse dependencies')]:
   d.add(String(offset+120,124,label,fontName='LatoBold',fontSize=11,textAnchor='middle',fillColor=teal))
   if offset==0:
    box(offset+81,86,78,25,'Factor A',gold);arrow(offset+120,86,offset+60,64);arrow(offset+120,86,offset+180,64)
   else:
    box(offset+21,86,78,25,'Factor A',gold);box(offset+141,86,78,25,'Factor B');arrow(offset+60,86,offset+60,64);arrow(offset+180,86,offset+180,64)
   box(offset+5,39,110,25,'Enhancer 1');box(offset+125,39,110,25,'Enhancer 2');arrow(offset+60,39,offset+120,25);arrow(offset+180,39,offset+120,25);box(offset+70,0,100,25,'Target output')
 else:
  box(0,90,145,35,'Shared source',gold);box(180,90,145,35,'AI / analyst A');box(359,90,145,35,'AI / analyst B');arrow(145,108,180,108);arrow(72,90,72,73);arrow(72,73,431,73);arrow(431,73,431,90)
  box(100,5,304,42,'Independent error-detection path|New data, separate implementation, specialist review');arrow(252,47,252,90);arrow(360,47,431,90)
 return d

papers=[
 dict(no=1,key='Architectural_Economy',old='v9',new='v10',baseline='Architectural_Economy_v9.pdf',path='papers/01-architectural-economy',title='Architectural Economy in Biological and Technological Systems',subtitle='From the PDP-8 to parallel computation and the regulatory genome',kind='return'),
 dict(no=2,key='Primate_Enhancer_FEM',old='v1.1',new='v1.2',baseline='Primate_Enhancer_FEM_v1.1.pdf',path='papers/02-primate-enhancer-fem',title='Functional Equivalence Mapping in Primate Enhancer Evolution',subtitle='A prospective extension: regulatory dependency diversity',kind='bio'),
 dict(no=3,key='The_Augmented_Investigator',old='v0.4',new='v0.5',baseline='The_Augmented_Investigator_v0.4.pdf',path='papers/03-augmented-investigator',title='The Augmented Investigator',subtitle='From circuits to genomes and back: independence of verification',kind='ai')]
sections=re.split(r'^## Paper \d+ — .*?\n',text,flags=re.M)[1:]
sections[-1]=sections[-1].split('## Shared evidence references')[0]
refs=[('H','H100 Boolean-dataflow laboratory v0.1','research/h100-lab/v0.1'),('M','Hopper-inspired matrix pilot v0.2','research/hopper-pilot/v0.2'),('C','C2G baseline manuscripts','papers')]
manifest=[]
for cfg,section in zip(papers,sections):
 n=cfg['no'];new=cfg['new'];old=cfg['old'];stem=cfg['key']+'_'+new
 supp=root/(stem+'_Revision.pdf'); out=root/(stem+'.pdf');base=root.parent/cfg['baseline']
 groups=re.split(r'^### (.+)\n',section.strip(),flags=re.M)[1:];groups=list(zip(groups[::2],groups[1::2]));story=[]
 story += [para('C2G  /  PAPER '+str(n)+'  /  EXPANDED REVIEW EDITION','meta'),para(cfg['title'],'title'),para(cfg['subtitle'],'sub'),para(f'Randall S. Young, Ed.S. | ORCID 0009-0003-1657-0243 | {new} | 26 November 2026 | Not peer reviewed','meta'),para(f'Revision pages R1 onward extend the complete {old} baseline reproduced after them with its original page numbers and figures. Read this updated synthesis first; it governs the interpretation of the preserved manuscript.','p')]
 for i,(heading,body) in enumerate(groups):
  # Page layout: put first summary on R1 with diagram; subsequent sections start at next page as needed.
  if i==1: story.append(PageBreak())
  if n==1 and i in (2,3):story.append(PageBreak())
  if n in (2,3) and i==2:story.append(PageBreak())
  story.append(para(heading,'h'))
  for paragraph in body.strip().split('\n\n'):story.append(para(paragraph.replace('\n',' ')))
  if i==0:
   story.append(diagram(cfg['kind']))
   story.append(para({1:'R-Figure 1. Reciprocal question and exploratory return direction; no demonstrated physical H100 result.',2:'R-Figure 1. Hypothetical alternative regulatory dependency topologies; not measured biological wiring.',3:'R-Figure 1. Shared sources can create correlated errors; independent pathways require explicit checking. Conceptual illustration, not empirical AI data.'}[n],'caption'))
  if n==1 and i==1:
   story.append(table([['Design','Nodes','Motif stuck-zero','All-site stuck-zero','All-site inversion'],['Dedicated','96.0','0.941','0.941','1.000'],['Shared','47.9','3.795','1.886','2.006'],['Modular','54.2','2.718','1.667','1.773'],['Buffered','89.6','0.108','1.008','2.395']],[100,70,110,112,112]));story.append(para('R-Table 1. K=32; rounded reported mean node counts and output blast from H100 lab v0.1 [H].','caption'))
  if n==1 and i==2:
   story.append(table([['Event','Shared parity','Separate stage','Separate root'],['Staged A corruption','8','0','0'],['Primary root corruption','64','64','0'],['Both roots corrupt','64','64','64'],['Shared B corruption','1','1','1'],['Opposing errors','2','2','2']],[174,110,110,110]));story.append(para('R-Table 2. Mean unflagged wrong outputs per named event [M]. Zero is detection, not necessarily correction. Selective duplication is discussed in the source results.','caption'))
 story.append(para('Evidence and reproducibility','h'))
 for k,label,p in refs:story.append(para(f'[{k}] {label}. https://github.com/RandoSY/circuits-to-genomes/tree/main/{p}','small'))
 if n==1:story.append(para('[A] Huang and Abraham (1984), Algorithm-Based Fault Tolerance for Matrix Operations. doi:10.1109/TC.1984.1676475 (from matrix pilot). [B] NVIDIA Hopper Tuning Guide: https://docs.nvidia.com/cuda/hopper-tuning-guide/','small'))
 story.append(para('AI-assisted revision; no new biological computation, actual H100 execution, comprehensive literature audit, or independent specialist validation. Author approval pending. Original empirical figures, data and references retained.','small'))
 def page(c,doc):
  c.setStrokeColor(rule);c.line(54,752,558,752);c.setFont('LatoBold',8);c.setFillColor(muted);c.drawString(54,764,f'C2G  /  PAPER {n}  /  {new.upper()} RESEARCH REVISION');c.line(54,40,558,40);c.setFont('Lato',8);c.drawString(54,27,'26 November 2026  |  Working manuscript  |  Not peer reviewed');c.drawRightString(558,27,'R'+str(doc.page))
 SimpleDocTemplate(str(supp),pagesize=(612,792),leftMargin=54,rightMargin=54,topMargin=54,bottomMargin=54,title=cfg['title']+' '+new+' revision',author='Randall S. Young').build(story,onFirstPage=page,onLaterPages=page)
 # Incremental merge: retain exact baseline bytes; append supplement objects and a revised page tree.
 shutil.copyfile(base,out)
 with fitz.open(out) as d,fitz.open(supp) as sd:
  num=len(sd);oldn=len(d); oldtoc=d.get_toc(); d.insert_pdf(sd,start_at=0)
  d.set_toc([[1,f'{new} revision: updated synthesis and new sections',1],[1,f'Preserved {old} baseline (original page numbers)',num+1]]+[[min(level+1,6),title,p+num] for level,title,p in oldtoc] if oldtoc else [[1,f'{new} revision: updated synthesis and new sections',1],[1,f'Preserved {old} baseline (original page numbers)',num+1]])
  m=d.metadata;m['title']=cfg['title']+' '+new+' (expanded review edition)';m['subject']='C2G coordinated revision, 26 November 2026';d.set_metadata(m);d.saveIncr()
 data=out.read_bytes();orig=base.read_bytes();assert data.startswith(orig)
 patch=root/(stem+'.pdf.delta');patch.write_bytes(data[len(orig):])
 with fitz.open(out) as d,fitz.open(base) as b:
  assert len(d)==num+len(b);assert all(d[i+num].get_text()==b[i].get_text() for i in range(len(b)))
  for i in range(num):
   p=d[i];pix=p.get_pixmap(matrix=fitz.Matrix(1.1,1.1));pix.save(str(root/f'qa_{n}_{i+1}.png'))
 def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
 manifest.append({**cfg,'new_pdf':out.name,'revision_pdf':supp.name,'delta':patch.name,'baseline_sha256':sha(base),'pdf_sha256':sha(out),'delta_sha256':sha(patch),'revision_sha256':sha(supp),'revision_pages':num,'baseline_pages':oldn,'total_pages':num+oldn,'pdf_bytes':out.stat().st_size,'delta_bytes':patch.stat().st_size})
 print(stem,'revision pages',num,'total',num+oldn,'delta',patch.stat().st_size,'full',out.stat().st_size)
(root/'RELEASE_MANIFEST.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
