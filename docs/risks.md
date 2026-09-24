# Risk review — post v0.1.0 (SRS 18.1)

| ID | Risk | Status after v0.1.0 |
| --- | --- | --- |
| RISK-01 | Infra sprawl delays ML/AIOps | controlled: one end-to-end path first, stack frozen in docs |
| RISK-02 | Synthetic telemetry unrealistic | open: seeds/load varied; real-trace option pending |
| RISK-03 | Time/episode leakage | controlled: frozen splits, purge, protected truth |
| RISK-04 | False alerts overwhelm | mitigated: persistence rule + baseline retained |
| RISK-05 | Correlation presented as causation | mitigated: limitation labeled in ranking |
| RISK-06 | Recovery worsens incident | mitigated: fencing, policy, kill switch |
| RISK-07 | Controllers fight recovery | mitigated: reconciliation_required state |
| RISK-08 | Telemetry gaps false confidence | mitigated: health checks + action inhibition |
| RISK-09 | Cross-project leak | mitigated: per-object checks + adversarial tests |
| RISK-10 | ML targets unachievable | open: honest shortfalls, baseline retained |
| RISK-11 | Integration breakage | controlled: pinned versions/locks |
| RISK-12 | Capacity overrun | mitigated: quotas + scheduling guard |
| RISK-13 | Unrestorable backups | partially: reconcile tested; timed restore pending cluster |
| RISK-14 | Specialist bottleneck | noted: ML/platform near limits |
| RISK-15 | Copilot leak/hallucination | n/a: R3 excluded |

Reserve: 48 PD planned; consumed ~0 (skeleton within base). All spend recorded in change-control.
