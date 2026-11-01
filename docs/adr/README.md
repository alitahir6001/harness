# Architecture Decision Records

Why this repo is shaped the way it is: one MADR 4.0 file per design decision. Read this index first.

- [0001](0001-three-store-split-one-home-per-fact.md) - Three-store split: skills, .ai/ and CLAUDE.md, one home per fact - accepted - 2026-07-06
- [0002](0002-validate-config-changes-by-tool-use-in-a-fresh-session.md) - Validate config changes by tool_use in a fresh Haiku session - accepted - 2026-07-12
- [0003](0003-four-file-ai-layout-read-at-session-start.md) - Four-file .ai/ layout, all read at session start - superseded by ADR-0006, ADR-0008, ADR-0009 - 2026-07-12
- [0004](0004-advisor-moves-to-its-own-plugin-repo.md) - Advisor moves to its own plugin repo; experiments/advisor-pattern/ frozen - accepted - 2026-08-11
- [0005](0005-retract-the-must-escalation-mandate.md) - Retract the "MUST get a second opinion" mandate; consult on demand only - accepted - 2026-09-07
- [0006](0006-session-start-reads-only-handoff.md) - Session start reads only .ai/handoff.md; the rest loads on demand - accepted - 2026-09-20
- [0007](0007-cap-session-files-in-bytes-not-lines.md) - Cap session files in bytes, not lines - accepted - 2026-09-20
- [0008](0008-retire-current-task-md-into-handoff.md) - Retire current-task.md; fold it into handoff's Active task - accepted - 2026-09-20
- [0009](0009-session-history-lives-in-ai-history-md.md) - Session history lives in .ai/history.md; backlog holds parked items only - accepted - 2026-11-01
- [0010](0010-enforce-verification-with-a-stop-hook.md) - Enforce verification with a deterministic Stop hook, not a prose rule - accepted (provisional) - 2026-10-31
- [0011](0011-register-the-stop-gate-globally-without-subagentstop.md) - Register the stop gate globally; do not register SubagentStop - accepted (provisional) - 2026-10-31
- [0012](0012-version-own-global-skills-in-global-skills.md) - Version the user's own global skills in global-skills/, symlinked into ~/.claude/skills/ - accepted - 2026-10-31
- [0013](0013-record-decisions-as-madr-adrs-in-docs-adr.md) - Record decisions as one MADR 4.0 ADR per decision in docs/adr/ - accepted - 2026-11-01
