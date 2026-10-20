"""Validate the Aether skill catalog and generated agent entries without dependencies."""

from __future__ import annotations

from pathlib import Path
import re
import sys

from sync_agent_entries import ENTRIES, ROOT, outputs


def check() -> list[str]:
    errors = []
    coverage_file = ROOT / ".agents/skills/aether-workflow/references/coverage.md"
    evidence_file = ROOT / ".agents/skills/aether-workflow/references/evidence.md"
    for required in (coverage_file, evidence_file):
        if not required.is_file():
            errors.append(f"Missing {required.relative_to(ROOT)}")
    coverage = coverage_file.read_text(encoding="utf-8") if coverage_file.is_file() else ""
    expected_skills = {entry[0] for entry in ENTRIES}
    actual_skills = {p.parent.name for p in (ROOT / ".agents/skills").glob("*/SKILL.md")}
    for missing in sorted(expected_skills - actual_skills):
        errors.append(f"Missing canonical skill: {missing}")
    for unexpected in sorted(actual_skills - expected_skills):
        errors.append(f"Uncataloged canonical skill: {unexpected}")
    for skill, agent, _, _ in ENTRIES:
        path = ROOT / ".agents/skills" / skill / "SKILL.md"
        if path.is_file():
            body = path.read_text(encoding="utf-8")
            match = re.match(r"\A---\nname: ([a-z0-9-]+)\ndescription: .+\n---\n", body)
            if not match or match.group(1) != skill:
                errors.append(f"Invalid frontmatter: {path.relative_to(ROOT)}")
        if f"`{skill}`" not in coverage or f"`{agent}`" not in coverage:
            errors.append(f"Missing catalog route: {skill} / {agent}")
    for path, expected in outputs().items():
        if not path.is_file():
            errors.append(f"Missing generated entry: {path.relative_to(ROOT)}")
        elif path.read_text(encoding="utf-8") != expected:
            errors.append(f"Out-of-sync generated entry: {path.relative_to(ROOT)}")
    return errors


if __name__ == "__main__":
    problems = check()
    if problems:
        print("\n".join(problems), file=sys.stderr)
        raise SystemExit(1)
    print(f"Validated {len(ENTRIES)} canonical skills and {len(outputs())} generated agent/skill entries.")
