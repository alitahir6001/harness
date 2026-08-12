# harness — Claude Code harness learning workspace + advisor/executor pattern

Workspace, not an app: no build or test suite. Runnable code lives under `experiments/`.

## Phase / status
Advisor/workhorse pattern SHIPPED as a plugin (2026-08-11): it now lives in its own repo,
`~/Desktop/projects/the-advisor` (github.com/alitahir6001/the-advisor, public), installed
here via `claude plugin install the-advisor@the-advisor`. Remaining: cross-project DoD
checks 3-5, then install on a second machine.

## Commands
- Fresh-session behavior test (the validation bar for config changes):
  `claude -p "<prompt>" --model haiku --output-format stream-json --verbose`
  Parse the stream for actual `tool_use` entries — that, not the prose reply, is the evidence.
- Read the advisor's consult log (plugin writes to its own data dir, NOT `~/.claude/advisor/`,
  which is the pre-plugin archive of 9 consults):
  `ADVISOR_LOG=~/.claude/plugins/data/the-advisor-the-advisor/consult-log.jsonl python3 ~/.claude/advisor/consults.py --stats`

## Architecture / non-obvious decisions
- One home per fact: skills = durable knowledge, `.ai/` = live session state, this file =
  per-turn rules only. Details in the `harness-architecture-contract` skill.
- Config edits (this file, settings, hooks, skills) are gated — check `harness-change-control` first.
- The advisor pattern NO LONGER LIVES HERE. Canonical source is the `the-advisor` repo;
  edit there. The manual `~/.claude/` copies and user-scope MCP entry were deleted
  2026-08-11 once the plugin provided them (duplicates caused two competing advisor
  agents/servers). `experiments/advisor-pattern/` is a frozen dev snapshot, kept for
  history only — it is NOT what runs.
- Escalation policy has ONE home: the advisor subagent's description, in router form
  (MUST get a second opinion; prefer the `consult_advisor` MCP tool, spawn the agent only
  as fallback). Reason: agent descriptions are always in context; MCP tool descriptions
  can be deferred and don't drive proactive consults (verified 2026-07-12). Don't re-add
  MUST wording to the tool or skill.

## Active gotchas
1. Nested `claude -p` fails unless `CLAUDE*` env vars are stripped from the subprocess
   (advisor_server.py already does this).
2. No API keys on this machine: the anthropic-api/openai-api adapters are coded but
   UNTESTED; the gemini CLI is authed (free personal tier) and is the live cross-provider path.
3. Escalation rules for small workhorse models must be directive ("You MUST consult BEFORE
   finalizing...") — polite "consult when appropriate" wording fails (verified 2026-07-12).
4. Standalone CLI login keeps lapsing (`claude -p` → "Not logged in", 3x on 2026-08-11,
   including AFTER `claude setup-token`). Root cause found: the token was never exported
   in a shell profile, so only the one terminal had it. Real fix = put
   `CLAUDE_CODE_OAUTH_TOKEN` in `~/.zshrc`. Not fatal — consults fall back to the advisor
   subagent, and gemini-cli is unaffected.
5. The advisor server strips `CLAUDE*` env vars from its subprocess (gotcha #1) — which
   would also strip `CLAUDE_CODE_OAUTH_TOKEN` and log the advisor out. That var is now
   explicitly preserved. Any future env-stripping change must keep that exception.

## Repo etiquette
- The user makes their own commits; agent commits only when explicitly asked.

## Recent context
- 2026-07-08 (s1): rebuilt the three session-context skills in ~/.claude/skills/ and smoke-tested them against this repo.
