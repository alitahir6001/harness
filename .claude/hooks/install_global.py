#!/usr/bin/env python3
"""Register stop_gate.py in ~/.claude/settings.json (user scope) and drop this repo's
project-local copy so nothing nudges twice. --uninstall removes the user-scope entries.

  python3 .claude/hooks/install_global.py [--uninstall]

Prints only the `hooks` key: the settings file's `env` holds an OAuth token.
"""
import argparse
import json
import os
import shlex
import shutil
import stat
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
GATE = os.path.join(HERE, "stop_gate.py")
# The [ -f ] guard matters: python3 exits 2 on a missing script, and exit 2 on Stop blocks.
COMMAND = f"[ -f {shlex.quote(GATE)} ] && python3 {shlex.quote(GATE)}"
MATCHER = "Edit|Write|MultiEdit|NotebookEdit|Bash"
USER = os.path.expanduser("~/.claude/settings.json")
LOCAL = os.path.join(os.path.dirname(HERE), "settings.local.json")


def strip_gate(settings):
    """Remove every stop_gate handler; drop groups, events and `hooks` left empty."""
    hooks = settings.get("hooks", {})
    for event in list(hooks):
        groups = []
        for g in hooks[event]:
            kept = [h for h in g.get("hooks", []) if "stop_gate.py" not in h.get("command", "")]
            if kept:
                groups.append(dict(g, hooks=kept))
        if groups:
            hooks[event] = groups
        else:
            del hooks[event]
    if not hooks:
        settings.pop("hooks", None)
    return settings


def add_gate(settings):
    """Register the gate once on PostToolUse and Stop, leaving other hooks alone."""
    strip_gate(settings)
    hooks = settings.setdefault("hooks", {})
    hooks.setdefault("PostToolUse", []).append(
        {"matcher": MATCHER, "hooks": [{"type": "command", "command": COMMAND}]})
    hooks.setdefault("Stop", []).append({"hooks": [{"type": "command", "command": COMMAND}]})
    return settings


def rewrite(path, change, backup=None):
    with open(path) as f:
        settings = json.load(f)
    if backup:
        shutil.copy2(path, backup)
        os.chmod(backup, 0o600)
    settings = change(settings)
    mode = stat.S_IMODE(os.stat(path).st_mode)
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path))
    with os.fdopen(fd, "w") as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)
        f.write("\n")
    os.chmod(tmp, mode)
    os.replace(tmp, path)
    return settings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--uninstall", action="store_true")
    args = ap.parse_args()
    backup = f"{USER}.bak-stopgate-{time.strftime('%Y%m%d-%H%M%S')}"
    settings = rewrite(USER, strip_gate if args.uninstall else add_gate, backup)
    if not args.uninstall and os.path.exists(LOCAL):
        rewrite(LOCAL, strip_gate)
    print(json.dumps({"backup": backup, "user_hooks": settings.get("hooks")}, indent=2))


if __name__ == "__main__":
    main()
