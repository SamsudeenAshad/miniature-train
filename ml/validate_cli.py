"""Validate a dataset CSV and write the quarantine report (dvc validate stage)."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def main(argv: list[str] | None = None) -> dict:
    from ml.validate import validate_rows

    ap = argparse.ArgumentParser(description="Validate dataset CSV")
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", dest="out", required=True)
    args = ap.parse_args(argv)
    with open(args.inp, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        if "orders" in r and r["orders"] != "":
            try:
                r["orders"] = int(r["orders"])
            except ValueError:
                pass
    report = validate_rows(rows)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"status": report["status"], "rows": report["rows"]}))
    return report


if __name__ == "__main__":
    main()
