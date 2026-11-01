# harness — Claude Code harness learning workspace

Workspace, not an app: no build or test suite. Runnable code lives under `experiments/`.

## Phase / status
Learning workspace and versioned home of the global session skills (`global-skills/`).
The advisor pattern shipped 2026-08-11 and lives in `~/Desktop/projects/the-advisor`.
Live state: `.ai/handoff.md`.

## Commands
- Fresh-session behavior test (the validation bar for config changes):
  `claude -p "<prompt>" --model haiku --output-format stream-json --verbose`
  Parse the stream for actual `tool_use` entries — that, not the prose reply, is the evidence.

## Architecture / non-obvious decisions
- One home per fact: skills = durable knowledge, `.ai/` = live session state, this file =
  per-turn rules only. Details in the `harness-architecture-contract` skill.
- Config edits (this file, settings, hooks, skills) are gated — check `harness-change-control` first.
- The advisor pattern NO LONGER LIVES HERE: edit the `the-advisor` repo.
  `experiments/advisor-pattern/` is a frozen dev snapshot, NOT what runs.
- The advisor's "MUST get a second opinion" escalation was tested and retracted
  (the-advisor CLAUDE.md gotcha 28). Don't re-add mandate wording expecting it to fire.
- Design decisions: docs/adr/ (index: docs/adr/README.md). Write new ones with the write-adr skill.

## Active gotchas
1. Nested `claude -p` fails unless `CLAUDE*` env vars are stripped from the subprocess
   (advisor_server.py already does this).
2. No API keys on this machine: the anthropic-api/openai-api adapters are coded but
   UNTESTED; the gemini CLI is authed (free personal tier) and is the live cross-provider path.
3. A model acknowledging a rule is not evidence the rule fires: a fresh session read the
   escalation mandate, said it would follow it, then made zero calls (measured 2026-09-07).
   Verify rules by `tool_use` in the stream, not by the reply.
4. Standalone CLI login lapsed (`claude -p` → "Not logged in", 3x on 2026-08-11). Root
   cause: `~/.zshrc` exported the wrong name (`CLAUDE_OAUTH_TOKEN`). Fix: `CLAUDE_CODE_OAUTH_TOKEN`,
   now in `~/.zshrc` and `~/.claude/settings.json` `env`. Never print either file raw.
5. The advisor server strips `CLAUDE*` env vars from its subprocess (gotcha #1) — which
   would also strip `CLAUDE_CODE_OAUTH_TOKEN` and log the advisor out. That var is
   explicitly preserved. Any future env-stripping change must keep that exception.

## Repo etiquette
- The user makes their own commits; agent commits only when explicitly asked.
