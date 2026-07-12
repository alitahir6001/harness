---
name: harness-reference
description: Claude Code harness domain reference — config layers (CLAUDE.md, settings.json, skills, hooks, subagents, MCP, memory), where each lives, when each loads, and its token cost. Use when deciding WHERE a behavior belongs (rule vs skill vs hook), when explaining harness concepts, or when a config file's precedence/location is unclear. Keywords: CLAUDE.md, settings, skills, hooks, agents, MCP, memory, permissions, config layer, token cost.
---

# Claude Code harness reference (as it applies to THIS user)

Facts verified 2026-07-06 against Claude Code **2.1.193** on this machine (no git in this
repo, so no commit hashes). "UNVERIFIED" = from documentation/training, not observed here.

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
| A delegated worker with its own context | A subagent (`.claude/agents/*.md`, UNVERIFIED format — none installed here) | Isolated context window; costs a cold start |
| Facts that persist across sessions | Auto-memory (see below) | Claude maintains it; index loads each session |

## CLAUDE.md layers (verified via CLAUDE.template.md in this repo, which encodes Anthropic's guidance)

- `~/.claude/CLAUDE.md` — all projects (this user HAS one: response-style prefs)
- `./CLAUDE.md` — project root, shared via git
- `./CLAUDE.local.md` — personal, gitignored
- `subdir/CLAUDE.md` — pulled in when Claude works in that subdir
- Import syntax: `@path/to/file.md`
- Target under ~30 lines. Every line is reprocessed every turn. If a rule is ignored,
  the file is probably too long — prune, don't add emphasis.
- `CLAUDE.template.md` in this repo is deliberately NOT named `CLAUDE.md` so
  auto-discovery never loads it (see `harness-architecture-contract`).

## settings.json layers (keys verified from real files on this machine)

| File | Scope | Observed contents here |
|---|---|---|
| `~/.claude/settings.json` | user, all projects | `model: opus`, `effortLevel: high`, `tui: fullscreen` |
| `.claude/settings.json` | project, shared | none in this repo |
| `.claude/settings.local.json` | project, personal | `permissions.allow`: WebSearch, `WebFetch(domain:www.anthropic.com)`, plus read-only allows accumulated from approved permission prompts (the harness persists approvals here) |

Permission rule syntax observed: `ToolName` or `ToolName(qualifier)` e.g.
`WebFetch(domain:www.anthropic.com)`, `Bash(git *)`. Precedence (UNVERIFIED, per docs):
enterprise policy > CLI args > local project > project > user.

Hooks live under a `hooks` key in settings.json. Standard events per docs (UNVERIFIED
locally — no hooks configured anywhere on this machine yet): `PreToolUse`, `PostToolUse`,
`UserPromptSubmit`, `Stop`, `SessionStart`, plus others. Re-verify against docs before
writing your first hook: https://code.claude.com/docs/en/hooks

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

## CLI flags worth knowing (verified via `claude --help`, 2.1.193)

- `-p/--print` — non-interactive one-shot; the cheapest way to test config in a fresh
  session (see `harness-evidence-and-analysis`)
- `--model`, `--effort`, `--agent` — per-session overrides of settings.json
- `--bare` — skips hooks, auto-memory, CLAUDE.md auto-discovery; good for isolating
  whether a config layer causes a behavior
- `-c/--continue`, `--resume`, `--fork-session` — session continuity
- `--allowedTools`, `--append-system-prompt`, `--add-dir`

## This user's operating constraint (from memory, 2026-07-06)

Pro plan; regularly hits the rolling 5-hour usage limit. Default model is **opus with
high effort** (verified in `~/.claude/settings.json`) — the single biggest burn lever.
Everything in this library is written token-cost-first because of this. See
`harness-token-efficiency-campaign`.

## Provenance and maintenance

- CLI version: `claude --version` (was 2.1.193 on 2026-07-06)
- Flags: `claude --help`
- User settings: `cat ~/.claude/settings.json`
- Skill format: `head -5 ~/.claude/skills/build-skill-library/SKILL.md`
- Hook events (UNVERIFIED here): check https://code.claude.com/docs/en/hooks
- Memory layout: `ls ~/.claude/projects/-Users-pakfro-home-Desktop-projects-harness/memory/`
