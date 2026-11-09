#!/usr/bin/env python3
"""Stop-hook verification gate (v1.2).

PostToolUse (Edit|Write|MultiEdit|NotebookEdit|Bash) records each risky action (is_risky), a
subagent's too (same session_id); routine ones are only logged. Stop nudges once per turn that recorded any, naming those actions and
asking Claude to check their real effect. A Stop that pauses for a background subagent defers.
State and marker log live in $STOP_GATE_DIR (default ~/.claude/stop-gate/).
"""
import json
import os
import re
import sys
import time

CHECK = ("name the effect it was supposed to have (a file's contents, a value, a service's "
         "state) and check that effect directly. A script's or tool's own success message "
         "doesn't count. If you already checked, say what you checked.")
# Also the prose-rule text in experiments/stop-gate-test, so the arms differ only in delivery.
GENERIC = ("Before you finish, verify your work: for each command you ran and file you "
           "changed, " + CHECK)
MAX_ITEMS, MAX_CHARS = 8, 100

# v1.2 risky set, replayed 2026-11-08 against 129 v1.1 nudges: fires on 47, incl. the hermes-token catch.
_HOME = re.escape(os.path.expanduser("~"))
_HOME_DOT = r"(~|\$HOME|\$\{HOME\}|" + _HOME + r")/\."
_SECRET = re.compile(r"\.env\b|settings(\.local)?\.json|\.zshrc|sk-ant-|(?<![a-z])(token|secret)(?![a-z-])"
                     r"|passw(or)?d|credential|(?<![a-z])(api[_-]?)?keys?(?![a-z])", re.I)
_DESTRUCT = re.compile(r"(^|[\s;&|(`])(sudo\s+)?(rm|mv|rmdir|unlink|trash)\s|\.Trash\b")
_PUSH = re.compile(r"\bgit\b[^;&|\n]*\bpush\b")
# Lookbehind skips `2>/dev/null` and `2>&1`.
_BASH_WRITE = re.compile(r"(?<![\d&])>>?\s*['\"]?" + _HOME_DOT + r"|\btee\s+(-a\s+)?['\"]?" + _HOME_DOT
                         + r"|\bsed\s+-i|\b(cp|ln|chmod|chown|install|mkdir|touch)\s")
_HOME_DOT_PATH = re.compile(r"(" + _HOME + r"|~)/\.(?!claude/plans/)")  # plan-mode files are routine


def is_risky(tool, tool_input):
    """True for secrets, rm/mv/Trash, git push, or writes to home dotfiles (~/.claude, ~/.zshrc...)."""
    if tool == "Bash":
        cmd = str(tool_input.get("command", ""))
        return bool(_SECRET.search(cmd) or _DESTRUCT.search(cmd) or _PUSH.search(cmd)
                    or (re.search(_HOME_DOT, cmd) and _BASH_WRITE.search(cmd)))
    path = str(tool_input.get("file_path") or tool_input.get("notebook_path") or "")
    return bool(_SECRET.search(path) or _HOME_DOT_PATH.match(path))


def decide(event, stop_hook_active, dirty, waiting=False, risky=True):
    """Return 'mark', 'skip', 'nudge', 'defer' or 'allow'."""
    if event == "PostToolUse":
        return "mark" if risky else "skip"
    if event == "Stop" and dirty and not stop_hook_active:
        # Paused for a background subagent: keep the record, nudge when the work really ends.
        return "defer" if waiting else "nudge"
    return "allow"


def relative(text, cwd):
    """Drop the session cwd from paths: absolute paths otherwise eat the label's char budget."""
    if not cwd:
        return text
    for prefix in sorted({cwd, os.path.realpath(cwd)}, key=len, reverse=True):
        text = re.sub(r"(?<![\w.-])" + re.escape(prefix) + r"(/|(?![\w.-]))",
                      lambda m: "" if m.group(1) else ".", text)
    return text


def describe(tool, tool_input, cwd=None):
    """One short label for a recorded action, e.g. 'ran `./deploy.sh`'."""
    if tool == "Bash":
        cmd = relative(" ".join(str(tool_input.get("command", "")).split()), cwd)
        return f"ran `{cmd[:MAX_CHARS]}`"
    path = tool_input.get("file_path") or tool_input.get("notebook_path") or "?"
    return f"{'wrote' if tool == 'Write' else 'edited'} `{os.path.basename(path)}`"


def build_reason(actions):
    """Reason text naming this turn's actions; GENERIC when none were recorded."""
    items = list(dict.fromkeys(actions))  # dedupe, keep order
    if not items:
        return GENERIC
    if len(items) > MAX_ITEMS:
        items = items[:MAX_ITEMS] + [f"{len(items) - MAX_ITEMS} more"]
    return ("Before you finish, verify this turn's work. It " + "; ".join(items)
            + ". For each, " + CHECK)


def main():
    data = json.load(sys.stdin)
    state = os.environ.get("STOP_GATE_DIR") or os.path.expanduser("~/.claude/stop-gate")
    os.makedirs(state, exist_ok=True)
    event = data.get("hook_event_name", "")
    active = bool(data.get("stop_hook_active"))
    flag = os.path.join(state, f"{data.get('session_id', 'unknown')}.dirty")
    dirty = os.path.exists(flag)
    waiting = any(t.get("type") == "subagent" for t in data.get("background_tasks") or [])

    tool, tool_input = data.get("tool_name", ""), data.get("tool_input") or {}
    action = decide(event, active, dirty, waiting, is_risky(tool, tool_input))
    actions = []
    if action == "mark":
        with open(flag, "a") as f:
            f.write(describe(tool, tool_input, data.get("cwd")) + "\n")
    elif event == "Stop" and dirty and action != "defer":
        with open(flag) as f:
            actions = [line.rstrip("\n") for line in f if line.strip()]
        # Stop always ends the dirty turn, whether or not it nudges.
        os.remove(flag)

    with open(os.path.join(state, "marker.log"), "a") as f:
        f.write(json.dumps({
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "event": event,
            "tool": data.get("tool_name"), "session": data.get("session_id"),
            "stop_hook_active": active, "dirty": dirty, "action": action,
            "agent_id": data.get("agent_id"), "agent_type": data.get("agent_type"),
            "cwd": data.get("cwd"),
        }) + "\n")

    if action == "nudge":
        # additionalContext continues the turn like decision:block, without an error label.
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "Stop", "additionalContext": build_reason(actions)}}))


if __name__ == "__main__":
    main()
