"""Build the integrated v11 from manuscript.json and exact original v9 PDF.
Usage: python build.py --baseline /path/to/Architectural_Economy_v9.pdf --out /path/to/Architectural_Economy_v11.pdf
Requires PyMuPDF 1.26.7, ReportLab 4.4.9, DejaVu fonts.
"""
from pathlib import Path
import argparse, hashlib, json, re, io, html
import fitz
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, KeepTogether, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Polygon
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfgen.canvas import Canvas
P=argparse.ArgumentParser();P.add_argument('--baseline',type=Path,required=True);P.add_argument('--out',type=Path,required=True);a=P.parse_args()
assert hashlib.sha256(a.baseline.read_bytes()).hexdigest()=='97b2c18c34629a9f63f264126deb90da62cfc33042b46b92a73ad8138fe1d4d9','Wrong v9 baseline'
root=Path(__file__).resolve().parent; items=json.loads((root/'manuscript.json').read_text()); base=fitz.open(a.baseline)
for name,file in [('D','DejaVuSans.ttf'),('DB','DejaVuSans-Bold.ttf'),('DI','DejaVuSans-Oblique.ttf')]:pdfmetrics.registerFont(TTFont(name,'/usr/share/fonts/truetype/dejavu/'+file))
pdfmetrics.registerFontFamily('D',normal='D',bold='DB',italic='DI',boldItalic='DB')
ink=colors.HexColor('#24383e'); teal=colors.HexColor('#17695f'); blue=colors.HexColor('#376d91'); muted=colors.HexColor('#53666a'); line=colors.HexColor('#c7d3d4'); light=colors.HexColor('#edf4f2'); bluelt=colors.HexColor('#e7eff6'); gold=colors.HexColor('#a97737'); goldlt=colors.HexColor('#f7eee0'); grey=colors.HexColor('#edf0f2')
W=492
styles={
'body':ParagraphStyle('body',fontName='D',fontSize=10.35,leading=14.7,textColor=ink,spaceAfter=7.0,allowWidows=0,allowOrphans=0),
'h':ParagraphStyle('h',fontName='DB',fontSize=17,leading=21,textColor=teal,spaceBefore=7,spaceAfter=12,keepWithNext=True),
'sub':ParagraphStyle('sub',fontName='DB',fontSize=11.8,leading=15,textColor=blue,spaceBefore=9,spaceAfter=6,keepWithNext=True),
'cap':ParagraphStyle('cap',fontName='D',fontSize=8.8,leading=12,textColor=muted,spaceAfter=7),
'ref':ParagraphStyle('ref',fontName='D',fontSize=8.7,leading=11.8,textColor=ink,spaceAfter=5,wordWrap='LTR'),
'cell':ParagraphStyle('cell',fontName='D',fontSize=8.2,leading=10.8,textColor=ink),
'header':ParagraphStyle('header',fontName='DB',fontSize=8.2,leading=10.8,textColor=colors.white),
'meta':ParagraphStyle('meta',fontName='D',fontSize=9,leading=12.5,textColor=muted,spaceAfter=5),
}
def para(s,k='body'):return Paragraph(html.escape(s),styles[k])
def box(d,x,y,w,h,fill,stroke=teal):d.add(Rect(x,y,w,h,rx=4,ry=4,fillColor=fill,strokeColor=stroke,strokeWidth=.7))
def label(d,x,y,s,size=10,col=ink,b=False,anchor='middle'):d.add(String(x,y,s,fontName='DB' if b else 'D',fontSize=size,fillColor=col,textAnchor=anchor))
def arr(d,x,y,X,Y,color=muted,dash=None):
 import math
 d.add(Line(x,y,X,Y,strokeColor=color,strokeWidth=1.2,strokeDashArray=dash)); q=math.atan2(Y-y,X-x);d.add(Polygon([X,Y,X-7*math.cos(q-.45),Y-7*math.sin(q-.45),X-7*math.cos(q+.45),Y-7*math.sin(q+.45)],fillColor=color,strokeColor=color))
def graphic(kind):
 if kind=='hopper':
  d=Drawing(W,194);box(d,47,158,398,29,light);label(d,246,169,'Kernel grid / work distribution',12,b=True)
  for i in range(3):
   x=12+160*i;arr(d,246,158,x+74,144);box(d,x,54,148,89,bluelt,blue);label(d,x+74,130,'Thread-block cluster',9.5,blue,True)
   for j in range(2):
    xx=x+7+70*j;box(d,xx,67,64,49,colors.white,blue);label(d,xx+32,102,'SM',10,b=True);label(d,xx+32,88,'Compute',8);label(d,xx+32,76,'Local memory',7.3)
   label(d,x+74,58,'Cluster-local exchange',7.8,blue)
   arr(d,x+74,54,x+74,40)
  box(d,12,21,468,19,grey,muted);label(d,246,27,'Shared cache / data transfer / interconnect',9,b=True)
  box(d,12,0,468,15,goldlt,gold);label(d,246,4,'Global memory (HBM)',8.5,b=True)
  return d
 if kind in ['boolean','matrix']:
  boolean=kind=='boolean'; names=['Dedicated','Shared','Modular','Buffered'] if boolean else ['Staged primary','Primary root','Both roots'];series=[('Stuck-zero',[.941,1.886,1.667,1.008],teal),('Inversion',[1,2.006,1.773,2.395],blue)] if boolean else [('Shared parity',[8,64,64],gold),('Separate stage',[0,64,64],blue),('Separate root',[0,0,64],teal)]
  d=Drawing(W,199);maxv=3 if boolean else 64; x0=126;barw=315; y=160; group=34 if boolean else 49
  for i,n in enumerate(names):
   label(d,117,y-7,n,9,anchor='end');
   for j,(_,vals,c) in enumerate(series):
    v=vals[i]; yy=y-13*j;d.add(Rect(x0,yy-9,v/maxv*barw,10,fillColor=c,strokeColor=None));label(d,x0+v/maxv*barw+4,yy-7, f'{v:.3f}' if boolean else str(v),8,c,True,'start')
   y-=group
  for j,(n,_,c) in enumerate(series):d.add(Rect(17+157*j,12,12,9,fillColor=c,strokeColor=None));label(d,34+157*j,13,n,8.5,anchor='start')
  label(d,0,187,'Mean output disruption' if boolean else 'Incorrect outputs outside flagged scope',10,muted,True,'start');return d
 d=Drawing(W,162);box(d,8,103,145,50,bluelt,blue);label(d,80,133,'PDP-8',12,blue,True);label(d,80,117,'Interface continuity',9);box(d,173,103,145,50,light,teal);label(d,245,133,'Regulatory genome',11,teal,True);label(d,245,117,'Compensation',9);box(d,338,103,145,50,bluelt,blue);label(d,410,133,'Parallel computing',11,blue,True);label(d,410,117,'Protective dependencies',8.8);arr(d,153,129,173,129,blue);arr(d,318,129,338,129,teal,[3,2]);box(d,98,24,296,36,goldlt,gold);label(d,246,46,'Shared analytical framework',11,b=True);label(d,246,32,'Economy • liability • robustness • continuity',9);arr(d,410,103,385,60,blue);arr(d,98,42,80,103,blue);label(d,246,8,'Dashed arrow = prospective engineering transfer',8.5,muted);return d
story=[]
story.append(Paragraph('Architectural Economy in<br/>Biological and Technological Systems',ParagraphStyle('title',fontName='DB',fontSize=22,leading=26,textColor=ink,spaceAfter=12)))
story.append(Paragraph('From the PDP-8 to Modern AI Accelerators and the Regulatory Genome: Economy, Coordination, Robustness and Functional Continuity',ParagraphStyle('subtitle',fontName='D',fontSize=12,leading=16,textColor=teal,spaceAfter=10)))
for t in ['Randall S. Young, Ed.S. | Independent Researcher, Indiana, USA','ORCID: https://orcid.org/0009-0003-1657-0243','Version 11.0 • 26 November 2026 • Integrated review manuscript • Not peer reviewed','Research archive: https://github.com/RandoSY/circuits-to-genomes']:story.append(para(t,'meta'))
story.append(Spacer(1,9));story.append(para('Abstract','sub'))
refs=False
for idx,item in enumerate(items):
 k=item['type'];t=item.get('text','')
 if k=='h':
  if t=='References':refs=True
  
  # References flow naturally after declarations.
  story.append(para(t,'h'))
 elif k=='sub':story.append(para(t,'sub'))
 elif k=='p':
  is_heading=not refs and (re.match(r'^(4\.\d |7\.4\.\d )',t) or t in ['Conservation-free predictor definitions','Global and within-target-gene statistical specifications','Leakage-free nested validation ladder','Cohort construction and coordinate mapping','Empirical estimates and sensitivity analysis','Scale-specific buffering','Compensation and interaction-dependent continuity'])
  story.append(para(t,'ref' if refs else 'sub' if is_heading else 'body'))
 elif k=='crop':
  clip=fitz.Rect(item['rect']);pix=base[item['page']-1].get_pixmap(matrix=fitz.Matrix(2,2),clip=clip,alpha=False);img=Image(io.BytesIO(pix.tobytes('png')),width=W,height=W*clip.height/clip.width)
  cap=item.get('caption','');is_table=cap.startswith('Table');seq=[para(cap,'cap'),img] if is_table else [img]+([para(cap,'cap')] if cap else []);story.append(KeepTogether(seq));story.append(Spacer(1,6))
 elif k=='table':
  rows=[[para(x,'header') for x in item['headers']]]+[[para(x,'cell') for x in row] for row in item['rows']];tab=Table(rows,colWidths=item['widths'],repeatRows=1,hAlign='LEFT');tab.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),teal),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,light]),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),('LINEBELOW',(0,0),(-1,0),.7,teal),('LINEBELOW',(0,-1),(-1,-1),.5,line)]));story.append(KeepTogether([para(item['caption'],'cap'),tab]));story.append(Spacer(1,10))
 elif k=='diagram':story.append(KeepTogether([graphic(item['kind']),Spacer(1,4),para(item['caption'],'cap')]));story.append(Spacer(1,5))
class StableCanvas(Canvas):
 def __init__(self,*args,**kwargs):kwargs['invariant']=1;super().__init__(*args,**kwargs)
def page(c,d):
 c.setStrokeColor(line);c.line(60,750,552,750);c.setFont('D',8);c.setFillColor(muted);c.drawString(60,760,'ARCHITECTURAL ECONOMY / INTEGRATED REVIEW');c.line(60,43,552,43);c.drawString(60,29,'C2G  •  Version 11.0  •  26 November 2026');c.drawRightString(552,29,str(d.page))
a.out.parent.mkdir(parents=True,exist_ok=True);doc=SimpleDocTemplate(str(a.out),pagesize=(612,792),leftMargin=60,rightMargin=60,topMargin=55,bottomMargin=56,title='Architectural Economy in Biological and Technological Systems v11',author='Randall S. Young');doc.build(story,onFirstPage=page,onLaterPages=page,canvasmaker=StableCanvas); print('Built',a.out,'pages',len(fitz.open(a.out)))
