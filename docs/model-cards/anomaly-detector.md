# Model card — operational anomaly detector (stat baseline 1.0)

- Inputs: 60s windows (rate, error ratio, p95, cpu, mem, queue) vs healthy history.
- Output: normalized anomaly score (not a probability) + threshold + deviations.
- Trigger: 2-of-3 windows over threshold; cold start <24h history → learned unavailable.
- Benchmark targets: recall ≥0.80, precision ≥0.75, ≤2 false/24h, median ≤120s, p95 ≤180s (held-out, unmeasured here).
- Challenger: Isolation Forest only on measured frozen win.
