# My Agent Toolbox

This repository is an agents hub: a personal workbench for using self-created AI agents and a catalog for presenting selected agents publicly.

## Mental model

- **Agent** — an independent module with its own code, dependencies, docs, tests, assets, and manifest.
- **Manifest** — the agent's identity card: what it does, who it is for, how to run it, and its lifecycle status.
- **Hub** — the front door where people discover, run, organize, and eventually share agents.
- **Workspace** — private inputs, outputs, and experiments; it should not be treated as agent source code.

## Repository map

```text
agents/       One folder per agent. Each agent owns its code, tests, docs, assets, and manifest.
backend/      FastAPI service. routers/ for HTTP endpoints, adapters/ for the agent contract.
frontend/     Vite + React Hub UI (views, components, styles).
registry/     The machine-readable catalog used by the Hub and automation.
shared/       Cross-agent schemas, runtime helpers, UI primitives, and common instructions.
tools/        Validation and other repository tooling.
docs/         Product decisions, architecture notes, and contribution guidance.
workspace/    Local working material: inbox, outputs, and archive. Keep sensitive data here.
```

## Development workflow

Start the backend and frontend together:

```bash
# Backend (FastAPI, serves /api/*)
uvicorn backend.main:app --reload --port 8000

# Frontend (Vite dev server, proxies /api to :8000)
cd frontend && npm run dev
```

Validate and test before committing:

```bash
python tools/validate_agents.py
pytest
```

## Adapter contract

Every agent exposes the `AgentAdapter` protocol (`backend/adapters/base.py`) with
three operations: `metadata`, `health`, and `run`. The backend adapts an agent
through this contract instead of importing its internal framework.

## Adding an agent

1. Copy `shared/agent-template/` to `agents/<agent-slug>/`.
2. Fill in `agent.yaml`, `README.md`, and the agent's source entrypoint.
3. Add the agent to `registry/agents.yaml` so the Hub can discover it.
4. Add tests and a small example under the agent folder.
5. Run `python tools/validate_agents.py` and `pytest`.

Use lowercase kebab-case slugs, such as `meeting-summarizer` or `research-librarian`. Keep each agent independently understandable and runnable. The Hub is an integration layer; an agent must not depend on another agent to operate.

## Lifecycle

Agents can move through `idea`, `building`, `ready`, `featured`, `maintenance`, and `retired`. The registry is the source of truth for the current status.

## Privacy

Never commit API keys, personal credentials, private customer data, or unreviewed generated content. Use `.env` for secrets and `workspace/` for local data.
