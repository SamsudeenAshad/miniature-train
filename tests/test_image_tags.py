"""Image pin tests (Step 82). No floating tags anywhere in manifests or Dockerfiles."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def _images():
    imgs = []
    for f in list((ROOT / "infra/k8s").glob("*.yaml")) + list((ROOT / "infra/workflows").glob("*.yaml")):
        for d in yaml.safe_load_all(f.read_text()):
            if not d:
                continue
            for key in ("containers",):
                try:
                    containers = d["spec"]["template"]["spec"][key]
                except (KeyError, TypeError):
                    try:
                        containers = d["spec"]["templates"]
                        containers = [t.get("container", {}) for t in containers if isinstance(t, dict)]
                    except (KeyError, TypeError):
                        continue
                for c in containers:
                    if isinstance(c, dict) and "image" in c:
                        imgs.append((str(f.relative_to(ROOT)), c["image"]))
    for f in (ROOT / "infra/docker").glob("*.Dockerfile"):
        for line in f.read_text().splitlines():
            if line.startswith("FROM"):
                imgs.append((str(f.relative_to(ROOT)), line.split()[1]))
    return imgs


def test_no_floating_tags():
    bad = [(f, i) for f, i in _images() if i.endswith(":latest") or ":" not in i]
    assert not bad, bad


def test_first_party_tags_uniform():
    ours = [(f, i) for f, i in _images() if i.startswith("miniature-train/")]
    assert ours, "no first-party images found"
    assert all(i.endswith(":v0.15.0") for _, i in ours), ours
