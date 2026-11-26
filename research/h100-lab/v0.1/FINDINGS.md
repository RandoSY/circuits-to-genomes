# H100 laboratory v0.1 — findings and preservation record

**26 November 2026 | C2G | Randall S. Young, Ed.S. | Exploratory computational experiment, not peer reviewed**

## Start with the exact release

[Download the original complete laboratory ZIP](C2G_H100_Lab_v0.1.zip), extract it, and run `RUN_WINDOWS.bat` or `python lab.py`. The ZIP contains all original files, including the 32,168-row fault-site dataset and seed metrics. The original README, protocol, code, launchers, run log, manifest, descriptive summary, paired differences and HTML report are also browsable here. The full fault-site and seed-metric CSVs are inside the ZIP rather than duplicated in the tree. The original README and checksum manifest are frozen release artifacts; verify the manifest inside the extracted complete package.

The archived ZIP's Git blob identifier is `718d855f7a9e29c31a60ea273591c9fda818eb35` (160,163 bytes). Each browsable release file was also checked against its original Git blob identifier. This establishes byte preservation, not independent scientific validation.

## Observed CPU results

Thirty matched seeded portfolios at each of K=8, 16, 32 outputs; 12 binary inputs (all 4,096 states). Four logical architectures, 360 fault-free portfolio equivalence checks passed, 32,168 simulated single-node fault cases across two fault models. Output integrators and backup OR coordinators are counted as faultable sites.

| Architecture (K=32) | Mean internal nodes | Motif-only blast, stuck zero | All-site blast, stuck zero | All-site blast, inversion |
|---|---:|---:|---:|---:|
| Dedicated | 96.0 | 0.941 | 0.941 | 1.000 |
| Shared | 47.9 | 3.795 | 1.886 | 2.006 |
| Modular | 54.2 | 2.718 | 1.667 | 1.773 |
| Buffered | 89.6 | 0.108 | 1.008 | 2.395 |

Source: [summary.csv](baseline_results/summary.csv), [manifest](baseline_results/manifest.json), [paired differences](baseline_results/paired_differences.csv). Values rounded for readability. All-site blast is the mean count of outputs altered on at least one input by an internal-node fault, with equal within-design site and across-seed weights.

At K=32, shared computation uses about half the dedicated internal nodes but has greater mean modeled fault blast. Explicit OR buffering protects against motif stuck-zero faults, yet its advantage over the dedicated design disappears at all-site scope; all-site inversion disruption is larger than in any of the other three designs. The effect depends on both the architecture and fault model. These outcomes are conditioned on the chosen synthetic workload and construction; they do not prove a universal law, estimate physical GPU reliability or establish actual energy or throughput improvements.

## The golden thread

Paper 1 uses PDP-8 and synthetic computational models to motivate questions about functional continuity and coordination liability. Paper 2 examines a molecular question about primate enhancer activity. Paper 3 emphasizes preserving the reciprocal research question: biology may in turn inform computing. This experiment makes that return direction testable, but has not yet demonstrated a genuinely novel bio-inspired engineering improvement.

This Boolean-dataflow lab complements, rather than replaces, the separate [Hopper matrix pilots](../../hopper-pilot/). They use different workload constructions and must not be pooled as if they were one experiment.

## Next validation gates

- Stage A: executed CPU model; independent reproduction, expanded fault distributions and matched-budget comparisons remain open.
- Stage B: [portable CUDA validation](gpu_validate.py) supplied and syntax checked, not run on GPU. Compare exact output maps and measured performance across available devices. No H100-specific hardware measurements are claimed.
- Stage C: [prospective protocol](PROTOCOL.md) for distinct, cost-matched compensatory architectures and independently assessed evidence of biological-to-engineering transfer.

Preserve negative results. The lab is not a fourth paper and does not revise the three current manuscript baselines.
