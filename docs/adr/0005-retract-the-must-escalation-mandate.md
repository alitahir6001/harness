---
status: accepted
date: 2026-09-07
---
# Retract the "MUST get a second opinion" mandate; consult on demand only

## Context and Problem Statement
The advisor relied on a "MUST get a second opinion" rule to make the model escalate hard-to-reverse decisions on its own. A clean test on 2026-09-07 gave the model a real hard-to-reverse decision with no trigger words: it saw the mandate, said it would act on it, and made zero `consult_advisor` calls (`experiments/escalation-test/RESULT.md:15-18`). Should the mandate stay?

## Considered Options
* Retract the mandate; consults happen on demand only
* Keep or strengthen the directive wording
* Enforce escalation with a deterministic hook

## Decision Outcome
Chosen option: "retract; on demand only", because stronger wording did not close the gap (`README.md:52-57`) and an acknowledged rule is not evidence it fires (`CLAUDE.md` gotcha 3). Hook enforcement was not rejected: it is named as the real fix (`RESULT.md:17-18`) and deferred, listed as the next build after the stop-gate kill-test (`.ai/handoff.md:48`).

### Consequences
* Good, because CLAUDE.md no longer claims behavior that was measured not to happen (`CLAUDE.md:21-22`).
* Bad, because proactive escalation is unsolved until a hook exists.

## More Information
Evidence: `experiments/escalation-test/RESULT.md:15-18`; `CLAUDE.md:21-22`; 7c8579a (2026-10-31, CLAUDE.md retraction applied here); the-advisor `CLAUDE.md` gotcha 28. Related: ADR-0002 (validation bar), ADR-0004, ADR-0010 (the hook approach applied to verification).
