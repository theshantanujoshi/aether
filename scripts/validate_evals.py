"""Validate the per-skill evaluation sets that ship with the kit.

Each skill folder carries two evaluation files:

* `evals/evals.json` — behavior cases with a prompt, the expected output, and
  checkable assertions.
* `evals/trigger-queries.json` — prompts labeled with whether the skill
  should be loaded, including near-misses that look similar but need a
  different skill.

This script checks their structure and prints coverage. It never runs an
agent, so it verifies that the cases exist and are well formed rather than
how the skill performs.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


MIN_TRIGGER_CASES = 10
MIN_SHOULD_TRIGGER = 6
MIN_SHOULD_NOT_TRIGGER = 4
MIN_BEHAVIOR_CASES = 2
EVALS_FILE = "evals/evals.json"
TRIGGER_FILE = "evals/trigger-queries.json"


def _read_json(path: Path, problems: list[str]) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except OSError as error:
        problems.append(f"{path.as_posix()}: unreadable ({error})")
    except json.JSONDecodeError as error:
        problems.append(f"{path.as_posix()}: invalid JSON ({error})")
    return None


def check_behavior_cases(skill: str, path: Path, problems: list[str]) -> int:
    """Validate one `evals/evals.json` file and return the case count."""
    payload = _read_json(path, problems)
    if payload is None:
        return 0
    if not isinstance(payload, dict):
        problems.append(f"{path.as_posix()}: expected a JSON object")
        return 0
    if payload.get("skill_name") != skill:
        problems.append(f"{path.as_posix()}: skill_name must match the skill folder name '{skill}'")
    cases = payload.get("evals")
    if not isinstance(cases, list):
        problems.append(f"{path.as_posix()}: 'evals' must be a list")
        return 0
    if len(cases) < MIN_BEHAVIOR_CASES:
        problems.append(f"{path.as_posix()}: needs at least {MIN_BEHAVIOR_CASES} behavior cases")
    seen: set[int] = set()
    for index, case in enumerate(cases, start=1):
        if not isinstance(case, dict):
            problems.append(f"{path.as_posix()}: case {index} must be an object")
            continue
        identifier = case.get("id")
        if not isinstance(identifier, int):
            problems.append(f"{path.as_posix()}: case {index} needs an integer id")
        elif identifier in seen:
            problems.append(f"{path.as_posix()}: duplicate case id {identifier}")
        else:
            seen.add(identifier)
        for key in ("prompt", "expected_output"):
            if not isinstance(case.get(key), str) or not case[key].strip():
                problems.append(f"{path.as_posix()}: case {index} needs a non-empty '{key}'")
        assertions = case.get("assertions", [])
        if not isinstance(assertions, list):
            problems.append(f"{path.as_posix()}: case {index} 'assertions' must be a list")
        elif any(not isinstance(item, str) or not item.strip() for item in assertions):
            problems.append(f"{path.as_posix()}: case {index} has an empty assertion")
        files = case.get("files", [])
        if not isinstance(files, list) or any(not isinstance(item, str) for item in files):
            problems.append(f"{path.as_posix()}: case {index} 'files' must be a list of paths")
    return len(cases)


def check_trigger_queries(skill: str, path: Path, problems: list[str]) -> tuple[int, int]:
    """Validate one `evals/trigger-queries.json` file and return the label counts."""
    payload = _read_json(path, problems)
    if payload is None:
        return 0, 0
    if not isinstance(payload, list):
        problems.append(f"{path.as_posix()}: expected a JSON list of queries")
        return 0, 0
    should_trigger = 0
    should_not_trigger = 0
    for index, case in enumerate(payload, start=1):
        if not isinstance(case, dict):
            problems.append(f"{path.as_posix()}: query {index} must be an object")
            continue
        if not isinstance(case.get("query"), str) or not case["query"].strip():
            problems.append(f"{path.as_posix()}: query {index} needs a non-empty 'query'")
        label = case.get("should_trigger")
        if not isinstance(label, bool):
            problems.append(f"{path.as_posix()}: query {index} needs a boolean 'should_trigger'")
        elif label:
            should_trigger += 1
        else:
            should_not_trigger += 1
    if len(payload) < MIN_TRIGGER_CASES:
        problems.append(f"{path.as_posix()}: needs at least {MIN_TRIGGER_CASES} trigger queries")
    if should_trigger < MIN_SHOULD_TRIGGER:
        problems.append(f"{path.as_posix()}: needs at least {MIN_SHOULD_TRIGGER} queries that should trigger")
    if should_not_trigger < MIN_SHOULD_NOT_TRIGGER:
        problems.append(f"{path.as_posix()}: needs at least {MIN_SHOULD_NOT_TRIGGER} near-miss queries that should not trigger")
    return should_trigger, should_not_trigger


def check(root: Path) -> tuple[list[str], list[dict]]:
    """Return the problems found in the evaluation sets and a per-skill summary."""
    problems: list[str] = []
    summary: list[dict] = []
    skills_root = root / ".agents/skills"
    if not skills_root.is_dir():
        return [f"{skills_root.as_posix()}: missing skills directory"], summary
    for skill_md in sorted(skills_root.glob("*/SKILL.md")):
        skill = skill_md.parent.name
        folder = skill_md.parent
        behavior_path = folder / EVALS_FILE
        trigger_path = folder / TRIGGER_FILE
        if not behavior_path.is_file():
            problems.append(f"{skill}: missing {EVALS_FILE}")
            behavior_count = 0
        else:
            behavior_count = check_behavior_cases(skill, behavior_path, problems)
        if not trigger_path.is_file():
            problems.append(f"{skill}: missing {TRIGGER_FILE}")
            positives = negatives = 0
        else:
            positives, negatives = check_trigger_queries(skill, trigger_path, problems)
        summary.append({
            "skill": skill,
            "behavior_cases": behavior_count,
            "should_trigger": positives,
            "should_not_trigger": negatives,
        })
    return problems, summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1], help="Repository root")
    args = parser.parse_args()
    problems, summary = check(args.root)
    width = max((len(row["skill"]) for row in summary), default=10)
    print(f"{'skill'.ljust(width)}  cases  trigger  near-miss")
    for row in summary:
        print(f"{row['skill'].ljust(width)}  {row['behavior_cases']:>5}  {row['should_trigger']:>7}  {row['should_not_trigger']:>9}")
    if problems:
        print("\n".join(problems), file=sys.stderr)
        raise SystemExit(1)
    print(f"\nChecked {len(summary)} skill evaluation sets.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
