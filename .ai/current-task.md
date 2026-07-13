# Current task

## What
Take the advisor/workhorse pattern (all 3 rungs built and verified in this repo,
2026-07-12) from local experiment to portable tool: polish locally, promote to global
scope, prove it from another project, then package as a plugin.

## Why
User wants the pattern available in all projects and replicable onto other machines.
The plugin is the end state: one installable unit bundling the agent, the skill, and
the MCP server. Ordered rollout (local -> global -> plugin) so each move has a real
test behind it before the next.

## Order of operations
1. [x] Local polish pass (session 4 cont.): de-conflicted the three consult surfaces via
   dogfood consult (advisor recommended MCP-carries-MUST; testing DISPROVED it — MCP tool
   descriptions don't drive proactive consults and can be deferred out of context).
   Final design: agent description = router (MUST + prefer consult_advisor, agent as
   fallback), MCP tool + skill non-directive. Consult logging added to advisor_server.py
   (verbatim JSONL, ADVISOR_LOG override). Test matrix all green: unsteered decision ->
   one MCP consult; trivial task -> zero consults; MCP absent -> subagent fallback
   consult. Open micro-decision for step 4: log location project-local vs ~/.claude
   global once multi-machine - agent
2. [ ] Promote globally: move `.claude/agents/advisor.md` and
   `.claude/skills/consult-advisor-cli/` to `~/.claude/`, register the MCP server
   globally; delete the project-local copies (one home per fact) - agent, gated as a
   global-scope change per `harness-change-control`
3. [ ] Real cross-project test: fresh session in a DIFFERENT project, verify the advisor
   registers and a seeded decision triggers exactly one consult - agent
4. [ ] Package as plugin: bundle agent + skill + MCP server config; install on this
   machine from the plugin and re-run the rung tests against the plugin-provided
   versions - agent
5. [ ] Replicate onto another machine via the plugin - user

## Out of scope
- Non-Claude workhorse (needs an external orchestrator; parked — see
  `harness-research-frontier` for the Agent SDK path).
- Live-testing the anthropic-api / openai-api adapters — no API keys on this machine;
  they stay marked untested until keys exist.
