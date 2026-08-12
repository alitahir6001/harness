# Current task

## What
Finish validating "The Advisor" plugin in real use, then replicate it to a second machine.
The build is done; what remains is evidence and distribution.

## Why
The pattern is public and linked from the user's resume/website, so the claims in its
README need to hold up. The escalation behavior is the one claim still only proven under
artificial conditions — the seeded test prompts literally contained the words
"hard-to-reverse architectural decision", which match the escalation rule almost verbatim.
Every consult in real use so far has been user-invoked (`/advisor`), never spontaneous.

## Order of operations
1. [~] Cross-project DoD, running in real projects (alitahir6001.github.io and others):
   1 registration [x] — a session in an unrelated repo named the MCP-first route,
     the subagent fallback, and both skills, unprompted
   2 at-will `/advisor` [x] — well-synthesized ~800-token context; log confirmed the
     MCP route (anthropic-cli, 46.8s, ok)
   3 proactive escalation on UNLABELED real work [ ] - user
   4 restraint: zero consults across routine work [ ] - user
   5 subagent fallback with the MCP server removed [ ] - user, optional
2. [ ] Depending on check 3: either strengthen the README's escalation sentence (currently
   hedged: "how reliably it fires depends on your workhorse model") or tune the rule
   wording in `the-advisor/agents/advisor.md` and retest - agent
3. [ ] Push the 2 unpushed README/diagram commits — user asked to unstage and self-commit;
   changes sit in the-advisor's working tree (README.md modified, docs/ untracked) - user
4. [ ] Pin `the-advisor` and `harness` on the GitHub profile (browser only) - user
5. [ ] Install the plugin on the second machine and confirm a consult works there - user

## Out of scope
- Periodic/oversight mode (checkpoint or hook-fired consults). Considered and rejected
  2026-08-11: keep it event-triggered. Revisit only if check 4 shows missed escalations.
- Non-Claude workhorse — needs an external orchestrator; see `harness-research-frontier`.
- Live-testing the anthropic-api / openai-api adapters — no API keys on this machine.
