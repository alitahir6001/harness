---
name: harness-change-control
description: How config changes are classified and gated in this workspace — which edits are free, which need a fresh-session test, which touch global scope and need explicit user sign-off. Use BEFORE editing any CLAUDE.md, settings.json, hook, skill, or ~/.claude file, or when asked to "just add a rule/permission/hook". Keywords: change control, is this safe, edit settings, add permission, add hook, modify CLAUDE.md, promote, gate.
---

# Change control — harness workspace

Every change here alters how FUTURE Claude sessions behave, for this project or for all
of the user's projects. That's the risk being gated: a bad application-code change breaks
one feature; a bad harness change silently degrades every session after it. Repo files
are in git since 2026-07-12, so revert via git; `~/.claude/` files outside
`global-skills/` have no history at all.

**When NOT to use this skill:** for what the config surfaces are, see
`harness-reference`. For HOW to run the verification tests below, see
`harness-evidence-and-analysis`; commands live in `harness-runbook`.

## Classification

| Class | What | Gate |
|---|---|---|
| A — free | `.ai/` edits; new skill drafted as candidate; anything in scratch dirs | None. Note it in `.ai/history.md`. |
| B — per-project blast radius | Live `CLAUDE.md` / `CLAUDE.local.md`; `.claude/settings*.json`; hooks; editing an existing skill's `description` | Fresh-session test BEFORE calling it done (below), + token-cost check for anything always-loaded |
| C — global blast radius | Anything under `~/.claude/` (global CLAUDE.md, user settings.json, user-level skills); changing the default model/effort | Explicit user sign-off in the current conversation, every time. Prior approval of a similar change does not carry over. |

## Non-negotiables (with rationale — seeded 2026-07-06 from Anthropic's CLAUDE.md best-practices guidance plus the user's Pro-limit constraint)

1. **Always-loaded text pays rent.** Before adding a line to any CLAUDE.md or any skill
   `description`, ask: "would removing this cause a mistake?" If no, don't add it.
   Rationale: loaded every turn/session; the user hits the Pro 5-hour cap, so bloat
   directly costs him working time (see `harness-token-efficiency-campaign`).
2. **Project-local before global.** New permissions and settings go in
   `.claude/settings.local.json` first; promote to `~/.claude/settings.json` only after
   they've proven useful in more than one project. Rationale: limits blast radius; local
   is the only layer where a mistake affects just this repo.
3. **No unverified facts in skills.** A claim goes into a skill only if observed in a
   real session, verified against `claude --help`/local files, or explicitly labeled
   UNVERIFIED. Rationale: a wrong runbook misleads every future session that trusts it.
4. **Templates stay inert.** Never rename `*.template.md` (e.g.
   `global-skills/create-session-context/CLAUDE.template.md`) to a name auto-discovery
   picks up (`CLAUDE.md`, `CLAUDE.local.md`) without the user asking.
5. **Hooks must be observable.** Any hook added must have a way to confirm it fired
   (e.g. append to a marker file) before it's trusted. Rationale: hooks fail silently;
   an unfired hook is indistinguishable from a working one until it matters.
6. **Don't route around this file.** If a change doesn't fit a class, treat it as the
   higher class.

## The Class B fresh-session test (the minimum bar)

A config change is DONE only when demonstrated in a session that did not exist when you
made the change — reading the file back proves nothing about behavior:

```bash
# cheapest probe: one-shot, non-interactive
claude -p "one-line task that exercises the changed behavior"
```

Expected: the new rule/permission/skill visibly shapes the output. If unchanged →
diagnose with the symptom table in `harness-runbook` before touching the config again.

## Recording

Every Class B/C change gets one line in `.ai/history.md`: date, what, why, how verified.
Git records what changed; the history line records why and how it was verified.

## Provenance and maintenance

- Written 2026-07-06 (CC 2.1.193); updated 2026-10-31 (CC 2.1.281). Sources: Anthropic's
  CLAUDE.md best-practices guidance (the usage block in
  `global-skills/create-session-context/CLAUDE.template.md`), user constraint from
  auto-memory (Pro plan, hourly caps).
- First real incident behind rule 3: the advisor's "MUST" escalation rule was believed to
  work, then measured not to fire (2026-09-07, the-advisor gotcha 28).
- Re-verify the permission baseline: `cat .claude/settings.local.json`
