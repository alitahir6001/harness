---
status: accepted
date: 2026-07-06
---
# Three-store split: skills, .ai/ and CLAUDE.md, one home per fact

## Context and Problem Statement
The workspace holds three kinds of text that load at very different costs: durable knowledge, live session state, and rules needed every turn. Duplicated facts drift, and every line in CLAUDE.md is a per-turn token cost on a plan that hits its usage cap (`.claude/skills/harness-architecture-contract/SKILL.md:18-29`). Where should each fact live?

## Considered Options
* Three stores with one home per fact: skills = durable knowledge, `.ai/` = live state, CLAUDE.md = per-turn rules; knowledge graduates inward
* Move knowledge into CLAUDE.md "so it's always available"

## Decision Outcome
Chosen option: "three stores, one home per fact", because CLAUDE.md is loaded every turn, so putting knowledge there turns a pay-per-use cost (a skill, loaded on trigger) into a pay-every-turn cost (`.claude/skills/harness-token-efficiency-campaign/SKILL.md:86-89`).

### Consequences
* Good, because each fact has one authoritative copy; the others point to it (`harness-architecture-contract/SKILL.md:26-29`).
* Good, because findings follow a fixed path: raw in `.ai/`, verified into a skill, into CLAUDE.md only if needed every turn (`harness-architecture-contract/SKILL.md:43-46`).
* Bad, because a session must know which store to look in; agents that read three versions of a fact pick the wrong one when the split blurs (`README.md:42-44`).

## More Information
Evidence: `.claude/skills/harness-architecture-contract/SKILL.md:18-29,43-46` (written 2026-07-06, per its provenance at line 75); `.claude/skills/harness-token-efficiency-campaign/SKILL.md:86-89` (the rejected direction, listed as a fenced-off path); `README.md:42-44`. The decision predates git; the first commit is 4b06f20 (2026-07-12). Date taken from the skill's provenance line.
