---
status: accepted
date: 2026-09-20
---
# Retire current-task.md; fold it into handoff's Active task

## Context and Problem Statement
ADR-0003 kept the current task in its own `current-task.md`. Once session start reads only `handoff.md` (ADR-0006), a separate task file is either an extra startup read or invisible. Where should the active task live?

## Considered Options
* Fold the task into an "Active task" section of `handoff.md`
* Keep the 4-file layout (ADR-0003)

## Decision Outcome
Chosen option: "fold into handoff", because the 2026-09-20 session-context change reads `handoff.md` only, so the task belongs where the session already looks (9474b93 message).

### Consequences
* Good, because one startup read carries the active task.
* Bad, because projects still on the old layout need a legacy branch: read `current-task.md` if handoff names no task (`global-skills/get-session-context/SKILL.md:23`; `global-skills/update-session-context/SKILL.md:49`).

## More Information
Evidence: 9474b93 (2026-10-31, removes this repo's `.ai/current-task.md`); `global-skills/update-session-context/SKILL.md:49`. Decided 2026-09-20; applied here 2026-10-31. Supersedes ADR-0003.
