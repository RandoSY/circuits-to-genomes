# C2G — From Genomes Back to Circuits
## Hopper-inspired architectural economy pilot v0.1 | 26 November 2026

Exploratory computational model, not a measurement of NVIDIA hardware, not peer reviewed.

### Question
Does the trade-off between shared resources and failure exposure identified in Paper 1 (Architectural Economy v9) also occur in a logical parallel matrix-computation workload? Can localized redundancy and compensation preserve output while retaining some operand-reuse savings?

### Reproduce
Windows PowerShell (or Linux):

```
python -m pip install numpy
python pilot.py
```

The script writes `results.csv` beside itself. It uses 30 deterministic random seeds, seven configurations, 64 distinct 8x8 integer matrix products per configuration. A common operand A is multiplied by each distinct B_i. Each architecture stages a different number of copies of A. The original A source, B tiles and output sinks are invariant costs and not injected sites. Groups are logical fault-containment domains, not physical SMs or literal hardware thread-block clusters. A global-sharing group of 64 is an abstract shared domain, not a legal 64-block Hopper cluster.

### Fault model
Enumerate every modeled local site once per seed: staged primary/shadow A, group router, data computation, parity computation and recovery logic when present. One detectable erasure per trial; no simultaneous faults. A router outage blocks its entire group including parity. Backup and recovery operations are modeled as ideal conditional operations except for the enumerated site failures. A parity product uses P = A @ sum(B_i); a missing C_j can be recovered as P - sum(C_i for i != j). All products use exact small integers, not FP8 or BF16 arithmetic. A separate silent-corruption test changes a single entry in one group's A, and tests whether the internally consistent parity calculation notices. Sites are weighted equally for mean blast radius, not by measured hardware failure rates. Aggregate blast is the sum of lost/corrupt output counts over sites, not an expected reliability metric. Thirty seeds check numerical behavior; they are not independent architecture samples or confidence intervals.

### Results
13,440 fault-free outputs match the reference. 19,740 local fail-stop fault injections. Dedicated: 64 A copies, mean disruption 1, worst 1. Global sharing: one A copy, mean 2.909, worst 64. Cluster 8: eight A copies, mean 2.4, worst 8. Cluster 8 + shadow + parity: 16 A copies, eight routers, eight parity computations and eight recovery units, mean 0.6154, worst 8. The combination uses 75% fewer staged A copies than the dedicated model, adds 12.5% matrix products (plus checksum additions, storage and coordination), and reduces mean blast by 38.46% under the specified equal-site model. Sum of blast over local sites is 64 versus 128 for dedicated. Worst case is eight times larger than dedicated. All eight outputs in a corrupted cluster are wrong in the silent primary-operand test; parity raises no alarm because both data and check use the same corrupted A. A global source failure, excluded from the local model, could defeat every configuration. No claim of Pareto dominance, actual power, latency, fault rates, or hardware improvement.

### Interpretation and next experiment
The pilot extends Paper 1's computational question to parallel matrix workloads. The biology-inspired framing is localized protection and compensation through alternative relationships, not a claim that biological enhancers implement linear checksums. Algorithm-based fault tolerance (ABFT) predates this study. The novelty, if any, must be established through comparison against strong engineering baselines and genuine H100 measurements. Next: implement independent, shared and clustered CUDA matrix kernels; measure time, energy, memory traffic, occupancy, synchronization overhead, numerical error and recovery on actual H100 hardware. Add independent checksum inputs, common-source faults, realistic weighting, double faults and matched-cost controls; compare A100 and H100 where feasible. Do not infer physical failure behavior from these logical injections. Keep this pilot separate from the three existing manuscripts until reviewed.

### Sources
- Young, R.S., Architectural Economy in Biological and Technological Systems, v9 (2026), sections 6–7; C2G project: https://github.com/RandoSY/circuits-to-genomes
- NVIDIA Hopper architecture in depth: https://developer.nvidia.com/blog/nvidia-hopper-architecture-in-depth/
- NVIDIA Hopper tuning guide: https://docs.nvidia.com/cuda/hopper-tuning-guide/index.html
- NVIDIA matrix multiplication background: https://docs.nvidia.com/deeplearning/performance/dl-performance-matrix-multiplication/
- Huang and Abraham (1984), Algorithm-Based Fault Tolerance for Matrix Operations: https://doi.org/10.1109/TC.1984.1676475
- NVBitFI: https://github.com/NVlabs/nvbitfi (Hopper compatibility not established here).
