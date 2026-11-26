"""FEM-GPU v0.1: prediction baseline, not a biological equivalence test."""
import argparse,csv,hashlib,itertools,json,sys,platform,re
from collections import defaultdict,Counter
from pathlib import Path
import numpy as np

B="ACGT"
WORDS=["".join(w) for k in (1,2,3) for w in itertools.product(B,repeat=k)]
def features(s):
    counts=Counter(s[i:i+k] for k in (1,2,3) for i in range(len(s)-k+1))
    return [counts[w]/(len(s)-len(w)+1) for w in WORDS]
def digest(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for block in iter(lambda:f.read(1048576),b""): h.update(block)
    return h.hexdigest()
def demo():
    rng=np.random.default_rng(20261126); rows=[]
    for i in range(100):
        h="".join(rng.choice(list(B),171)); c=list(h)
        for j in rng.choice(171,12,replace=False):
            c[j]=rng.choice([b for b in B if b!=c[j]])
        c="".join(c)
        def act(s):
            return (30*s.count("A")/171+15*s.count("CG")/170+rng.normal(0,.05,3)).tolist()
        rows.append((f"DEMO{i:03}",f"DEMO{i:03}",h,c,act(h),act(c)))
    return rows,0.,{"synthetic":True}
def real(data):
    sys.path.insert(0,str(Path(__file__).resolve().parents[3]/"validation"))
    from reconstruct_har_cohort import load_design_sequences,compute_activities
    paths=[data/"GSE110758_HAR_design.tsv.gz"]+[data/f"WTc-N2-{i}-{k}.tsv.gz" for i in (1,2,3) for k in ("DNA","RNA")]
    seq=load_design_sequences(paths[0]); act=compute_activities(data,"WTc-N2")
    neg=[np.mean(v) for k,v in act.items() if "neg_ctrl" in k.lower() or "negative_control" in k.lower()]
    if not neg: raise ValueError("No negative controls; check files")
    pairs=defaultdict(lambda:defaultdict(list))
    pattern=r"^([^_]+)__species=(human|chimp)__coordinates_tested_in_hg19=\[([^\]]+)\]__(cut=\d+_of_\d+)__(.+)$"
    for cid,v in sorted(act.items()):
        m=re.match(pattern,cid)
        if m:
            har,sp,coord,cut,_=m.groups()
            pairs[(har,coord,cut)][sp].append((seq.get(cid,"").upper(),v,cid))
    rows=[]; excluded=Counter()
    for (har,coord,cut),d in sorted(pairs.items()):
        if len(d["human"])!=1 or len(d["chimp"])!=1:
            excluded["missing_or_ambiguous"]+=1; continue
        h,ha,hid=d["human"][0]; c,ca,cid=d["chimp"][0]
        if len(h)!=171 or len(c)!=171 or set(h+c)-set(B):
            excluded["invalid_sequence"]+=1; continue
        if h==c:
            excluded["identical"]+=1; continue
        rows.append((har,coord+"|"+cut+"|"+hid+"|"+cid,h,c,ha,ca))
    return rows,float(np.percentile(neg,75)),{"synthetic":False,"negative_controls":len(neg),"excluded":dict(excluded),"input_hashes":{p.name:digest(p) for p in paths}}
def fit(x,y,xt,device):
    mean=x.mean(0); sd=x.std(0); sd[sd==0]=1
    z=(x-mean)/sd; t=(xt-mean)/sd; ym=y.mean()
    cpu=t@np.linalg.solve(z.T@z+np.eye(z.shape[1]),z.T@(y-ym))+ym
    if device=="cpu": return cpu,0.
    import torch
    if not torch.cuda.is_available(): raise RuntimeError("No CUDA available; use CPU")
    Z=torch.as_tensor(z,dtype=torch.float64,device="cuda")
    T=torch.as_tensor(t,dtype=torch.float64,device="cuda")
    Y=torch.as_tensor(y-ym,dtype=torch.float64,device="cuda")
    w=torch.linalg.solve(Z.T@Z+torch.eye(z.shape[1],dtype=torch.float64,device="cuda"),Z.T@Y)
    gpu=(T@w+ym).cpu().numpy()
    gap=float(np.max(np.abs(gpu-cpu)))
    if gap>1e-7: raise RuntimeError(f"CPU/CUDA disagreement: {gap}")
    return gpu,gap
def metrics(y,p,b,mask):
    a=y[mask]; c=p[mask]; d=b[mask]
    if not len(a): return {"pairs":0,"gate":False}
    mae=lambda x:float(np.mean(np.abs(x)))
    m=mae(a-c); ref=mae(a-d)
    delta=a[:,0]-a[:,1]; pred=c[:,0]-c[:,1]
    dm=mae(delta-pred); dr=mae(delta)
    g1=1-m/ref if ref else None; g2=1-dm/dr if dr else None
    return {"pairs":len(a),"activity_mae":m,"constant_mae":ref,"delta_mae":dm,"zero_delta_mae":dr,
            "activity_improvement":g1,"delta_improvement":g2,
            "gate":bool(g1 is not None and g2 is not None and g1>=.1 and g2>=.1)}
def main():
    p=argparse.ArgumentParser(); q=p.add_mutually_exclusive_group(required=True)
    q.add_argument("--demo",action="store_true"); q.add_argument("--geo",type=Path)
    p.add_argument("--out",type=Path,required=True); p.add_argument("--device",choices=["cpu","cuda"],default="cpu")
    a=p.parse_args()
    if a.out.exists(): raise SystemExit("Output exists; choose a new --out directory.")
    rows,threshold,meta=demo() if a.demo else real(a.geo)
    groups=sorted({r[0] for r in rows},key=lambda s:hashlib.sha256(s.encode()).hexdigest())
    if len(groups)<5: raise ValueError("Need at least five HAR groups")
    mapping={g:i%5 for i,g in enumerate(groups)}
    f=np.array([mapping[r[0]] for r in rows])
    x=np.array([[features(r[2]),features(r[3])] for r in rows])
    y=np.array([[np.mean(r[4]),np.mean(r[5])] for r in rows])
    active=y.max(1)>=threshold
    pred=np.empty_like(y); baseline=np.empty_like(y); gaps=[]
    for fold in range(5):
        tr=f!=fold; te=~tr
        xx=x[tr].reshape(-1,len(WORDS)); yy=y[tr].reshape(-1)
        pp,gap=fit(xx,yy,x[te].reshape(-1,len(WORDS)),a.device)
        pred[te]=pp.reshape(-1,2); baseline[te]=yy.mean(); gaps.append(gap)
    allm=metrics(y,pred,baseline,np.ones(len(rows),dtype=bool)); am=metrics(y,pred,baseline,active)
    count_ok=a.demo or int(active.sum())==386
    summary={"version":"0.1","device":a.device,"python":platform.python_version(),"numpy":np.__version__,"provenance":meta,
             "groups":len(groups),"active_threshold":threshold,"active_count_matches_prior":bool(count_ok),
             "all":allm,"active":am,"prediction_gate":bool(count_ok and allm["gate"] and am["gate"]),
             "max_cpu_cuda_difference":max(gaps) if a.device=="cuda" else None,"warning":"Prediction only; not empirical functional equivalence."}
    if a.device=="cuda":
        import torch
        summary["torch"]=torch.__version__; summary["gpu"]=torch.cuda.get_device_name()
    a.out.mkdir(parents=True)
    with (a.out/"cohort.csv").open("w",newline="") as file:
        w=csv.writer(file); w.writerow(["har","pair","human_sequence","chimp_sequence","human_rep1","human_rep2","human_rep3","chimp_rep1","chimp_rep2","chimp_rep3"])
        for r in rows: w.writerow([*r[:4],*r[4],*r[5]])
    with (a.out/"predictions.csv").open("w",newline="") as file:
        w=csv.writer(file); w.writerow(["har","pair","fold","active","human_observed","chimp_observed","human_predicted","chimp_predicted","observed_delta","predicted_delta"])
        for i,r in enumerate(rows): w.writerow([r[0],r[1],f[i],active[i],*y[i],*pred[i],y[i,0]-y[i,1],pred[i,0]-pred[i,1]])
    (a.out/"summary.json").write_text(json.dumps(summary,indent=2))
    print(json.dumps(summary,indent=2))
if __name__=="__main__": main()
