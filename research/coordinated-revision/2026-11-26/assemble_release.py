"""Recover byte-exact coordinated C2G review editions from the archived baselines.
Usage: python assemble_release.py --repo PATH [--publish]
No third-party libraries required; --publish requires a clean Git checkout on main.
"""
from pathlib import Path
import argparse, hashlib, json, subprocess, sys, zipfile
here=Path(__file__).resolve().parent
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,required=True);p.add_argument('--publish',action='store_true');p.add_argument('--archive',type=Path,default=here/'exact_deltas.zip');args=p.parse_args();repo=args.repo.resolve()
manifest=json.loads((here/'RELEASE_MANIFEST.json').read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*cmd):return subprocess.check_output(['git','-C',str(repo),*cmd],text=True).strip()
if args.publish:
 if git('branch','--show-current')!='main' or git('status','--porcelain'):raise SystemExit('Use a clean checkout on main before publishing.')
 if 'RandoSY/circuits-to-genomes' not in git('remote','get-url','origin'):raise SystemExit('Incorrect origin; expected RandoSY/circuits-to-genomes.')
 subprocess.run(['git','-C',str(repo),'pull','--ff-only','origin','main'],check=True)
output=[]
with zipfile.ZipFile(args.archive) as z:
 for item in manifest:
  base=repo/item['path']/item['baseline'];delta=z.read(item['delta']);before=base.read_bytes()
  if sha(before)!=item['baseline_sha256'] or sha(delta)!=item['delta_sha256']:raise SystemExit('Input checksum mismatch: '+item['key'])
  result=before+delta
  if sha(result)!=item['pdf_sha256'] or len(result)!=item['pdf_bytes']:raise SystemExit('Output checksum mismatch: '+item['key'])
  target=repo/item['path']/item['new_pdf']
  if target.exists() and target.read_bytes()!=result:raise SystemExit('Refusing to overwrite different existing file: '+str(target))
  output.append((target,result,item))
for target,result,item in output:
 target.write_bytes(result);print(f"Verified {target.name} — {item['total_pages']} pages — SHA256 {item['pdf_sha256']}")
if args.publish:
 paths=[str(t.relative_to(repo)) for t,_,_ in output]
 # Indexes already link the release record; add actual file paths and checksums after exact reconstruction.
 for fn in ['README.md','papers/README.md','docs/PUBLICATION_STATUS.md']:
  path=repo/fn; txt=path.read_text(encoding='utf-8'); mark='<!-- COORDINATED_REVIEW_PDFS -->'
  if mark not in txt:
   prefix='' if fn=='README.md' else '../'
   links='\n'.join('- ['+i['title']+' '+i['new']+' ('+str(i['total_pages'])+' pages)]('+prefix+i['path']+'/'+i['new_pdf']+')' for _,_,i in output)
   path.write_text(txt.rstrip()+'\n\n'+mark+'\n## Coordinated expanded review PDFs (verified)\n\n'+links+'\n',encoding='utf-8');paths.append(fn)
 sums=repo/'papers/SHA256SUMS.txt';txt=sums.read_text(encoding='utf-8').rstrip();existing=set(txt.splitlines());new=[i['pdf_sha256']+'  '+i['path']+'/'+i['new_pdf'] for _,_,i in output];sums.write_text(txt+'\n'+''.join(l+'\n' for l in new if l not in existing),encoding='utf-8');paths.append('papers/SHA256SUMS.txt')
 subprocess.run(['git','-C',str(repo),'add','--',*paths],check=True)
 if git('diff','--cached','--name-only'):
  subprocess.run(['git','-C',str(repo),'commit','-m','Publish exact coordinated review PDFs v10, v1.2 and v0.5'],check=True)
  subprocess.run(['git','-C',str(repo),'push','origin','main'],check=True)
 print('Git publication command finished. Check remote tree before declaring success.')
