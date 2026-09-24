"""Component watchdogs + degraded rules (FR-037 slice, AT-22)."""

from __future__ import annotations


def watchdog(detector_ok: bool, registry_ok: bool, db_ok: bool, telemetry_ok: bool) -> dict:
    learned_stale = not detector_ok
    pause_promotion = not registry_ok or not telemetry_ok
    no_approvals_actions = not db_ok
    deterministic_alerts = telemetry_ok  # independent path when its own deps healthy
    disable_unsafe = not (detector_ok and telemetry_ok)
    degraded = not (detector_ok and registry_ok and db_ok and telemetry_ok)
    return {
        "learned_stale": learned_stale,
        "pause_promotion": pause_promotion,
        "no_approvals_actions": no_approvals_actions,
        "deterministic_alerts": deterministic_alerts,
        "disable_unsafe_changes": disable_unsafe,
        "degraded": degraded,
    }


def perf_report(topology: str, versions: dict, load: dict, intervals: list[dict]) -> dict:
    required = ("warmup_s", "duration_s", "rps", "payload_kb")
    missing = [k for k in required if k not in load]
    if missing:
        raise ValueError(f"missing_load_field:{missing}")
    return {"topology": topology, "versions": versions, "load": load, "intervals": intervals, "p50_p95_p99": None}
