# Agent Hub

The Hub will be the front door for this toolbox. It should support two modes:

1. **Workbench** — private use: browse agents, open one, provide inputs, see outputs, and inspect history.
2. **Showcase** — optional public use: publish selected agents with a clear description, examples, screenshots, and a “try it” path.

## Suggested first release

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
