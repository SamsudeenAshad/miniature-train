"""Snapshot a dataset CSV with manifest (dvc snapshot stage)."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def main(argv: list[str] | None = None) -> dict:
    from ml.snapshot import snapshot_dataset

    ap = argparse.ArgumentParser(description="Snapshot dataset CSV")
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", dest="out", required=True)
    ap.add_argument("--source", default="synthetic:demand-gen")
    args = ap.parse_args(argv)
    with open(args.inp, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    manifest = snapshot_dataset(rows, source=args.source, out_dir=Path(args.out))
    print(json.dumps({"digest": manifest["content_digest"][:12], "rows": manifest["row_count"]}))
    return manifest


if __name__ == "__main__":
    main()
