---
status: accepted
date: 2026-10-31
---
# Register the stop gate globally; do not register SubagentStop

## Context and Problem Statement
The stop gate (ADR-0010) was first registered in this repo's `.claude/settings.local.json` (`.ai/history.md:42-44`), so it only covered work done here. Should it cover every project, and should subagents get their own hook?

## Considered Options
* Register `Stop` in user settings, with the command pointing into this repo; no `SubagentStop`
* Project-local `.claude/settings.local.json` (used first, then removed)
* Also register `SubagentStop`

## Decision Outcome
Chosen option: "global `Stop` only", because the parent's Stop nudge already names subagent actions (6/6): subagent tool calls share the parent's `session_id` and land in its record (`experiments/stop-gate-test/RESULT.md:79-81,103-104`), while `SubagentStop` would also nudge read-only Explore agents (`.ai/history.md:16-17`). Registration is done by `.claude/hooks/install_global.py`, user-approved as a Class C change (`.ai/history.md:18-22`).

### Consequences
* Good, because one hook covers direct and delegated work in all projects.
* Bad, because the command points into this repo: moving or renaming it silences the gate everywhere, as a quiet exit (`.ai/handoff.md:46-47`).
* Provisional: subject to the same 2026-11-07 kill-test as ADR-0010.
* This departs from change-control rule 2 ("project-local before global", `.claude/skills/harness-change-control/SKILL.md`) by explicit user approval (inferred to be an approved exception; the sources record the approval, not the exception as such).

## More Information
Evidence: fc2c9f0 (2026-10-31, installer); `.ai/history.md:16-22`; `experiments/stop-gate-test/RESULT.md:79-81,103-104`. Related: ADR-0010.
