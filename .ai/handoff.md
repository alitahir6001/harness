# Handoff — live state snapshot

## Last updated
2026-07-12 — session 4. Advisor/executor plan re-evaluated and revised; git initialized;
waiting on user to pick a starting rung before any code is written.

## Current state
User asked for a second-opinion evaluation of the session-3 plan (which Opus 4.8 drafted)
before building. Evaluation kept the core (stateless MCP `consult_advisor` tool,
escalation rule in the tool description) but revised the approach into a 3-rung learning
ladder — see `current-task.md` step 6. Key new fact, verified against Anthropic's help
center (article 15036540) after the user challenged it: the May 14 2026 announcement that
`claude -p`/Agent SDK usage would leave subscription limits on June 15 was PAUSED before
taking effect — headless `claude -p` still bills to Pro/Max subscription today, so a
subscription-billed Anthropic advisor via `claude -p` subprocess is viable. Policy may
still change ("reworking the plan"), which is why rung 3's design uses swappable adapter
backends {anthropic-cli, anthropic-api, openai-api} behind env-var dispatch. Also
diagnosed and fixed live: user's standalone CLI returned 401 on `claude -p` — stale
login, not policy; re-login with subscription fixed it, verified working. `git init` run
(session 4); repo has untracked files, nothing committed yet.

## Changed files (this session)
- `.git/` created (git init — no commits yet)
- `.ai/current-task.md` — steps 4-7 rewritten for the ladder plan
- `.ai/handoff.md` — this update

## Open threads
- User to pick starting rung (1: subagent advisor, zero code; 2: `claude -p`-via-Bash
  skill; 3: full MCP server with adapters). Recommendation on record: start at rung 1 to
  learn escalation-discipline tuning before building plumbing.
- Initial git commit not yet made — user hasn't asked; offer at next natural point.
- Cost framing agreed: pattern only helps the Pro 5-hour-limit problem if the workhorse
  runs on a cheaper model with rare escalations; advisor consults on strong models eat
  the same subscription window.

## Next recommended step
Get the user's rung choice, then build it. Rung 1 is
`.claude/agents/advisor.md` with `model:` frontmatter + escalation criteria in the
description — testable same-session by running the main session on a cheaper model.
