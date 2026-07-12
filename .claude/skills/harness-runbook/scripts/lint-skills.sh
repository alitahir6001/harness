#!/bin/bash
# Read-only lint of .claude/skills/: frontmatter present, name matches dir, description non-empty.
# Usage: bash .claude/skills/harness-runbook/scripts/lint-skills.sh
set -u
PROJ="$(cd "$(dirname "$0")/../../../.." && pwd)"
FAIL=0
for s in "$PROJ"/.claude/skills/*/SKILL.md; do
  [ -f "$s" ] || { echo "no skills found"; exit 0; }
  dir="$(basename "$(dirname "$s")")"
  head -1 "$s" | grep -q '^---$' || { echo "FAIL $dir: no frontmatter"; FAIL=1; continue; }
  name="$(awk -F': ' '/^name:/{print $2; exit}' "$s")"
  desc="$(awk -F': ' '/^description:/{print $2; exit}' "$s")"
  [ "$name" = "$dir" ] || { echo "FAIL $dir: name '$name' != dir"; FAIL=1; }
  [ -n "$desc" ] || { echo "FAIL $dir: empty description"; FAIL=1; }
  grep -q '## Provenance' "$s" || { echo "WARN $dir: no Provenance section"; }
done
[ "$FAIL" -eq 0 ] && echo "OK: all skills pass"
exit "$FAIL"
