---
name: harness-token-efficiency-campaign
description: Decision-gated campaign against the hardest live problem — hitting the Pro plan's rolling 5-hour usage limit. Phased plan with exact commands, expected observations at each gate, ranked levers (model/effort choice, always-loaded context diet, session hygiene) each with a kill-test, and fenced-off wrong paths. Use when the user hits usage limits, complains sessions are expensive, asks how to save tokens/context, or before adding anything always-loaded. Keywords: usage limit, rate limit, 5-hour cap, token cost, context budget, expensive, opus vs sonnet, compact.
---

# Campaign: stop hitting the Pro 5-hour cap

Problem (from memory, confirmed 2026-07-06): Pro plan, regularly hits the rolling
5-hour usage limit, rarely the weekly one. Every phase below routes changes through
`harness-change-control` (model/effort defaults are Class C — user sign-off).

**When NOT to use this skill:** for what the config layers cost in general, see
`harness-reference`. For designing the measurement probes, see
`harness-evidence-and-analysis`.

## Phase 0 — Baseline (no baseline, no campaign)

Measured baseline (September 2026, audit of 171 sessions across the user's projects):
- Session startup in job-apply: ~49k tokens reading every `.ai/` file eagerly → ~15k
  after lazy loading (handoff only) and CLAUDE.md dedupe, a 69% cut.
- Late wrap-ups cost ~2× the output of early ones (~11,200 vs ~5,700 tokens), holding
  when matched on workload. Write the handoff at a task boundary.
- Method gotchas: transcript JSONL repeats one response's `usage` across several
  records, so dedupe by `requestId` or counts double; dense markdown ran ~2.5 bytes/token,
  not the usual 4.

```bash
bash .claude/skills/harness-runbook/scripts/audit-config.sh   # always-loaded inventory
```
In an active session: `/context` (context composition) and `/cost` (session usage).
Then log in `.ai/history.md` for ~3 working days: date, sessions until cap, model used,
task types.

**Gate:** you have numbers. If `/context` or `/cost` output differs from expectations
(UNVERIFIED: exact output format on Pro; subscription sessions may not show dollar
figures) → record what they DO show and use that as your metric. If you can't measure
at all → fall back to the crudest metric: wall-clock time until the cap message.

## Phase 1 — The big lever: model and effort

Verified 2026-07-06: `~/.claude/settings.json` set `model: opus`, `effortLevel: high`
— the most expensive default available, applied to ALL projects, including trivial tasks.
As of 2026-10-31 it has no `model` key and `effortLevel: medium` (audit script).

- Action: keep opus for hard work, drop to sonnet for routine work — per-session
  (`claude --model sonnet` or `/model`) before changing the global default.
- Theory of value: usage limits weight opus far above sonnet; most sessions aren't
  opus-hard. (Exact weighting UNVERIFIED — Anthropic doesn't publish the multiplier;
  the direction is documented.)
- **Kill-test:** run one typical week's mix on sonnet-by-default. If output quality
  forces redos often enough to erase the gain, or caps still hit at the same rate, the
  lever is dead — revert and move to Phase 2 as primary.
- Expected at gate: measurably more sessions per 5-hour window. If you see no change →
  your burn is dominated by context size, not model choice → Phase 2 matters more.

## Phase 2 — Always-loaded diet

Every line in global CLAUDE.md, memory MEMORY.md, and every skill description is paid
on every turn/session. Current footprint is small (audit, 2026-07-06: 7-line global
CLAUDE.md, 2-line memory index, ~9 skill descriptions) — so the risk is GROWTH, not
the current state. The growth happened: 2026-10-31 audit shows a 113-line global
CLAUDE.md, a 40-line project CLAUDE.md and a 6-line memory index.
- Action: enforce change-control rule 1 ("always-loaded text pays rent"); re-run the
  audit monthly; keep skill descriptions dense but single-sentence-per-concern.
- **Kill-test:** if the audit shows the always-loaded set under ~150 lines total,
  further dieting is noise — stop optimizing here.

## Phase 3 — Session hygiene (ranked, cheapest first)

1. `/clear` between unrelated tasks — context from task A is pure cost for task B.
2. Point Claude at exact files/lines instead of letting it search; searches read many
   files into context.
3. Ask for targeted reads ("read only lines 100–150") on big files.
4. `/compact` only at natural boundaries (after a task completes), not mid-task.
- **Kill-test per habit:** watch `/context` before/after for a week; a habit that
  doesn't visibly change context growth gets dropped from the routine.

## Fenced-off wrong paths (do not revisit without new evidence)

- **Spawning subagents "to save context."** Each starts cold and re-reads everything;
  on a capped plan this is the most expensive shape (also stated in the
  build-skill-library skill). Only worth it when the parent context is already huge AND
  the subtask needs little of it.
- **Aggressive mid-task `/compact`.** Loses working state; the redo costs more than the
  compaction saved.
- **Moving knowledge into CLAUDE.md "so it's always available."** That converts a
  pay-per-use cost (skill) into a pay-every-turn cost. Direction of travel is the
  opposite: CLAUDE.md → skill (see `harness-architecture-contract`, three-store rule).
- **Shorter replies as a savings strategy.** Output tokens are a minor share of an
  agentic session's usage vs repeated context (input) processing. (UNVERIFIED ratio;
  directionally solid.)

## Validation & promotion

Success metric (measurable, never by eye): **sessions—or tasks—completed per 5-hour
window before the cap**, logged in `.ai/history.md`, compared to the Phase 0 baseline.
A lever is promoted (made a default, e.g. changing `~/.claude/settings.json` model) only
after its kill-test fails to kill it across ≥1 week of normal use, and only via a
Class C sign-off (`harness-change-control`).

## Provenance and maintenance

- Written 2026-07-06, CC 2.1.193; updated 2026-10-31, CC 2.1.281. Settings facts:
  `audit-config.sh` (never `cat ~/.claude/settings.json`: its `env` holds the OAuth token).
- Phase 0 baseline source: the September 2026 cross-project audit (README "Cost" findings).
- Footprint numbers: re-run `audit-config.sh` (they WILL drift as skills are added).
- Plan limits change; re-check https://www.anthropic.com pricing/limits pages before
  trusting the Phase 1 weighting claim.
