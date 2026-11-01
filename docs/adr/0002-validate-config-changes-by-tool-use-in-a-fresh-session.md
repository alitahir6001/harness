---
status: accepted
date: 2026-07-12
---
# Validate config changes by tool_use in a fresh Haiku session

## Context and Problem Statement
Every config change here alters how future sessions behave, and a model can say it will follow a rule without ever acting on it. A fresh session read the escalation mandate, said it would follow it, then made zero calls (`CLAUDE.md` gotcha 3, `CLAUDE.md:30-32`). What counts as proof that a config change works?

## Considered Options
* A fresh `claude -p --model haiku --output-format stream-json --verbose` session, judged by `tool_use` entries in the stream
* Reading the changed file back
* Trusting the prose reply of the session

## Decision Outcome
Chosen option: "fresh Haiku session judged by `tool_use`", because reading the file back "proves nothing about behavior" (`.claude/skills/harness-change-control/SKILL.md:48-56`) and the reply is not evidence (gotcha 3). Haiku is deliberate: a rule that only works on a frontier model is a suggestion that happened to land (`README.md:27-29`).

### Consequences
* Good, because a change is only called done when a session that did not exist at edit time shows it (`harness-change-control/SKILL.md:48-56`).
* Good, because the evidence is mechanical (tool calls in the event stream), not a reading of prose.
* Bad, because each check costs a real session run against the user's usage limit (inferred from the token-budget concerns in ADR-0001).

## More Information
Evidence: `.claude/skills/harness-change-control/SKILL.md:48-56`; `CLAUDE.md:11-13,30-32`; `README.md:17-29`. Timeline: the fresh-session test is in the first commit (4b06f20, 2026-07-12, change-control skill line 46; the skill itself was written 2026-07-06); the `stream-json` + `tool_use` form first appears in 8e2b9a6 (2026-07-13) and was written into CLAUDE.md and README in 9f7c1b2 (2026-08-11). Related: ADR-0005 (the incident behind gotcha 3).
