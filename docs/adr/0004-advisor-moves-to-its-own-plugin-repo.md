---
status: accepted
date: 2026-08-11
---
# Advisor moves to its own plugin repo; experiments/advisor-pattern/ frozen

## Context and Problem Statement
The advisor/workhorse pattern was built in this repo, then promoted to user-level copies under `~/.claude/`. Providing the same agent both manually and via a plugin yielded two advisor agents and two MCP servers in one session (`README.md:66-67`). Where should the advisor live?

## Considered Options
* Its own public repo, packaged as a Claude Code plugin; this repo keeps a frozen dev snapshot
* Global copies under `~/.claude/` (promoted, then deleted as duplicates)

## Decision Outcome
Chosen option: "own plugin repo", because duplicate installs compete: one source, or neither (`README.md:66-67`). The plugin is [the-advisor](https://github.com/alitahir6001/the-advisor).

### Consequences
* Good, because there is one installed source of the advisor.
* Good, because `experiments/advisor-pattern/` stays as history (`README.md:90-91`).
* Bad, because the snapshot looks runnable; CLAUDE.md has to warn that it is NOT what runs (`CLAUDE.md:19-20`).

## More Information
Evidence: 9f7c1b2 (2026-08-11: deletes `.claude/agents/advisor.md`, the advisor skills and `.mcp.json`); `CLAUDE.md:19-20`; `README.md:66-67,84-91`; `.ai/history.md:58-60` (promoted to `~/.claude/`, then repackaged and the global copies deleted). Advisor design decisions are recorded in the-advisor's own ADRs. Related: ADR-0005.
