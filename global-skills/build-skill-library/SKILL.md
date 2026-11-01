---
name: build-skill-library
description: Build a tailor-made project skill library under .claude/skills/ (5 skills — change-control, domain reference, architecture contract, runbook, plus one advanced skill chosen with the user: hardest-problem campaign, evidence & analysis toolkit, or research frontier) so future zero-context sessions and smaller models can carry the project forward. Reads the project's .ai/ directory first. Works inline in one session, no subagents. Use when the user asks to build/create/bootstrap a skill library, document a project for future sessions or handoff, or make a repo "Sonnet-proof".
---

# Build a per-project skill library

Author a skill library under `.claude/skills/` so a zero-context junior engineer or
Sonnet-class model can carry this project forward. Work **INLINE in this session — do NOT
spawn subagents** (each subagent re-reads the repo cold; a swarm is the most expensive
possible shape). Budget: ~5 skills, sized to the repo. Adapt everything below to what
discovery actually finds — the slots are fixed, the content is this repo's.

## Phase 1 — Discover (read-only)

**Start with `.ai/` — the user maintains this directory by hand in most of their projects.**
The usual layout (may vary per project): `handoff.md` (live state snapshot; its Active
task section names the current task), `rules.md` (locked project rules), `backlog.md`
(parked work), `history.md` (session logs; older projects may still keep them in backlog), sometimes `notes.md` or demo/readiness docs.
A legacy `current-task.md` may still exist in unmigrated projects. Sessions read only
`handoff.md` at startup, but this is a one-time build: read every file in it.
Treat its contents as the primary source for history, incidents, priorities, and
unwritten rules — it usually answers most discovery questions outright. **Note which
files are still placeholders or thin**: each gap becomes a targeted question below, and
the skills must not cite a placeholder as if it were settled history.

Then read: README/manifest, CLAUDE.md, contributor docs, package/build config, test + CI
setup (**note if absent — that fact reshapes the validation content**), docs/ or notes
directories, `git log --oneline` (look for reverts, renames, stalled work). Cheap targeted
reads only; don't read the whole tree.

Then ask the user AT MOST 3 questions — targeted at what `.ai/` and the repo did NOT
answer, not generic. Derive them from the actual gaps found. Fallbacks if the docs are
rich and little is missing:
1. What is the hardest live problem right now? (Skip if handoff's Active task (or a legacy
   `current-task.md`) already names it — instead CONFIRM it in one line while asking
   something else.)
2. Who is the audience (future AI sessions? human juniors? both) and what do they NOT know?
3. Any unwritten rules or expensive past failures not captured in `.ai/` or any doc?
If a placeholder file exists for a topic (e.g. an empty `rules.md`), ask the question that
would fill it — and offer to draft that `.ai/` file from the answer as a side benefit
(only write it if the user says yes; `.ai/` is theirs, skills go in `.claude/skills/`).

Fold the answers into everything below.

## Phase 2 — Author 5 skills, one at a time, verifying claims as you write

1. `<project>-change-control` — how changes are classified/gated here; every
   non-negotiable with its RATIONALE and the incident behind it (mine `.ai/` first,
   then git history, for incidents).
2. `<domain>-reference` — the domain knowledge a mid-level person lacks, as it applies
   HERE (not a textbook). Pick the domain from discovery (compliance rules, protocol
   math, business logic — whatever this repo is actually about).
3. `<project>-architecture-contract` — load-bearing design decisions + WHY, the
   invariants that must hold, known-weak points stated plainly.
4. `<project>-runbook` — setup from scratch, run commands, full config catalog
   (enumerate by grepping for env/config reads, not from memory), symptom→triage
   debugging table, and the validation bar (what counts as evidence in THIS repo).
   Include small read-only diagnostic scripts in `scripts/` and RUN them to prove they
   work.
5. **One ADVANCED skill** — settle the choice with the user during the Phase 1
   questions (this is one of your ≤3 questions unless the answer is obvious):
   - `<project>-<hardest-problem>-campaign` (DEFAULT when Phase 1 surfaced a clear
     hardest live problem): an EXECUTABLE, decision-gated campaign — numbered phases
     with exact commands, EXPECTED observations at every gate ("if you see X instead
     → branch to Y"), a ranked solution menu with each option's theory-of-value and
     kill-test, known wrong paths explicitly fenced off with the reason, and a
     validation-and-promotion protocol with MEASURABLE success criteria (never judged
     by eye) that routes through the project's change control.
   - `<project>-evidence-and-analysis`: how a hunch becomes an accepted result here —
     analysis recipes (premise teardown, build-vs-buy, discriminating experiment,
     root-cause) each with a worked example mined from THIS repo's history (`.ai/`
     history/handoff entries are the richest vein).
   - `<project>-research-frontier`: open problems where this project could advance
     past its current state — for each: why the current approach falls short, the
     project's specific asset, the first three concrete steps IN THIS REPO, and a
     falsifiable "you have a result when…" milestone.
   Whichever is chosen, fold that skill's essential evidence-bar rules ("what counts
   as proof here") into the runbook's validation section so they aren't lost. If the
   history is thin or still placeholders, build worked examples from git log + the
   user's Phase 1 answers, and say so.

### Authoring rules
- Audience: zero-context reader (human or model). Imperative runbook voice,
  copy-pasteable commands, every jargon term defined once, tables/checklists over prose.
  Each skill states when NOT to use it and which sibling to use instead.
- Format: `.claude/skills/<name>/SKILL.md`, YAML frontmatter with `name` and a
  trigger-rich `description` (symptoms, task types, keywords — this is what makes the
  skill load itself at the right moment).
- GROUND TRUTH ONLY: verify every command/flag/path/claim against the repo before
  stating it; label anything unverifiable as UNVERIFIED. A wrong runbook is worse than
  none.
- Date-stamp volatile facts (date + commit hash); end each skill with a
  **"Provenance and maintenance"** section containing one-line re-verification commands
  for anything that may drift.
- No oversell: unproven things stay labeled open/candidate. Nothing may contradict the
  project's own rules; no skill may route around its change control.
- One home per fact — siblings cross-reference, never duplicate.
- Write ONLY inside `.claude/skills/`; the rest of the repo is read-only; no mutating
  git commands; never modify live data files.

## Phase 3 — Self-review (inline, no agents)

- Re-grep every cross-reference (no dangling skill names).
- Re-run every command and script you shipped.
- Dedupe facts across skills.
- Report to the user: the inventory with one-liners, what you verified by re-running,
  and what remains uncertain.
