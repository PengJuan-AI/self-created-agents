"""Minimal FastAPI service for the Agents Hub."""

from pathlib import Path

import yaml
from fastapi import FastAPI

app = FastAPI(title="Agents Hub API", version="0.1.0")
REGISTRY = Path(__file__).resolve().parents[1] / "registry" / "agents.yaml"


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/agents")
def agents() -> list[dict]:
    return yaml.safe_load(REGISTRY.read_text(encoding="utf-8")).get("agents", [])
