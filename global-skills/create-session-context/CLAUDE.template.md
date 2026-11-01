<!-- Durable, project-specific knowledge for the agent. Auto-loaded every session.
     Maintenance: permanent facts only (ephemeral state -> .ai/handoff.md); add gotchas as
     you hit them and never delete them (compress instead); edit only when the user asks.
     Soft cap ~200-250 lines, ideally far less.
     At session start get-session-context reads .ai/handoff.md only; .ai/rules.md and
     .ai/backlog.md load on demand. -->

# [Project name]

## What this project is
[1-3 sentences: what it does, who it's for. Note if a more detailed roadmap lives
elsewhere (e.g. TODO.md) or if `.ai/` should be read first for live state.]

## Stack
[Runtime/language, framework, deployment target, storage, key external APIs/services —
only what Claude can't guess from package.json/Makefile/pyproject.toml.]

## Architecture (mental model)
[How the pieces fit together — a short ASCII tree or 3-6 bullets showing load-bearing
relationships. Not a full file listing.]

## File map (load-bearing only)
<!-- Only files Claude would otherwise have to discover by reading everything. Small,
     single-purpose projects can delete this section. -->
- `path` — [what it does, plus any non-obvious detail]

## Phase / status
[What's built, what's not, what's live vs WIP. Point to `.ai/handoff.md` for exact
current state rather than duplicating it here.]

## Active gotchas
<!-- Numbered, append-only. Never delete an entry — compress it instead if this grows long. -->
1. [A non-obvious behavior, constraint, or past bug that WILL bite someone who doesn't know it.]

## Conventions / what NOT to do
- [Things that look reasonable but are wrong here — e.g. "don't add a bundler", "never run
  git, that's the user's job", "don't fabricate content".]

<!-- =========================================================
     DELETE EVERYTHING BELOW BEFORE USING — it's usage guidance.
     =========================================================

  Rules of thumb (from Anthropic's best-practices guide):
  - This file loads EVERY message. Every line is re-processed each turn.
    Bloat is a recurring token tax AND makes Claude ignore rules lost in noise.
  - For each line ask: "Would removing this cause Claude to make a mistake?"
    If no -> delete it.
  - INCLUDE: non-guessable commands, style that DIFFERS from defaults,
    test runners, repo etiquette, architecture decisions, env quirks, gotchas.
  - EXCLUDE: anything Claude can read from code, standard conventions,
    long API docs (link instead), file-by-file descriptions, "write clean code".
  - Sometimes-relevant knowledge -> a Skill (.claude/skills/), not here.
  - Deterministic "always do X" -> a Hook (.claude/settings.json), not here.
  - Target: under ~250 lines, ideally far less. If Claude keeps ignoring a
    rule, the file is probably too long. Prune, don't add emphasis.
  - Check it into git so the team shares it. Treat it like code: prune when
    things go wrong.
  - Small/single-purpose projects (POCs, single-integration tools) don't need every
    section above — What this project is / Stack / a "Key behaviors" list / Out of
    scope / Known constraints is often enough. Skip File map and Architecture
    if there's not enough project to say anything non-obvious in them.
  - Session history goes in .ai/history.md, not here.

  Placement:
  - ./CLAUDE.md            project root, shared via git
  - ./CLAUDE.local.md      personal, gitignored
  - ~/.claude/CLAUDE.md    applies to ALL your projects
  - subdir/CLAUDE.md       pulled in on demand when Claude reads that subdir
  - Import others with: @path/to/file.md
============================================================ -->
