# ADR-001 — Modular monolith with isolated workers

Date: 2026-09-24
Status: accepted (proposed baseline)

Begin with a modular control-plane application plus separate training,
inference, detection, and execution workers (SRS ADR-01). Fewer
operational components; keep module boundaries for future extraction.
