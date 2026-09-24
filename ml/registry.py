"""Model registry: immutable versions, aliases pin resolved numeric version (FR-011 slice)."""

from __future__ import annotations

_registry: dict[int, dict] = {}
_aliases: dict[str, int] = {}
_next_version = 1


def reset() -> None:
    global _registry, _aliases, _next_version
    _registry, _aliases, _next_version = {}, {}, 1


def register(artifact_digest: str, run_id: str, model_card: dict) -> dict:
    global _next_version
    v = _next_version
    _next_version += 1
    entry = {"version": v, "artifact_digest": artifact_digest, "run_id": run_id, "model_card": model_card}
    _registry[v] = entry
    return entry


def set_alias(alias: str, version: int) -> None:
    if version not in _registry:
        raise KeyError(f"unknown version {version}")
    _aliases[alias] = version


def resolve(alias_or_version: str | int) -> dict:
    if isinstance(alias_or_version, int):
        return _registry[alias_or_version]
    return _registry[_aliases[alias_or_version]]


def get_running_version(pinned_version: int) -> dict:
    """Running service stays pinned; alias moves do not change it."""
    return _registry[pinned_version]
