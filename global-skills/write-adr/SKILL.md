---
name: write-adr
description: Write or backfill an Architecture Decision Record (MADR) in docs/adr/. Use when a design or architecture decision is made, reversed, or needs its "why" recorded, or when the user says "write an ADR".
---

# write-adr

One file per decision, in `docs/adr/`. ADRs are committed and may be public: a fresh clone plus an agent reading `docs/adr/README.md` should learn every decision that shapes the project.

## Does it deserve an ADR?
Yes if a future session could reasonably reverse it without knowing why: a choice between real alternatives with lasting consequences (architecture, interfaces, data model, provider, workflow contract, naming the user relies on).
No for session narrative, bug fixes, or operational traps; those belong in `.ai/history.md`, git, or `CLAUDE.md` gotchas.

## Check the current MADR first
The template below matches MADR 4.0.0 (checked 2026-11-08). Before writing, look for a newer release:

```bash
gh api repos/adr/madr/releases/latest --jq .tag_name
# without gh: git ls-remote --tags --refs https://github.com/adr/madr.git | sed 's|.*refs/tags/||' | grep -E '^[0-9]+\.[0-9]+\.[0-9]+$' | sort -V | tail -1
```

- Same version: use the template below.
- Newer: read its `template/adr-template-minimal.md` and `template/adr-template.md` (`gh api "repos/adr/madr/contents/template/<file>?ref=<tag>" -H "Accept: application/vnd.github.raw"`). Show the user what changed against the template below (sections, their order, required vs optional, fixed wording). Ask before writing; if they adopt it, update this file and its version line.
- Check fails (offline, rate limit): use the template below and tell the user the check was skipped.
- Kept unless the user says otherwise: the `docs/adr/` folder (MADR suggests `docs/decisions/`) and the `(alternatives not recorded)` rule.

## File
- Path: `docs/adr/NNNN-title-with-dashes.md`. Write it to the repo with Write/Edit; never publish an ADR as an artifact or anywhere outside the repo. NNNN = next unused number, zero-padded, never reused. Title lowercase, dashes.
- Template (MADR minimal, plus the full template's optional front matter and More Information):

```markdown
---
status: accepted
date: YYYY-MM-DD
---
# {short title: the problem and the chosen solution}

## Context and Problem Statement
{2-4 sentences: the situation and the question that forced a decision. Cite evidence.}

## Considered Options
* {option 1}
* {option 2}

## Decision Outcome
Chosen option: "{option}", because {reason}.

### Consequences
* Good, because {...}
* Bad, because {...}

## More Information
Evidence: {commits, files, gotcha numbers, docs}. {Related ADRs.}
```

- `status`: `proposed` | `accepted` | `rejected` | `deprecated` | `superseded by ADR-NNNN`.
- `date`: when the decision was made (backfill: the date the evidence shows), not today.
- Quote the chosen option exactly as it is listed under Considered Options.
- Consequences are `Good, because` or `Bad, because`; MADR keeps `Neutral` for its Pros and Cons section. A neutral fact goes in Decision Outcome (scope) or More Information.

## Evidence rules
- Every fact cites a source: commit hash, `file:line`, a `CLAUDE.md` gotcha number, or a doc in the repo.
- Only list options the sources show were actually considered. If the sources name none, write `* (alternatives not recorded)` rather than inventing them.
- Label anything inferred: `(inferred from ...)`.
- Cite existing design docs instead of copying them.

## Public-safe
No secrets, keys, tokens, local machine paths, personal or client details, or private repo contents. If the decision can't be explained without them, stop and ask the user.

## Changing a decision
Never rewrite an accepted ADR's decision. Write a new ADR, then set the old one's status to `superseded by ADR-NNNN` and link back. Typos and broken links may be fixed in place.

## Index
Keep `docs/adr/README.md` current: one line per ADR, `NNNN - title - status - date`, linked. Create it with the first ADR. A fresh session reads this file first.

## Backfilling
1. Mine `.ai/history.md`, `.ai/handoff.md`, `CLAUDE.md`, `docs/`, and `git log` for decision candidates.
2. Show the user a table (date, decision, evidence, status, confidence) and wait for their picks.
3. Write the picked ADRs in chronological order so numbers follow time; add superseded links as you go.
