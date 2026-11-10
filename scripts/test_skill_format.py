"""Checks for the portable skill folder format."""

from __future__ import annotations

from pathlib import Path
import sys
import tempfile
import unittest


sys.path.insert(0, str(Path(__file__).resolve().parent))

from skill_format import check_skill_folder, parse_frontmatter  # noqa: E402


VALID_SKILL = """---
name: sample-skill
description: Use this skill when you need to check the sample behaviour end to end.
license: MIT
metadata:
  aether-kit-version: "0.2.0"
  aether-skill-version: "1.0"
---

# Sample

1. Do the thing.
2. Report the result.

Reference the bundled guide at `references/guide.md`.
"""


class FrontmatterTests(unittest.TestCase):
    def test_parses_scalars_and_nested_maps(self) -> None:
        fields, body, errors = parse_frontmatter(VALID_SKILL)
        self.assertEqual(errors, [])
        self.assertEqual(fields["name"], "sample-skill")
        self.assertTrue(fields["description"].startswith("Use this skill"))
        self.assertEqual(fields["license"], "MIT")
        self.assertEqual(fields["metadata"]["aether-kit-version"], "0.2.0")
        self.assertIn("# Sample", body)

    def test_reports_missing_and_unterminated_frontmatter(self) -> None:
        _, _, errors = parse_frontmatter("no frontmatter here")
        self.assertEqual(errors, ["missing YAML frontmatter"])
        _, _, errors = parse_frontmatter("---\nname: x\n")
        self.assertEqual(errors, ["unterminated YAML frontmatter"])

    def test_rejects_unquoted_value_with_a_colon(self) -> None:
        _, _, errors = parse_frontmatter("---\nname: x\ndescription: Use this skill when: the user asks\n---\n")
        self.assertTrue(any("must be quoted because it contains a colon" in error for error in errors))

    def test_accepts_quoted_value_with_a_colon(self) -> None:
        _, _, errors = parse_frontmatter('---\nname: x\ndescription: "Use this skill when: the user asks"\n---\n')
        self.assertEqual(errors, [])


class SkillFolderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write_skill(self, name: str, body: str = VALID_SKILL) -> Path:
        folder = self.root / name
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "SKILL.md").write_text(body, encoding="utf-8")
        return folder

    def test_valid_skill_passes(self) -> None:
        folder = self.write_skill("sample-skill")
        (folder / "references").mkdir()
        (folder / "references" / "guide.md").write_text("Guide\n", encoding="utf-8")
        self.assertEqual(check_skill_folder(folder), [])

    def test_missing_skill_file(self) -> None:
        folder = self.root / "empty-skill"
        folder.mkdir()
        self.assertEqual(check_skill_folder(folder), ["empty-skill: missing SKILL.md"])

    def test_name_must_match_directory(self) -> None:
        folder = self.write_skill("other-name")
        problems = check_skill_folder(folder)
        self.assertTrue(any("must match the skill directory name" in problem for problem in problems))

    def test_rejects_invalid_names(self) -> None:
        for name in ("Sample-Skill", "-sample", "sample-", "sam--ple", "a" * 65):
            body = VALID_SKILL.replace("name: sample-skill", f"name: {name}")
            folder = self.write_skill("sample-skill", body)
            problems = check_skill_folder(folder)
            self.assertTrue(problems, f"expected a problem for name {name}")

    def test_rejects_missing_and_oversized_descriptions(self) -> None:
        body = VALID_SKILL.replace(
            "description: Use this skill when you need to check the sample behaviour end to end.",
            "description: " + "x" * 1100,
        )
        folder = self.write_skill("sample-skill", body)
        problems = check_skill_folder(folder)
        self.assertTrue(any("description is longer" in problem for problem in problems))

        body = VALID_SKILL.replace(
            "description: Use this skill when you need to check the sample behaviour end to end.",
            "description: \"\"",
        )
        folder = self.write_skill("sample-skill", body)
        problems = check_skill_folder(folder)
        self.assertTrue(any("missing description" in problem for problem in problems))

    def test_rejects_unknown_frontmatter_fields(self) -> None:
        body = VALID_SKILL.replace("license: MIT", "licence: MIT")
        folder = self.write_skill("sample-skill", body)
        problems = check_skill_folder(folder)
        self.assertTrue(any("unsupported frontmatter field" in problem for problem in problems))

    def test_rejects_empty_metadata_values(self) -> None:
        body = VALID_SKILL.replace('aether-skill-version: "1.0"', 'aether-skill-version: ""')
        folder = self.write_skill("sample-skill", body)
        problems = check_skill_folder(folder)
        self.assertTrue(any("metadata value" in problem for problem in problems))

    def test_reports_missing_bundled_resource(self) -> None:
        folder = self.write_skill("sample-skill")
        problems = check_skill_folder(folder)
        self.assertTrue(any("referenced resource 'references/guide.md' is missing" in problem for problem in problems))

    def test_rejects_deep_reference_chains(self) -> None:
        body = VALID_SKILL.replace("references/guide.md", "references/nested/guide.md")
        folder = self.write_skill("sample-skill", body)
        problems = check_skill_folder(folder)
        self.assertTrue(any("one level deep" in problem for problem in problems))

    def test_rejects_oversized_body(self) -> None:
        body = VALID_SKILL + "\n".join(f"line {index}" for index in range(600))
        folder = self.write_skill("sample-skill", body)
        problems = check_skill_folder(folder)
        self.assertTrue(any("line limit" in problem for problem in problems))

    def test_accepts_repository_level_resources(self) -> None:
        body = VALID_SKILL.replace("references/guide.md", "scripts/check.py")
        folder = self.write_skill("sample-skill", body)
        (self.root / "scripts").mkdir()
        (self.root / "scripts" / "check.py").write_text("print('ok')\n", encoding="utf-8")
        problems = check_skill_folder(folder, repo_root=self.root)
        self.assertEqual(problems, [])


if __name__ == "__main__":
    unittest.main()
