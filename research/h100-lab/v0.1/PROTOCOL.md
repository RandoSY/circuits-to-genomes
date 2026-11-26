# Prospective study protocol: extending architectural economy to AI accelerators

## Golden thread
PDP-8 evolution motivates questions about biological functional continuity. Regulatory compensation motivates questions about engineered fault tolerance. Hopper is a candidate test environment, not evidence that the analogy is true. Keep the two directions distinct: a historical analogy is not a demonstrated mechanism of transfer.

## Questions and predicted outcomes
A1: At equal Boolean portfolios, reuse reduces static node count and increases mean single-node fault blast radius relative to dedicated computation. This is partly a consequence of the construction; the magnitude and boundaries are informative, not an independent proof of a universal principle.
A2: Explicit backup coordination can reduce or eliminate a motif-only robustness advantage when all internal sites are included. Compare stuck-zero and inversion independently. Report contrary outcomes.
B1: The portable CUDA implementation preserves exact integer outputs across devices. Any mismatch rejects equivalence for that implementation/configuration.
B2: At fixed batch, task, seed, and software environment, sharing may reduce logical work while adding gather/synchronization/memory overhead. No direction of actual elapsed time is guaranteed. Measure separately from the model.
C1 (new design, not yet implemented): Replace identical OR backup with a cost-matched arrangement of complementary modules, e.g. independently encoded primary and backup computations plus explicit checking/selection. Test against private, shared, OR-buffered and conventional triplication designs. Distinguish redundancy from nonadditive interactions. Biological reporter compensation motivates this test but does not establish the proposed design.

## Decision gates
- A: exact equivalence for every seed; retain all failures. Expand seed range, motif distributions, fan-out caps, and fault types, including correlated events. Treat static cost and fault scope as modeled quantities. Compare with original Paper 1 configurations only after aligning definitions.
- B: verify exact outputs before benchmarking. Record device SKU, MIG mode, CUDA/PyTorch, drivers, clocks, workload and complete raw timing. If possible use paired seed/batch runs and report uncertainty across runs, not merely across kernel events. For architecture-level claims, use profiler counters (Nsight Compute) and controlled native CUDA C++ kernels; study thread-block clusters, TMA and shared memory using documented features. GPU model is not hardware emulator. No assertion that abstract faults correspond to real physical GPU defects. Record energy only with validated instrumentation and explicit sampling limitations.
- C: define alternative architecture and resource budget before seeing results. Compare cost vectors: operations, storage, latency, energy where measured, failure scope, correctness. Count checker, dispatcher, routing, memory and coordination liabilities. Test independent and correlated fault modes, and test workload generalization. Assess whether the bio-inspired design improves the cost/robustness frontier over conventional alternatives. If not, retain the negative result. Qualified external review required before claims of novel architectural insight.

## Record format
For each run preserve: question, code hash, dataset/seed, config, hardware, output paths, verification, result, limitation, next decision. Capture -> Analyze -> Publish. Do not use AI agreement as independent replication. Archive both positive and negative results. A paper proposal is not a fourth paper's verified result.

## Sources and context
- Young RS. Architectural Economy in Biological and Technological Systems, v9 (26 Nov 2026). Supplied manuscript, sections 6.1 and 7: matched computational portfolios, fan-in/fan-out, all-site fault scope; independent validation pending. https://github.com/RandoSY/architectural-economy
- Young RS. Functional Equivalence Mapping in Primate Enhancer Evolution, v1.1, and The Augmented Investigator, v0.4. Companion drafts, C2G master repository: https://github.com/RandoSY/circuits-to-genomes
- NVIDIA Hopper Tuning Guide, https://docs.nvidia.com/cuda/hopper-tuning-guide/ (consulted 26 Nov 2026): hierarchy, block clusters, distributed shared memory, TMA.
- NVIDIA Hopper Compatibility Guide, https://docs.nvidia.com/cuda/hopper-compatibility-guide/ (consulted 26 Nov 2026): compatibility depends on suitable GPU code/PTX and architecture-specific requirements, not universal binary portability.
- PyTorch installation: https://pytorch.org/get-started/locally/

No comprehensive literature review, peer review or actual H100 execution was conducted for this pilot. This package provides a reproducible starting point, not a publishable hardware result.
