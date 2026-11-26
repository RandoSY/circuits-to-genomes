"""Stage B optional: same exact portfolio on a CUDA device using PyTorch.
Measures software-visible batched Boolean dataflow, NOT physical GPU fault injection.
"""
import argparse, csv, json, statistics, subprocess, sys, time, hashlib
from pathlib import Path
from lab import graph, evaluate, DESIGNS, N, STATES

def main():
    p=argparse.ArgumentParser();p.add_argument('--seed',type=int,default=0);p.add_argument('--k',type=int,default=32);p.add_argument('--repeat',type=int,default=20);p.add_argument('--batch-repeat',type=int,default=16);p.add_argument('--out',type=Path,default=Path('gpu_results'));a=p.parse_args()
    if not(1<=a.k<=512 and 1<=a.repeat<=1000 and 1<=a.batch_repeat<=128):p.error('Parameter out of range')
    try:import torch
    except ImportError:sys.exit('PyTorch is required only for Stage B; see README.md.')
    if not torch.cuda.is_available():sys.exit('CUDA GPU not available; no benchmark produced.')
    dev=torch.device('cuda:0');props=torch.cuda.get_device_properties(dev);a.out.mkdir(parents=True,exist_ok=True)
    # Topological levels vectorized by operation. Allocation and index prep are outside timing.
    x=((torch.arange(STATES,device=dev)[:,None]>>torch.arange(N,device=dev))&1).to(torch.int32).repeat(a.batch_repeat,1)
    ref=evaluate(*graph(a.seed,a.k,'dedicated'))
    expected=torch.tensor([[((word>>s)&1) for word in ref] for s in range(STATES)],dtype=torch.int32,device=dev).repeat(a.batch_repeat,1)
    prepared={}; rows=[]
    for d in DESIGNS:
        nodes,outs=graph(a.seed,a.k,d);depth=[0]*N;groups={}
        for i,(op,args,_) in enumerate(nodes,N):
            level=1+max(depth[j] for j in args);depth.append(level);groups.setdefault((level,op),[]).append((i,args))
        stages=[]
        for (_,op),g in sorted(groups.items()):
            idx=torch.tensor([i for i,_ in g],device=dev);args=torch.tensor([j for _,j in g],device=dev).T.contiguous();stages.append((op,idx,args))
        dest=torch.tensor(outs,device=dev);work=torch.empty((len(x),N+len(nodes)),dtype=torch.int32,device=dev)
        prepared[d]=(stages,dest,work,len(nodes))
    def execute(d):
        stages,dest,work,_=prepared[d];work[:,:N]=x
        for op,idx,args in stages:
            aa=work[:,args[0]];bb=work[:,args[1]]
            if op=='andnot':z=aa&bb&(1-work[:,args[2]])
            elif op=='orand':z=(aa|bb)&work[:,args[2]]
            elif op=='and':z=aa&bb
            elif op=='xor':z=aa^bb
            elif op=='or':z=aa|bb
            else:raise ValueError(op)
            work[:,idx]=z
        return work[:,dest]
    # Verify every row; all warm-ups and timing use the same batch.
    for d in DESIGNS:
        if not torch.equal(execute(d),expected):raise RuntimeError('Mismatch '+d)
        for _ in range(5):execute(d)
    torch.cuda.synchronize()
    samples={d:[] for d in DESIGNS}
    # Rotate order to reduce simple thermal/order bias; record all repetitions.
    for i in range(a.repeat):
        for d in DESIGNS[i%4:]+DESIGNS[:i%4]:
            start=torch.cuda.Event(enable_timing=True);end=torch.cuda.Event(enable_timing=True)
            start.record();y=execute(d);end.record();end.synchronize();ms=start.elapsed_time(end)
            samples[d].append(ms);rows.append(dict(repetition=i,design=d,ms=ms,batch=len(x),outputs=a.k))
    def csvwrite(name,data):
        with (a.out/name).open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
    csvwrite('timings.csv',rows);csvwrite('summary.csv',[dict(design=d,median_ms=statistics.median(samples[d]),min_ms=min(samples[d]),max_ms=max(samples[d]),modeled_nodes=prepared[d][3],workspace_bytes=prepared[d][2].numel()*4,exact_match=True) for d in DESIGNS])
    try:smi=subprocess.run(['nvidia-smi','-q'],capture_output=True,text=True,timeout=20).stdout
    except (OSError,subprocess.TimeoutExpired):smi='nvidia-smi unavailable'
    (a.out/'nvidia-smi.txt').write_text(smi,encoding='utf-8')
    meta=dict(device=props.name,compute_capability=f'{props.major}.{props.minor}',total_memory=props.total_memory,torch=torch.__version__,cuda_build=torch.version.cuda,seed=a.seed,k=a.k,repetitions=a.repeat,batch_repeat=a.batch_repeat,exact_match=True,gpu_script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),lab_sha256=hashlib.sha256(Path(__file__).with_name('lab.py').read_bytes()).hexdigest(),scope='PyTorch integer dataflow; timing includes kernel launches and intermediate allocation; not Tensor Core throughput, physical fault injection, or energy measurement')
    (a.out/'manifest.json').write_text(json.dumps(meta,indent=2),encoding='utf-8');print(json.dumps(meta,indent=2));print('Results:',a.out)
if __name__=='__main__':main()
