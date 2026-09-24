# Platform requirements (cluster operators, not owned manifests)

Our manifests use CRDs owned by these controllers. Install before applying:

| CRD kind | Controller |
| --- | --- |
| Rollout, AnalysisTemplate | Argo Rollouts |
| WorkflowTemplate | Argo Workflows |
| Application | Argo CD |
| VirtualService | Istio |
| ServiceMonitor | Prometheus Operator |
| ExternalSecret, ClusterSecretStore | External Secrets Operator |

CoreDNS, object-store buckets (`miniature-train/mlflow`), and the
`platform-store` secret backend are also entry conditions (SRS ASM-04).
Versions are pinned at implementation time per SRS D-06; floating latest is not used.
