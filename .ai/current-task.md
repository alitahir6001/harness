# Current task

## What
Build a model-agnostic advisor/executor agent pattern in this repo, inspired by the
ClaudeDevs "advisor tool" pipeline (frontier advisor consulted mid-task by a cheaper
workhorse). Workhorse stays Claude-family, swapped via Claude Code's own model controls;
the advisor is rebuilt outside Anthropic's native Advisor tool (which is server-side and
Claude-only) as a custom MCP tool so it can point at any provider via config.

## Why
User wants the planner/advisor + workhorse split from
https://x.com/ClaudeDevs/status/2074606058128224365, but fully model-agnostic — swap
either role without touching code. Native Advisor tool can't do that (Anthropic-only,
server_tool_use). Fits this repo's role #2 (future home of the user's own harness/Agent
SDK work) per `harness-architecture-contract`.

## Order of operations
1. [x] Research native Advisor tool + advisor/executor pattern - agent (confirmed
   server-side, Claude-only, via platform docs + vanja.io writeup)
2. [x] Clarify scope via AskUserQuestion - user chose "Claude family only" for workhorse;
   advisor swappable to any provider
3. [x] Propose plan: `experiments/advisor-pattern/advisor_server.py` (MCP server, stdio),
   provider dispatch via `ADVISOR_PROVIDER`/`ADVISOR_MODEL`/API-key env vars, escalation
   rule embedded in the tool's MCP description, register in project `.mcp.json`, Class B
   fresh-session test, backlog entry - agent
4. [x] User answered: git init done (session 4, nothing committed yet); providers =
   Anthropic + OpenAI; build deferred pending re-evaluation - user
5. [x] Second-opinion evaluation (Fable 5, session 4): plan revised to a 3-rung ladder,
   and confirmed `claude -p` still bills to subscription (June 15 2026 billing change was
   announced May 14 but PAUSED before taking effect — see help center article 15036540).
   Advisor adapters should dispatch to CLIs (subscription-billed) or APIs (credit-billed),
   selected by env var - agent
6. [ ] User to pick starting rung:
   - Rung 1: advisor subagent (`.claude/agents/advisor.md`, `model:` frontmatter,
     escalation rule in description) — zero code, Claude-only, subscription
   - Rung 2: skill instructing Bash consult via `claude -p` / other vendor CLIs — teaches
     cross-provider trick, no MCP
   - Rung 3: `advisor_server.py` MCP server as originally planned, but with
     {anthropic-cli, anthropic-api, openai-api} adapter backends - user
7. [ ] Build chosen rung(s); rung 3 keeps the Class B `.mcp.json` fresh-session test bar - agent

## Out of scope
- Making the workhorse itself non-Claude — ruled out by the user's answer. That would
  need an external orchestrator outside Claude Code, not this repo's current shape.
- Creating a root `CLAUDE.md` — still deferred per `harness-architecture-contract`;
  unrelated to this task.
