# Backlog

Rolling log of recent sessions, newest first. Roll entries out to CLAUDE.md once 4+ stack up.

## Last session: 2026-07-12 (session 4)
Built and verified all three rungs of the advisor/workhorse ladder: advisor subagent
(Fable, directive MUST-form escalation rule — polite wording demonstrably fails with
Haiku), cross-provider CLI consult skill (proven live against Gemini), and a stdlib-only
MCP server with provider adapters (anthropic-cli/gemini-cli tested; api adapters coded,
untested — no keys). Also: git init + user's initial commit, verified `claude -p` still
bills subscription (June 15 billing change was paused), created root CLAUDE.md from the
template (template deleted), corrected two stale invariants in
harness-architecture-contract. Open: polish -> global promotion -> cross-project test ->
plugin (see current-task.md).

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

## Parked items (not session-bound)
