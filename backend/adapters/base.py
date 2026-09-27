"""Adapter contract shared by every agent integration.

Each agent exposes a small, stable surface to the Hub so the backend never
imports an agent's internal framework directly. An adapter bridges an agent's
core implementation to the Hub with three operations:

- ``metadata`` — the agent's manifest (identity, status, inputs, outputs).
- ``health`` — readiness status (whether the agent can run right now).
- ``run`` — the agent's primary operation.
"""

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class AgentAdapter(Protocol):
    """The interface every agent integration implements."""

    def metadata(self) -> dict[str, Any]:
        """Return the agent's manifest metadata."""
        ...

    def health(self) -> dict[str, Any]:
        """Return readiness status, e.g. ``{"ready": True, "message": ...}``."""
        ...

    def run(self, request: dict[str, Any]) -> dict[str, Any]:
        """Execute the agent's primary operation and return a result dict."""
        ...
