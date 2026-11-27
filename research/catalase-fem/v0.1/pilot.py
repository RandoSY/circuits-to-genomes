"""C2G catalase pilot: descriptive reanalysis, no inference of equivalence."""
import csv, math, statistics as s, json
from pathlib import Path
p=Path(__file__).parent
with (p/'kinetics.csv').open(newline='') as f: rows=list(csv.DictReader(f))
metrics=['specific_activity_U_mg','observed_max_per_heme_s','half_max_mM','heat_half_min_65C']
def describe(rs):
    out={}
    for m in metrics:
        v=[float(r[m]) for r in rs]
        out[m]={'min':min(v),'max':max(v),'median':s.median(v),'fold_range':max(v)/min(v)}
    return out
def loo(m):
    v=[math.log10(float(r[m])) for r in rows]; a=[]; b=[]
    for i,r in enumerate(rows):
        tr=[v[j] for j in range(len(v)) if i!=j]
        cl=[v[j] for j in range(len(v)) if i!=j and rows[j]['clade_2002']==r['clade_2002']]
        a.append(abs(v[i]-s.median(tr))); b.append(abs(v[i]-s.median(cl)))
    return {'global_median_mae_log10':s.mean(a),'clade_median_mae_log10':s.mean(b),'improvement_percent':100*(1-s.mean(b)/s.mean(a))}
result={'n':len(rows),'all':describe(rows),'clades':{c:{'n':len(rs),'metrics':describe(rs)} for c in sorted(set(r['clade_2002'] for r in rows)) if (rs:=[r for r in rows if r['clade_2002']==c])},'exploratory_LOO':{m:loo(m) for m in metrics},'warning':'Retrospective, tiny uneven clades; LOO is not phylogenetically independent, no significance or validated prediction claimed.'}
(p/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
