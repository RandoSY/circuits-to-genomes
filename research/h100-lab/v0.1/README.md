# From PDP-8 to Hopper — C2G experimental laboratory v0.1
**26 November 2026 | Exploratory companion study | Randall S. Young, Ed.S.**

## Start here (Windows)
1. Extract the ZIP into a directory.
2. Double-click `RUN_WINDOWS.bat`. Requires Python 3.10+; no packages, internet, GPU or paid account needed.
3. Your browser opens `results/report.html`. The data are CSV files in `results/`.

Or use PowerShell in the extracted directory:
```powershell
python .\lab.py
```
Linux/macOS: `bash run.sh`. The included `baseline_results/report.html` can be opened immediately without running anything. This is a verified CPU run, not an H100 run.

## Why this experiment exists
Paper 1 (Architectural Economy v9) tests reuse, fault concentration and the costs of coordination in synthetic networks and a PDP-8 instruction-level model. Paper 2 investigates regulatory functional continuity in primate enhancer data. Paper 3 v0.4 makes the reciprocal direction explicit: biological observations can motivate new questions in computing. This lab asks whether a deliberately abstract parallel dataflow architecture can reproduce the architectural trade-off under two distinct fault models, then whether the same functional portfolio can be executed and compared on real GPUs. It is a **new exploratory experiment**, not an exact replication of Paper 1 and not evidence of biological-to-engineering transfer by itself.

### Stage A: CPU, already executed
- Fixed 12 Boolean inputs, all 4,096 input states, 16 seeded three-input motifs; 8, 16 and 32 outputs. Thirty matched seeds at each size.
- Each output integrates two distinct motifs using AND or XOR. All four designs have identical fault-free output maps. Dedicated: private copies. Shared: maximal reuse. Modular: fan-out capped at four. Buffered: modular primary and shadow motif copies combined by explicit OR gates for groups serving at least two outputs.
- Fault each internal node separately, including output nodes and backup coordinators. Stuck-at-zero and inversion are separate models. A fault persists for the full truth-table sweep. Inputs and interconnect edges are not faulted; multiple simultaneous faults are not modeled.
- Blast radius is the count of outputs that disagree on at least one input. Wrong fraction is the fraction of all input/output pairs that disagree. Static cost counts abstract internal nodes and directed input dependencies. It is not area, transistor count, execution time, wattage, or real fault probability.
- Every architecture is checked against the dedicated truth table. This is an equivalence check against a common implementation, not an independently constructed oracle. All site metrics weight sites equally within a design, then seeds equally; different architectures have different site counts. Report both motif-only and all-site disruption to reveal coordinator liability. Paired differences use seed as the unit, with descriptive SD, not significance claims.

### Recorded initial findings (K=32, 30 seeds)
| Design | Mean internal nodes | Mean motif blast (stuck0) | Mean all-site blast (stuck0) | Mean all-site blast (invert) |
|---|---:|---:|---:|---:|
| Dedicated | 96.0 | 0.941 | 0.941 | 1.000 |
| Shared | 47.9 | 3.795 | 1.886 | 2.006 |
| Modular | 54.2 | 2.718 | 1.667 | 1.773 |
| Buffered | 89.6 | 0.108 | 1.008 | 2.395 |

The OR backup is well suited to a zero-clamp fault but not necessarily an inversion. Including its own failures removes the apparent all-site robustness advantage here. This is an example of the architecture/fault-model interaction; it does not imply actual H100 reliability. The calculations were executed in the supplied Python code, not independently replicated. See `baseline_results/manifest.json` for the run details.

### Stage B: actual CUDA device (optional; not run here)
NVIDIA's Hopper tuning guide documents thread-block clusters, distributed shared memory, and the Tensor Memory Accelerator. These motivate hierarchy and coordination hypotheses. This first GPU benchmark deliberately uses portable integer operations rather than Hopper-specific instructions. It validates functional continuity and tests performance of a software-visible implementation, **not** Hopper's physical circuitry.

1. Use a machine or rented notebook with an NVIDIA CUDA GPU. Run `nvidia-smi`. Start on a GPU you already have or a free/low-cost instance; an H100 is not required for an initial correctness test.
2. Install a CUDA-enabled PyTorch build appropriate for the available driver using the official selector: https://pytorch.org/get-started/locally/ . In hosted environments PyTorch may already be installed. Check `python -c "import torch; print(torch.cuda.is_available())"`.
3. Copy the extracted directory and run:
```bash
python gpu_validate.py --seed 0 --k 32 --repeat 20 --batch-repeat 16
```
4. Save `gpu_results/` (device manifest, raw timings, summary, driver information) per device. Use the same parameters on another GPU, e.g. A100 and H100, to compare portability and measured timings. Repeat with several seeds and batch sizes; record clocks, device configuration, driver and software. Compare identical workloads and don't equate compute capability with speed.
5. If the test fails, preserve the error and stop. No cloud resources are provisioned automatically. Do not spend money until Stage A and a low-cost GPU test are understood.

The CUDA benchmark preallocates graph workspace and index tensors; intermediate PyTorch ops still allocate temporary tensors. It checks exact output equality to the CPU truth table, warms up, rotates timing order, and uses CUDA events. Workspace bytes exclude temporaries and allocator overhead. Timings are for the particular implementation; do not claim pure arithmetic latency, Tensor Core performance, hardware fault tolerance or architectural energy economy. This GPU script has been syntax-checked, not executed on a CUDA device.

## Stage C: return from genomes to circuits (prospective)
Read `PROTOCOL.md` before making claims. The return direction requires a biological mechanism to generate a distinct engineering design and an independently testable prediction. OR backups are a baseline, not a novel biological invention. Compare interaction-aware compensation, distributed redundancy and cost-matched baselines. Do not claim reciprocal transfer until the new design is tested.

## Contents
- `lab.py`, `RUN_WINDOWS.bat`, `run.sh` — CPU experiment
- `gpu_validate.py` — optional GPU validation
- `baseline_results/` — genuine CPU run, including all fault sites, seed metrics, paired contrasts, summary and HTML report
- `PROTOCOL.md` — prospective experiments, evidence boundaries, references
- `SHA256SUMS.txt` — integrity manifest (excluding itself)

This package is a local review checkpoint. It does not modify the C2G repository or any manuscript. The next decision is whether the abstract model is appropriate before investing in hardware measurements.
