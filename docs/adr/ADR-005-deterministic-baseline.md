# ADR-005 — Deterministic rules stay when ML arrives

Date: 2026-09-27
Status: accepted

The learned detector runs alongside deterministic health rules, never instead
of them. Two alert paths cost more to manage but preserve a fallback and a
measured baseline for every detector release.
