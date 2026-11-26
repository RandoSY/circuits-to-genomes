# Actual GPU validation: staged protocol (not executed)

NVIDIA Hopper preserves the CUDA programming model and adds optional thread-block clusters, distributed shared memory and TMA (official tuning guide: https://docs.nvidia.com/cuda/hopper-tuning-guide/index.html). The CPU experiments are logical models, not implementations of those features.

## Stage A: portable actual-device baseline

Install a CuPy wheel matching the host CUDA runtime (see https://docs.cupy.dev/en/stable/install.html). On a rented or institutional H100, first record `nvidia-smi -q`, OS, driver, runtime, device name and clocks. Then run from this directory:

```
python gpu_baseline.py --backend gpu --size 64 --repeats 30 --out h100_64.json
python gpu_baseline.py --backend gpu --size 128 --repeats 30 --out h100_128.json
python gpu_baseline.py --backend gpu --size 256 --repeats 30 --out h100_256.json
```

The harness uses resident arrays and high-level CuPy batched matrix multiplication. Float32 small integer input makes exact comparison to an independent NumPy int64 oracle reasonable at these sizes; confirm normal results before timing. It reports host-wall time including launch, staging, allocations, check and synchronization, not pure kernel time; does not establish actual memory traffic, energy, cluster mapping or hardware fault rates. Software injection changes arrays, not physical circuits. CPU smoke test only; no CUDA compiler or device was available. No performance measurements from this harness should be cited as H100 results until it has actually run there. Repeat on A100 or V100 if available, with matched workload, runtime versions and settings; record unsupported features, not substitute estimated timings. Run multiple independent sessions, counterbalance order, record clock/thermal state and use a predeclared estimator.

## Stage B: native architecture experiment (future implementation)

Compare dedicated global operand loads, shared-memory tiling, and Hopper native clusters with distributed shared memory, where legal and supported; compare matched work and matrix-product precision. Use CUDA event timing and Nsight Compute profiling, including global memory traffic, occupancy, synchronization and shared-memory traffic. Compare established ABFT and duplicate/check schemes at matched cost, add independent reference sources and separate verification paths. Explicitly include common source and coordinator faults, checker corruption and multi-error cases. Measure availability and detection separately; model rates only with justified empirical weights. FP16/BF16/FP8 require format-specific accuracy and nonzero tolerances; no exact-integer equivalence claim transfers automatically. Use NVML power sampling only with appropriate workload duration and sampling caveats. Native cluster kernels, profiler measurements and physical validation are not delivered here. Stage A gives a cheap executable starting point and a gate before more ambitious GPU development.
