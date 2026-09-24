"""Seeded retail-demand generator (SRS 7.3, WBS 3.1 slice).

Generates >=12 weeks of hourly observations for 10 product/store series
(~20,160 rows), with known seasonality and controlled promotion effects.
Pure stdlib + deterministic seed. No leakage: splits are time-ordered with
a one-hour label-horizon purge at boundaries.

Columns: series_id, event_time (UTC ISO), orders, promotion_known_at,
hour, day_of_week, is_weekend, on_promotion.
Target for training (derived, not stored): orders at t+1 using values
available at or before prediction timestamp t.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

GENERATOR_VERSION = "demand-gen-0.1.0"
SERIES_IDS = [f"store_{s}_sku_{p}" for s in (1, 2) for p in (1, 2, 3, 4, 5)]
HOURS_TOTAL = 12 * 7 * 24  # 2016 per series
START = datetime(2026, 1, 5, 0, 0, 0, tzinfo=timezone.utc)  # a Monday

# Split by week index (0-based): weeks 1-8 train, 9-10 val, 11-12 holdout.
TRAIN_WEEKS = set(range(0, 8))
VAL_WEEKS = set(range(8, 10))
TEST_WEEKS = set(range(10, 12))
HOURS_PER_WEEK = 7 * 24


@dataclass(frozen=True)
class SeriesParams:
    base: float
    daily_amp: float
    weekly_uplift: float
    promo_lift: float
    noise_std: float


def _series_params(rng: random.Random) -> dict[str, SeriesParams]:
    params: dict[str, SeriesParams] = {}
    for i, sid in enumerate(SERIES_IDS):
        params[sid] = SeriesParams(
            base=18.0 + 2.0 * i,
            daily_amp=6.0 + 0.4 * (i % 3),
            weekly_uplift=4.0 if i % 2 == 0 else 7.0,
            promo_lift=9.0 + float(i % 4),
            noise_std=2.0,
        )
    return params


def assign_split(event_time: datetime) -> str:
    """Time-ordered split; raises if outside the 12-week range."""
    delta_h = int((event_time - START).total_seconds() // 3600)
    if not 0 <= delta_h < HOURS_TOTAL:
        raise ValueError(f"event_time out of range: {event_time.isoformat()}")
    week = delta_h // HOURS_PER_WEEK
    if week in TRAIN_WEEKS:
        return "train"
    if week in VAL_WEEKS:
        return "validation"
    return "test"


def is_purge_hour(event_time: datetime) -> bool:
    """Last hour of train/val whose t+1 label crosses into the next split."""
    delta_h = int((event_time - START).total_seconds() // 3600)
    hour_in_week = delta_h % HOURS_PER_WEEK
    week = delta_h // HOURS_PER_WEEK
    return hour_in_week == HOURS_PER_WEEK - 1 and week in (7, 9)


def generate_rows(seed: int) -> list[dict]:
    rng = random.Random(seed)
    params = _series_params(rng)
    # Promotion schedule derived deterministically from seed + series index.
    rows: list[dict] = []
    for idx, sid in enumerate(SERIES_IDS):
        p = params[sid]
        for h in range(HOURS_TOTAL):
            ts = START + timedelta(hours=h)
            hour = ts.hour
            dow = ts.weekday()  # Mon=0
            is_weekend = dow >= 5
            # Seeded promotion: ~5% of days, known 24h in advance.
            promo_day = ((h // 24) * 7 + idx * 13 + seed) % 20 == 0
            on_promo = promo_day and 9 <= hour <= 20
            daily = p.daily_amp * math.sin(2 * math.pi * (hour - 9) / 24.0)
            weekly = p.weekly_uplift if is_weekend else 0.0
            promo = p.promo_lift if on_promo else 0.0
            noise = rng.gauss(0.0, p.noise_std)
            orders = max(0, int(round(p.base + daily + weekly + promo + noise)))
            promo_known_at = (ts - timedelta(hours=24)).isoformat().replace("+00:00", "Z")
            rows.append(
                {
                    "series_id": sid,
                    "event_time": ts.isoformat().replace("+00:00", "Z"),
                    "orders": orders,
                    "promotion_known_at": promo_known_at,
                    "hour": hour,
                    "day_of_week": dow,
                    "is_weekend": int(is_weekend),
                    "on_promotion": int(on_promo),
                    "split": assign_split(ts),
                    "purge_excluded": int(is_purge_hour(ts)),
                }
            )
    rows.sort(key=lambda r: (r["event_time"], r["series_id"]))
    return rows


def write_dataset(seed: int, out_csv: Path, out_manifest: Path) -> dict:
    rows = generate_rows(seed)
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    digest = hashlib.sha256(out_csv.read_bytes()).hexdigest()
    manifest = {
        "generator": GENERATOR_VERSION,
        "seed": seed,
        "rows": len(rows),
        "series": SERIES_IDS,
        "columns": list(rows[0].keys()),
        "start": START.isoformat().replace("+00:00", "Z"),
        "digest_sha256": digest,
        "splits": {
            "train": "weeks 1-8",
            "validation": "weeks 9-10",
            "test": "weeks 11-12 (final holdout, use once)",
            "purge": "one-hour label-horizon purge at train/val boundaries",
            "leakage_controls": "time-ordered only; no random row split; promotion known 24h ahead",
        },
    }
    out_manifest.parent.mkdir(parents=True, exist_ok=True)
    out_manifest.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main() -> None:
    ap = argparse.ArgumentParser(description="Generate seeded demand dataset")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out", default="data/demand.csv")
    ap.add_argument("--manifest", default="data/manifest.json")
    args = ap.parse_args()
    m = write_dataset(args.seed, Path(args.out), Path(args.manifest))
    print(json.dumps({"rows": m["rows"], "digest": m["digest_sha256"][:12]}))


if __name__ == "__main__":
    main()
