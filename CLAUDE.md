# harness — Claude Code harness learning workspace + advisor/executor pattern

Workspace, not an app: no build or test suite. Runnable code lives under `experiments/`.

## Phase / status
Advisor/workhorse pattern: all 3 rungs built and verified locally (2026-07-12).
Next: promote globally (~/.claude/), test from another project, then package as a plugin.

## Commands
- Fresh-session behavior test (the validation bar for config changes):
  `claude -p "<prompt>" --model haiku --output-format stream-json --verbose`
  (add `--mcp-config .mcp.json --allowedTools "mcp__advisor__consult_advisor"` to exercise the MCP advisor)

## Architecture / non-obvious decisions
- One home per fact: skills = durable knowledge, `.ai/` = live session state, this file =
  per-turn rules only. Details in the `harness-architecture-contract` skill.
- Config edits (this file, settings, hooks, skills) are gated — check `harness-change-control` first.
- Advisor pattern artifacts: `.claude/agents/advisor.md` (subagent), `.claude/skills/consult-advisor-cli/`
  (CLI consult), `experiments/advisor-pattern/advisor_server.py` + `.mcp.json` (model-agnostic MCP).
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

## Repo etiquette
- The user makes their own commits; agent commits only when explicitly asked.

## Recent context
- 2026-07-08 (s1): rebuilt the three session-context skills in ~/.claude/skills/ and smoke-tested them against this repo.
