# C2G return-direction pilot v0.2 — independence and common-mode failure

26 November 2026. Exploratory CPU experiment, not peer reviewed. Builds on the immutable Hopper-inspired v0.1 and Paper 1 v9, Paper 2 v1.1, Paper 3 v0.4. No NVIDIA hardware measured. No new genomic calculation. The term Hopper-inspired describes the parallel workload and questions about shared resources, not physical SMs or native thread-block clusters.

## Reproduce

```powershell
python -m pip install numpy
python pilot.py
python gpu_baseline.py --backend cpu --size 16 --repeats 5 --out cpu_smoke.json
```

Python 3, NumPy. `pilot.py` regenerates `results.csv`; `run.log` is its captured output. `cpu_smoke.json` checks the separate device benchmark scaffold on CPU (timings are illustrative, machine dependent). `gpu_baseline.py` can be run on a CUDA-equipped machine using a compatible CuPy wheel; see GPU_PROTOCOL.md. The GPU branch was not executed here.

## Question and scope

Can separation of verification dependencies improve detection without increasing the nominal staged-operand or matrix-product budget? Compare four logical architectures, 64 products in groups of eight, 30 seeds, 8x8 integer matrices. Every architecture allocates 16 staged A copies (primary and standby), 72 matrix products, eight group routers and nominally two root copies (some unused). These are matched counts, NOT matched area, energy, storage traffic, root acquisition, additions, coordination cost, or equal effective source redundancy. The separate-root configuration assumes an initially identical second logical source with independently injectable corruption; genuine independence is an external requirement, not proved by copying an array. No independence is assumed for B. The checksum and duplicate comparator are established engineering techniques, not new inventions.

- shared_parity: data and parity use the same staged primary.
- separate_stage_parity: parity uses the standby staged from the same upstream root.
- separate_root_parity: parity and standby use a separate logical root.
- selective_duplicate: the same extra matrix-product budget is spent recomputing just one selected tile per group from the standby of the same upstream root; not a state-of-the-art ABFT comparison.

The 17 event families (including fault-free) are specified in code. Enumerate all single compute sites, all group sites for named cases, selected paired faults, and global root events; repeat across seeds. 7,680 fault-free output checks and 33,000 modeled fault trials, not random hardware samples or exhaustive two-fault enumeration. Faults are deterministic injections; site/event probabilities are unknown. Missing output means unavailable. Wrong means present and unequal to test harness gold. Unflagged wrong means an incorrect output outside any flagged scope, NOT an accepted result. Flagged output count includes correct outputs within a flagged scope, so a flag is not localization or correction. A parity recovery after an identified erasure satisfies the checksum by construction. Checked scope only denotes the operation performed, not proof of correctness. No fail-closed policy or automatic silent-error repair is implemented. The golden array is an evaluation oracle, never a recovery input. No global power, physical fault, energy or throughput measurements.

## Selected results

Mean unflagged wrong outputs per named trial (not expected field failure rates):

| Fault scenario | Shared parity | Separate stage | Separate root | Selective duplicate |
|---|---:|---:|---:|---:|
| One compute corruption | 0 | 0 | 0 | 0.875 |
| One staged primary corruption | 8 | 0 | 0 | 7 |
| Primary root corruption | 64 | 64 | 0 | 64 |
| Both roots identically corrupt | 64 | 64 | 64 | 64 |
| One shared B corruption | 1 | 1 | 1 | 1 |
| Opposing compute errors | 2 | 2 | 2 | 1 |
| Primary corruption + unavailable check | 8 | 8 | 8 | 8 |

All three parity variants recover every single known compute erasure; the selective duplicate leaves 0.875 missing tiles per such trial. For the specified two erasures (first two tiles of one group), parity leaves two missing; selective duplicate leaves one missing. This pair selection favors the duplicate comparator and does not generalize to arbitrary pairs. A router outage loses all eight tiles for every configuration. Separate-root parity flags all 64 data outputs when just its verification root is corrupted, although all data outputs are correct. A corrupt checksum alone flags eight correct outputs for parity or one for selective duplication. A gate that rejects flagged outputs would incur availability cost; no such gate is modeled. Opposing equal-magnitude errors evade a simple sum. These limitations are as important as the positive finding.

## Interpretation

The same nominal component/product counts do not guarantee equivalent protection: dependency placement matters. Separation at one layer protects against some local failures but fails when paths share an upstream cause. A distinct logical verification source detects primary-root corruption in this model, not necessarily in real hardware. The result is a mathematical consequence of the fault model and checksum algebra, not a novel universal law or measured GPU reliability. Comparing source diversity at matched count generates a biological question (not biological evidence), and the common-mode failure gives an illustrative analogy for multi-model scientific review (not measured AI error dependence).

## Files and next steps

- `REVISION_PLAN.md`: three bounded manuscript insertions and prospective biological/education tests.
- `GPU_PROTOCOL.md`: actual-device measurement protocol and next gate.
- `gpu_baseline.py`: high-level GPU benchmark scaffold; CPU smoke-tested only.
- `results.csv`: all event-specific means and worst unflagged wrong outputs; not aggregated across unequally sampled event families.

NVIDIA Hopper tuning guide: https://docs.nvidia.com/cuda/hopper-tuning-guide/index.html. NVIDIA Hopper architecture: https://developer.nvidia.com/blog/nvidia-hopper-architecture-in-depth/. Huang and Abraham (1984), Algorithm-Based Fault Tolerance for Matrix Operations, https://doi.org/10.1109/TC.1984.1676475. C2G: https://github.com/RandoSY/circuits-to-genomes.
