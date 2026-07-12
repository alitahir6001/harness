# [Project name] — one line on what it is and its stack

## Commands
<!-- Only commands Claude can't guess from package.json/Makefile. Delete any that are obvious. -->
- Build: `[e.g. pnpm build]`
- Test (single): `[e.g. pnpm test path/to/file]`  <!-- prefer single-test over full suite for speed -->
- Test (all): `[e.g. pnpm test]`
- Lint / typecheck: `[e.g. pnpm lint && pnpm typecheck]`
- Run dev: `[e.g. pnpm dev]`

## Code style
<!-- ONLY where you differ from the language's defaults. If it's the standard convention, delete it. -->
- [e.g. ES modules (import/export), never require()]
- [e.g. Named exports only, no default exports]
- [e.g. Errors: throw typed AppError, never bare strings]

## Testing
- [e.g. Vitest; colocate *.test.ts next to source]
- [e.g. No network in unit tests — use the fakes in test/fakes]
- [e.g. Always add a failing test that reproduces a bug before fixing]

## Architecture / non-obvious decisions
<!-- Things Claude would get wrong by guessing. Keep to real gotchas. -->
- [e.g. All DB access goes through repositories in src/data — never import the client directly]
- [e.g. Auth tokens refresh in src/auth/refresh.ts; don't touch the cookie logic in middleware]

## Gotchas / environment quirks
- [e.g. Requires DATABASE_URL and REDIS_URL set; see .env.example]
- [e.g. The build fails on Node < 20]

## Repo etiquette
- [e.g. Branch names: feature/*, fix/*]
- [e.g. Conventional commits; open a PR, never push to main]

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
  - Target: under ~30 lines. If Claude keeps ignoring a rule, the file is
    probably too long. Prune, don't add emphasis.
  - Add "IMPORTANT:" / "YOU MUST" sparingly to boost adherence on the few
    rules that really matter.
  - Check it into git so the team shares it. Treat it like code: prune when
    things go wrong.

  Placement:
  - ./CLAUDE.md            project root, shared via git
  - ./CLAUDE.local.md      personal, gitignored
  - ~/.claude/CLAUDE.md    applies to ALL your projects
  - subdir/CLAUDE.md       pulled in on demand when Claude reads that subdir
  - Import others with: @path/to/file.md
============================================================ -->
