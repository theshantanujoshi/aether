"""Checks for the per-skill evaluation sets."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest


sys.path.insert(0, str(Path(__file__).resolve().parent))

import validate_evals  # noqa: E402


def behavior_cases(skill: str) -> dict:
    return {
        "skill_name": skill,
        "evals": [
            {
                "id": 1,
                "prompt": "Do the first thing.",
                "expected_output": "A result grounded in the sources.",
                "assertions": ["The output names the source"],
            },
            {
                "id": 2,
                "prompt": "Do the second thing with a missing file.",
                "expected_output": "A report of the gap.",
                "assertions": ["The gap is reported"],
            },
        ],
    }


def trigger_queries(positives: int = 6, negatives: int = 4) -> list:
    cases = [{"query": f"trigger {index}", "should_trigger": True} for index in range(positives)]
    cases += [{"query": f"near miss {index}", "should_trigger": False} for index in range(negatives)]
    return cases


class EvalValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write_skill(self, name: str, behavior: object = None, triggers: object = None) -> None:
        folder = self.root / ".agents" / "skills" / name
        (folder / "evals").mkdir(parents=True, exist_ok=True)
        (folder / "SKILL.md").write_text(f"---\nname: {name}\ndescription: Use this skill when testing.\n---\n\nBody\n", encoding="utf-8")
        if behavior is not None:
            (folder / "evals" / "evals.json").write_text(json.dumps(behavior), encoding="utf-8")
        if triggers is not None:
            (folder / "evals" / "trigger-queries.json").write_text(json.dumps(triggers), encoding="utf-8")

    def test_complete_sets_pass(self) -> None:
        self.write_skill("sample-skill", behavior_cases("sample-skill"), trigger_queries())
        problems, summary = validate_evals.check(self.root)
        self.assertEqual(problems, [])
        self.assertEqual(summary[0]["behavior_cases"], 2)
        self.assertEqual(summary[0]["should_trigger"], 6)
        self.assertEqual(summary[0]["should_not_trigger"], 4)

    def test_missing_files_are_reported(self) -> None:
        self.write_skill("sample-skill")
        problems, _ = validate_evals.check(self.root)
        self.assertTrue(any("missing evals/evals.json" in problem for problem in problems))
        self.assertTrue(any("missing evals/trigger-queries.json" in problem for problem in problems))

    def test_too_few_trigger_queries_are_reported(self) -> None:
        self.write_skill("sample-skill", behavior_cases("sample-skill"), trigger_queries(positives=2, negatives=1))
        problems, _ = validate_evals.check(self.root)
        self.assertTrue(any("at least 10 trigger queries" in problem for problem in problems))
        self.assertTrue(any("at least 6 queries that should trigger" in problem for problem in problems))
        self.assertTrue(any("at least 4 near-miss queries" in problem for problem in problems))

    def test_invalid_json_is_reported(self) -> None:
        self.write_skill("sample-skill", behavior_cases("sample-skill"), trigger_queries())
        path = self.root / ".agents/skills/sample-skill/evals/evals.json"
        path.write_text("{not json", encoding="utf-8")
        problems, _ = validate_evals.check(self.root)
        self.assertTrue(any("invalid JSON" in problem for problem in problems))

    def test_skill_name_mismatch_is_reported(self) -> None:
        self.write_skill("sample-skill", behavior_cases("other-skill"), trigger_queries())
        problems, _ = validate_evals.check(self.root)
        self.assertTrue(any("skill_name must match" in problem for problem in problems))

    def test_duplicate_case_ids_are_reported(self) -> None:
        cases = behavior_cases("sample-skill")
        cases["evals"][1]["id"] = 1
        self.write_skill("sample-skill", cases, trigger_queries())
        problems, _ = validate_evals.check(self.root)
        self.assertTrue(any("duplicate case id" in problem for problem in problems))

    def test_missing_prompt_is_reported(self) -> None:
        cases = behavior_cases("sample-skill")
        del cases["evals"][0]["prompt"]
        self.write_skill("sample-skill", cases, trigger_queries())
        problems, _ = validate_evals.check(self.root)
        self.assertTrue(any("needs a non-empty 'prompt'" in problem for problem in problems))

    def test_query_without_label_is_reported(self) -> None:
        queries = trigger_queries()
        del queries[0]["should_trigger"]
        self.write_skill("sample-skill", behavior_cases("sample-skill"), queries)
        problems, _ = validate_evals.check(self.root)
        self.assertTrue(any("boolean 'should_trigger'" in problem for problem in problems))


if __name__ == "__main__":
    unittest.main()
