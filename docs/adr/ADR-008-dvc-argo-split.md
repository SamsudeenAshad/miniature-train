# ADR-008 — DVC for reproducibility, Argo for scheduling

Date: 2026-09-27
Status: accepted

Two retry/state owners would fight: Argo owns task attempts while each task
invokes its pinned pipeline stage. DVC tracks data references and stage
definitions; it never schedules.
