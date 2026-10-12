# Benchmark calibration

Run a representative workload on target hardware, record median runtime and exact workload configuration, then compare it with the simulator estimate. A simple calibration factor is `measured_seconds / predicted_seconds`; validate it on separate workloads before trusting it. A single factor will not generalize across all batch sizes, model shapes, and memory-bound workloads.
