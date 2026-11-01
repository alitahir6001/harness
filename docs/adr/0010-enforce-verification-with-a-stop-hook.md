---
status: accepted
date: 2026-10-31
---
# Enforce verification with a deterministic Stop hook, not a prose rule

## Context and Problem Statement
Prose rules were measured not to fire (ADR-0005), and the user's global "Done requires evidence" rule loaded in every arm of the test without changing the outcome (`experiments/stop-gate-test/RESULT.md:22-23`). On a deploy fixture whose copy step fails silently, control and prose-rule runs all reported success. How should "verify before calling it done" be enforced?

## Considered Options
* A Stop hook that, once per turn, returns a non-blocking `additionalContext` nudge naming the turn's recorded actions (v1)
* The same instruction as a prose CLAUDE.md rule
* A generic "check the downstream effect" nudge (v0)
* Continuing the turn with `decision: block`

## Decision Outcome
Chosen option: "Stop hook with an action-naming `additionalContext` nudge", because it checked the real effect 3/3 vs 0/3 for the prose rule and 0/3 for control (`RESULT.md:25-31`). v0's generic nudge made Haiku re-verify the file it had just written; naming the turn's actions is the one thing a hook can say that a standing rule cannot (`RESULT.md:45-48`). `additionalContext` continues the turn like `decision: block`, without an error label (`.claude/hooks/stop_gate.py:96`).

### Consequences
* Good, because the check is deterministic and observable via a marker log (`stop_gate.py:86-93`).
* Bad, because it costs ~2.9x the tokens on the test task (`RESULT.md:50-51`).
* Bad, because it reports failures but does not repair them: 0/9 runs corrected the CHANGELOG (`RESULT.md:49`).
* Provisional: n=3 per arm, one model, one fixture (`RESULT.md:55`); a kill-test on live use is due 2026-11-07 (`.ai/handoff.md:34-45`).

## More Information
Evidence: e87f6a7 (2026-10-31, gate v1.1); `experiments/stop-gate-test/RESULT.md:25-51`; `.claude/hooks/stop_gate.py:95-98`. Related: ADR-0005, ADR-0011 (where it is registered).
