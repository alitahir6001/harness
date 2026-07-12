---
name: harness-research-frontier
description: Open problems where this workspace can advance past stock Claude Code usage — building an own harness on the Agent SDK, skill-triggering reliability measurement, hook-based context hygiene. Each with why stock falls short, this repo's asset, the first three concrete steps, and a falsifiable "you have a result when…" milestone. Use when the user asks what to build next, wants to start the own-harness project, or asks how to level up from config usage to harness construction. Keywords: build my own harness, agent SDK, next project, roadmap, experiment, what should I work on.
---

# Research frontier — harness workspace

The user's stated arc (memory, 2026-07-06): master the Claude Code config layer → build
an own harness on the Agent SDK. Building is aspirational, not a live project; nothing
below is committed work. Everything here is OPEN/CANDIDATE — no result exists yet.

**When NOT to use this skill:** for operating today's setup, use `harness-runbook`;
for today's live problem (usage caps), use `harness-token-efficiency-campaign`.

## Frontier 1 — Minimal own harness on the Agent SDK (the headline goal)

- **Why stock falls short:** no control over context assembly. Stock CC decides what
  enters the window (system prompt, tool schemas, memory, skill descriptions); on a
  capped Pro plan, unremovable overhead is unremovable cost. An own harness makes every
  token opt-in.
- **This repo's asset:** the accumulated harness knowledge in these skills — especially
  the token-cost model in `harness-reference` — is exactly the design spec for a lean
  harness. Plus `.ai/` as the experiment log.
- **Step 0 (do first, it gates everything): settle auth/billing.** Whether Agent SDK /
  API calls can run on the Pro subscription or need separate API credits is UNVERIFIED
  and decisive for how much experimenting is affordable. Check the Agent SDK docs +
  account console before writing code.
- **First three steps in this repo:**
  1. `experiments/01-loop/` — smallest possible agent: hand-written system prompt, one
     tool (bash), one task ("list this repo's files and summarize"). No framework
     beyond the SDK.
  2. `experiments/02-skills/` — add opt-in knowledge loading: inject a SKILL.md body
     only when the task matches its description (your own trigger logic).
  3. Benchmark: same 3 tasks in stock `claude -p` vs your harness; capture input-token
     counts from the API usage data.
- **You have a result when:** the same task completes correctly in your harness with
  measurably fewer input tokens than stock CC — numbers logged, not judged by eye
  (evidence bar: `harness-runbook` → Validation).

## Frontier 2 — Skill-triggering reliability (measurement, not vibes)

- **Why stock falls short:** auto-triggering is opaque; nobody (including these skills'
  author) knows this library's real trigger hit-rate. Descriptions were written by
  intuition.
- **Asset:** a fresh 7-skill library with honest descriptions, plus recipe 3 in
  `harness-evidence-and-analysis` as the probe design.
- **First three steps:** (1) write 3 natural phrasings per skill into
  `.ai/notes.md`; (2) run each as `claude -p`, record trigger hit/miss; (3) rewrite the
  worst description using the missed phrasings, re-run.
- **You have a result when:** a before/after hit-rate table exists and the rewritten
  description measurably beats its old version.

## Frontier 3 — First hook: deterministic context hygiene

- **Why stock falls short:** habits like "clear between tasks" (campaign Phase 3)
  depend on the model or user remembering; hooks make behavior deterministic. Also the
  agreed-but-undone next step from the 2026-07-06 session ("a lint/test hook") — there
  is no lint/test to run here yet, so the harness-native variant is a session-event
  hook instead.
- **Asset:** `harness-change-control` non-negotiable 5 (marker-file observability) and
  the audit script give a safe path to a first hook.
- **First three steps:** (1) read the hooks doc (URL in `harness-reference`) and verify
  event names — they are UNVERIFIED locally; (2) add a `SessionStart`-type hook in
  `.claude/settings.local.json` that just appends to a marker file; (3) verify with
  recipe 2, then give it a real payload (e.g. echo the audit script's line counts).
- **You have a result when:** the marker proves the hook fires on every session start,
  and the payload survives a week without being annoying enough to remove.

## Ordering recommendation

3 → 2 → 1. Frontiers 3 and 2 are hours-sized, run on the existing subscription, and
teach the exact mechanics (context injection, triggering) that Frontier 1 reimplements.
Frontier 1 waits on its Step 0 billing answer.

## Provenance and maintenance

- Written 2026-07-06, CC 2.1.193, from user-confirmed goals + auto-memory. No
  experiment has run yet; delete or update frontiers as results land (log in
  `.ai/backlog.md`, promote findings per `harness-architecture-contract` decision 3).
- Agent SDK status/auth: re-check docs before Frontier 1 — the SDK moves fast.
