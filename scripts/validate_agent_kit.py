"""Validate the Aether skill catalog, skill folders, and generated agent entries.

The checks run without third-party dependencies. They cover three things:

* Every canonical skill folder follows the portable skill format: valid
  frontmatter, matching directory name, bundled resources that exist, and
  instructions that stay inside the size budget.
* Every skill carries evaluation sets for behavior and for triggering.
* The generated Codex agents, Claude agents, Claude skill entries, and shared
  reference mirrors match the canonical skills.
"""

from __future__ import annotations

from pathlib import Path
import re
import sys

import validate_evals
from skill_format import check_skill_folder, check_skill_folders
from sync_agent_entries import ENTRIES, MIRRORED_REFERENCES, ROOT, outputs


def check_canonical_skills() -> list[str]:
    """Check the format of every canonical skill folder."""
    expected = {entry[0] for entry in ENTRIES}
    return check_skill_folders(ROOT / ".agents/skills", expected, ROOT)


def check_coverage() -> list[str]:
    """Check that the capability map routes every skill and agent."""
    problems = []
    coverage_file = ROOT / ".agents/skills/aether-workflow/references/coverage.md"
    evidence_file = ROOT / ".agents/skills/aether-workflow/references/evidence.md"
    for required in (coverage_file, evidence_file):
        if not required.is_file():
            problems.append(f"Missing {required.relative_to(ROOT)}")
    coverage = coverage_file.read_text(encoding="utf-8") if coverage_file.is_file() else ""
    for skill, agent, _, _ in ENTRIES:
        if f"`{skill}`" not in coverage or f"`{agent}`" not in coverage:
            problems.append(f"Missing catalog route: {skill} / {agent}")
    return problems


def check_client_entries() -> list[str]:
    """Check the generated Claude skill entries for format problems."""
    problems = []
    for skill, _, _, _ in ENTRIES:
        entry = ROOT / ".claude/skills" / skill / "SKILL.md"
        if not entry.is_file():
            continue
        problems.extend(check_skill_folder(entry.parent, skill))
        body = entry.read_text(encoding="utf-8")
        if f".agents/skills/{skill}/SKILL.md" not in body:
            problems.append(f".claude/skills/{skill}/SKILL.md: must point at the canonical skill")
    return problems


def check_generated_entries() -> list[str]:
    """Check that generated entries match the canonical skills."""
    problems = []
    for path, expected in outputs().items():
        if not path.is_file():
            problems.append(f"Missing generated entry: {path.relative_to(ROOT)}")
        elif path.read_text(encoding="utf-8") != expected:
            problems.append(f"Out-of-sync generated entry: {path.relative_to(ROOT)}")
    for destination, source in MIRRORED_REFERENCES.items():
        source_path = ROOT / source
        if source_path.is_file() and not (ROOT / destination).is_file():
            problems.append(f"Missing mirrored reference: {destination}")
    return problems


def check_descriptions() -> list[str]:
    """Check that every skill description states what it does and when to use it."""
    problems = []
    pattern = re.compile(r"\buse (this skill )?when\b", re.IGNORECASE)
    for skill, _, _, _ in ENTRIES:
        path = ROOT / ".agents/skills" / skill / "SKILL.md"
        if not path.is_file():
            continue
        body = path.read_text(encoding="utf-8")
        match = re.search(r"^description:\s*(.+)$", body, re.MULTILINE)
        description = match.group(1).strip().strip('"') if match else ""
        if description and not pattern.search(description):
            problems.append(f"{skill}: description should state when to use the skill")
    return problems


def check() -> list[str]:
    problems = []
    problems.extend(check_canonical_skills())
    problems.extend(check_coverage())
    problems.extend(check_client_entries())
    problems.extend(check_generated_entries())
    problems.extend(check_descriptions())
    eval_problems, _ = validate_evals.check(ROOT)
    problems.extend(eval_problems)
    return problems


if __name__ == "__main__":
    found = check()
    if found:
        print("\n".join(found), file=sys.stderr)
        raise SystemExit(1)
    print(
        f"Validated {len(ENTRIES)} canonical skills, {len(outputs())} generated agent/skill entries, "
        f"and {len(MIRRORED_REFERENCES)} mirrored reference."
    )
