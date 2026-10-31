# Handoff — live state snapshot

## Last updated
2026-10-31 (cleanup session). Repo-wide drift fix: session files moved to the 3-file
layout, CLAUDE.md and the seven project skills brought up to date.

## Current state
The advisor pattern lives in its own repo (`~/Desktop/projects/the-advisor`); this repo is
the learning workspace plus the versioned home of the global session skills
(`global-skills/`, symlinked into `~/.claude/skills/`). Its proactive-escalation test came
back negative on 2026-09-07 (the-advisor gotcha 28), so the "MUST" wording is retracted
and consults are on-demand only. The test stubs behind the README findings now live in
`experiments/`.

## Active task
None. The advisor validation task is closed here:
- [x] DoD 1 registration and DoD 2 at-will consult (2026-08-11)
- [x] DoD 3 proactive escalation on unlabeled work: NEGATIVE, run in the-advisor 2026-09-07
- [x] Push the 2 the-advisor README/diagram commits
- DoD 4-5 and the second-machine install are tracked by the-advisor's v1.0 gate, not here.

## Open threads
- [ ] Pin `the-advisor` and `harness` on the GitHub profile - user (unverifiable from here)
- [ ] Commit this cleanup - user
- [ ] Originals of the 4 symlinked skills sit in `~/.claude/skills-aside-2026-10-31/`;
  remove once satisfied - user. `grill-me` is third-party and stays out of the repo.
- [ ] `global-skills/create-session-context/CLAUDE.template.md` header comment and
  `build-skill-library` Phase 1 still describe the 4-file `.ai/` read order (Class C edit)

## Next recommended step
Pick a first hook from `harness-research-frontier` Frontier 3: an escalation-enforcement
hook or the Stop-hook verification gate (both motivated by gotcha 28).

## Out of scope
Advisor plugin work (edit the-advisor repo); rerunning the stub tests in place (copy them out first).
