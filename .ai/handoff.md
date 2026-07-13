# Handoff — live state snapshot

## Last updated
2026-07-12 — session 4 (wrapped). Advisor/workhorse pattern: all three rungs built and
verified; repo got git, a live CLAUDE.md, and an updated architecture contract.

## Current state
The advisor/executor pattern is fully working locally, three ways: (1) advisor subagent
`.claude/agents/advisor.md` — Fable via `model:` frontmatter, read-only tools, directive
MUST-form escalation rule in the description; (2) cross-provider CLI consult skill
`.claude/skills/consult-advisor-cli/` — proven live against Google Gemini via the
`gemini` CLI; (3) model-agnostic MCP server
`experiments/advisor-pattern/advisor_server.py` (stdlib-only, stdio, newline-delimited
JSON-RPC) registered in `.mcp.json` with adapters {anthropic-cli, gemini-cli,
anthropic-api, openai-api} selected by ADVISOR_PROVIDER/ADVISOR_MODEL; default
anthropic-cli + fable. Every rung passed fresh-session behavioral tests (headless Haiku
workhorse); the durable findings were promoted to CLAUDE.md "Active gotchas" (directive
escalation wording, CLAUDE* env-strip for nested `claude -p`, untested API adapters /
authed gemini CLI). Session-end housekeeping: root `CLAUDE.md` created from
`CLAUDE.template.md` (template deleted per user instruction; recoverable at commit
4b06f20), and the `harness-architecture-contract` skill's two stale invariants (no live
CLAUDE.md, no git) were corrected. Billing context that shaped the design: `claude -p`
still bills the subscription — the announced June 15 2026 change was paused
(help center article 15036540).

## Changed files (this session)
- `.claude/agents/advisor.md` — new (rung 1)
- `.claude/skills/consult-advisor-cli/SKILL.md` — new (rung 2)
- `experiments/advisor-pattern/advisor_server.py`, `.mcp.json` — new (rung 3)
- `CLAUDE.md` — new (from template); `CLAUDE.template.md` — deleted
- `.claude/skills/harness-architecture-contract/SKILL.md` — 2 stale invariants updated
- `.ai/` trio — this update; `.git/` — initialized (user made initial commit 4b06f20)

## Open threads
- Everything after the local polish pass is uncommitted — user commits their own work;
  remind at session start if `git status` is dirty.
- anthropic-api / openai-api adapters coded but never run (no keys).
- Roadmap steps live in current-task.md: polish -> global promotion (gated, Class C-ish
  per harness-change-control) -> cross-project test -> plugin -> other machines.

## Next recommended step
Use the pattern in real work here (rung 1 fires automatically in any fresh session in
this repo). When consults feel right, do the global promotion + cross-project test in
one sitting — they're the same afternoon of work.
