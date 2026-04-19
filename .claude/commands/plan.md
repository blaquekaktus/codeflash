# /plan

Use maximum reasoning depth for this planning session. Do not write code yet.

## Your task

Given the feature, fix, or refactor described in this session:

1. **Restate the goal** in one sentence. If anything is ambiguous, surface it now with AskUserQuestion before continuing.
2. **Map the blast radius** — which files, modules, and systems will be affected? List them.
3. **Identify edge cases and blockers** — what could go wrong? What decisions need to be made before work starts?
4. **Produce a numbered step-by-step plan** — each step should be small enough to commit independently, with a clear acceptance criterion.
5. **Flag any Layer 0 risks** — does this task touch PII, currency values, or public-facing identity claims?

## Output format

```
Goal: <one sentence>

Affected files:
- path/to/file — reason

Blockers / open questions:
- <question or blocker>

Plan:
1. <step> → acceptance: <what done looks like>
2. ...

Layer 0 risks: <none | description>
```

## After planning

- Review the plan with the user before executing.
- Switch to a fresh, focused session for implementation — context from the planning session is usually not needed for execution and wastes token budget.
- For speculative or risky steps, use the `experiment` agent with `isolation: worktree`.

