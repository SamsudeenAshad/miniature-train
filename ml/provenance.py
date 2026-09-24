"""Image provenance records (FR-012 slice, WBS 4.4)."""

from __future__ import annotations

import hashlib
import json


def build_record(image: str, sbom: dict, vuln: str, signer: str) -> dict:
    rec = {"image": image, "sbom_digest": hashlib.sha256(json.dumps(sbom, sort_keys=True).encode()).hexdigest(),
           "vuln": vuln, "signer": signer}
    rec["provenance_digest"] = hashlib.sha256(json.dumps(rec, sort_keys=True).encode()).hexdigest()
    rec["loadable"] = signer == "ml-pipeline" and vuln not in ("critical", "high")
    return rec
