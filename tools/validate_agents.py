"""Validate the agent registry and manifests for consistency.

Usage::

    python tools/validate_agents.py

Exit code 0 means the registry and every manifest are valid and consistent.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = REPOSITORY_ROOT / "registry" / "agents.yaml"

VALID_STATUSES = {"idea", "building", "ready", "featured", "maintenance", "retired"}
REQUIRED_MANIFEST_FIELDS = {"id", "name", "version", "status", "entrypoint"}


def _load_yaml(path: Path) -> Any:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as error:
        raise ValueError(f"Malformed YAML in {path}: {error}") from error


def validate() -> list[str]:
    """Return a list of validation errors (empty means valid)."""
    errors: list[str] = []

    try:
        registry = _load_yaml(REGISTRY_PATH)
    except ValueError as error:
        return [str(error)]

    agents = registry.get("agents") if isinstance(registry, dict) else None
    if not isinstance(agents, list):
        return ["registry must contain an 'agents' list"]

    seen_ids: set[str] = set()
    for agent in agents:
        if not isinstance(agent, dict):
            errors.append("registry contains a non-mapping agent entry")
            continue

        agent_id = agent.get("id")
        if not agent_id:
            errors.append("registry contains an agent entry without an id")
            continue

        # Duplicate IDs.
        if agent_id in seen_ids:
            errors.append(f"duplicate agent id: {agent_id}")
        seen_ids.add(agent_id)

        # Invalid lifecycle status.
        status = agent.get("status")
        if status not in VALID_STATUSES:
            errors.append(f"agent '{agent_id}' has invalid status: {status!r}")

        # Missing / nonexistent entrypoint (relative to repository root).
        entrypoint = agent.get("entrypoint")
        if not entrypoint:
            errors.append(f"agent '{agent_id}' is missing an entrypoint")
        elif not (REPOSITORY_ROOT / entrypoint).exists():
            errors.append(f"agent '{agent_id}' entrypoint does not exist: {entrypoint}")

        # Manifest checks.
        manifest_rel = agent.get("manifest")
        if not manifest_rel:
            errors.append(f"agent '{agent_id}' is missing a manifest path")
            continue
        manifest_path = REPOSITORY_ROOT / manifest_rel
        if not manifest_path.exists():
            errors.append(f"agent '{agent_id}' manifest does not exist: {manifest_rel}")
            continue

        try:
            manifest = _load_yaml(manifest_path)
        except ValueError as error:
            errors.append(str(error))
            continue

        if not isinstance(manifest, dict):
            errors.append(f"agent '{agent_id}' manifest is not a mapping")
            continue

        # Malformed manifest: missing required fields.
        for field in REQUIRED_MANIFEST_FIELDS:
            if field not in manifest:
                errors.append(f"agent '{agent_id}' manifest is missing required field: {field}")

        # Registry/manifest mismatch on shared identity fields.
        for field in ("id", "name", "status"):
            if field in manifest and manifest.get(field) != agent.get(field):
                errors.append(
                    f"agent '{agent_id}' {field} mismatch: "
                    f"registry={agent.get(field)!r} manifest={manifest.get(field)!r}"
                )

        # Manifest entrypoint is relative to the agent folder.
        manifest_entrypoint = manifest.get("entrypoint")
        if manifest_entrypoint and not (REPOSITORY_ROOT / "agents" / str(agent_id) / manifest_entrypoint).exists():
            errors.append(f"agent '{agent_id}' manifest entrypoint does not exist: {manifest_entrypoint}")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        print(f"Validation failed with {len(errors)} error(s):")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("Validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
