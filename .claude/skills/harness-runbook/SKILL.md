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
3. Orient: run the audit script (below), then read `.ai/handoff.md` (the only live-state
   file; `rules.md` and `backlog.md` load on demand).
   New machine: recreate the global-skill symlinks, one per dir in `global-skills/`:
   `ln -s "$PWD/global-skills/<name>" ~/.claude/skills/<name>`.
4. Auto-memory for this project lives at
   `~/.claude/projects/-Users-pakfro-home-Desktop-projects-harness/memory/` —
   note the path flattens BOTH `/` and `_` to `-`. It won't exist on a new machine;
   the skills and `.ai/` are the portable copy of anything load-bearing.

## Config catalog (everything that shapes a session here — enumerated by audit, 2026-10-31)

| File | Effect |
|---|---|
| `~/.claude/CLAUDE.md` (113 lines) | Global response-style and working rules, every turn, every project |
| `~/.claude/settings.json` | `env` (OAuth token, never print raw), `effortLevel: medium`, `tui: fullscreen`, the-advisor plugin enabled + its `pluginConfigs`, `hooks` (stop gate); no `model` key |
| `CLAUDE.md` (40 lines) | Project per-turn rules and gotchas |
| `.claude/settings.local.json` | Project permission allows (WebSearch, anthropic.com fetch, accumulated approvals) |
| `.claude/skills/*/SKILL.md` | This library — descriptions always loaded, bodies on trigger |
| `~/.claude/skills/<name>` → `global-skills/<name>` | Symlinks: create/get/update-session-context, build-skill-library. `grill-me` is a plain dir, not in the repo |
| Plugin `the-advisor@the-advisor` (0.5.2, user scope) | `advisor` agent, `advisor` MCP server (`consult_advisor`), skills consult/second-opinion/advisor-model/doctor. Source: `~/Desktop/projects/the-advisor` |
| memory `MEMORY.md` (6 lines) + 6 files | User profile, learning goal, working-style feedback; index loaded each session |
| `~/.claude/settings.json` `hooks` → `.claude/hooks/stop_gate.py` (global since 2026-10-31) | Stop-hook verification gate v1.1: PostToolUse records Bash/edit actions (subagents' too), Stop nudges once naming them, defers while a background subagent runs. Command points into THIS repo behind a `[ -f ]` guard: move or rename the repo and the gate goes silent everywhere (rerun `install_global.py` from the new path). Marker log: `~/.claude/stop-gate/marker.log`. Tests: `python3 .claude/hooks/test_stop_gate.py` |
| Project subagents | None configured (as of 2026-10-31) |

## Diagnostics (read-only, verified working 2026-10-31)

```bash
# Full config audit: layers, line counts (token tax), settings (secrets redacted), skills, hooks
bash .claude/skills/harness-runbook/scripts/audit-config.sh

# Lint this skill library: frontmatter, name/dir match, provenance sections
bash .claude/skills/harness-runbook/scripts/lint-skills.sh

# Advisor consult log (live: ~/.the-advisor/consult-log.jsonl, from 2026-09-07; older history
# in ~/.claude/plugins/data/the-advisor-*/ and ~/.claude/advisor/; ADVISOR_LOG=<path> reads one)
python3 ~/Desktop/projects/the-advisor/server/consults.py --stats

# Stop gate field data: per project, nudges, share followed by a tool call, extra tokens
python3 experiments/stop-gate-test/field_report.py

# Stop gate install / removal (Class C: user sign-off first; prints only the hooks key)
python3 .claude/hooks/install_global.py [--uninstall]
```

## Symptom → triage

| Symptom | Check, in order |
|---|---|
| Skill doesn't auto-trigger | 1. `lint-skills.sh` (frontmatter valid? name = dir?) 2. Is the description trigger-rich for the phrasing you used? 3. Does explicit `/<name>` work? If yes → description problem, rewrite it with the symptoms/keywords you actually typed. |
| CLAUDE.md rule ignored | 1. `audit-config.sh` — is the file present and in a loaded location? 2. Line count — over ~30 lines, adherence drops; prune before adding emphasis (rationale in `harness-reference`). 3. Is it phrased as a directive, not a description? |
| Unexpected permission prompts | `audit-config.sh` settings section — is there an allow rule matching the exact tool+qualifier? Add to `.claude/settings.local.json` (Class B — see `harness-change-control`). |
| Hook seems not to fire | 1. `tail ~/.claude/stop-gate/marker.log` after a fresh `claude -p` that runs Bash: expect `mark`, `nudge`, `allow`. 2. No lines → hook not registered or JSON invalid (`audit-config.sh` settings section). 3. Interactive sessions hold hooks back until the folder is trusted; `-p` treats every folder as trusted (hooks docs, 2026-10-31). 4. Adding a hook to `settings.local.json` reaches already-running sessions too (observed 2026-10-31: a session started before registration logged PostToolUse lines right after). 5. No new lines from any project → the script path is gone (repo moved). The `[ -f ]` guard makes that a silent exit 1; without it, `python3 <missing>` exits 2, which blocks every Stop. 6. A/B runner arms pass `--settings '{"disableAllHooks": true}'`; a session from `run_ab.py` never shows in the global log. |
| Behavior differs from another project | Diff the layers: global CLAUDE.md and user settings apply everywhere; run the audit in both projects and compare. |
| Hitting the 5-hour usage cap | Go to `harness-token-efficiency-campaign` — don't improvise. |
| Config seems loaded but you can't tell | `claude --bare -p "..."` strips CLAUDE.md/hooks/memory; if behavior changes vs plain `claude -p`, a config layer is responsible — bisect by layer. Caveat: `--bare` reads only `ANTHROPIC_API_KEY`, never OAuth (`claude --help`, 2.1.281), so it can't auth on this key-less machine; use the stream-json init event to see what loaded instead. |

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

- Written 2026-07-06, CC 2.1.193; updated 2026-10-31, CC 2.1.281. Both scripts run and
  pass on that date.
- Config catalog drifts: re-run `audit-config.sh` and update the table when it disagrees.
- Global CLAUDE.md line count: `wc -l ~/.claude/CLAUDE.md` (113 on 2026-10-31).
- Symlinks intact: `ls -l ~/.claude/skills/`
