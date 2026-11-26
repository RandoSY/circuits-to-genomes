"""C2G Hopper-inspired logical fault model. No GPU required. Python 3 + NumPy."""
import csv, json
from pathlib import Path
import numpy as np
N=64; D=8; SEEDS=30
ROOT=Path(__file__).resolve().parent

def trial(seed, group, shadow=False, parity=False):
    rng=np.random.default_rng(seed)
    A=rng.integers(-3,4,(D,D),dtype=np.int64)
    B=rng.integers(-3,4,(N,D,D),dtype=np.int64)
    gold=A@B
    groups=[list(range(i,i+group)) for i in range(0,N,group)]
    # independently staged copies of A; common original source excluded from local scope
    sites=[]
    for j,g in enumerate(groups):
        sites.append(('A-primary',j))
        if shadow: sites.append(('A-shadow',j))
        if group>1 or shadow: sites.append(('router',j))
        if parity: sites += [('parity-compute',j),('recovery',j)]
    sites += [('compute',i) for i in range(N)]
    # Independent B tiles and output sinks are invariant costs, excluded from local fault scope.
    def run(fault=None, silent=False):
        out=[None]*N; alarms=0
        for j,g in enumerate(groups):
            if fault==('router',j): continue
            X=A.copy()
            if fault==('A-primary',j):
                if silent: X[0,0]+=1
                elif not shadow: continue
                # detectable primary erasure uses separately staged shadow
            for i in g:
                if fault==('compute',i): continue
                out[i]=X@B[i]
            if parity and fault!=('parity-compute',j):
                P=X@B[g].sum(axis=0)
                missing=[i for i in g if out[i] is None]
                if len(missing)==1 and fault!=('recovery',j):
                    out[missing[0]]=P-sum((out[i] for i in g if out[i] is not None),np.zeros((D,D),dtype=np.int64))
                if all(out[i] is not None for i in g):
                    alarms+=int(not np.array_equal(P,sum((out[i] for i in g),np.zeros((D,D),dtype=np.int64))))
        wrong=sum(x is None or not np.array_equal(x,gold[i]) for i,x in enumerate(out))
        return wrong,alarms
    assert run()==(0,0)
    rows=[(kind,run((kind,i))[0]) for kind,i in sites]
    # A fault shared by compute and parity may escape algebraic consistency checks.
    silent_wrong, silent_alarm=run(('A-primary',0),silent=True)
    return dict(copies=len(groups)*(1+shadow),routers=len(groups) if group>1 or shadow else 0,
                parity_tiles=len(groups) if parity else 0, recovery_units=len(groups) if parity else 0,
                sites=len(sites),mean=np.mean([v for _,v in rows]),worst=max(v for _,v in rows),
                sum_blast=sum(v for _,v in rows),compute_blast=np.mean([v for k,v in rows if k=='compute']),
                primary_blast=np.mean([v for k,v in rows if k=='A-primary']),
                router_blast=np.mean([v for k,v in rows if k=='router']) if group>1 or shadow else None,
                silent_wrong=silent_wrong,silent_alarm=silent_alarm)

def main():
    cases=[('Dedicated',1,False,False),('Global share',64,False,False),('Cluster 4',4,False,False),('Cluster 8',8,False,False),('Cluster 8 + shadow',8,True,False),('Cluster 8 + parity',8,False,True),('Cluster 8 + both',8,True,True)]
    results=[]
    for name,g,sh,pa in cases:
        vals=[trial(s,g,sh,pa) for s in range(SEEDS)]
        row=dict(architecture=name,group=g,shadow=sh,parity=pa)
        for k in vals[0]:
            row[k]=None if vals[0][k] is None else float(np.mean([v[k] for v in vals]))
        results.append(row)
    with open(ROOT/'results.csv','w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=results[0]);w.writeheader();w.writerows(results)
    print(json.dumps(results,indent=2))
    print(f'Fault-free verification: {len(cases)*SEEDS*N} output tiles; all exact.')
    print(f'Enumerated local fail-stop site injections: {int(sum(r["sites"] for r in results)*SEEDS)}.')
if __name__=='__main__': main()
