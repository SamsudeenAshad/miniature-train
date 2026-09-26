# Risk review — post v0.23.0 (SRS 18.1)

| ID | Risk | Status after v0.23.0 |
| --- | --- | --- |
| RISK-01 | Infra sprawl delays ML/AIOps | controlled: platform manifests complete, fleet sweeps guard drift |
| RISK-02 | Synthetic telemetry unrealistic | open: seeds/load varied; real-trace option pending |
| RISK-03 | Time/episode leakage | controlled: frozen splits, purge, protected truth |
| RISK-04 | False alerts overwhelm | mitigated: persistence rule + baseline retained |
| RISK-05 | Correlation presented as causation | mitigated: limitation labeled in ranking |
| RISK-06 | Recovery worsens incident | mitigated: fencing, policy, kill switch, least-privilege executor RBAC |
| RISK-07 | Controllers fight recovery | mitigated: field ownership doc + Argo CD ignore rules |
| RISK-08 | Telemetry gaps false confidence | mitigated: health checks + action inhibition + full probe coverage |
| RISK-09 | Cross-project leak | mitigated: membership enforcement in API, tokenless pods, secret sweeps |
| RISK-10 | ML targets unachievable | open: honest shortfalls, baseline retained |
| RISK-11 | Integration breakage | controlled: pinned versions/locks, clean supply-chain audits |
| RISK-12 | Capacity overrun | mitigated: quotas + scheduling guard + namespace envelope |
| RISK-13 | Unrestorable backups | partially: reconcile tested, backup CLI real; timed restore pending cluster |
| RISK-14 | Specialist bottleneck | noted: ML/platform near limits |
| RISK-15 | Copilot leak/hallucination | n/a: R3 excluded |

New since v0.22.0: guides describe the real system; frontend units run in CI;
screens fully covered. Cluster apply remains the open proof.
In-memory API stores still pending a driver; schema is ready and tested.
Reserve: 48 PD planned; consumed ~0 (skeleton within base). All spend recorded in change-control.
