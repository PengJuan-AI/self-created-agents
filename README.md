# Self-Created Agents

> This repository is now organized as a home for multiple self-created agents. Drafter is the first agent; the project structure and onboarding guide live in [AGENTS.md](AGENTS.md).

Drafter is a small local web application for drafting and revising documents with an AI writing assistant. It serves a browser interface and keeps each browser session's working document in memory.

## Requirements

- Python 3.10 or newer
- A DeepSeek API key
- The Python packages used by the agent: `python-dotenv`, `langchain-core`, and `langchain-deepseek`

Install the dependencies in your preferred virtual environment, for example:

```bash
python -m pip install python-dotenv langchain-core langchain-deepseek
```

## Configuration

Create a local `.env` file (it is intentionally ignored by Git):

```dotenv
DEEPSEEK_API_KEY=your_api_key_here
# Optional; defaults to deepseek-v4-pro
DEEPSEEK_MODEL=deepseek-v4-pro
```

## Run

From this directory, start the server:

```bash
cd agents/drafter
python3 Drafter.py
```

Then open <http://127.0.0.1:8000> in a browser. You can choose a different host or port with `--host` and `--port`.

The health endpoint is available at `/api/health`. Explicit save requests create text files under the ignored `documents/` directory.

## Project layout

- `agents/` — one folder per agent, including manifests and agent-specific docs/tests/assets
- `agents/drafter/Drafter.py` — Drafter HTTP server and agent/tool integration
- `agents/drafter/static/index.html` — Drafter browser UI
- `agents/drafter/documents/` — generated drafts; created at runtime and ignored by Git
- `registry/agents.yaml` — catalog consumed by the future Agent Hub
- `shared/agent-template/` — copy this when creating a new agent
- `hub/` — planned workbench and public showcase interface
- `workspace/` — local inputs, outputs, and archive for personal use
- `docs/` — architecture, roadmap, and instructions for adding agents

## Security

Never commit API keys. Keep credentials in `.env` or another local secret manager, and rotate any key that has been exposed publicly.
