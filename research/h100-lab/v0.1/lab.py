"""C2G Stage A: exact Boolean portfolio, abstract dataflow, not a GPU emulator."""
import argparse, csv, json, random, statistics, sys, platform, html, hashlib
from pathlib import Path
N=12; STATES=1<<N; MASK=(1<<STATES)-1
INPUTS=[sum(1<<s for s in range(STATES) if s&(1<<i)) for i in range(N)]
DESIGNS=('dedicated','shared','modular','buffered')

def portfolio(seed,k):
    r=random.Random(seed)
    lib=[]
    while len(lib)<16:
        a,b,c=r.sample(range(N),3); spec=(min(a,b),max(a,b),c,r.randrange(2))
        if spec not in lib: lib.append(spec)
    tasks=[(*r.sample(range(16),2),r.randrange(2)) for _ in range(k)]
    return lib,tasks

def graph(seed,k,design,cap=4):
    lib,tasks=portfolio(seed,k); nodes=[]; outputs=[]; pools={}
    def add(op,args,role):
        nodes.append((op,tuple(args),role));return N+len(nodes)-1
    def motif(m):
        a,b,c,op=lib[m];return add('andnot' if op==0 else 'orand',(a,b,c),'motif')
    def use(m):
        pool=pools.setdefault(m,[])
        limit=1 if design=='dedicated' else k*2 if design=='shared' else cap
        if not pool or pool[-1][1]>=limit: pool.append([motif(m),0,[]])
        p=pool[-1];p[1]+=1;return p
    # Build the same portfolio, then explicitly insert backup combiners before outputs.
    refs=[(use(a),use(b),op) for a,b,op in tasks]
    if design=='buffered':
        for m,pool in pools.items():
            for p in pool:
                if p[1]>=2:
                    backup=motif(m);p[0]=add('or',(p[0],backup),'coordinator')
    for a,b,op in refs: outputs.append(add('and' if op==0 else 'xor',(a[0],b[0]),'output'))
    return nodes,outputs

def evaluate(nodes,outputs,fault=None,mode='stuck0'):
    v=INPUTS.copy()
    for i,(op,args,role) in enumerate(nodes,N):
        a,b,*c=[v[j] for j in args]
        if op=='andnot': z=a&b&(~c[0]&MASK)
        elif op=='orand': z=(a|b)&c[0]
        elif op=='and': z=a&b
        elif op=='xor': z=a^b
        elif op=='or': z=a|b
        else: raise ValueError(op)
        if i==fault: z=0 if mode=='stuck0' else z^MASK
        v.append(z)
    return [v[i] for i in outputs]

def run(seeds,ks,cap,out):
    out.mkdir(parents=True,exist_ok=True); summary=[]; raw=[]
    for k in ks:
        for seed in range(seeds):
            ref=evaluate(*graph(seed,k,'dedicated',cap))
            for design in DESIGNS:
                nodes,outputs=graph(seed,k,design,cap); actual=evaluate(nodes,outputs)
                if actual!=ref: raise AssertionError((k,seed,design,'functional mismatch'))
                for mode in ('stuck0','invert'):
                    group=[]
                    for i,(_,_,role) in enumerate(nodes,N):
                        faults=evaluate(nodes,outputs,i,mode); errors=[(a^b).bit_count() for a,b in zip(ref,faults)]
                        row=dict(k=k,seed=seed,design=design,fault=mode,node=i,role=role,blast=sum(e>0 for e in errors),wrong_fraction=sum(errors)/(k*STATES));raw.append(row);group.append(row)
                    def mean(rows,key):return statistics.mean(x[key] for x in rows) if rows else None
                    m=[x for x in group if x['role']=='motif']; c=[x for x in group if x['role']=='coordinator'];
                    summary.append(dict(k=k,seed=seed,design=design,fault=mode,nodes=len(nodes),edges=sum(len(a) for _,a,_ in nodes),coordinators=len(c),all_blast=mean(group,'blast'),motif_blast=mean(m,'blast'),coordinator_blast=mean(c,'blast'),all_wrong_fraction=mean(group,'wrong_fraction'),max_blast=max(x['blast'] for x in group)))
    def write(name,rows):
        with (out/name).open('w',newline='',encoding='utf-8') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    write('seed_metrics.csv',summary);write('fault_sites.csv',raw)
    agg=[]
    for k in ks:
        for mode in ('stuck0','invert'):
            for d in DESIGNS:
                rs=[x for x in summary if (x['k'],x['fault'],x['design'])==(k,mode,d)]
                agg.append(dict(k=k,fault=mode,design=d,**{key:statistics.mean(x[key] for x in rs) for key in ('nodes','edges','all_blast','motif_blast','all_wrong_fraction','max_blast')},all_blast_sd=statistics.stdev(x['all_blast'] for x in rs) if len(rs)>1 else 0))
    write('summary.csv',agg)
    # paired seed-level differences relative to dedicated; no pseudo-replicate significance tests
    paired=[]
    for k in ks:
        for mode in ('stuck0','invert'):
            for d in DESIGNS[1:]:
                base={x['seed']:x for x in summary if (x['k'],x['fault'],x['design'])==(k,mode,'dedicated')}
                rs=[x for x in summary if (x['k'],x['fault'],x['design'])==(k,mode,d)]
                for metric in ('nodes','all_blast','all_wrong_fraction'):
                    diffs=[x[metric]-base[x['seed']][metric] for x in rs]
                    paired.append(dict(k=k,fault=mode,design=d,metric=metric,mean_difference=statistics.mean(diffs),sd_difference=statistics.stdev(diffs) if len(diffs)>1 else 0,n_seeds=len(diffs)))
    write('paired_differences.csv',paired)
    manifest=dict(model='abstract Boolean dataflow v0.1',python=sys.version,platform=platform.platform(),seeds=list(range(seeds)),k=ks,cap=cap,states=STATES,exact_portfolio_checks=seeds*len(ks)*len(DESIGNS),fault_sites=len(raw),sha256_source=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    # offline readable report, both fault scopes visible
    rows=''.join(f"<tr><td>{a['k']}</td><td>{a['fault']}</td><td>{a['design']}</td><td>{a['nodes']:.1f}</td><td>{a['motif_blast']:.3f}</td><td>{a['all_blast']:.3f}</td><td>{a['all_wrong_fraction']:.5f}</td></tr>" for a in agg)
    (out/'report.html').write_text('''<!doctype html><meta charset="utf-8"><title>C2G Stage A</title><style>body{font:16px system-ui;max-width:1050px;margin:40px auto;padding:0 20px;color:#193438}h1,h2{color:#17695f}table{border-collapse:collapse;width:100%}td,th{padding:8px;border-bottom:1px solid #ccd8d6;text-align:right}td:nth-child(3),th:nth-child(3){text-align:left}th{background:#e8f1ee}tr:nth-child(2n){background:#f7faf9}</style><h1>From PDP-8 to Hopper</h1><p>Stage A: abstract architecture experiment, not H100 hardware measurements.</p><h2>Matched portfolios</h2><p>Each design implements identical output functions over all 4,096 inputs. Mean blast radius counts outputs that change on at least one input. All-site results include output nodes and backup combiners. Lower is better for cost and disruption; the model omits physical costs and probabilities.</p><table><thead><tr><th>Outputs</th><th>Fault</th><th>Design</th><th>Nodes</th><th>Motif blast</th><th>All-site blast</th><th>Wrong fraction</th></tr></thead><tbody>'''+rows+'</tbody></table><p>Seed-level results and all individual fault sites are available in the adjacent CSV files. No inference to hardware fault rates or biological fitness is warranted.</p>',encoding='utf-8')
    print(json.dumps(manifest,indent=2));print('Open',out/'report.html')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--seeds',type=int,default=30);p.add_argument('--k',type=int,nargs='+',default=[8,16,32]);p.add_argument('--cap',type=int,default=4);p.add_argument('--out',type=Path,default=Path('results'));a=p.parse_args()
    if not(1<=a.seeds<=1000 and all(1<=k<=512 for k in a.k) and 1<=a.cap<=512):p.error('Out of range')
    run(a.seeds,a.k,a.cap,a.out)
