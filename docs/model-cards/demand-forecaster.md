# Model card — retail demand forecaster (candidate 1.0)

- Lineage: snapshot digest → features `demand-features-1.0` → run seed 42 → evaluation → gates → registry.
- Baseline: seasonal-naive (168h); candidate: + per-series promo lift.
- Metrics: validation MAE vs baseline, per-series slices, n reported in eval bundle.
- Thresholds: ≥10% MAE gain, no series >5% worse; final holdout used once.
- Limits: synthetic data; short pilot; no business-accuracy claim.
