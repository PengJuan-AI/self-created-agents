# Self-Created Agents

A personal workbench and future public catalog for independent AI agent modules.

Each agent is an independent module with its own code, manifest, tests, and assets.
The Hub provides a shared discovery and access layer without coupling agents together.

## Quick start

The Hub has two parts: a FastAPI backend and a Vite + React frontend.

```bash
# 1. Backend (serves /api/*)
uvicorn backend.main:app --reload --port 8000

# 2. Frontend (Vite dev server, proxies /api to :8000)
cd frontend
npm install
npm run dev
```

Open <http://127.0.0.1:5173>. The backend serves the registry catalog at `/api/agents`
and agent endpoints under `/api/agents/<id>/...`.

## Tests and validation

```bash
# Validate registry + manifests
python tools/validate_agents.py

# Run the test suite (install dev deps first)
pip install -r requirements-dev.txt
pytest
```

## Repository structure

- `agents/<agent-id>/` — one independent agent module (code, manifest, docs, tests, assets)
- `backend/` — FastAPI service; `backend/routers/` for HTTP, `backend/adapters/` for the agent contract
- `frontend/` — Vite + React Hub UI
- `registry/agents.yaml` — the catalog the Hub discovers agents from
- `shared/agent-template/` — starting point for a new agent
- `tools/` — validation and other tooling
- `docs/` — architecture, roadmap, and contributor guidance
- `workspace/` — private inputs, outputs, and archive

## Included agents

- `agents/drafter/` — document drafting and revision agent (ready)
- `agents/rag/` — retrieval-augmented research agent (building)

## Add an agent

```bash
cp -R shared/agent-template agents/my-agent
```

Complete its `agent.yaml`, implementation, README, tests, and a registry entry. See
[AGENTS.md](AGENTS.md) and [docs/adding-an-agent.md](docs/adding-an-agent.md).

## Adapter contract

Every agent exposes a small, stable surface to the Hub via the `AgentAdapter`
protocol in `backend/adapters/base.py`: `metadata`, `health`, and `run`. The
backend never imports an agent's internal framework directly.

## Current limitations

- Sessions are in-memory and lost on restart.
- Workspace data is stored locally and is not synchronized.
- There is no authentication or multi-user support.
- The backend assumes a single process (no distributed state).

## Security

Never commit API keys, private documents, vector stores, or unreviewed generated
content. Keep secrets in `.env` and personal runtime data in `workspace/`.
