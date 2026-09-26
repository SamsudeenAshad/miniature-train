# ADR-004 — Git holds desired state; rollback reconciles Git

Date: 2026-09-26
Status: accepted

The release controller owns approved digests in Git. A canary abort restores
traffic first, then the controller records the failed revision and proposes the
desired-state correction. Until Git and observed state agree, releases report
`reconciliation_required` instead of recovered.
