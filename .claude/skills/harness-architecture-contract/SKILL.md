---
name: harness-architecture-contract
description: Load-bearing design decisions of the harness workspace repo — why files live where they do, the three-store separation (skills vs .ai/ vs CLAUDE.md), naming conventions like CLAUDE.template.md, and known weak points. Use when adding/moving/renaming files in this repo, when unsure where new knowledge should be recorded, or when something about the repo layout seems wrong or redundant. Keywords: repo structure, where does this go, template, .ai directory, design decision, invariant.
---

# Architecture contract — harness workspace

Status 2026-10-31: this repo is a workspace, not an app. No build, no tests; the only
runnable code is under `experiments/`. It has three roles, in order: (1) learning
workspace and knowledge base for the Claude Code harness, (2) future home of the user's
own harness built on the Agent SDK, (3) source of reusable templates for other projects,
now concretely `global-skills/`. (Roles confirmed by the user, 2026-07-06.)

**When NOT to use this skill:** for what the harness config layers DO, use
`harness-reference`. For whether a change is allowed and how it's gated, use
`harness-change-control`.

## The three-store separation (the core invariant)

| Store | Holds | Loaded |
|---|---|---|
| `.claude/skills/` | Durable, verified knowledge and procedures | On trigger only |
| `.ai/` | Live state: `handoff.md` (read at start), `rules.md` + `backlog.md` (on demand) | When Claude reads it |
| `CLAUDE.md` (any level) | Only rules needed EVERY message | Every turn (token tax) |

**Invariant: one home per fact.** A fact lives in exactly one store; the others point to
it. When you find duplication, keep the copy in the store matching the table and replace
the rest with a reference. Rationale: duplicated facts drift, and every duplicated line
in CLAUDE.md is a recurring per-turn cost (user is on Pro and hits hourly limits).

## Decisions and why

1. **Templates are suffixed `.template.md`** so Claude Code's auto-discovery never
   loads them as live instructions. If you create more templates, keep this convention.
   The repo's own `CLAUDE.template.md` became the live root `CLAUDE.md` on 2026-07-12
   (old file recoverable from git, commit 4b06f20). The one template left is
   `global-skills/create-session-context/CLAUDE.template.md`.
2. **`settings.local.json` is verification-first.** Its seed allows are `WebSearch` +
   `WebFetch(domain:www.anthropic.com)`: harness facts get checked against Anthropic
   sources or the local CLI, not arbitrary blogs. The harness also appends allows here
   when the user approves permission prompts — read-only additions are fine; anything
   mutating or network-widening is a gated change (see `harness-change-control`).
3. **Knowledge graduates inward.** Raw findings land in `.ai/` (notes/backlog); once
   verified and stable they are promoted into a skill; only if needed every single turn
   do they reach a CLAUDE.md. Never skip the verification step
   (see `harness-evidence-and-analysis` for what counts as verified).
4. **The future harness gets built HERE.** Agent SDK experiments belong in
   `experiments/`, so the skills and `.ai/` history stay attached to the work. See
   `harness-research-frontier` for the roadmap. Current contents:
   - `advisor-pattern/` — frozen dev snapshot of the advisor; the-advisor repo is what runs.
   - `escalation-test/`, `rules-ab-test/{control,withrule}/` — the stub projects behind
     the README findings, each with a `RESULT.md`. **Copy a stub outside this repo before
     rerunning it:** run in place, it inherits this repo's `CLAUDE.md` and skills, which
     contaminates the result.
5. **`global-skills/` is the versioned source of user-level skills.** Each dir is
   symlinked from `~/.claude/skills/<name>`, so edits here are live in every project
   (Class C, see `harness-change-control`). Only skills the user wrote go here; the repo
   is public.

## Known weak points (stated plainly)

- **Git since 2026-07-12** (`git init` + user's initial commit 4b06f20). The weak
  point now is discipline, not absence: the user makes their own commits, so uncommitted
  work can still pile up between sessions — check `git status` at session start.
- **Auto-memory is outside the repo.** The six memory files (user profile, learning
  goal, and four working-style feedback notes) live in `~/.claude/projects/.../memory/`
  and won't travel with this folder. Anything load-bearing from memory has been copied
  into these skills or `.ai/`.
- **`.ai/` history is seeded, not accumulated.** The scaffold was written 2026-07-06
  from one session's context. Treat early backlog entries as reconstruction, not
  incident record.

## Provenance and maintenance

- Written 2026-07-06 (CC 2.1.193); updated 2026-10-31 (CC 2.1.281). Re-verify layout:
  `find . -not -path './.git*' -type f`
- Uncommitted work: `git status --short`
- Symlinks point into this repo: `ls -l ~/.claude/skills/`
- Memory file count: `ls ~/.claude/projects/-Users-pakfro-home-Desktop-projects-harness/memory/`
