---
name: harness-evidence-and-analysis
description: How a hunch about harness behavior becomes an accepted fact here — discriminating-probe recipes for config changes (fresh-session tests, marker files for hooks, --bare bisection), premise teardown, and root-cause for "Claude ignored my rule". Use when verifying whether a config change works, debating whether a claim is true, testing skill triggering, or before writing any new fact into a skill. Keywords: verify, prove, test config, experiment, evidence, did it work, root cause, hypothesis.
---

# Evidence & analysis — harness workspace

The failure mode this skill exists to prevent: config edits that "look right" get
trusted, then silently do nothing (or worse) in every later session. The repo's evidence
bar is summarized in `harness-runbook` → Validation bar; this skill is the how.

**When NOT to use this skill:** for whether you're ALLOWED to make the change, see
`harness-change-control`. For triaging a known symptom, start with the
`harness-runbook` table.

## Core principle: the discriminating probe

A probe is discriminating when old-config and new-config produce **visibly different
outputs** on it. "It seems to behave better" is not evidence. Cheapest fresh session:

```bash
claude -p "probe task here"          # one-shot, non-interactive
claude --bare -p "probe task here"   # same, with CLAUDE.md/hooks/memory stripped
```

The pair gives you a bisection for free: plain vs `--bare` differ → some config layer
causes the behavior; then reintroduce layers one at a time (`--add-dir`,
`--append-system-prompt`, `--settings`) to find which. (Flags verified against
`claude --help`, 2.1.193 and 2.1.281.) Caveat: `--bare` authenticates only with
`ANTHROPIC_API_KEY`/`apiKeyHelper`, never OAuth, so on this key-less machine the bare
half can't run; bisect by copying the project out and adding layers back instead.

## Recipes

### 1. "Does my CLAUDE.md rule work?"
Write a probe whose natural answer VIOLATES the rule, run `claude -p` fresh, check
whether the rule shaped the output. Example from this machine's global CLAUDE.md
("short answers for factual questions"): probe `claude -p "what does chmod +x do"` —
rule working = a couple of lines; a tutorial essay = rule not loading or drowned out
(then: runbook symptom table, "rule ignored" row).

### 2. "Does my hook fire?" (marker-file technique)
Give the hook command a side effect you can check:
`"command": "... && echo fired-$(date +%s) >> /tmp/hook-marker"` — run a session that
should trigger the event, then `cat /tmp/hook-marker`. No marker = hook not firing;
debug registration before debugging the hook's real payload. This is the mandatory
first test for any hook (`harness-change-control`, non-negotiable 5). Real example:
`.claude/hooks/stop_gate.py` logs every call to `~/.claude/stop-gate/marker.log`; its
smoke run showed the hook firing correctly while its v0 message still misdirected the
model, so check the marker AND the behavior. Lines carry `session`, `action`, `agent_id`/
`agent_type` (set on subagent calls) and `cwd`; `experiments/stop-gate-test/field_report.py`
joins them to transcripts for per-project nudge counts, follow-through and extra tokens.
Read what the hook actually injected from the transcript's `hook_additional_context` row:
that's how the v1 truncated-label bug was found while the marker looked healthy.

### 3. "Does my skill trigger?"
Two-step: (a) explicit `/<name>` — proves the file parses and loads; (b) fresh session
phrased the way a real user would ask, WITHOUT naming the skill — proves the
description triggers. Only (b) passing makes auto-trigger claims true. Log phrasings
that failed to trigger; they are the exact words to add to the description.

### 4. Premise teardown (before building anything)
State the premise, then ask what the cheapest observation is that would falsify it.
Worked example (this repo, 2026-07-06): premise "this repo needs discovery of its
codebase" — one `ls` falsified it (2 files, no code); the real sources were auto-memory
and the user. Cost of the teardown: one command. Cost of skipping it: a skill library
describing an imaginary codebase.

### 5. Root-cause chain for "Claude ignored X"
Ask in order, stop at first failure: **Loaded?** (audit script / `/context`) →
**Findable?** (is the file over ~30 lines / is the rule buried?) → **Directive?**
(phrased as an instruction, not background?) → **Contradicted?** (does another layer
say otherwise — check global vs project). Fixing a later link while an earlier one is
broken wastes the effort. All four can pass and the rule still not fire: the advisor's
"MUST" rule was loaded, directive and uncontradicted, and the model acknowledged it, then
made zero calls (2026-09-07, the-advisor gotcha 28). Past that point, the fix is a hook.

### 6. A test can contaminate its own result
The probe's framing can force the behavior on its own. Real case (2026-09-07,
`experiments/rules-ab-test/`): an A/B on a "verify the downstream effect" rule came out
inconclusive twice, because asking "did it work?" made the model check carefully with or
without the rule. The real failures happened mid-task, when nobody asked. Design the
probe so the behavior is a side effect of an unrelated task, never the question itself.
Also run stubs outside this repo: in place they inherit its `CLAUDE.md` and skills.

## Worked-example honesty

Recipe 4's example and recipes 5–6's 2026-09-07 cases are real; recipes 1–3 are
constructed from 2026-07-06 verification work, not from accumulated incidents.
Replace them with real cases as they occur — a recipe with a real local failure attached
teaches far better. Log candidates in `.ai/backlog.md`.

## Provenance and maintenance

- Written 2026-07-06, CC 2.1.193; updated 2026-10-31, CC 2.1.281. Flags re-check:
  `claude --help | grep -E 'bare|print|append'`.
- Global-CLAUDE.md probe example depends on `~/.claude/CLAUDE.md` keeping its
  short-answers rule — re-check: `cat ~/.claude/CLAUDE.md`.
