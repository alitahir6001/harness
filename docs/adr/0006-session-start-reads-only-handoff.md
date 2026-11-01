---
status: accepted
date: 2026-09-20
---
# Session start reads only .ai/handoff.md; the rest loads on demand

## Context and Problem Statement
Under ADR-0003 every session read rules, current-task, handoff and backlog at start. Measured 2026-09-20: across the user's 12 projects with this system, the full set cost 5k-49k tokens per session start, and most went unused (`global-skills/get-session-context/SKILL.md:18`). What should a session read at start?

## Considered Options
* Read `handoff.md` only; `rules.md`, `backlog.md`, `history.md` and CLAUDE.md on demand
* Keep the full eager read

## Decision Outcome
Chosen option: "handoff only", because reading only the handoff and pulling the rest on demand cut startup from about 49,000 to about 15,000 tokens in the largest project, a 69% cut (`README.md:71-74`).

### Consequences
* Good, because startup cost drops sharply and the other files stay authoritative, loaded when the work needs them (`get-session-context/SKILL.md:16-24`).
* Bad, because a session can miss a rule it never read unless the handoff points to it (inferred from the on-demand triggers at `get-session-context/SKILL.md:19-24`).

## More Information
Evidence: `global-skills/get-session-context/SKILL.md:16-24`; `README.md:71-74`; c3c087a (2026-10-31, this repo's `rules.md` stops prescribing the eager read). Decided 2026-09-20 in a cross-project audit; applied to this repo 2026-10-31 (`.ai/history.md:48-50`). Supersedes ADR-0003.
