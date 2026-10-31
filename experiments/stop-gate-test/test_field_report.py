#!/usr/bin/env python3
"""Tests for field_report.py. Run: python3 experiments/stop-gate-test/test_field_report.py -v"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from field_report import continuations  # noqa: E402


def prompt(text):
    return {"type": "user", "message": {"content": text}}


def assistant(req, blocks, out, cache_read=100):
    return {"type": "assistant", "requestId": req, "message": {
        "content": [{"type": b} for b in blocks],
        "usage": {"input_tokens": 1, "cache_read_input_tokens": cache_read, "output_tokens": out}}}


NUDGE = {"type": "attachment", "attachment": {
    "type": "hook_additional_context", "hookName": "Stop",
    "content": ["Before you finish, verify this turn's work. It ran `x`."]}}
TOOL_RESULT = {"type": "user", "message": {"content": [{"type": "tool_result"}]}}


class TestContinuations(unittest.TestCase):
    def test_counts_tools_and_dedupes_usage_by_request(self):
        rows = [prompt("go"), assistant("r0", ["tool_use"], 50), NUDGE,
                assistant("r1", ["thinking"], 30), assistant("r1", ["tool_use"], 30),
                TOOL_RESULT, assistant("r2", ["text"], 20),
                prompt("next"), assistant("r3", ["tool_use"], 99)]
        self.assertEqual(continuations(rows),
                         [{"tool_calls": 1, "output": 50, "input_side": 202}])

    def test_text_only_continuation_and_subagent_rows_ignored(self):
        side = dict(assistant("s1", ["tool_use"], 500), isSidechain=True)
        rows = [NUDGE, side, assistant("r1", ["text"], 10)]
        self.assertEqual(continuations(rows), [{"tool_calls": 0, "output": 10, "input_side": 101}])

    def test_other_hooks_context_is_not_a_nudge(self):
        other = {"type": "attachment", "attachment": {
            "type": "hook_additional_context", "hookName": "Stop", "content": ["lint ok"]}}
        self.assertEqual(continuations([other, assistant("r1", ["tool_use"], 5)]), [])


if __name__ == "__main__":
    unittest.main()
