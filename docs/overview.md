# miniature-train — engineering baseline MT-SRS-WBS-001 v1.0

Source: `C:\Users\HP\Downloads\miniature-train_SRS_WBS.md` (proposed, not implemented claims).

- R1 core platform + R2 advanced platform are the baseline; R3 copilot optional.
- Reference workload: retail demand forecasting API (synthetic, non-personal).
- Key contracts: `packages/contracts/openapi-v1.yaml`, `packages/contracts/events/`, `packages/contracts/schemas/`.
- Lineage: Deployment → ModelVersion → PipelineRun → Snapshot + Features + Commit + Lock → Evaluation → Approval.
- Verification: `python -m pytest -q` (NFR-013).
