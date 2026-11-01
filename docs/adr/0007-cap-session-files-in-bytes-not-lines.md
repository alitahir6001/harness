---
status: accepted
date: 2026-09-20
---
# Cap session files in bytes, not lines

## Context and Problem Statement
The session files had line caps: ~150 lines for the handoff (`4b06f20:.ai/rules.md` line 8), a 200-line rules limit, and a ~200-250-line soft cap in the CLAUDE.md template. One project's rules file reached 57 KB against its "200 line" limit, because a line cap on paragraph-length entries is no cap at all (`global-skills/update-session-context/SKILL.md:38`). How should size be capped?

## Considered Options
* Byte caps: handoff and rules 8 KB, CLAUDE.md 12 KB
* Line caps (~150-line handoff, 200-line rules, ~200-250-line template)

## Decision Outcome
Chosen option: "byte caps", because they bound what is actually loaded, regardless of line length (`update-session-context/SKILL.md:38`; `global-skills/create-session-context/SKILL.md:92`).

### Consequences
* Good, because the cap measures the cost it is meant to limit.
* Bad, because bytes are harder to eyeball than lines; checking needs `wc -c` (inferred).

## More Information
Evidence: `global-skills/update-session-context/SKILL.md:38` (8 KB handoff cap, the 57 KB incident); `global-skills/create-session-context/SKILL.md:92` (12 KB CLAUDE.md cap); `git show 4b06f20:.ai/rules.md` line 8 (the old ~150-line cap). Date inferred from the 2026-09-20 session-context audit and the file's last change on that date; adopted in this repo 2026-10-31 (c3c087a: handoff "Cap 8 KB"). Related: ADR-0006.
