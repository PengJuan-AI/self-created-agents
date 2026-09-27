"""FastAPI service for the Agents Hub."""

from pathlib import Path

import yaml
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.drafter import router as drafter_router

app = FastAPI(title="Agents Hub API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

REGISTRY = Path(__file__).resolve().parents[1] / "registry" / "agents.yaml"

app.include_router(drafter_router)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/agents")
def agents() -> list[dict]:
    return yaml.safe_load(REGISTRY.read_text(encoding="utf-8")).get("agents", [])
