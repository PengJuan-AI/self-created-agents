# Adding a new agent

## Standard workflow

```bash
cp -R shared/agent-template agents/my-agent
```

Then:

1. Rename and complete `agents/my-agent/agent.yaml`.
2. Replace the example implementation in `src/`.
3. Write a focused README with examples and limitations.
4. Add tests under `tests/`.
5. Add a matching entry to `registry/agents.yaml`.
6. Decide whether the agent is `private`, `unlisted`, or `public`.
7. Add a showcase image or icon under `assets/` when the Hub needs one.
8. Run `python tools/validate_agents.py` to confirm the registry and manifest are consistent.

## Design rules

- One agent, one folder, one clear responsibility.
- Keep the interface stable and describe inputs and outputs in the manifest.
- Keep secrets out of the repository.
- Make the agent runnable independently whenever practical.
- Put reusable code in `shared/` only when at least two agents need it.
- Treat the registry as metadata, not as the implementation.

## Adapter contract

To expose the agent through the Hub, add an adapter in `backend/adapters/` that
implements the `AgentAdapter` protocol (`backend/adapters/base.py`): `metadata`,
`health`, and `run`. Then register its routes in `backend/routers/` and include
them in `backend/main.py`.

## Validation

Run the validator to check for duplicate IDs, invalid statuses, missing
entrypoints, and registry/manifest mismatches:

```bash
python tools/validate_agents.py
```
