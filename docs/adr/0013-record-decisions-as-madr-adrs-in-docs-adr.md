---
status: accepted
date: 2026-11-01
---
# Record decisions as one MADR 4.0 ADR per decision in docs/adr/

## Context and Problem Statement
Design decisions here were spread across skills, `.ai/history.md`, CLAUDE.md and commit messages, so a future session could reverse one without knowing why (inferred from the scattered evidence cited in ADR-0001 to ADR-0012). How should decisions be recorded?

## Considered Options
* One MADR 4.0 file per decision in `docs/adr/`, written via a global `write-adr` skill, with an index at `docs/adr/README.md`
* A single flat history file (inferred: `.ai/history.md` already logs changes, but the sources do not record it being weighed)

## Decision Outcome
Chosen option: "MADR ADRs in `docs/adr/`", chosen by the user for several of their projects at once (`.ai/history.md:6`).

### Consequences
* Good, because each decision has one file with context, options and evidence, and a fresh clone learns them from the index.
* Bad, because ADRs must be kept public-safe and superseded ADRs linked by hand (`global-skills/write-adr/SKILL.md`).

## More Information
Evidence: ae3cdeb (2026-11-01, `global-skills/write-adr/SKILL.md`, symlinked into `~/.claude/skills/`); `.ai/history.md:6` (Class C, verified by a fresh Haiku session invoking the skill as its first `tool_use`). ADR-0001 to ADR-0012 were backfilled on 2026-11-01 with this skill. Related: ADR-0012.
