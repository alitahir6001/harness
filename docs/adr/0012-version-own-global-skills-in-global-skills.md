---
status: accepted
date: 2026-10-31
---
# Version the user's own global skills in global-skills/, symlinked into ~/.claude/skills/

## Context and Problem Statement
User-level skills under `~/.claude/skills/` change how every project behaves, but files there have no history (`.claude/skills/harness-change-control/SKILL.md`, intro). How should the user's global skills be versioned, given this repo is public?

## Considered Options
* Keep the source in `global-skills/` and symlink `~/.claude/skills/<name>` to it; only the user's own skills
* Leave unversioned originals in `~/.claude/skills/` (set aside on migration)
* Include third-party skills such as `grill-me` (excluded)

## Decision Outcome
Chosen option: "`global-skills/` plus symlinks, own skills only", because edits get git history while staying live in every project, and the repo is public so third-party skills stay out (`.claude/skills/harness-architecture-contract/SKILL.md:55-58`; `.ai/handoff.md:27-28`).

### Consequences
* Good, because global skill edits are reviewable and revertible via git.
* Bad, because every edit in `global-skills/` is live everywhere at once: Class C, needs user sign-off (`harness-architecture-contract/SKILL.md:55-57`).

## More Information
Evidence: ef405e7, 4e7c316, f17e3f9, 9f3b7aa (2026-10-31, one commit per skill; ef405e7 notes the copy was byte-identical); `.claude/skills/harness-architecture-contract/SKILL.md:55-58`; `.ai/handoff.md:27-28`; `.ai/history.md:33-37` (migration verified by a fresh Haiku run listing all four symlinked skills). Related: ADR-0013 (`write-adr` added the same way).
