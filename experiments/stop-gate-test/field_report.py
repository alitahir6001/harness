#!/usr/bin/env python3
"""Field report for the Stop-hook gate: per project, how often it nudged, whether the model
acted on the nudge, and what the continuation cost.

  python3 experiments/stop-gate-test/field_report.py [--log ~/.claude/stop-gate/marker.log]

Sessions come from the gate's marker.log; each one's transcript is found by session id under
~/.claude/projects. Subagent tokens spent inside a continuation live in `subagents/` files
and are not counted.
"""
import argparse
import glob
import json
import os
from collections import defaultdict

PROJECTS = os.path.expanduser("~/.claude/projects")
NUDGE_PREFIX = "Before you finish, verify"


def is_nudge(row):
    a = row.get("attachment") or {}
    return (row.get("type") == "attachment" and a.get("type") == "hook_additional_context"
            and a.get("hookName") == "Stop"
            and any(str(c).startswith(NUDGE_PREFIX) for c in a.get("content") or []))


def is_prompt(row):
    """A human turn: a main-thread user row that isn't only tool results or injected meta."""
    if row.get("type") != "user" or row.get("isSidechain") or row.get("isMeta"):
        return False
    content = (row.get("message") or {}).get("content")
    return isinstance(content, str) or any(c.get("type") != "tool_result" for c in content or [])


def continuations(rows):
    """One entry per nudge: tool calls and tokens from the nudge to the next human prompt.
    Transcripts repeat a request's usage on every content-block row, so dedupe by requestId."""
    found, cur = [], None
    for r in rows:
        if is_nudge(r):
            cur = {"tool_calls": 0, "usage": {}}
            found.append(cur)
        elif cur is not None and is_prompt(r):
            cur = None
        elif cur is not None and r.get("type") == "assistant" and not r.get("isSidechain"):
            m = r.get("message") or {}
            cur["tool_calls"] += sum(1 for c in m.get("content") or [] if c.get("type") == "tool_use")
            if r.get("requestId"):
                cur["usage"][r["requestId"]] = m.get("usage") or {}
    return [{
        "tool_calls": c["tool_calls"],
        "output": sum(u.get("output_tokens", 0) for u in c["usage"].values()),
        "input_side": sum(u.get(k, 0) for u in c["usage"].values() for k in (
            "input_tokens", "cache_read_input_tokens", "cache_creation_input_tokens")),
    } for c in found]


def load_jsonl(path):
    rows = []
    with open(path) as f:
        for line in f:
            try:
                rows.append(json.loads(line))
            except ValueError:
                pass
    return rows


def report(log_path):
    sessions = defaultdict(lambda: {"cwd": None, "marker_nudges": 0})
    for e in load_jsonl(log_path):
        s = sessions[e.get("session")]
        s["cwd"] = s["cwd"] or e.get("cwd")
        s["marker_nudges"] += e.get("action") == "nudge"
    projects = defaultdict(lambda: {"sessions": 0, "marker_nudges": 0, "nudges": [],
                                    "no_transcript": 0})
    for sid, s in sessions.items():
        paths = glob.glob(os.path.join(PROJECTS, "*", f"{sid}.jsonl"))
        rows = load_jsonl(paths[0]) if paths else []
        cwd = s["cwd"] or next((r["cwd"] for r in rows if r.get("cwd")), "?")
        p = projects[cwd]
        p["sessions"] += 1
        p["marker_nudges"] += s["marker_nudges"]
        p["no_transcript"] += not paths
        p["nudges"] += continuations(rows)
    return projects


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--log", default=os.path.expanduser("~/.claude/stop-gate/marker.log"))
    args = ap.parse_args()
    projects = report(args.log)
    print("project | sessions | nudges (log/transcript) | followed by a tool call | "
          "mean extra output tok | mean extra input-side tok | no transcript")
    for cwd, p in sorted(projects.items()):
        n = p["nudges"]
        k = len(n) or 1
        followed = sum(1 for x in n if x["tool_calls"])
        print(f"{cwd} | {p['sessions']} | {p['marker_nudges']}/{len(n)} | "
              f"{followed}/{len(n)} | {sum(x['output'] for x in n) // k} | "
              f"{sum(x['input_side'] for x in n) // k} | {p['no_transcript']}")


if __name__ == "__main__":
    main()
