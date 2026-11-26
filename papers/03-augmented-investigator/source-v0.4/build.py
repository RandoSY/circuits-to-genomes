from pathlib import Path
import re, html
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Polygon
from reportlab.graphics import renderSVG
from reportlab.lib.utils import simpleSplit
P=Path(__file__).parent
for n,f in [('Body','DejaVuSans.ttf'),('Bold','DejaVuSans-Bold.ttf'),('Italic','DejaVuSans-Oblique.ttf')]:pdfmetrics.registerFont(TTFont(n,'/usr/share/fonts/truetype/dejavu/'+f))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='Bold',italic='Italic',boldItalic='Bold')
ink='#163638'; teal='#17695f'; blue='#346c90'; muted='#52676a'; border='#b9ceca'; pale='#e7f1ed'; amber='#a36a2e'; amberp='#f5ecdc'; bluep='#e7eff6'; gray='#e9edee'; W=496
C=HexColor
styles={
 'title':ParagraphStyle('title',fontName='Bold',fontSize=25,leading=30,textColor=C(ink),spaceAfter=8),
 'sub':ParagraphStyle('sub',fontName='Body',fontSize=14,leading=19,textColor=C(muted),spaceAfter=14),
 'head':ParagraphStyle('head',fontName='Bold',fontSize=16,leading=21,textColor=C(teal),spaceBefore=4,spaceAfter=10,keepWithNext=True),
 'body':ParagraphStyle('body',fontName='Body',fontSize=10.3,leading=14.5,textColor=C(ink),spaceAfter=9),
 'meta':ParagraphStyle('meta',fontName='Body',fontSize=9,leading=12.5,textColor=C(muted),spaceAfter=4),
 'caption':ParagraphStyle('caption',fontName='Italic',fontSize=8.5,leading=11.7,textColor=C(muted),spaceAfter=12),
 'quote':ParagraphStyle('quote',fontName='Body',fontSize=10.2,leading=15,textColor=C(ink),leftIndent=14,rightIndent=14,spaceBefore=8,spaceAfter=12,backColor=C(pale),borderColor=C(border),borderWidth=.5,borderPadding=8),
 'table':ParagraphStyle('table',fontName='Body',fontSize=8.6,leading=12.0,textColor=C(ink)),
 'th':ParagraphStyle('th',fontName='Bold',fontSize=8.8,leading=12,textColor=white),
 'ref':ParagraphStyle('ref',fontName='Body',fontSize=9.2,leading=12.8,textColor=C(ink),spaceAfter=7),
}
def para(t,style='body'):
 t=html.escape(t);t=re.sub(r'\*\*(.*?)\*\*',r'<b>\1</b>',t);return Paragraph(t,styles[style])
def draw(name):
 h={'reciprocal':182,'dimensions':132,'trajectory':140,'equivalence':157,'prediction':151,'workflow':172,'cycle':175}[name];d=Drawing(W,h)
 def box(x,y,w,z,fill=pale,stroke=border):d.add(Rect(x,h-y-z,w,z,rx=5,ry=5,fillColor=C(fill),strokeColor=C(stroke),strokeWidth=.8))
 def text(x,y,s,size=9.4,color=ink,bold=False,align='start'):
  d.add(String(x,h-y,s,fontName='Bold' if bold else 'Body',fontSize=size,fillColor=C(color),textAnchor=align))
 def line(x,y,X,Y,color=muted,dash=False,sw=1.2):
  l=Line(x,h-y,X,h-Y,strokeColor=C(color),strokeWidth=sw);l.strokeDashArray=[4,3] if dash else None;d.add(l)
 def arrow(x,y,X,Y,color=muted,dash=False):
  import math
  line(x,y,X,Y,color,dash);a=math.atan2(Y-y,X-x);pts=[X,h-Y,X-6*math.cos(a-.55),h-(Y-6*math.sin(a-.55)),X-6*math.cos(a+.55),h-(Y-6*math.sin(a+.55))];d.add(Polygon(pts,fillColor=C(color),strokeColor=C(color),strokeWidth=.3))
 if name=='reciprocal':
  box(0,9,222,80,bluep,blue);box(274,9,222,80,pale,teal)
  text(111,30,'COMPUTING',11,blue,True,'middle');text(111,47,'PDP-8 compatible implementations',8.8,ink,False,'middle');text(111,64,'Economy · reuse · fault liability',8.7,ink,False,'middle')
  text(385,30,'BIOLOGY',11,teal,True,'middle');text(385,47,'Changing DNA; retained activity?',9,ink,False,'middle');text(385,64,'Motifs · compensation · buffering',8.7,ink,False,'middle');arrow(223,35,273,35,blue);arrow(273,73,223,73,teal,True)
  box(0,103,W,70,amberp,amber);text(12,122,'A reciprocal scientific program',10,amber,True);text(12,139,'Forward: analogy → hypothesis → reporter-assay analysis',9.3);text(12,155,'Return: candidate design principle → controlled computing benchmark',9.3);text(12,168,'Neither direction alone proves predictive transfer.',8.5,muted)
 elif name=='dimensions':
  for i,(title,q,fill,col) in enumerate([('Methodological reach','What can I do?',pale,teal),('Epistemic competence','What can I explain?',bluep,blue),('Evidential warrant','What can I claim?',amberp,amber)]):
   x=i*169;box(x,5,158,53,fill,col);text(x+79,23,title,8.8,col,True,'middle');text(x+79,42,q,9.2,ink,False,'middle');arrow(x+79,58,x+79,82)
  box(0,83,496,40,teal,teal);text(248,100,'Independent checking + qualified judgment',11,'#ffffff',True,'middle');text(248,114,'Capability, understanding and evidence do not automatically advance together.',8.1,'#ffffff',False,'middle')
 elif name=='trajectory':
  data=[('23–24 NOV','Analogy + H2 pilot'),('24 NOV','Paper 1 v7/v8'),('24 NOV','FEM v1.0'),('25 NOV','Paper 3 v0.2'),('25 NOV','FEM v1.1'),('26 NOV','Paper 1 v9 / v0.3 drafts')]
  for i,(date,s) in enumerate(data):
   x=i%3*169;y=i//3*57;box(x,y+3,158,48,amberp if i==0 else pale,amber if i==0 else border);text(x+9,y+18,date,8,muted,True);text(x+9,y+35,s,8.7,ink,True)
   if i%3!=2:arrow(x+158,y+27,x+169,y+27)
  text(248,130,'Negative evidence retained  •  empirical findings feed back into theory',9,muted,False,'middle')
 elif name=='equivalence':
  vals=[('±0.15  /  moderated',63.2,teal),('±0.15  /  unmoderated',43.5,blue),('±0.50  /  moderated',99.2,amber)]
  text(0,11,'PERCENT CLASSIFIED EQUIVALENT',8.5,muted,True)
  for i,(lab,v,col) in enumerate(vals):
   y=22+i*34;text(0,y+13,lab,9,ink,True);box(161,y,290,20,gray,gray);box(161,y,290*v/100,20,col,col);text(462,y+13,str(v)+'%',8.7,ink,True)
  for n in [0,25,50,75,100]:x=161+n*2.9;line(x,126,x,130);text(x,142,str(n),8,muted,False,'middle')
 elif name=='prediction':
  text(0,12,'LEAVE-ONE-CHROMOSOME-OUT ROC-AUC',8.5,muted,True)
  for i,(lab,v,col) in enumerate([('Baseline',.5971,muted),('Consensus motifs',.6014,amber),('JASPAR PWMs',.6260,teal)]):
   y=22+i*34;text(0,y+14,lab,9,ink,True);box(145,y,298,21,gray,gray);box(145,y,298*v,21,col,col);text(454,y+14,f'{v:.4f}',9,ink,True)
  line(294,18,294,122,ink,True);text(294,143,'0.5 chance reference',8.5,muted,False,'middle');text(145,143,'0',8,muted,False,'middle');text(443,143,'1',8,muted,False,'middle')
 elif name=='workflow':
  box(93,0,310,29,teal,teal);text(248,18,'Human investigator: question, direction, judgment',10,'#ffffff',True,'middle')
  for i,(a,b) in enumerate([('ChatGPT','Browser'),('Gemini','NEON / CARBON'),('Claude','Parallel draft')]):
   x=i*169;arrow(248,29,x+79,43);box(x,44,158,44,bluep,blue);text(x+79,62,a,10,blue,True,'middle');text(x+79,77,b,9,muted,False,'middle');arrow(x+79,88,248,106)
  box(84,107,328,25,pale,teal);text(248,123,'GitHub: versioned evidence + critique',10,ink,True,'middle');arrow(248,132,248,142);box(84,143,328,25,amberp,amber);text(248,159,'Independent specialist verification — pending',9.6,ink,True,'middle')
 elif name=='cycle':
  box(0,0,W,27,bluep,blue);text(248,17,'PURPOSE GATE: Does this analysis address the originating question?',10,blue,True,'middle')
  labels=[('1  Ask','Question'),('2  Formalize','Hypothesis + test'),('3  Execute','Data + code'),('4  Interpret','Evidence + scope'),('5  Verify','Seek qualified help'),('6  Communicate','Bounded claim')]
  for i,(a,b) in enumerate(labels):
   x=i%3*169;y=37+i//3*48;box(x,y,158,39,amberp if i==4 else pale,amber if i==4 else border);text(x+9,y+15,a,9.4,ink,True);text(x+9,y+29,b,8.5,muted)
   if i%3!=2:arrow(x+158,y+20,x+169,y+20)
  box(0,137,W,33,teal,teal);text(248,151,'EVIDENTIAL GATE: Is the claim adequately checked?',9.8,'#ffffff',True,'middle');text(248,163,'If not, revise, seek help, or communicate explicitly as provisional.',8.1,'#ffffff',False,'middle')
 renderSVG.drawToFile(d,str(P/(name+'.svg')));return d

def tab(name):
 if name=='audit':
  rows=[['Audit target','Documented response','Remaining obligation'],['Margin timing','Frozen ±0.50; primary ±0.15 after inspection; sensitivity grid.','Biological and statistical justification pending.'],['Variance moderation','Raw and moderated estimates reported: 43.5% vs 63.2%.','Check prior, calibration and sensitivity with three replicates.'],['Epistasis threshold','95% and 90% critical values separated; 4/8 vs 5/8.','Review test assumptions, selection and multiplicity.'],['Observation independence','Barcodes treated as technical subsamples; clustering reported.','Audit replicate identities and clustering.'],['Assay comparisons','High-variance capture-MPRA often inconclusive.','Different contexts; do not attribute effect solely to platform.'],['Reproduction','AI-assisted raw-barcode reconstruction reported.','Independent execution and specialist review still open.'],['New JASPAR audit','Post-hoc model; modest AUC improvement.','Quantify uncertainty and test independent cohort.']];widths=[116,198,182]
 else:
  rows=[['Biological observation','Candidate computing test','Criterion / falsifier'],['Nonadditive mutational buffering','Compare alternative component combinations with matched task outputs.','Does combined behavior remain within tolerance more often than conventional designs?'],['Scale-specific redundancy','Compare local backup vs module-level redundancy, including coordinator faults.','Does module protection survive coordination failure at equal resource cost?'],['Predicted interaction disruption','Rank substitutions by effects on dependency structure vs raw component changes.','Does interaction-based prediction generalize to held-out tasks?']];widths=[125,185,186]
 a=[[para(v,'th' if i==0 else 'table') for v in r] for i,r in enumerate(rows)];t=Table(a,colWidths=widths,repeatRows=1,hAlign='LEFT');t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),C(teal)),('ROWBACKGROUNDS',(0,1),(-1,-1),[C('#f6f9f8'),white]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,0),(-1,-1),.45,C(border))]));return t

def footer(c,d):
 c.setStrokeColor(C(border));c.line(58,750,554,750);c.line(58,43,554,43);c.setFont('Bold',8);c.setFillColor(C(muted));c.drawString(58,760,'THE AUGMENTED INVESTIGATOR  /  METASCIENCE & STEM EDUCATION');c.setFont('Body',8);c.drawString(58,29,'C2G  •  Working manuscript v0.4  •  26 November 2026');c.drawRightString(554,29,str(d.page))
md=(P/'manuscript.md').read_text();md=re.sub(r'(\!\[(?:FIG|TABLE):[^\]]+\])\n',r'\1\n\n',md)
story=[]
for i,group in enumerate(md.strip().split('<!-- PAGE -->')):
 if i:story.append(PageBreak())
 for b in re.split(r'\n\s*\n',group.strip()):
  if b.startswith('# '):
   for l in b.splitlines():
    if l.startswith('# '):story.append(para(l[2:],'title'))
    elif l.startswith('## '):story.append(para(l[3:],'sub'))
    else:story.append(para(l,'meta'))
  elif b.startswith('### '):
   # headings normally separated by blank lines; abstract title and para may share block
   lines=b.splitlines();story.append(para(lines[0][4:],'head'))
   if len(lines)>1:story.append(para(' '.join(lines[1:])))
  elif b.startswith('![FIG:'):
   story.append(draw(b[6:-1]));story.append(Spacer(1,6))
  elif b.startswith('![TABLE:'):
   story.append(tab(b[8:-1]));story.append(Spacer(1,6))
  elif b.startswith('*Figure') or b.startswith('*Table'):story.append(para(b.strip('*'),'caption'))
  elif b.startswith('> '):story.append(para(b[2:],'quote'))
  else:story.append(para(b,'ref' if i==15 else 'body'))
out=P.parent/'The_Augmented_Investigator_v0.4.pdf'
SimpleDocTemplate(str(out),pagesize=letter,leftMargin=52,rightMargin=52,topMargin=58,bottomMargin=54,title='The Augmented Investigator v0.4',author='Randall S. Young, Ed.S.').build(story,onFirstPage=footer,onLaterPages=footer)
print(out)
