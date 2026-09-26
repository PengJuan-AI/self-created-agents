# Commit Rules

Use small, focused commits so each change is easy to review, revert, or reuse.

## Rules

- Keep one logical change per commit.
- Keep the commit subject under 50 characters.
- Start with an imperative verb: `Add`, `Update`, `Fix`, `Remove`, or `Refactor`.
- Describe the result, not the implementation process.
- Do not combine frontend, backend, documentation, and tooling changes unless they are inseparable.
- Do not commit secrets, local environments, dependency directories, or generated build output.
- Review `git diff --check` before committing.
- Run the smallest relevant validation for the changed area.

## Suggested format

```text
<Verb> <focused change>
```

Examples:

```text
Add Vite hub frontend
Add FastAPI health endpoint
Update hub setup docs
Ignore frontend build output
```

## Before committing

```bash
git status --short
git diff --check
git diff -- <files>
```

Stage only the files belonging to the current logical change, then verify the staged diff:

```bash
git diff --cached --check
git diff --cached --stat
```
