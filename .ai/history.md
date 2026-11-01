# History

Session logs, change logs and archived history, moved out of backlog.md 2026-11-01. Never read at session start; read only when asked about past work.

## 2026-11-01 (change log)
- Class C: new global skill `write-adr` (global-skills/write-adr, symlinked into ~/.claude/skills). Why: user chose per-decision MADR ADRs in docs/adr/ for five of the user's repos. Verified: fresh `claude -p --model haiku` session invoked Skill write-adr as its first tool_use. Description 217 B, always loaded.
- Class C: session-context skills route history to `.ai/history.md` (CLAUDE.template.md, create-/get-session-context, build-skill-library); backlog.md is parked items only. User sign-off 2026-11-01.
- Class C, user-approved 2026-11-01: `CLAUDE.template.md:4` cap changed from "~200-250 lines" to "12 KB (bytes, not lines)" to match create-session-context's byte cap (ADR-0007). Doc fix only.
- Class A + B: backfilled ADR-0001 to ADR-0013 in `docs/adr/` (index `docs/adr/README.md`) with write-adr; CLAUDE.md gained a one-line pointer under Architecture. Verified: fresh `claude -p --model haiku` run (Bash/Edit/Write disallowed) made Read `docs/adr` -> Glob `docs/adr/**/*` -> Read `docs/adr/0001-...md` and summarized ADR 0001 correctly.

## Last session: 2026-10-31 (stop gate: subagents, global, field report)
- Class B, `stop_gate.py` v1.1: marker lines gain `agent_id`/`agent_type`/`cwd`; labels drop
  the session cwd; Stop defers while a background subagent runs. Why: the subagent A/B
  (Haiku, n=3) showed truncated labels (`…/project/d`) and a nudge spent on a waiting turn,
  so the parent checked 1/3. After v1.1: 2/3. Verified: 20 unit tests + 3 Haiku runs.
- SubagentStop: NOT registered (user decision 2026-10-31). The parent's nudge already
  names subagent actions (6/6); SubagentStop would also nudge read-only Explore agents.
- Class C, user-approved 2026-10-31: gate registered in `~/.claude/settings.json` via
  `.claude/hooks/install_global.py` (backup `settings.json.bak-stopgate-20261031-160521`,
  chmod 600; only `hooks` added, verified by diff vs backup). Project-local registration
  removed. Verified: fresh Haiku `-p` in a scratch dir logged mark, nudge, allow; this
  session kept logging once per call after the switch.
- Runner isolation: control/prose pass `disableAllHooks`; proven by 0 global marker lines.
- `field_report.py` + 3 tests, run on the live log (4 nudges, 2 projects).
- Haiku spend this session (`modelUsage`): 1,767,511 cache-read, 192,452 cache-write,
  727 input, 19,081 output, over 10 runs.

## 2026-10-31 (cleanup)
Fixed repo-wide drift found by the 2026-10-30 review. `current-task.md` folded into
`handoff.md` and removed; `rules.md` took the current create-session-context template;
CLAUDE.md lost its retracted "MUST"/directive-wording claims; the seven project skills
dropped `CLAUDE.template.md` / "no git" / `current-task.md` references. Moved the three
test stubs into `experiments/` with RESULT.md files, and the four global session skills
into `global-skills/` (Class C, user-approved 2026-10-31) with symlinks back from
`~/.claude/skills/`. Regenerated SKILLS_AVAILABLE.md. Verified with fresh Haiku
`claude -p` runs: from an unrelated dir the init event listed all 4 symlinked skills; in
this repo `/get-session-context` made exactly one Read, of `.ai/handoff.md`.

Then built the first hook: `.claude/hooks/stop_gate.py`, a Stop-hook verification gate
(Class B). A/B on the deploy fixture, Haiku, n=3: hook checked the real effect 3/3,
control 0/3, same text as a prose CLAUDE.md rule 0/3; ~2.9x tokens. v0's generic nudge
verified the wrong file; v1 names the turn's recorded actions. Registered in
`.claude/settings.local.json`, verified by a fresh `-p` run in this repo (marker:
mark, nudge, allow). Details: `experiments/stop-gate-test/RESULT.md`.

## 2026-08-12 to 2026-10-30 (no backlog entries were written)
Per the 2026-10-30 review: sessions in this folder were design work for other projects
(Pocket Professor, Worklore, Readlore), not harness work. The 2026-09-20 cross-project
session-context audit (4 files -> 3, lazy loading) ran in scratch_pad; this repo was one of
the unmigrated projects until 2026-10-31. Advisor validation moved to the-advisor, where
DoD check 3 came back negative on 2026-09-07 (its gotcha 28).

## Last session: 2026-08-11 (session 4)
Long session that took the advisor/workhorse pattern from idea to a published plugin.
Built all three rungs (advisor subagent, cross-provider CLI skill, stdlib-only MCP server
with provider adapters), then de-conflicted routing after testing DISPROVED the design
the advisor itself recommended — MCP tool descriptions can be deferred out of context, so
the MUST rule has to live on the always-loaded agent description. Promoted to `~/.claude/`,
then repackaged everything as the public plugin "The Advisor" in its own repo
(github.com/alitahir6001/the-advisor) and deleted the now-duplicate global copies.
Learned: escalation wording must be directive; `claude -p` still bills subscription (the
June 15 2026 change was paused); the CLI login lapses unless `CLAUDE_CODE_OAUTH_TOKEN` is
in the shell profile. Corrected an overclaim before publishing — proactive escalation is
only proven against seeded prompts containing the rule's own trigger words. Open: DoD
checks 3-5, then a second-machine install.
(Superseded 2026-09-07: directive wording did not make escalation fire; see the-advisor gotcha 28.)

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
`git ls-files` it's tracked in a private project, oneness-suite, and alitahir6001.github.io. Updated
`SKILLS_AVAILABLE.md` to reflect the rename. Trio is now considered done; no open task.

## 2026-07-08 (session 1, from CLAUDE.md "Recent context")
Rebuilt the three session-context skills in ~/.claude/skills/ and smoke-tested them against this repo.

