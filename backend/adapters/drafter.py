"""Adapter that bridges the Drafter core to the Hub."""

from pathlib import Path
from typing import Any

import yaml

from agents.drafter.Drafter import AgentConfigurationError, DRAFTER

__all__ = ["DrafterAdapter", "AgentConfigurationError"]

MANIFEST_PATH = Path(__file__).resolve().parents[2] / "agents" / "drafter" / "agent.yaml"


class DrafterAdapter:
    """Exposes Drafter's document drafting through the adapter contract."""

    def metadata(self) -> dict[str, Any]:
        return yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8"))

    def health(self) -> dict[str, Any]:
        return DRAFTER.status()

    def run(self, request: dict[str, Any]) -> dict[str, Any]:
        return DRAFTER.respond(request.get("session_id"), request.get("message", ""))
