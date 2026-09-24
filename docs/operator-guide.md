# Operator guide (skeleton, WBS 11.1)

1. Seed demo: `python -m ml.data_generator --seed 42 --out data/demand.csv --manifest data/manifest.json`
2. Validate: quarantine report must be `accepted` before training.
3. Train/evaluate: check gates; blocked releases stay in `proposed`.
4. Deploy: stage -> shadow -> independent approve -> promote; rollback restores pinned digest.
5. Monitor: telemetry health `degraded` inhibits actions; drift needs 500 obs.
6. Incident: correlate alerts, rank hypotheses (correlation, not causation).
7. Recover: dry-run -> approve exact plan hash -> fenced execute -> verify.
8. Kill switch: stops new mutations; in-flight verification continues.
