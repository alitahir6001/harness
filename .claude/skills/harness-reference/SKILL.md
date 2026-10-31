---
name: harness-reference
description: Claude Code harness domain reference — config layers (CLAUDE.md, settings.json, skills, hooks, subagents, MCP, memory), where each lives, when each loads, and its token cost. Use when deciding WHERE a behavior belongs (rule vs skill vs hook), when explaining harness concepts, or when a config file's precedence/location is unclear. Keywords: CLAUDE.md, settings, skills, hooks, agents, MCP, memory, permissions, config layer, token cost.
---

# Claude Code harness reference (as it applies to THIS user)

Facts verified 2026-07-06 against Claude Code **2.1.193** on this machine; settings, flags
and layers re-checked 2026-10-31 on **2.1.281**. "UNVERIFIED" = from documentation/training,
not observed here.

**When NOT to use this skill:** for making a change to config, go to
`harness-change-control` first. For step-by-step commands and diagnostics, use
`harness-runbook`. For why THIS repo is laid out the way it is, use
`harness-architecture-contract`.

## The one decision that matters: where does a behavior belong?

| You want… | Put it in | Why |
|---|---|---|
| A rule Claude must follow EVERY message | `CLAUDE.md` (right level, see below) | Loaded every turn — also a per-turn token tax, so keep tiny |
| Knowledge needed only for certain tasks | A skill in `.claude/skills/` | Body loads only when triggered; only the `description` is always in context |
| A deterministic "always do X on event Y" | A hook in settings.json | The harness executes it — doesn't rely on the model remembering |
| A delegated worker with its own context | A subagent (`.claude/agents/*.md`; example: `the-advisor/agents/advisor.md`, via the plugin) | Isolated context window; costs a cold start |
| Facts that persist across sessions | Auto-memory (see below) | Claude maintains it; index loads each session |

## CLAUDE.md layers

- `~/.claude/CLAUDE.md` — all projects (observed: this user has one, 113 lines)
- `./CLAUDE.md` — project root, shared via git (observed: this repo has one)
- `./CLAUDE.local.md` — personal, gitignored (UNVERIFIED, per docs)
- `subdir/CLAUDE.md` — pulled in when Claude works in that subdir (UNVERIFIED, per docs)
- Import syntax: `@path/to/file.md` (UNVERIFIED, per docs)
- Keep it short: every line is reprocessed every turn. If a rule is ignored, the file is
  probably too long — prune, don't add emphasis (Anthropic best-practices guidance).
- An acknowledged rule is not a followed rule: verify by `tool_use` in a fresh session
  (CLAUDE.md gotcha 3).

## settings.json layers (keys verified from real files on this machine)

| File | Scope | Observed contents here |
|---|---|---|
| `~/.claude/settings.json` | user, all projects | `env` (holds the OAuth token: never print raw), `effortLevel: medium`, `tui: fullscreen`, `enabledPlugins`, `extraKnownMarketplaces`, `pluginConfigs`, `hooks` (the stop gate); no `model` key (2026-10-31) |
| `.claude/settings.json` | project, shared | none in this repo |
| `.claude/settings.local.json` | project, personal | `permissions.allow`: WebSearch, `WebFetch(domain:www.anthropic.com)`, plus read-only allows accumulated from approved permission prompts (the harness persists approvals here) |

Permission rule syntax observed: `ToolName` or `ToolName(qualifier)` e.g.
`WebFetch(domain:www.anthropic.com)`, `Bash(git *)`. Precedence (UNVERIFIED, per docs):
enterprise policy > CLI args > local project > project > user.

Hooks live under a `hooks` key in settings.json. Events per docs include `PreToolUse`,
`PostToolUse`, `UserPromptSubmit`, `Stop`, `SessionStart`, plus others; `PostToolUse` and
`Stop` verified locally 2026-10-31 (this repo's `stop_gate.py`). Stop facts that matter:
`transcript_path` can lag the current turn, so track state via PostToolUse instead;
`additionalContext` continues the turn without the error label `decision: block` gets;
`stop_hook_active` plus an 8-continuation cap prevent loops. Docs:
https://code.claude.com/docs/en/hooks

Measured 2026-10-31 (CC 2.1.281, `experiments/stop-gate-test/RESULT.md`):
- A subagent's tool calls fire the settings-file PostToolUse hooks with the **parent's**
  `session_id`, plus `agent_id`/`agent_type` (6/6 runs). Parent-keyed state sees them.
- Agent-tool subagents ran async in 6/7 `-p` Haiku runs: that's the default when
  `run_in_background` is unset (the 7th passed `false`). The main turn can end while one runs. Stop input's `background_tasks` lists it (`type: "subagent"`;
  docs). A Stop hook that ignores it fires on that waiting turn.
- An identical handler command in user settings and `--settings` runs once (dedup).
- `--settings '{"disableAllHooks": true}'` keeps user-scope hooks out of one run.
- `python3 <missing file>` exits 2, and exit 2 on Stop blocks. Guard script paths with `[ -f ]`.
- In transcripts a Stop hook's `additionalContext` is an `attachment` row of type
  `hook_additional_context`; usage repeats per content block, so dedupe by `requestId`.

## Skills (format verified from ~/.claude/skills/build-skill-library/SKILL.md)

- Path: `.claude/skills/<name>/SKILL.md` (project) or `~/.claude/skills/<name>/SKILL.md` (user).
- YAML frontmatter: `name` + `description`. The **description is the trigger** — it is
  always in context and is what makes the model load the body. Write it rich with
  symptoms/keywords; keep it honest about when NOT to fire.
- Invoked explicitly as `/<name>` or auto-loaded when relevant.
- Token model: N skills cost N descriptions per session + 1 body per actual use.

## Auto-memory (verified — live in this session)

- Path: `~/.claude/projects/<flattened-project-path>/memory/`
  (this project: `-Users-pakfro-home-Desktop-projects-harness`)
- One fact per file with frontmatter; `MEMORY.md` is the index, loaded each session.
- It lives OUTSIDE the repo — it does not travel with the project. Durable project
  knowledge belongs in the repo (skills or `.ai/`), not only in memory.

## CLI flags worth knowing (verified via `claude --help`, 2.1.281)

- `-p/--print` — non-interactive one-shot; the cheapest way to test config in a fresh
  session (see `harness-evidence-and-analysis`)
- `--output-format stream-json --verbose` (with `-p`) — event stream; `tool_use` entries
  are the evidence of behavior
- `--model`, `--effort`, `--agent` — per-session overrides of settings.json
- `--bare` — skips hooks, plugin sync, auto-memory, CLAUDE.md auto-discovery. Auth is
  `ANTHROPIC_API_KEY` or `apiKeyHelper` only (OAuth never read), so it can't run on this
  key-less machine
- `-c/--continue`, `-r/--resume`, `--fork-session` — session continuity
- `--allowedTools`, `--append-system-prompt`, `--add-dir`, `--settings`

## This user's operating constraint (from memory, 2026-07-06)

Pro plan; regularly hits the rolling 5-hour usage limit. On 2026-07-06 the default was
opus at high effort; on 2026-10-31 `~/.claude/settings.json` has no `model` key and
`effortLevel: medium`. Model/effort is still the single biggest burn lever. Everything in
this library is written token-cost-first because of this. See
`harness-token-efficiency-campaign`.

## Provenance and maintenance

- CLI version: `claude --version` (2.1.281 on 2026-10-31)
- Flags: `claude --help`
- User settings (redacted): `bash .claude/skills/harness-runbook/scripts/audit-config.sh`
- Skill format: `head -5 ~/.claude/skills/build-skill-library/SKILL.md`
- Hook events (UNVERIFIED here): check https://code.claude.com/docs/en/hooks
- Memory layout: `ls ~/.claude/projects/-Users-pakfro-home-Desktop-projects-harness/memory/`
