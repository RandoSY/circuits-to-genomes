// Reproducible dependency-free rendering of Paper 3 v0.3.
// Node.js: node build_v03.cjs (run beside the manuscript Markdown).
const fs=require('node:fs'),path=require('node:path');
function build(md) {
  const W=612,H=792,L=58,R=554, CW=496;
  const palette={ink:"#193438",teal:"#17695f",blue:"#376d91",muted:"#52676a",line:"#c3d2cf",pale:"#e8f1ee",bluep:"#e7eff5",amber:"#b0803c",amberp:"#f7eedf",white:"#ffffff",gray:"#edf0f1"};
  const figDefs={
    "01-dimensions":{h:154,draw(g){
      g.label(0,12,"THREE DISTINCT DIMENSIONS",9,"muted",true);
      const a=[["Methodological reach","What can I do?","teal","pale"],["Epistemic competence","What can I explain?","blue","bluep"],["Evidential warrant","What can I claim?","amber","amberp"]];
      a.forEach((d,i)=>{let x=i*169;g.box(x,24,158,67,d[3],d[2]);g.label(x+79,44,d[0],11,d[2],true,"center");g.label(x+79,64,d[1],10,"ink",false,"center");});
      g.arrow(79,94,79,112);g.arrow(248,94,248,112);g.arrow(417,94,417,112);
      g.box(0,116,496,31,"teal","teal");g.label(248,136,"Independent checking and qualified judgment connect the three.",11,"white",true,"center");
    }},
    "02-trajectory":{h:154,draw(g){
      const a=[["23-24 Nov","Concept + H2 pilot"],["24 Nov","Paper 1 v7/v8"],["24 Nov","Paper 2 v1.0"],["25 Nov","Paper 3 v0.2"],["25 Nov","Paper 2 v1.1"],["26 Nov","Paper 1 v9 prepared"]];
      a.forEach((d,i)=>{let x=(i%3)*169,y=Math.floor(i/3)*73;g.box(x,y+4,158,61,i===0?"amberp":"pale",i===0?"amber":"teal");g.label(x+10,y+23,d[0],10,"muted",true);g.label(x+10,y+43,d[1],11,"ink",true);if(i%3!==2)g.arrow(x+158,y+35,x+169,y+35);});
      g.label(248,153,"Negative pilot retained | empirical results feed back into theory",9,"muted",false,"center");
    }},
    "03-equivalence":{h:144,draw(g){
      const vals=[["Moderated",63.2,"teal"],["Unmoderated",43.5,"blue"]];
      g.label(0,12,"EQUIVALENT FRAGMENTS (%)",9,"muted",true);
      vals.forEach((d,i)=>{let y=25+i*39;g.label(0,y+14,d[0],11,"ink",true);g.box(112,y,340,22,"gray","gray");g.box(112,y,340*d[1]/100,22,d[2],d[2]);g.label(462,y+15,d[1].toFixed(1)+"%",10,"ink",true);});
      [0,25,50,75,100].forEach(n=>{let x=112+n*3.4;g.line(x,106,x,111,"muted");g.label(x,124,String(n),9,"muted",false,"center");});
      g.label(112,142,"Same 386 fragments; same +/-0.15 log2 margin",9,"muted");
    }},
    "04-prediction":{h:169,draw(g){
      g.label(0,12,"HELD-OUT CHROMOSOME ROC-AUC",9,"muted",true);
      const vals=[["Baseline",0.5971,"muted"],["Consensus motifs",0.6014,"amber"],["JASPAR PWMs",0.6260,"teal"]];
      vals.forEach((d,i)=>{let y=25+i*35;g.label(0,y+15,d[0],10,"ink",true);g.box(113,y,328,21,"gray","gray");g.box(113,y,328*d[1],21,d[2],d[2]);g.label(451,y+15,d[1].toFixed(4),10,"ink",true);});
      g.line(277,21,277,130,"ink",1.2);[0,.5,1].forEach(n=>{let x=113+n*328;g.line(x,130,x,135,"muted");g.label(x,147,n.toFixed(1),9,"muted",false,"center");});g.label(277,163,"Chance ranking reference",9,"muted",false,"center");
    }},
    "05-workflow":{h:184,draw(g){
      g.box(130,0,236,30,"teal","teal");g.label(248,19,"Human investigator: question + judgment",11,"white",true,"center");
      g.arrow(180,30,111,48);g.arrow(316,30,385,48);
      g.box(0,49,222,47,"bluep","blue");g.box(274,49,222,47,"pale","teal");
      g.label(111,66,"ChatGPT / browser",11,"blue",true,"center");g.label(111,82,"Analysis, critique, drafting",10,"ink",false,"center");
      g.label(385,66,"Gemini / Antigravity",11,"teal",true,"center");g.label(385,82,"NEON / CARBON (user labels)",10,"ink",false,"center");
      g.arrow(222,72,274,72);g.arrow(111,96,200,113);g.arrow(385,96,296,113);
      g.box(87,114,322,29,"gray","line");g.label(248,133,"GitHub: versioned artifacts and evidence",11,"ink",true,"center");
      g.arrow(248,143,248,153);g.box(87,154,322,29,"amberp","amber");g.label(248,173,"Independent specialist review - pending",11,"ink",true,"center");
    }},
    "06-cycle":{h:150,draw(g){
      const a=[["1 Ask","Question"],["2 Formalize","Test + assumptions"],["3 Execute","Code + data"],["4 Interpret","Evidence + limits"],["5 Verify","Expert / rerun"],["6 Communicate","Calibrated claim"]];
      a.forEach((d,i)=>{let x=(i%3)*169,y=Math.floor(i/3)*62;g.box(x,y+3,158,49,i===4?"amberp":"pale",i===4?"amber":"teal");g.label(x+9,y+22,d[0],11,"ink",true);g.label(x+9,y+38,d[1],10,"muted");if(i%3!==2)g.arrow(x+158,y+27,x+169,y+27);});
      g.arrow(417,52,417,58);g.box(0,126,496,23,"teal","teal");g.label(248,141,"Unresolved material uncertainty: revisit earlier stages or stay provisional.",10,"white",true,"center");
    }}
  };
  const xml=s=>s.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
  const esc=s=>s.replace(/\\/g,"\\\\").replace(/\(/g,"\\(").replace(/\)/g,"\\)");
  const clean=s=>s.replace(/[^\x20-\x7e]/g,c=>({"–":"-","—":"-","’":"'","“":'"',"”":'"',"±":"+/-","→":"->"}[c]||"?"));
  const widths={};const chars=" !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~";
  const vals=[278,278,355,556,556,889,667,191,333,333,389,584,278,333,278,278,...Array(10).fill(556),278,278,584,584,584,556,1015,667,667,722,722,667,611,778,722,278,500,667,556,833,722,778,667,778,722,667,611,722,667,944,667,667,611,278,278,278,469,556,333,556,556,500,556,556,278,556,556,222,222,500,222,833,556,556,556,556,333,500,278,556,500,722,500,500,500,334,260,334,584];
  [...chars].forEach((c,i)=>widths[c]=vals[i]||600);
  function measure(s,size,bold=false){return [...s].reduce((a,c)=>a+(widths[c]||600)*(bold?1.065:1),0)*size/1000;}
  function wrap(s,size,width,bold=false){const lines=[];let line="";for(const w of clean(s).split(/\s+/)){if(!w)continue;if(measure(w,size,bold)>width){if(line){lines.push(line);line="";}let chunk="";for(const ch of w){if(measure(chunk+ch,size,bold)>width){lines.push(chunk);chunk=ch;}else chunk+=ch;}line=chunk;continue;}const n=line?line+" "+w:w;if(measure(n,size,bold)>width&&line){lines.push(line);line=w;}else line=n;}if(line)lines.push(line);return lines;}
  const col=k=>palette[k]||k;
  const rgb=k=>{let h=col(k).slice(1);return [0,2,4].map(i=>(parseInt(h.slice(i,i+2),16)/255).toFixed(3)).join(" ");};
  const svgFiles={};
  for(const [name,d] of Object.entries(figDefs)){
    let a=[];const g={box(x,y,w,h,f,s){a.push(`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="3" fill="${col(f)}" stroke="${col(s)}"/>`);},label(x,y,s,z,c,b=false,align="left"){a.push(`<text x="${x}" y="${y}" font-size="${z}" font-weight="${b?700:400}" text-anchor="${align==="center"?"middle":"start"}" fill="${col(c)}">${xml(s)}</text>`);},line(x,y,X,Y,c,sw=0.9){a.push(`<path d="M${x} ${y}L${X} ${Y}" fill="none" stroke="${col(c)}" stroke-width="${sw}"/>`);},arrow(x,y,X,Y){g.line(x,y,X,Y,"muted",1.1);const q=Math.atan2(Y-y,X-x);for(const v of [-.55,.55])g.line(X,Y,X-5*Math.cos(q+v),Y-5*Math.sin(q+v),"muted",1.1);}};
    d.draw(g);svgFiles[name]=`<svg xmlns="http://www.w3.org/2000/svg" width="992" height="${d.h*2}" viewBox="-1 -1 498 ${d.h+2}" role="img" font-family="Arial,Helvetica,sans-serif"><title>${xml(name.replace(/-/g," "))}</title><rect x="-1" y="-1" width="498" height="${d.h+2}" fill="#fff"/>${a.join("")}</svg>\n`;
  }
  let pages=[],p=null,y=0,report=[];
  function tx(x,Y,s,z=11,c="ink",bold=false,ital=false,align="left"){s=clean(s);if(align==="center")x-=measure(s,z,bold)/2;p.push(`${rgb(c)} rg BT /${ital?"F3":bold?"F2":"F1"} ${z} Tf 1 0 0 1 ${x.toFixed(2)} ${(H-Y).toFixed(2)} Tm (${esc(s)}) Tj ET`);}
  function rect(x,Y,w,h,f,s){p.push(`${rgb(f)} rg ${rgb(s)} RG 0.6 w ${x.toFixed(2)} ${(H-Y-h).toFixed(2)} ${w.toFixed(2)} ${h.toFixed(2)} re B`);}
  function line(x,Y,X,Y2,c="line",sw=.8){p.push(`${rgb(c)} RG ${sw} w ${x.toFixed(2)} ${(H-Y).toFixed(2)} m ${X.toFixed(2)} ${(H-Y2).toFixed(2)} l S`);}
  function start(){p=[];pages.push(p);y=69;tx(L,33,"THE AUGMENTED INVESTIGATOR  /  METASCIENCE & STEM EDUCATION",8.2,"muted",true);line(L,43,R,43);tx(L,763,"C2G  |  Working manuscript v0.3  |  26 November 2026",8,"muted");tx(R-22,763,String(pages.length),9,"muted",true);line(L,749,R,749);}
  function ensure(h){if(y+h>733){report.push({page:pages.length,bottom:y});start();}}
  function paragraph(s,kind){const z=kind==="caption"?9.4:kind==="quote"?10.7:kind==="meta"?10:10.8;const leading=kind==="caption"?12.4:kind==="meta"?13.4:14.8;const indent=kind==="quote"?15:0;const txt=s.replace(/\*\*/g,"").replace(/^\*|\*$/g,"");const lines=wrap(txt,z,CW-indent-(kind==="quote"?8:0),false);ensure(lines.length*leading+8);if(kind==="quote"){rect(L,y-11,CW,lines.length*leading+10,"pale","line");}for(const t of lines){tx(L+indent,y,t,z,kind==="caption"?"muted":"ink",false,kind==="caption"||kind==="quote");y+=leading;}y+=kind==="meta"?3:8;}
  function heading(s,level){const size=level===1?29:level===2?16:level===3?17:12;const leading=size*1.22;const lines=wrap(s,size,CW,true);ensure(lines.length*leading+34);for(const t of lines){tx(L,y,t,size,level===1?"ink":level===2?"muted":"teal",true);y+=leading;}y+=level===1?5:level===2?12:9;}
  function figure(name){const d=figDefs[name];if(!d)throw Error("Unknown figure "+name);ensure(d.h+48);const top=y-4;const g={box(x,Y,w,h,f,s){rect(L+x,top+Y,w,h,f,s);},label(x,Y,s,z,c,b=false,align="left"){tx(L+x,top+Y,s,z,c,b,false,align);},line(x,Y,X,Y2,c,sw=.8){line(L+x,top+Y,L+X,top+Y2,c,sw);},arrow(x,Y,X,Y2){g.line(x,Y,X,Y2,"muted",1.1);const q=Math.atan2(Y2-Y,X-x);for(const v of [-.55,.55])g.line(X,Y2,X-5*Math.cos(q+v),Y2-5*Math.sin(q+v),"muted",1.1);}};d.draw(g);y+=d.h+12;}
  const groups=md.trim().split(/<!-- PAGE -->/);
  for(const group of groups){if(p)report.push({page:pages.length,bottom:y});start();for(const block of group.trim().split(/\n\s*\n/)){const s=block.trim();if(!s)continue;if(s.startsWith("# ")){heading(s.slice(2),1);}else if(s.startsWith("## ")){heading(s.slice(3),2);}else if(s.startsWith("### ")){heading(s.slice(4),3);}else if(s.startsWith("#### ")){heading(s.slice(5),4);}else if(s.startsWith("![")){const m=s.match(/figures\/v03\/([a-z0-9-]+)\.svg/);figure(m[1]);}else if(s.startsWith("> ")){paragraph(s.slice(2),"quote");}else if(s.startsWith("*Figure ")){paragraph(s,"caption");}else if(s.startsWith("Randall S.")){for(const line of s.split(/\n/))paragraph(line.trim(),"meta");}else{paragraph(s,"body");}}}
  report.push({page:pages.length,bottom:y});
  const obj=[null,"<< /Type /Catalog /Pages 2 0 R >>",null,"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>","<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>","<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Oblique /Encoding /WinAnsiEncoding >>"];
  const ids=[];
  for(const page of pages){let stream=page.join("\n")+"\n";const c=obj.length;obj.push(`<< /Length ${stream.length} >>\nstream\n${stream}endstream`);const id=obj.length;ids.push(id);obj.push(`<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 3 0 R /F2 4 0 R /F3 5 0 R >> >> /Contents ${c} 0 R >>`);}
  obj[2]=`<< /Type /Pages /Count ${ids.length} /Kids [${ids.map(i=>i+" 0 R").join(" ")}] >>`;
  let info=obj.length;obj.push("<< /Title (The Augmented Investigator v0.3) /Author (Randall S. Young) /Subject (Metacognition and AI-augmented scientific inquiry) >>");
  let pdf="%PDF-1.4\n";const offsets=[0];for(let i=1;i<obj.length;i++){offsets[i]=pdf.length;pdf+=`${i} 0 obj\n${obj[i]}\nendobj\n`;}const xref=pdf.length;pdf+=`xref\n0 ${obj.length}\n0000000000 65535 f \n${offsets.slice(1).map(n=>String(n).padStart(10,"0")+" 00000 n \n").join("")}trailer\n<< /Size ${obj.length} /Root 1 0 R /Info ${info} 0 R >>\nstartxref\n${xref}\n%%EOF\n`;
  if(/[^\x00-\x7f]/.test(pdf))throw Error("PDF not ASCII");
  return {pdf,svgFiles,report,pages:pages.length,words:md.split(/\s+/).length};
}
const root=__dirname; const o=build(fs.readFileSync(path.join(root,'The_Augmented_Investigator_v0.3.md'),'utf8'));fs.writeFileSync(path.join(root,'The_Augmented_Investigator_v0.3.pdf'),o.pdf,'ascii');fs.mkdirSync(path.join(root,'figures/v03'),{recursive:true});for(const [n,s] of Object.entries(o.svgFiles))fs.writeFileSync(path.join(root,'figures/v03',n+'.svg'),s,'utf8');console.log(JSON.stringify({pages:o.pages,words:o.words,report:o.report}));
