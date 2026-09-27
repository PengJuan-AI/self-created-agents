# Architecture direction

The repository's primary product is the **Agents Hub**. It gives independent modules a shared discovery and access layer without turning them into one coupled application.

```text
                   +------------------+
                   |      Hub UI       |
                   | browse / run /    |
                   | showcase agents   |
                   +---------+--------+
                             |
                   +---------v--------+
                   |  Registry/catalog |
                   | metadata + policy |
                   +---------+--------+
                             |
             +---------------+---------------+
             |               |               |
       +-----v-----+   +-----v-----+   +-----v-----+
       |  Drafter  |   |  Agent B  |   |  Agent C  |
       |  adapter  |   |  adapter  |   |  adapter  |
       +-----------+   +-----------+   +-----------+
```

Each agent exposes a small adapter contract, defined by the `AgentAdapter`
protocol in `backend/adapters/base.py`:

- `metadata()` — the agent's manifest (identity, status, inputs, outputs).
- `health()` — readiness status.
- `run(request)` — the agent's primary operation.

The backend adapts an agent through this contract and never imports an agent's
internal framework directly. See `backend/adapters/drafter.py` for the reference
implementation.

Keep these concerns separate:

- source code and tests live with each agent;
- shared utilities live in `shared/`;
- discoverability metadata lives in `registry/`;
- UI lives in `frontend/`;
- API and adapters live in `backend/`;
- personal run data lives in `workspace/`.
