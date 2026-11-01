# Backlog

Parked items only. Not read at session start; history lives in history.md.

## Parked items (not session-bound)
- Hook ideas (2026-08-13), each needs a marker-file proof before it is trusted:
  - Config regression tester: replay fixed prompts via `claude -p --output-format stream-json`
    and assert on `tool_use` entries, not prose.
  - Stop-hook verification gate: block "done" until a verification command has run.
  - Destructive-command rail: PreToolUse guard on rm/mv/overwrite with an undo ledger.
