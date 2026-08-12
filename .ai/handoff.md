# Handoff — live state snapshot

## Last updated
2026-08-11 — session 4. The advisor pattern shipped as a public plugin and moved out of
this repo. Earlier entries in this session were mislabeled 2026-07-12; the real date is
2026-08-11.

## Current state
The advisor/workhorse pattern is finished and now lives in its OWN repo,
`~/Desktop/projects/the-advisor` (public at github.com/alitahir6001/the-advisor), packaged
as a Claude Code plugin named "The Advisor". It is installed on this machine via
`claude plugin marketplace add` + `claude plugin install the-advisor@the-advisor`, and a
fresh session in an unrelated directory shows exactly one advisor agent, one MCP server,
and two skills — all plugin-scoped. The manual `~/.claude/` copies and the user-scope MCP
registration were DELETED once the plugin supplied them, because having both produced two
competing advisor agents and servers. `~/.claude/advisor/` survives only as an archive:
the pre-plugin consult log (9 entries) plus `consults.py`, the log reader. This repo's
`experiments/advisor-pattern/` is now a frozen snapshot, not what runs.

Plugin structure follows the docs plus the official marketplace cached at
`~/.claude/plugins/marketplaces/claude-plugins-official` (a better reference than prose
docs): `.claude-plugin/{plugin,marketplace}.json` — the repo is its own marketplace, so
one command installs it — plus `agents/`, `skills/`, `.mcp.json` using
`${CLAUDE_PLUGIN_ROOT}` and `${CLAUDE_PLUGIN_DATA}`, `server/`, `docs/*.svg`, README, MIT.

Three substantive changes were made while packaging. Hardcoded model defaults were removed
(user's point: they contradict model-agnosticism and go stale) so model is pure config —
CLI providers fall back to the CLI's own default, API providers error clearly when unset.
The log directory now auto-creates. And a real bug was fixed: the env stripper removed all
`CLAUDE*` vars including `CLAUDE_CODE_OAUTH_TOKEN`, which would have logged the
anthropic-cli advisor out for anyone using a setup-token.

Honest status of the headline claim: proactive escalation is verified ONLY against seeded
prompts that contained the escalation rule's own trigger words. In real use every consult
has been user-invoked. The README was corrected to stop claiming "automatically, without
you asking" and now leads with `/advisor`; check 3 is what would let that be strengthened.

## Changed files (this session)
- `the-advisor/` — new repo: full plugin, 3 committed diagrams, README, LICENSE
- `~/.claude/`: agents/advisor.md, skills/advisor, skills/consult-advisor-cli DELETED;
  user-scope MCP `advisor` removed; `advisor/` kept as archive + log reader
- harness `CLAUDE.md` — phase/status, architecture, gotchas 4-5, commands
- harness `.ai/` trio — this update
- harness working tree still shows the promotion deletions, uncommitted (user commits)

## Open threads
- DoD checks 3-5 unrun (see current-task.md). Check 3 is the one that matters.
- 2 commits in the-advisor were reset at the user's request (README tightening + diagrams);
  they sit unstaged in the working tree for the user to commit and push themselves.
- Second-machine install not attempted.
- Two user rules learned this session, saved to memory: never use the `gh` CLI (plain git
  only; hand GitHub-side actions back), and don't raise commits unless asked.

## Next recommended step
Run DoD check 3 — a real task with an unlabeled architectural decision, on a cheap
workhorse model, without mentioning the advisor. That single result decides whether the
README's hedged escalation sentence gets strengthened or the rule wording gets retuned.
