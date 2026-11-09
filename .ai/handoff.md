# Handoff — live state snapshot

## Last updated
2026-10-31 (review session, last of three that day). Earlier: the cleanup session
(3-file layout, skills) and the stop-gate session (gate v1.1 global, field report).
This session dropped Recent context from the global CLAUDE.md template.

## Current state
The advisor pattern lives in its own repo (`~/Desktop/projects/the-advisor`); this repo is
the learning workspace plus the versioned home of the global session skills
(`global-skills/`, symlinked into `~/.claude/skills/`). Its proactive-escalation test came
back negative on 2026-09-07 (the-advisor gotcha 28), so the "MUST" wording is retracted
and consults are on-demand only. The test stubs behind the README findings now live in
`experiments/`. Session logs and the change log live in `.ai/history.md` (split out of
`backlog.md` 2026-11-01, which now holds parked items only); read it only when asked
about past work.

## Active task
None. The advisor validation task is closed here:
- [x] DoD 1 registration and DoD 2 at-will consult (2026-08-11)
- [x] DoD 3 proactive escalation on unlabeled work: NEGATIVE, run in the-advisor 2026-09-07
- [x] Push the 2 the-advisor README/diagram commits
- DoD 4-5 and the second-machine install are tracked by the-advisor's v1.0 gate, not here.

## Open threads
- [ ] Pin `the-advisor` and `harness` on the GitHub profile - user (unverifiable from here)
- [ ] Delete `~/.claude/settings.json.bak-stopgate-20261031-160521` once the kill-test is
  settled - user
- [x] Originals of the 4 symlinked skills (`~/.claude/skills-aside-2026-10-31/`) moved to
  Trash 2026-11-08 - user. `grill-me` is third-party and stays out of the repo.
- [x] `CLAUDE.template.md` header and `build-skill-library` Phase 1 moved to the 3-file
  layout; template's Recent context section dropped, history goes to `history.md`
  (2026-10-31, user-approved Class C)

## Next recommended step
**Watch stop-gate v1.2 field data** (risk-scoped since 2026-11-08; kill-test done: kept and
tuned, see `.ai/history.md` 2026-11-08). The gate now nudges only after risky actions
(`is_risky()` in `.claude/hooks/stop_gate.py`); routine calls log `skip` in
`~/.claude/stop-gate/marker.log`. Replay predicted 64% fewer nudges. After ~a week: count
`nudge` vs `skip` in marker.log, rerun `field_report.py`, and sample a few nudges for real
catches. Watch for misses (risky work that got `skip`), e.g. scripts that write global config
without naming the path.
Fragility: the command points into this repo. Moving or renaming it silences the gate
everywhere (the `[ -f ]` guard makes that a quiet exit 1, not a blocking exit 2).
Next build after this: escalation enforcement.

## Out of scope
Advisor plugin work (edit the-advisor repo); rerunning the stub tests in place (copy them out first).
