# Drafter

Drafter is the first agent in this toolbox. Its implementation, manifest, tests, and assets live in this folder.

The agent core lives in `Drafter.py` and exposes a `DrafterService` with a `DRAFTER` singleton. It has no standalone web server; the hub backend adapts it through `backend/routers/drafter.py`, and the React UI lives under `frontend/views/DrafterWorkspace.jsx`.

Run the whole hub from the repository root:

```bash
# API (serves /api/agents/drafter/*)
cd backend
uvicorn main:app --reload --port 8000

# frontend (Vite + React)
cd frontend
npm install
npm run dev
```

Open <http://127.0.0.1:5173> and navigate to the Drafter workspace. Generated documents are saved under this agent's local `documents/` directory.
