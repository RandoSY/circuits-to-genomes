"""Matched local fault experiments; logical integer model, NOT H100 hardware."""
from pathlib import Path
import csv
import numpy as np
N,G,D,S=64,8,8,30
ROOT=Path(__file__).resolve().parent
# All four share the same 16 staged A copies, 72 matrix products, eight routers.
# Two root copies in every case; common variants leave root Q unused by the checker.
CASES=('shared_parity','separate_stage_parity','separate_root_parity','selective_duplicate')
# Prespecified for this run: event families, not probability weights.
EVENTS={'none':[0], 'compute_erasure':range(N),'compute_corruption':range(N),
        'two_compute_erasures':range(8),'primary_erasure':range(8),
        'primary_corruption':range(8),'primary_and_shadow_erasure':range(8),
        'router_outage':range(8),'check_erasure':range(8),
        'primary_corruption_and_check_erasure':range(8),
        'root_P_corruption':[0],'root_Q_corruption':[0],'both_roots_corruption':[0],
        'shadow_corruption':range(8), 'check_corruption':range(8),
        'common_B_corruption':range(N),'opposing_compute_errors':range(8)}

def run(case, A,B, kind,idx):
    # Golden result independently retained by the test harness only.
    gold=A@B; bad=gold.copy(); missing=np.zeros(N,bool); flagged=np.zeros(N,bool)
    verified=np.zeros(N,bool); alarms=0
    P=A.copy(); Q=A.copy()
    if kind in ('root_P_corruption','both_roots_corruption'): P[0,0]+=1
    if kind in ('root_Q_corruption','both_roots_corruption'): Q[0,0]+=1
    if case!='separate_root_parity': Q=P.copy()
    for j in range(N//G):
        lo=j*G; hi=lo+G; sl=slice(lo,hi)
        primary=P.copy(); shadow=Q.copy() if case=='separate_root_parity' else P.copy()
        # Shadow fallback is detectable erasure only; no oracle for silent corruption.
        local=idx==j
        if kind=='shadow_corruption' and local: shadow[0,0]+=1
        if kind in ('primary_corruption','primary_corruption_and_check_erasure') and local: primary[0,0]+=1
        if kind=='primary_erasure' and local: primary=shadow.copy()
        if kind in ('router_outage','primary_and_shadow_erasure') and local:
            missing[sl]=True; continue
        bs=B[sl].copy()
        if kind=='common_B_corruption' and lo<=idx<hi: bs[idx-lo,0,0]+=1
        c=primary@bs; m=np.zeros(G,bool)
        if kind=='compute_erasure' and lo<=idx<hi: m[idx-lo]=True
        if kind=='two_compute_erasures' and local: m[:2]=True
        if kind=='compute_corruption' and lo<=idx<hi: c[idx-lo,0,0]+=1
        if kind=='opposing_compute_errors' and local: c[0,0,0]+=1; c[1,0,0]-=1
        check_available=not(local and kind in ('check_erasure','primary_corruption_and_check_erasure'))
        if check_available:
            if case=='selective_duplicate':
                # Matched matrix-product budget: one independently staged recompute of tile 0.
                chk=shadow@bs[0]
                if kind=='check_corruption' and local: chk[0,0]+=1
                if m[0]: c[0]=chk; m[0]=False
                if not np.array_equal(c[0],chk): flagged[lo]=True; alarms+=1
                verified[lo]=True
            else:
                x=primary if case=='shared_parity' else shadow
                check=x@bs.sum(axis=0)
                if kind=='check_corruption' and local: check[0,0]+=1
                if m.sum()==1:
                    c[m]=check-c[~m].sum(axis=0); m[:]=False
                if not m.any():
                    # A single erasure recovery makes the parity relation tautological.
                    # No claim of independent verification of the reconstructed tile.
                    if not np.array_equal(c.sum(axis=0),check): flagged[sl]=True; alarms+=1
                    verified[sl]=True
        bad[sl]=c; missing[sl]=m
    wrong=(bad!=gold).any(axis=(1,2)) & ~missing
    return np.array([wrong.sum(),missing.sum(),(wrong&~flagged).sum(),flagged.sum(),alarms,verified.sum()],dtype=np.int64)

def main():
    rows=[]; trials=0
    for case in CASES:
        for event,indices in EVENTS.items():
            metrics=[]
            for seed in range(S):
                rng=np.random.default_rng(seed)
                A=rng.integers(-3,4,(D,D),dtype=np.int64)
                B=rng.integers(-3,4,(N,D,D),dtype=np.int64)
                for i in indices: metrics.append(run(case,A,B,event,i))
            x=np.array(metrics); trials+=len(x)
            if event=='none': assert not x[:,:5].any()
            rows.append(dict(architecture=case,event=event,trials=len(x),**{k:round(v,6) for k,v in zip(('wrong','missing','unflagged_wrong','flagged_outputs','alarms','checked_scope'),x.mean(axis=0))},worst_unflagged=int(x[:,2].max())))
    with (ROOT/'results.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rows[0]); w.writeheader(); w.writerows(rows)
    print('Fault-free output checks:',len(CASES)*S*N,'; fault scenarios:',trials-len(CASES)*S)
    for row in rows:
        if row['event'] in ('primary_corruption','root_P_corruption','both_roots_corruption','common_B_corruption','compute_erasure','two_compute_erasures','opposing_compute_errors','router_outage','primary_corruption_and_check_erasure'):
            print(row['architecture'],row['event'],row['wrong'],row['missing'],row['unflagged_wrong'],row['alarms'])
if __name__=='__main__': main()
