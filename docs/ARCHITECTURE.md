# Architecture

- `config.py`: validated JSON profile loading.
- `inventory.py` and `models.py`: logical rack and compact slotted device/job models.
- `workloads.py`: workload presets and analytical compute/memory/interconnect estimates.
- `scheduler.py`: FIFO GPU placement, memory reservation, job completion, and resource release.
- `power.py`: utilization-based power and first-order thermal estimates.
- `engine.py`: simulation clock and telemetry aggregation.
- `api.py` and `dashboard/index.html`: optional REST interface and operator UI.
- `benchmarks.py`: prediction-vs-measurement error summaries.

The simulator is not cycle accurate and does not model proprietary kernels, cache hierarchies, switch packet routing, or validated facility thermal behavior.
