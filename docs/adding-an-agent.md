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

## Design rules

- One agent, one folder, one clear responsibility.
- Keep the interface stable and describe inputs and outputs in the manifest.
- Keep secrets out of the repository.
- Make the agent runnable independently whenever practical.
- Put reusable code in `shared/` only when at least two agents need it.
- Treat the registry as metadata, not as the implementation.

## Future validation

The intended validation command is:

```bash
python tools/validate_agents.py
```

The validator does not exist yet; this is the planned contract for the Hub and CI layer.
