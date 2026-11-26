"""First actual-device benchmark scaffold. CuPy/CUDA required only with --backend gpu.
This measures a high-level batched-matmul workload, NOT native Hopper thread-block clusters.
"""
import argparse,json,time,platform
from pathlib import Path
import numpy as np

def workload(xp,A,Q,B,mode,inj):
    # B shape: group, task, row, col. Actual device arrays are resident.
    g,k,d,_=B.shape
    X=xp.broadcast_to(A,(g,d,d)).copy(); Y=xp.broadcast_to(Q,(g,d,d)).copy()
    if inj in ('stage','both'): X[0,0,0]+=1
    if inj=='both': Y[0,0,0]+=1
    C=xp.matmul(X[:,None,:,:],B)
    if inj=='output': C[0,0,0,0]+=1
    if mode=='duplicate':
        test=xp.matmul(Y,B[:,0]); alarm=(test!=C[:,0]).any(axis=(1,2))
    else:
        Z=X if mode=='shared' else Y
        test=xp.matmul(Z,B.sum(axis=1)); alarm=(test!=C.sum(axis=1)).any(axis=(1,2))
    return C,alarm

def main():
    p=argparse.ArgumentParser();p.add_argument('--backend',choices=['cpu','gpu'],default='cpu');p.add_argument('--size',type=int,default=64);p.add_argument('--repeats',type=int,default=30);p.add_argument('--out',default='device_results.json');args=p.parse_args()
    if args.size<1 or args.size>256 or args.repeats<1: p.error('size 1..256 and repeats >=1')
    xp=np; meta={'backend':args.backend,'python':platform.python_version(),'numpy':np.__version__}
    if args.backend=='gpu':
        import cupy as xp
        dev=xp.cuda.Device(); props=xp.cuda.runtime.getDeviceProperties(dev.id)
        name=props['name']; meta.update(device=name.decode() if isinstance(name,bytes) else name,compute_capability=dev.compute_capability,cuda_runtime=xp.cuda.runtime.runtimeGetVersion(),cupy=xp.__version__)
    d=args.size; rng=np.random.default_rng(20261126)
    ai=rng.integers(-3,4,(d,d),dtype=np.int64); bi=rng.integers(-3,4,(8,8,d,d),dtype=np.int64)
    gold=ai@bi; A=xp.asarray(ai,dtype=xp.float32); Q=A.copy(); B=xp.asarray(bi,dtype=xp.float32)
    def host(x): return xp.asnumpy(x) if args.backend=='gpu' else x
    def sync():
        if args.backend=='gpu': xp.cuda.Stream.null.synchronize()
    rows=[]
    for mode in ['shared','separate','duplicate']:
        C,alarm=workload(xp,A,Q,B,mode,'none'); sync(); assert np.array_equal(host(C),gold) and not host(alarm).any()
        for inj in ['none','stage','both','output']:
            C,alarm=workload(xp,A,Q,B,mode,inj); sync(); bad=(host(C)!=gold).any(axis=(2,3))
            rows.append(dict(mode=mode,injection=inj,wrong=int(bad.sum()),flagged_groups=int(host(alarm).sum())))
        ts=[]
        for _ in range(5): workload(xp,A,Q,B,mode,'none')
        sync()
        for _ in range(args.repeats):
            sync(); t=time.perf_counter(); workload(xp,A,Q,B,mode,'none'); sync(); ts.append((time.perf_counter()-t)*1000)
        rows.append(dict(mode=mode,median_wall_ms=float(np.median(ts)),p10_wall_ms=float(np.percentile(ts,10)),p90_wall_ms=float(np.percentile(ts,90))))
    report=dict(meta=meta,size=d,repeats=args.repeats,scope='resident arrays; staging, allocations, check, host launch and synchronization; no transfers in timed section; no energy or hardware fault-rate inference',results=rows)
    Path(args.out).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__': main()
