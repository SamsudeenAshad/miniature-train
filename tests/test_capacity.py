"""Capacity + topology tests (FR-024/031 slice)."""

from workers.aiops.capacity import recommend
from workers.aiops.topology import neighbors, update


def test_capacity_bounded_no_auto():
    r = recommend([10.0] * 10, 2, 4)
    assert r["status"] == "insufficient-data"
    r = recommend([10.0] * 24 + [15.0], 2, 4, unit_cost=0.5)
    assert r["recommendation"]["replicas"] <= 4
    assert r["auto_applied"] is False


def test_topology_expiry():
    edges: dict = {}
    update(edges, "api", "db", "trace", now=0.0)
    assert neighbors(edges, "api", now=10.0) == ["db"]
    assert neighbors(edges, "api", now=9999.0) == []
