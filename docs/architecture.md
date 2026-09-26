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

Each agent should expose a small adapter contract: metadata, health/readiness, and a run operation. The Hub should not need to know the internal framework or prompt design of an agent.

Keep these concerns separate:

- source code and tests live with each agent;
- shared utilities live in `shared/`;
- discoverability metadata lives in `registry/`;
- UI and orchestration live in `hub/`;
- personal run data lives in `workspace/`.
