# Backlog

Rolling log of recent sessions, newest first. Roll entries out to CLAUDE.md once 4+ stack up.

## Last session: 2026-07-12 (session 3)
Confirmed the session-context trio still orients correctly on a cold read (no changes).
Pivoted to a new goal: a model-agnostic advisor/executor pattern (ClaudeDevs-style
frontier-advisor + cheap-workhorse pipeline). Found Anthropic's native Advisor tool is
server-side and Claude-only, so it can't be the mechanism. User scoped it via
AskUserQuestion: workhorse = Claude family only (existing Claude Code model controls,
no new code); advisor = swappable to any provider (needs a custom MCP tool). Proposed
plan: `experiments/advisor-pattern/advisor_server.py`, provider dispatch via env vars,
escalation rule in the tool's MCP description, `.mcp.json` registration as a Class B
change. Nothing built yet — blocked on user answering proceed/git-init/which-providers.

## Last session: 2026-07-08 (session 2)
Real end-to-end test of `get-session-context`: user ran it from an actual fresh session via
`/get-session-context` and it correctly oriented from `.ai/*` (CLAUDE.md absent, as expected).
Found and fixed one real bug (Bash `ls` check on missing CLAUDE.md surfaced a false "failed
command" in the UI — switched to Read tool) and confirmed one non-bug (Skills don't appear in
the native "/" autocomplete menu; typed `/skill-name` still reaches Claude as text and gets
matched). Corrected an earlier wrong claim that `.ai/` is "often gitignored" — verified via
`git ls-files` it's tracked in job-apply, oneness-suite, and alitahir6001.github.io. Updated
`SKILLS_AVAILABLE.md` to reflect the rename. Trio is now considered done; no open task.

## Last session: 2026-07-08 (session 1)
Rebuilt the three session-context skills (`create-session-context`, `update-session-context`,
`get-session-context`) in `~/.claude/skills/` using patterns from job-apply, oneness-suite,
alitahir6001.github.io, and brads-tool `.ai/` directories. Deleted this repo's old (pre-rename)
`.ai/` and ran both playbooks against it as a smoke test; skipped creating a `CLAUDE.md` since
`harness-architecture-contract` documents that as intentionally deferred. Next: test
`get-session-context` from an actual fresh session.

## Parked items (not session-bound)
