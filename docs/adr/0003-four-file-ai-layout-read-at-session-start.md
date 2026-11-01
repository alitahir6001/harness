---
status: superseded by ADR-0006, ADR-0008, ADR-0009
date: 2026-07-12
---
# Four-file .ai/ layout, all read at session start

## Context and Problem Statement
Sessions needed a fixed place for live state that survives between conversations. The first committed contract defined four files and an order to read them in (`git show 4b06f20:.ai/rules.md`, lines 3-9).

## Considered Options
* (alternatives not recorded)

## Decision Outcome
Chosen option: "four files in `.ai/`, read at start in the order rules -> current-task -> handoff -> backlog", with `current-task.md` holding the current task only, `handoff.md` a rewritten-in-place snapshot (cap ~150 lines), and `backlog.md` a rolling archive whose old entries roll out to a CLAUDE.md "Recent context" section once 4+ stack up (`4b06f20:.ai/rules.md` lines 4-9).

### Consequences
* Good, because every session started with full state.
* Bad, because the full eager read was later measured at 5k-49k tokens per session start across the user's projects (`global-skills/get-session-context/SKILL.md:18`), which led to ADR-0006.
* Bad, because rolling history into CLAUDE.md made the most expensive file grow with session narrative (superseded by ADR-0009).

## More Information
Evidence: `git show 4b06f20:.ai/rules.md` lines 3-9. Superseded by ADR-0006 (read only handoff at start), ADR-0008 (retire `current-task.md`), ADR-0009 (history in `.ai/history.md`, not CLAUDE.md).
