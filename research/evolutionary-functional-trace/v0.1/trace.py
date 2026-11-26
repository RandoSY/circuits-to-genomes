#!/usr/bin/env python3
"""EFT v0.1: deterministic cohort selection and reference-checked alignment retrieval.
Python standard library only. No functional inference from ancestry.
"""
import argparse,csv,hashlib,json,re,statistics,urllib.request,urllib.parse,time
from pathlib import Path
from datetime import datetime,timezone
BASE='https://rest.ensembl.org'
TAG='length=171_of_171__0-171__NO_EcoRI_RESTRICTION_SITES_MODIFIED__NO_SbfI_RESTRICTION_SITES_MODIFIED'
THRESHOLD=0.004470700746986775

def revcomp(s): return s.translate(str.maketrans('ACGT','TGCA'))[::-1]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def select(p):
    rows=[]
    with p.open(newline='',encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            h,c=r['human_sequence'].upper(),r['chimp_sequence'].upper()
            hm,cm=[statistics.mean(float(r[f'{s}_rep{i}']) for i in (1,2,3)) for s in ('human','chimp')]
            m=re.match(r'chr([0-9]+|X|Y):(\d+)-(\d+)\|cut=1_of_1\|',r['pair'])
            if not m or r['pair'].count(TAG)!=2 or max(hm,cm)<THRESHOLD: continue
            chrom,start,end=m.groups(); start,end=int(start),int(end)
            if end-start!=171 or len(h)!=171 or len(c)!=171 or set(h+c)-set('ACGT'): continue
            rows.append((hashlib.sha256(('EFT-v0.1|'+r['har']).encode()).hexdigest(),dict(har=r['har'],chrom=chrom,start0=start,end0=end,human_sequence=h,chimp_sequence=c,human_mean=hm,chimp_mean=cm,delta=hm-cm,mismatches=sum(x!=y for x,y in zip(h,c)))))
    rows.sort(key=lambda x:x[0]); result=[]; seen=set()
    for _,r in rows:
        if r['har'] not in seen: result.append(r);seen.add(r['har'])
    return len(result),result[:10]
def fetch(path,params,dest,mime='application/json'):
    url=BASE+path+'?'+urllib.parse.urlencode({'content-type':mime,**params})
    if dest.exists(): raw=dest.read_bytes()
    else:
        req=urllib.request.Request(url,headers={'Accept':mime,'Content-Type':mime,'User-Agent':'C2G-EFT/0.1 research'})
        with urllib.request.urlopen(req,timeout=35) as response: raw=response.read()
        dest.write_bytes(raw);time.sleep(.3)
    return json.loads(raw) if mime=='application/json' else raw

def trace(r,folder):
    folder.mkdir(exist_ok=True); ch,s,e=r['chrom'],r['start0']+1,r['end0']
    region=f'{ch}:{s}..{e}:1'
    # Coordinates are a hypothesis until the assay construct matches the reference exactly.
    mapping=fetch(f'/map/human/GRCh37/{region}/GRCh38',{},folder/'mapping.json')['mappings']
    if len(mapping)!=1: raise ValueError('Mapping not unique/contiguous')
    o,m=mapping[0]['original'],mapping[0]['mapped']
    if (o['start'],o['end'])!=(s,e) or m['end']-m['start']+1!=171: raise ValueError('Mapping incomplete or length changed')
    target=f"{m['seq_region_name']}:{m['start']}..{m['end']}:1"
    seq=fetch(f'/sequence/region/human/{target}',{},folder/'reference.json')['seq'].upper()
    h=r['human_sequence']; orientation='forward' if seq==h else 'reverse' if revcomp(seq)==h else None
    if orientation is None: raise ValueError('Assay human sequence does not exactly match GRCh38 reference in either orientation')
    result={'har':r['har'],'target':target,'assay_orientation':orientation,'groups':{}}
    for group in ('primates','mammals'):
        try:
            args={'method':'EPO','species_set_group':group,'aligned':1}
            blocks=fetch(f'/alignment/region/human/{target}',args,folder/f'{group}.json')
            # Keep provider blocks intact; do not concatenate across uncertain breaks.
            if not isinstance(blocks,list): raise ValueError('Unexpected alignment payload')
            species=set(); ancestors=0; comparisons=[]
            for block in blocks:
                entries=block.get('alignments',[])
                human=[x for x in entries if x.get('species') in ('homo_sapiens','human')]
                if len(human)==1:
                    hs=str(human[0].get('seq','')).upper()
                    if hs.replace('-','') in (seq,revcomp(seq)):
                        for x in entries:
                            xs=str(x.get('seq','')).upper()
                            if len(xs)!=len(hs): continue
                            comparable=[(a,b) for a,b in zip(hs,xs) if a in 'ACGT' and b in 'ACGT']
                            n=len(comparable)
                            comparisons.append({'species':x.get('species'),'region':x.get('seq_region'),'comparable_bases':n,'identity':sum(a==b for a,b in comparable)/n if n else None})
                for entry in block.get('alignments',[]):
                    sp=str(entry.get('species','unknown'));species.add(sp)
                    if 'ancestr' in sp.lower() or str(entry.get('seq_region','')).startswith('Ancestor_'): ancestors+=1
            # phyloXML is needed to associate internal nodes with clades, not arbitrary IDs.
            xml_error=None
            try: fetch(f'/alignment/region/human/{target}',args,folder/f'{group}.xml','text/x-phyloxml')
            except Exception as exc: xml_error=str(exc)
            result['groups'][group]={'blocks':len(blocks),'labels':sorted(species),'ancestral_rows':ancestors,'full_reference_block_comparisons':comparisons,'tree_error':xml_error,'status':'retrieved; orthology and node assignment pending' if blocks else 'no alignment returned'}
        except Exception as exc: result['groups'][group]={'status':'failed','error':str(exc)}
    return result

def main():
    p=argparse.ArgumentParser();p.add_argument('--cohort',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--online',action='store_true');a=p.parse_args()
    a.out.mkdir(parents=True,exist_ok=False)
    count,rows=select(a.cohort)
    with (a.out/'pilot.csv').open('w',newline='',encoding='utf-8') as f:
        cols=[k for k in rows[0] if not k.endswith('_sequence')];w=csv.DictWriter(f,fieldnames=cols,extrasaction='ignore');w.writeheader();w.writerows(rows)
    result={'version':'0.1','created_utc':datetime.now(timezone.utc).isoformat(),'cohort_sha256':sha(a.cohort),'eligible_unique_HARs':count,'selected':len(rows),'mode':'online' if a.online else 'local','trace':[],'limits':'Measured activity is human/chimp reporter only; no ancestral function measured. No alignment is proof of absence.'}
    for r in rows:
        if a.online:
            print('Retrieving',r['har'],flush=True)
            try: result['trace'].append(trace(r,a.out/r['har']))
            except Exception as exc: result['trace'].append({'har':r['har'],'status':'failed','error':str(exc)})
        else: result['trace'].append({'har':r['har'],'status':'not queried'})
        (a.out/'summary.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
