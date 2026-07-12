---
name: harness-runbook
description: Operational runbook for the harness workspace — setup from scratch, config catalog, diagnostic scripts, symptom→triage table for misbehaving config (skill not triggering, rule ignored, permission prompts, hook silent), and the validation bar for calling a change done. Use when starting work in this repo cold, when a session behaves unexpectedly, or when verifying a config change. Keywords: setup, run, diagnose, debug, skill not loading, rule ignored, permission prompt, validate, triage.
---

# Runbook — harness workspace

**When NOT to use this skill:** for concepts and where-things-live, see
`harness-reference`. Before making the change you're about to verify, check
`harness-change-control`. This repo has no build, no tests, no CI, no server —
"running the project" means starting a Claude Code session in it.

## Setup from scratch (new machine or cold session)

1. Prereq: Claude Code CLI ≥ 2.1.193 on PATH (`claude --version`).
2. `cd` into this repo; start `claude`. Nothing else to install — there is no code.
3. Orient: run the audit script (below), then read `.ai/handoff.md` and
   `.ai/current-task.md` for live state.
4. Auto-memory for this project lives at
   `~/.claude/projects/-Users-pakfro-home-Desktop-projects-harness/memory/` —
   note the path flattens BOTH `/` and `_` to `-`. It won't exist on a new machine;
   the skills and `.ai/` are the portable copy of anything load-bearing.

## Config catalog (everything that shapes a session here — enumerated by audit, 2026-07-06)

| File | Effect |
|---|---|
| `~/.claude/CLAUDE.md` (7 lines) | Global response-style rules, every turn, every project |
| `~/.claude/settings.json` | `model: opus`, `effortLevel: high`, `tui: fullscreen` |
| `.claude/settings.local.json` | Project permission allows (WebSearch, anthropic.com fetch, accumulated read-only approvals) |
| `.claude/skills/*/SKILL.md` | This library — descriptions always loaded, bodies on trigger |
| `~/.claude/skills/build-skill-library/` | User-level skill that generated this library |
| memory `MEMORY.md` + files | User profile + learning goal, loaded each session |
| `CLAUDE.template.md` | INERT — template only, never auto-loaded |
| Hooks, subagents, MCP, project CLAUDE.md | None configured (as of 2026-07-06) |

## Diagnostics (read-only, verified working 2026-07-06)

```bash
# Full config audit: layers, line counts (token tax), settings, skills, hooks
bash .claude/skills/harness-runbook/scripts/audit-config.sh

# Lint this skill library: frontmatter, name/dir match, provenance sections
bash .claude/skills/harness-runbook/scripts/lint-skills.sh
```

## Symptom → triage

| Symptom | Check, in order |
|---|---|
| Skill doesn't auto-trigger | 1. `lint-skills.sh` (frontmatter valid? name = dir?) 2. Is the description trigger-rich for the phrasing you used? 3. Does explicit `/<name>` work? If yes → description problem, rewrite it with the symptoms/keywords you actually typed. |
| CLAUDE.md rule ignored | 1. `audit-config.sh` — is the file present and in a loaded location? 2. Line count — over ~30 lines, adherence drops; prune before adding emphasis (rationale in `harness-reference`). 3. Is it phrased as a directive, not a description? |
| Unexpected permission prompts | `audit-config.sh` settings section — is there an allow rule matching the exact tool+qualifier? Add to `.claude/settings.local.json` (Class B — see `harness-change-control`). |
| Hook seems not to fire | No hooks exist yet here. When one does: give it a marker-file side effect and check the marker (`harness-evidence-and-analysis`, recipe 2). |
| Behavior differs from another project | Diff the layers: global CLAUDE.md and user settings apply everywhere; run the audit in both projects and compare. |
| Hitting the 5-hour usage cap | Go to `harness-token-efficiency-campaign` — don't improvise. |
| Config seems loaded but you can't tell | `claude --bare -p "..."` strips CLAUDE.md/hooks/memory; if behavior changes vs plain `claude -p`, a config layer is responsible — bisect by layer. |

## Validation bar (what counts as evidence in THIS repo)

There are no tests, so the bar is behavioral, in a fresh session:

1. **File-read proof is not proof.** A change is validated only by a session started
   AFTER the change showing the new behavior: `claude -p "<probe task>"`.
2. **One discriminating probe beats ten impressions.** Design the probe so old and new
   config give visibly different outputs (recipes in `harness-evidence-and-analysis`).
3. **Claims get labels.** Observed / verified-against-CLI / UNVERIFIED — anything
   entering a skill must carry one (rule 3 in `harness-change-control`).
4. **Measured, never judged by eye**, when the claim is about cost: line counts and
   session counts from `audit-config.sh` and `.ai/backlog.md`, not vibes.

## Provenance and maintenance

- Written 2026-07-06, CC 2.1.193. Both scripts run and pass on that date.
- Config catalog drifts: re-run `audit-config.sh` and update the table when it disagrees.
- Global CLAUDE.md line count: `wc -l ~/.claude/CLAUDE.md` (was 7).
