# ADR-002 — PostgreSQL job/outbox, no Kafka at pilot scale

Date: 2026-09-26
Status: accepted

Control events flow through a Postgres job/outbox table with at-least-once
delivery and consumer dedup by event ID. Kafka is deferred until measured
throughput or replay needs demand it.
