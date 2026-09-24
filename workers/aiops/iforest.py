"""Isolation Forest challenger adapter (SRS 7.1/7.2 slice).

Same event contract as the statistical baseline. Requires scikit-learn;
when unavailable, reports unavailable and the baseline remains the
demonstrator. A challenger only replaces the baseline after a measured
win under the same frozen protocol.
"""

from __future__ import annotations

CHALLENGER_VERSION = "iforest-1.0"


def available() -> bool:
    try:
        import sklearn  # noqa: F401
        return True
    except Exception:
        return False


def detect(windows: list[dict], threshold: float = 0.72) -> dict:
    if not available():
        return {"detector_version": CHALLENGER_VERSION, "status": "unavailable",
                "score_semantics": "normalized_anomaly_score_not_probability"}
    raise NotImplementedError("wire to frozen benchmark before use")
