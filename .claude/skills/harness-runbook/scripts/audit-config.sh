#!/bin/bash
# Read-only audit of every config layer that shapes Claude Code sessions in this project.
# Usage: bash .claude/skills/harness-runbook/scripts/audit-config.sh
set -u
PROJ="$(cd "$(dirname "$0")/../../../.." && pwd)"
echo "== Claude Code config audit — $(date +%F) =="
echo "CLI: $(claude --version 2>/dev/null || echo 'claude not on PATH')"
echo
echo "-- Always-loaded layers (every line = per-turn cost) --"
for f in "$HOME/.claude/CLAUDE.md" "$PROJ/CLAUDE.md" "$PROJ/CLAUDE.local.md"; do
  if [ -f "$f" ]; then
    echo "  $f: $(wc -l < "$f" | tr -d ' ') lines"
  else
    echo "  $f: (absent)"
  fi
done
MEM="$HOME/.claude/projects/$(echo "$PROJ" | tr '/_' '--')/memory/MEMORY.md"
if [ -f "$MEM" ]; then
  echo "  memory index: $(wc -l < "$MEM" | tr -d ' ') lines ($MEM)"
else
  echo "  memory index: (absent)"
fi
echo
echo "-- Settings --"
# Never print settings raw: `env` holds tokens (CLAUDE_CODE_OAUTH_TOKEN).
redact() {
  python3 - "$1" <<'PY'
import json, re, sys
SECRET = re.compile(r"token|secret|password|key|auth", re.I)
def mask(o, under_env=False):
    if isinstance(o, dict):
        return {k: "<redacted>" if isinstance(v, str) and (under_env or SECRET.search(k))
                else mask(v, under_env or k == "env") for k, v in o.items()}
    if isinstance(o, list):
        return [mask(v, under_env) for v in o]
    return o
try:
    data = json.load(open(sys.argv[1]))
except ValueError:
    print("    (not valid JSON; not printed, may contain secrets)")
    sys.exit(0)
for line in json.dumps(mask(data), indent=2).splitlines():
    print("    " + line)
PY
}
for f in "$HOME/.claude/settings.json" "$PROJ/.claude/settings.json" "$PROJ/.claude/settings.local.json"; do
  if [ -f "$f" ]; then echo "  $f:"; redact "$f"; else echo "  $f: (absent)"; fi
done
echo
echo "-- Hooks configured --"
# Collect output, not grep's exit code: a missing settings file makes grep exit 2 even on a match.
hooks="$(grep -l '"hooks"' "$HOME/.claude/settings.json" "$PROJ/.claude/settings.json" "$PROJ/.claude/settings.local.json" 2>/dev/null)"
if [ -n "$hooks" ]; then echo "$hooks" | sed 's/^/  /'; else echo "  none"; fi
echo
echo "-- Skills (descriptions always load; bodies load on trigger) --"
for d in "$PROJ/.claude/skills" "$HOME/.claude/skills"; do
  if [ -d "$d" ]; then
    for s in "$d"/*/SKILL.md; do
      [ -f "$s" ] || continue
      echo "  $(basename "$(dirname "$s")") ($(wc -l < "$s" | tr -d ' ') lines) [$d]"
    done
  fi
done
echo
echo "-- Subagents --"
ls "$PROJ/.claude/agents" "$HOME/.claude/agents" 2>/dev/null || echo "  none"
