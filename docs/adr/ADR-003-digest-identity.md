# ADR-003 — Digests are the release identity

Date: 2026-09-26
Status: accepted

Immutable digests (artifact, image, snapshot) identify releases end to end.
Mutable aliases and tags are convenience pointers only and never change a
running service.
