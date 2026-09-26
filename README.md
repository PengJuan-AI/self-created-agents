# Self-Created Agents

This repository is an agents hub: a personal workbench and future public catalog for independent AI agent modules.

## Start the Hub

```bash
python3 hub/server.py
```

Open <http://127.0.0.1:8080>. The Hub is the entry website; it is intentionally separate from every individual agent.

## Repository structure

- `agents/<agent-id>/` — an independent agent module with its own code, manifest, docs, tests, config, and assets
- `hub/` — the Hub entry page and local web server
- `registry/agents.yaml` — the catalog of modules discovered by the Hub
- `shared/agent-template/` — starting point for a new agent module
- `workspace/` — private inputs, outputs, and archive
- `docs/` — architecture, roadmap, and contributor guidance

## Included agents

- `agents/drafter/` — a local document drafting and revision agent with its own browser interface
- `agents/rag/` — a building-stage retrieval-augmented research agent

## Add an agent

```bash
cp -R shared/agent-template agents/my-agent
```

Complete its `agent.yaml`, implementation, README, tests, and registry entry. An agent should be runnable independently from the terminal or an API. The Hub should integrate through the manifest and a future adapter contract, not through assumptions about the agent's internal framework.

See [AGENTS.md](AGENTS.md) and [docs/adding-an-agent.md](docs/adding-an-agent.md) for the full convention.

## Security

Never commit API keys, private documents, vector stores, or unreviewed generated content. Keep secrets in `.env` and personal runtime data in `workspace/`.
