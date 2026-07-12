# Project rules & how to maintain .ai/

## Maintaining these files
Read at session start, in this order: `rules.md` -> `current-task.md` -> `handoff.md` -> `backlog.md`.

- **rules.md** - this file. Read once per session. Edit only when a rule itself changes - not for session state.
- **current-task.md** - the CURRENT task only. Update on task transitions (finished, pivoted, started new). Not a history.
- **handoff.md** - live state snapshot. Rewrite in place, don't append like a log. Cap ~150 lines.
- **backlog.md** - rolling archive of recent sessions, newest first. Append at session end; roll old entries out (to CLAUDE.md "Recent context") once 4+ stack up.
- Permanent gotchas / non-obvious behavior that stays true for the project's life -> root `CLAUDE.md`, not here.

## Status marks
Use these for any step or task that needs a status — in `current-task.md` and elsewhere:
- `[ ]` todo
- `[~]` in progress
- `[x]` done
- `[!]` blocked

## Populating from empty
- **current-task.md** - What (the task) / Why (it matters) / Order of operations (numbered, mark each with a status above, tag owner: agent/user) / Out of scope.
- **handoff.md** - Last updated (date + session N) / Current state (one paragraph, what's true right now) / Changed files (this session) / Open threads / Next recommended step.
- **backlog.md** - leave empty until first session wrap, then prepend `## Last session: YYYY-MM-DD (session N)` + 2-3 sentences.

## Quick reference: when to touch what
| Event | handoff.md | current-task.md | backlog.md | CLAUDE.md |
|---|---|---|---|---|
| Made a code change | yes | - | - | - |
| Hit a blocker / found a bug | yes | - | - | - |
| Discovered a permanent gotcha | yes | - | - | yes |
| Finished task, starting new one | yes | yes | - | - |
| Session wrapping up | yes | - | yes | yes |

## Project-specific rules
<!-- Tech stack, code conventions, agent workflow constraints (e.g. "never run git"), security rules - append as discovered. Skip anything guessable from the code. -->

- Repo layout invariants (three-store separation, no git yet, no live `CLAUDE.md` yet) are
  documented in the `harness-architecture-contract` skill, not here — check it before
  adding a `CLAUDE.md`, restructuring `.ai/`, or wondering where a fact belongs. Per that
  skill's own rule ("one home per fact"), don't duplicate its content into this file.
