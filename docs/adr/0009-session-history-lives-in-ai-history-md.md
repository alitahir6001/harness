---
status: accepted
date: 2026-11-01
---
# Session history lives in .ai/history.md; backlog holds parked items only

## Context and Problem Statement
Under ADR-0003 old backlog entries rolled into a CLAUDE.md "Recent context" section, which put session narrative in the file loaded every turn. On 2026-10-31 the template dropped that section and history went to `backlog.md` as an interim step (c3d46e2; `.ai/handoff.md:29-31`). That made the backlog both a to-do list and an archive. Where should session history live?

## Considered Options
* A separate `.ai/history.md`, never read at start; `backlog.md` holds parked items only
* CLAUDE.md "Recent context" (ADR-0003)
* `backlog.md` as the archive (the 2026-10-31 interim step)

## Decision Outcome
Chosen option: "`.ai/history.md`", because history is needed only when someone asks about past work, so it should cost nothing at start (`global-skills/get-session-context/SKILL.md:22`).

### Consequences
* Good, because CLAUDE.md and backlog no longer grow with session narrative.
* Good, because Class B/C changes have one log: date, what, why, how verified (`.claude/skills/harness-change-control/SKILL.md`, Recording).
* Bad, because one more file in `.ai/` to keep straight.

## More Information
Evidence: c3d46e2 (2026-10-31, template drops Recent context); 64c1ea9 and 6dcc079 (2026-11-01, `history.md` created, backlog trimmed); 9d12a47 (`global-skills/create-session-context/CLAUDE.template.md:62`); dd7704c (`get-session-context` reads history only when asked); `.ai/history.md:3,7`. Supersedes the history-rollover part of ADR-0003.
