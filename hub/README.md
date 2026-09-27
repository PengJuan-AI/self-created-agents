# Agent Hub

The Hub is the front door for this repository. Its implementation now lives in
two places:

- **Frontend** — `frontend/` (Vite + React), run with `npm run dev`.
- **Backend** — `backend/` (FastAPI), run with `uvicorn backend.main:app`.

The legacy `server.py` (a `http.server` static file server) and `index.html` were
removed; the Hub is now a real API + single-page app.

## Modes

1. **Workbench** — private use: browse agents, open one, provide inputs, see outputs, and inspect history.
2. **Showcase** — optional public use: publish selected agents with a clear description, examples, screenshots, and a "try it" path.

## Product principles

- Agents are independent modules, not pages inside one monolithic application.
- The registry describes agents; it does not contain their implementation.
- The Hub launches or links to an agent through the adapter boundary.
- Private workbench behavior and public showcase behavior share the same catalog but have different visibility rules.

## Suggested page structure

- `/` — toolbox overview and featured agents
- `/agents` — searchable agent catalog
- `/agents/<id>` — agent profile, examples, and run interface
- `/workspace` — recent runs and saved outputs
- `/about` — why this toolbox exists and how public agents are shared

The Hub is intentionally a separate layer from the agents. Agents should remain useful from the terminal or API even if the website changes.
