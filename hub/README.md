# Agent Hub

The Hub is the front door for this repository. It supports two modes:

1. **Workbench** — private use: browse agents, open one, provide inputs, see outputs, and inspect history.
2. **Showcase** — optional public use: publish selected agents with a clear description, examples, screenshots, and a “try it” path.

## Current entrypoint

Run the local Hub from the repository root:

```bash
python3 hub/server.py
```

Then open <http://127.0.0.1:8080>. The home page is `hub/index.html`; it is intentionally independent from any one agent.

## Product principles

- Agents are independent modules, not pages inside one monolithic application.
- The registry describes agents; it does not contain their implementation.
- The Hub can launch or link to an agent through an adapter boundary.
- Private workbench behavior and public showcase behavior share the same catalog but have different visibility rules.

## First release

- Read agent cards from `registry/agents.yaml`.
- Filter by category, status, tags, and visibility.
- Open an agent detail page with its README, inputs, outputs, and run button.
- Use an adapter layer so each agent can expose a consistent `run(input)` interface.
- Keep authentication and secrets on the server side.

## Suggested page structure

- `/` — toolbox overview and featured agents
- `/agents` — searchable agent catalog
- `/agents/<id>` — agent profile, examples, and run interface
- `/workspace` — recent runs and saved outputs
- `/about` — why this toolbox exists and how public agents are shared

The Hub is intentionally a separate layer from the agents. Agents should remain useful from the terminal or API even if the website changes.
