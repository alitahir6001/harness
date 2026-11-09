#!/usr/bin/env python3
"""Tests for stop_gate.py. Run: python3 .claude/hooks/test_stop_gate.py -v
(`python3 -m unittest <path>` fails here: the leading-dot dir isn't an importable name.)"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from stop_gate import GENERIC, MAX_ITEMS, build_reason, decide, describe, is_risky  # noqa: E402
from install_global import COMMAND, add_gate, strip_gate  # noqa: E402

SCRIPT = os.path.join(HERE, "stop_gate.py")


class TestDecide(unittest.TestCase):
    def test_truth_table(self):
        cases = [
            ("PostToolUse", False, False, "mark"),
            ("PostToolUse", False, True, "mark"),
            ("Stop", False, True, "nudge"),
            ("Stop", True, True, "allow"),   # already continuing: never nudge twice
            ("Stop", False, False, "allow"),  # turn touched nothing
            ("Stop", True, False, "allow"),
            ("SessionStart", False, True, "allow"),
        ]
        for event, active, dirty, want in cases:
            with self.subTest(event=event, active=active, dirty=dirty):
                self.assertEqual(decide(event, active, dirty), want)

    def test_routine_tool_call_is_skipped(self):
        self.assertEqual(decide("PostToolUse", False, True, risky=False), "skip")

    def test_waiting_on_subagent_defers_only_a_would_be_nudge(self):
        self.assertEqual(decide("Stop", False, True, waiting=True), "defer")
        self.assertEqual(decide("Stop", True, True, waiting=True), "allow")
        self.assertEqual(decide("Stop", False, False, waiting=True), "allow")


H = os.path.expanduser("~")


class TestIsRisky(unittest.TestCase):
    RISKY = [
        ("Bash", "grep -rl 'sk-ant-' ~/.hermes"),  # the 2026-11 hermes-token catch
        ("Bash", "sed -n '475,479p' ~/.hermes/.env"),
        ("Bash", "python3 -I find_old_token.py scan"),
        ("Bash", "echo $ANTHROPIC_TOKEN | wc -c"),
        ("Bash", "grep -i secret config.yml"),
        ("Bash", "export API_KEY=x"),
        ("Bash", "cat ~/.claude/settings.json"),
        ("Bash", "rm -rf build"),
        ("Bash", "cd x && sudo rm f"),
        ("Bash", "mv ~/.claude/old ~/.Trash/"),
        ("Bash", "trash notes.txt"),
        ("Bash", "git push origin main"),
        ("Bash", "git -C ../repo push"),
        ("Bash", "echo x >> ~/.zshrc"),
        ("Bash", f"ln -s {H}/p/skill {H}/.claude/skills/skill"),
        ("Bash", "cp a.md $HOME/.config/x.md"),
        ("Edit", f"{H}/.claude/CLAUDE.md"),
        ("Write", f"{H}/.zshrc"),
        ("Write", "/p/app/.env.local"),
        ("Edit", "/p/.claude/settings.local.json"),
        ("Write", "/p/credentials.json"),
    ]
    ROUTINE = [
        ("Bash", "ls -la"),
        ("Bash", "git status && git diff"),
        ("Bash", "python3 field_report.py | grep tokens"),
        ("Bash", "cat .claude/skills/harness-token-efficiency-campaign/SKILL.md"),
        ("Bash", "cat ~/.claude/keybindings.json 2>/dev/null"),
        ("Bash", "tail ~/.claude/stop-gate/marker.log 2>&1"),
        ("Bash", "git commit -m 'remove dead code'"),
        ("Bash", "npm run format"),
        ("Edit", "/p/src/a.py"),
        ("Write", "/p/CHANGELOG.md"),
        ("Write", f"{H}/.claude/plans/zesty-plan.md"),
        ("Write", f"{H}/Desktop/projects/harness/.ai/handoff.md"),
        ("NotebookEdit", "/p/n.ipynb"),
    ]

    @staticmethod
    def inp(tool, arg):
        return {"command": arg} if tool == "Bash" else {"file_path": arg}

    def test_risky(self):
        for tool, arg in self.RISKY:
            with self.subTest(tool=tool, arg=arg):
                self.assertTrue(is_risky(tool, self.inp(tool, arg)))

    def test_routine(self):
        for tool, arg in self.ROUTINE:
            with self.subTest(tool=tool, arg=arg):
                self.assertFalse(is_risky(tool, self.inp(tool, arg)))


class TestReason(unittest.TestCase):
    def test_describe(self):
        self.assertEqual(describe("Bash", {"command": "./deploy.sh\n  --fast"}),
                         "ran `./deploy.sh --fast`")
        self.assertEqual(describe("Write", {"file_path": "/x/y/CHANGELOG.md"}), "wrote `CHANGELOG.md`")
        self.assertEqual(describe("Edit", {"file_path": "/x/a.py"}), "edited `a.py`")
        self.assertEqual(describe("NotebookEdit", {"notebook_path": "/n.ipynb"}), "edited `n.ipynb`")
        self.assertLessEqual(len(describe("Bash", {"command": "x" * 500})), 110)

    def test_describe_drops_cwd_so_long_paths_keep_the_script_name(self):
        cwd = "/private/var/folders/97/T/stopgate-hook-subagent-3-z9qgpl58/project"
        self.assertEqual(describe("Bash", {"command": f"{cwd}/deploy.sh"}, cwd), "ran `deploy.sh`")
        self.assertEqual(describe("Bash", {"command": f"bash {cwd}/deploy.sh"}, cwd), "ran `bash deploy.sh`")
        self.assertEqual(describe("Bash", {"command": f"ls -la {cwd}"}, cwd), "ran `ls -la .`")
        self.assertEqual(describe("Bash", {"command": f"ls {cwd}2/x"}, cwd), f"ran `ls {cwd}2/x`")
        self.assertEqual(describe("Bash", {"command": f"ls /x{cwd}/a"}, cwd), f"ran `ls /x{cwd}/a`")

    def test_describe_matches_the_realpath_form_of_cwd(self):
        with tempfile.TemporaryDirectory() as cwd:  # /var/... is /private/var/... on macOS
            real = os.path.realpath(cwd)
            self.assertEqual(describe("Bash", {"command": f"{real}/deploy.sh"}, cwd), "ran `deploy.sh`")
            self.assertEqual(describe("Bash", {"command": f"{cwd}/deploy.sh"}, cwd), "ran `deploy.sh`")

    def test_no_actions_is_generic(self):
        self.assertEqual(build_reason([]), GENERIC)

    def test_names_actions_in_order_deduped(self):
        r = build_reason(["ran `./deploy.sh`", "wrote `CHANGELOG.md`", "ran `./deploy.sh`"])
        self.assertIn("It ran `./deploy.sh`; wrote `CHANGELOG.md`. For each,", r)
        self.assertIn("success message doesn't count", r)

    def test_caps_long_lists(self):
        r = build_reason([f"ran `c{i}`" for i in range(MAX_ITEMS + 3)])
        self.assertIn("3 more", r)
        self.assertNotIn(f"c{MAX_ITEMS}`", r)


class TestInstall(unittest.TestCase):
    OTHER = {"type": "command", "command": "echo other"}

    def test_add_is_idempotent_and_keeps_other_keys_and_hooks(self):
        s = {"env": {"X": "1"}, "hooks": {"Stop": [{"hooks": [self.OTHER]}]}}
        add_gate(add_gate(s))
        self.assertEqual(s["env"], {"X": "1"})
        cmds = [h["command"] for g in s["hooks"]["Stop"] for h in g["hooks"]]
        self.assertEqual(cmds, ["echo other", COMMAND])
        self.assertEqual(len(s["hooks"]["PostToolUse"]), 1)

    def test_strip_removes_gate_and_empty_containers(self):
        s = add_gate({"permissions": {}})
        s["hooks"]["Stop"][0]["hooks"].append(self.OTHER)
        strip_gate(s)
        self.assertEqual(s["hooks"], {"Stop": [{"hooks": [self.OTHER]}]})
        self.assertEqual(strip_gate(add_gate({})), {})

    def test_strip_matches_old_unguarded_command(self):
        local = {"hooks": {"Stop": [{"hooks": [{"type": "command",
                                                "command": "python3 /r/.claude/hooks/stop_gate.py"}]}]}}
        self.assertEqual(strip_gate(local), {})

    def test_missing_script_is_non_blocking(self):
        # Exit 2 would block every Stop; the guard must turn a missing file into exit 1.
        cmd = COMMAND.replace("stop_gate.py", "gone_gate.py")
        self.assertEqual(subprocess.run(["sh", "-c", cmd], input="{}", text=True).returncode, 1)


class TestScript(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.env = dict(os.environ, STOP_GATE_DIR=self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def run_hook(self, payload):
        p = subprocess.run([sys.executable, SCRIPT], input=json.dumps(payload),
                           capture_output=True, text=True, env=self.env, check=True)
        return p.stdout.strip()

    def tool(self, name, tool_input, session="s1"):
        return self.run_hook({"hook_event_name": "PostToolUse", "session_id": session,
                              "tool_name": name, "tool_input": tool_input})

    def stop(self, active=False, background=()):
        return self.run_hook({"hook_event_name": "Stop", "session_id": "s1",
                              "stop_hook_active": active,
                              "background_tasks": [{"type": t} for t in background]})

    def test_stop_waiting_on_subagent_defers_then_nudges(self):
        self.tool("Bash", {"command": "git push"})
        self.assertEqual(self.stop(background=["subagent"]), "")
        self.tool("Write", {"file_path": "/p/.env"})
        reason = json.loads(self.stop())["hookSpecificOutput"]["additionalContext"]
        self.assertIn("ran `git push`; wrote `.env`", reason)

    def test_background_shell_does_not_defer(self):
        self.tool("Bash", {"command": "rm -f dev.log"})
        self.assertIn("hookSpecificOutput", self.stop(background=["shell"]))

    def test_clean_turn_stops(self):
        self.assertEqual(self.stop(), "")

    def test_dirty_turn_nudges_once_naming_actions(self):
        self.assertEqual(self.tool("Bash", {"command": "git push"}), "")
        self.tool("Write", {"file_path": "/p/.env"})
        out = json.loads(self.stop())["hookSpecificOutput"]
        self.assertEqual(out["hookEventName"], "Stop")
        self.assertIn("ran `git push`; wrote `.env`", out["additionalContext"])
        # The continuation stops with stop_hook_active set and the record already cleared.
        self.assertEqual(self.stop(active=True), "")
        self.assertEqual(self.stop(), "")

    def test_continuation_that_mutates_is_not_nudged_again(self):
        self.tool("Edit", {"file_path": "/p/.env"})
        self.stop()
        self.tool("Bash", {"command": "rm .env.bak"})
        self.assertEqual(self.stop(active=True), "")

    def test_sessions_are_independent(self):
        self.tool("Write", {"file_path": "/p/.env"}, session="other")
        self.assertEqual(self.stop(), "")

    def test_marker_log_records_every_call(self):
        self.tool("Bash", {"command": "ls"})
        self.tool("Bash", {"command": "git push"})
        self.stop()
        with open(os.path.join(self.tmp.name, "marker.log")) as f:
            actions = [json.loads(line)["action"] for line in f]
        self.assertEqual(actions, ["skip", "mark", "nudge"])

    def test_routine_turn_is_silent_and_risky_turn_names_only_risky_actions(self):
        self.tool("Edit", {"file_path": "/p/a.py"})
        self.tool("Bash", {"command": "pytest"})
        self.assertEqual(self.stop(), "")
        self.tool("Edit", {"file_path": "/p/a.py"})
        self.tool("Write", {"file_path": "/p/.env"})
        reason = json.loads(self.stop())["hookSpecificOutput"]["additionalContext"]
        self.assertIn("It wrote `.env`. For each,", reason)

    def test_routine_call_after_risky_one_keeps_the_record(self):
        self.tool("Bash", {"command": "git push"})
        self.tool("Bash", {"command": "ls"})
        self.assertIn("ran `git push`", self.stop())

    def test_subagent_call_logs_agent_and_marks_session(self):
        self.run_hook({"hook_event_name": "PostToolUse", "session_id": "s1", "tool_name": "Bash",
                       "tool_input": {"command": "git push"}, "agent_id": "a1",
                       "agent_type": "general-purpose", "cwd": "/p"})
        with open(os.path.join(self.tmp.name, "marker.log")) as f:
            line = json.loads(f.readline())
        self.assertEqual((line["agent_id"], line["agent_type"], line["cwd"]),
                         ("a1", "general-purpose", "/p"))
        self.assertIn("ran `git push`", json.loads(self.stop())["hookSpecificOutput"]["additionalContext"])


if __name__ == "__main__":
    unittest.main()
