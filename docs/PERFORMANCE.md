# Performance notes

The model uses `slots=True` data classes, prebuilt inventory arrays, and active-job iteration to keep per-tick work modest. Use larger tick intervals for long runs. Model outputs are estimates, not physical hardware benchmarks. Profile with representative runs before claiming speed improvements.
