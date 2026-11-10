"""Dependency-free checks for the portable skill folder format.

A skill is a directory that holds a `SKILL.md` file with YAML frontmatter
followed by Markdown instructions. Optional `scripts/`, `references/`, and
`assets/` directories travel with the skill. This module reads that structure
and reports every deviation from the rules the kit enforces:

* `name` is required, 1-64 characters, lowercase letters, digits, and single
  hyphens only, and matches the parent directory name.
* `description` is required, non-empty, and at most 1024 characters.
* `license`, `compatibility` (at most 500 characters), `metadata` (string
  values), and `allowed-tools` are optional and are the only other fields.
* `SKILL.md` stays under 500 lines so instructions load cheaply.
* Referenced `scripts/`, `references/`, and `assets/` paths exist inside the
  skill folder and stay one level deep.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import re


MAX_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024
MAX_COMPATIBILITY_LENGTH = 500
MAX_SKILL_LINES = 500
ALLOWED_FIELDS = ("name", "description", "license", "compatibility", "metadata", "allowed-tools")
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FIELD_PATTERN = re.compile(r"^(?P<key>[A-Za-z0-9_-]+):(?:\s+(?P<value>.*))?$")
NESTED_PATTERN = re.compile(r"^\s+(?P<key>[A-Za-z0-9_-]+):(?:\s+(?P<value>.*))?$")
RESOURCE_PATTERN = re.compile(r"(?<![\w./-])((?:references|scripts|assets)/[A-Za-z0-9._-]+(?:/[A-Za-z0-9._-]+)*)")
NON_STRING_PATTERN = re.compile(r"^(?:[-+]?[0-9]+(?:\.[0-9]+)?|true|false|yes|no|on|off|null|~)$", re.IGNORECASE)


@dataclass
class Skill:
    """Parsed `SKILL.md` content."""

    path: Path
    name: str = ""
    description: str = ""
    fields: dict[str, object] = field(default_factory=dict)
    body: str = ""
    errors: list[str] = field(default_factory=list)


def _unquote(value: str) -> tuple[str, bool]:
    """Return the scalar value and whether it was written as a quoted string."""
    stripped = value.strip()
    if len(stripped) >= 2 and stripped[0] == stripped[-1] and stripped[0] in "\"'":
        return stripped[1:-1].replace('\\"', '"'), True
    return stripped, False


def parse_frontmatter(text: str) -> tuple[dict[str, object], str, list[str]]:
    """Parse `SKILL.md` text into frontmatter fields, body, and parse errors."""
    errors: list[str] = []
    if not text.startswith("---\n"):
        return {}, "", ["missing YAML frontmatter"]
    end = text.find("\n---\n", 3)
    if end == -1:
        return {}, "", ["unterminated YAML frontmatter"]
    block = text[4:end]
    body = text[end + len("\n---\n"):]
    fields: dict[str, object] = {}
    nested_key: str | None = None
    nested: dict[str, str] = {}
    for number, line in enumerate(block.splitlines(), start=2):
        if not line.strip():
            continue
        if line.startswith((" ", "\t")):
            match = NESTED_PATTERN.match(line)
            if not match or nested_key is None:
                errors.append(f"line {number}: unsupported indentation")
                continue
            value, quoted = _unquote(match.group("value") or "")
            if not quoted and ": " in value:
                errors.append(f"line {number}: value must be quoted because it contains a colon")
            nested[match.group("key")] = value
            continue
        match = FIELD_PATTERN.match(line)
        if not match:
            errors.append(f"line {number}: unsupported frontmatter line")
            continue
        key = match.group("key")
        raw = match.group("value")
        if raw is None or not raw.strip():
            nested_key = key
            nested = {}
            fields[key] = nested
            continue
        value, quoted = _unquote(raw)
        if not quoted and ": " in value:
            errors.append(f"line {number}: value must be quoted because it contains a colon")
        fields[key] = value
        nested_key = None
    return fields, body, errors


def read_skill(path: Path) -> Skill:
    """Read and parse one `SKILL.md` file."""
    skill = Skill(path=path)
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as error:
        skill.errors.append(f"unreadable: {error}")
        return skill
    fields, body, errors = parse_frontmatter(text)
    skill.fields = fields
    skill.body = body
    skill.errors.extend(errors)
    skill.name = fields.get("name") if isinstance(fields.get("name"), str) else ""
    skill.description = fields.get("description") if isinstance(fields.get("description"), str) else ""
    return skill


def _check_name(skill: Skill, expected_name: str | None, problems: list[str]) -> None:
    location = skill.path.name
    if not skill.name:
        problems.append(f"{location}: missing name")
        return
    if len(skill.name) > MAX_NAME_LENGTH:
        problems.append(f"{location}: name is longer than {MAX_NAME_LENGTH} characters")
    if not NAME_PATTERN.match(skill.name):
        problems.append(f"{location}: name must use lowercase letters, digits, and single hyphens")
    if skill.name.startswith("-") or skill.name.endswith("-"):
        problems.append(f"{location}: name must not start or end with a hyphen")
    if "--" in skill.name:
        problems.append(f"{location}: name must not contain consecutive hyphens")
    if expected_name and skill.name != expected_name:
        problems.append(f"{location}: name must match the skill directory name '{expected_name}'")


def _check_description(skill: Skill, problems: list[str]) -> None:
    location = skill.path.name
    description = skill.description.strip()
    if not description:
        problems.append(f"{location}: missing description")
    elif len(description) > MAX_DESCRIPTION_LENGTH:
        problems.append(f"{location}: description is longer than {MAX_DESCRIPTION_LENGTH} characters")


def _check_optional_fields(skill: Skill, problems: list[str]) -> None:
    location = skill.path.name
    for key in skill.fields:
        if key not in ALLOWED_FIELDS:
            problems.append(f"{location}: unsupported frontmatter field '{key}'")
    for key in ("license", "compatibility", "allowed-tools"):
        if key in skill.fields and not isinstance(skill.fields[key], str):
            problems.append(f"{location}: '{key}' must be a string")
    compatibility = skill.fields.get("compatibility")
    if isinstance(compatibility, str) and len(compatibility) > MAX_COMPATIBILITY_LENGTH:
        problems.append(f"{location}: compatibility is longer than {MAX_COMPATIBILITY_LENGTH} characters")
    metadata = skill.fields.get("metadata")
    if metadata is not None:
        if not isinstance(metadata, dict):
            problems.append(f"{location}: metadata must be a mapping of strings")
        else:
            for key, value in metadata.items():
                if not isinstance(value, str) or not value.strip():
                    problems.append(f"{location}: metadata value for '{key}' must be a non-empty string")


def _check_resources(skill: Skill, problems: list[str], repo_root: Path | None) -> None:
    location = skill.path.name
    root = skill.path.parent
    lines = skill.body.splitlines()
    if len(lines) > MAX_SKILL_LINES:
        problems.append(f"{location}: SKILL.md has {len(lines)} lines, over the {MAX_SKILL_LINES} line limit")
    for match in RESOURCE_PATTERN.finditer(skill.body):
        relative = match.group(1).rstrip(".,;:)")
        if len(Path(relative).parts) > 2:
            problems.append(f"{location}: keep resource references one level deep ('{relative}')")
            continue
        if (root / relative).exists():
            continue
        if repo_root is not None and (repo_root / relative).exists():
            continue
        problems.append(f"{location}: referenced resource '{relative}' is missing from the skill folder")


def check_skill_folder(skill_dir: Path, expected_name: str | None = None, repo_root: Path | None = None) -> list[str]:
    """Return every format problem found in one skill folder."""
    problems: list[str] = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return [f"{skill_dir.name}: missing SKILL.md"]
    skill = read_skill(skill_md)
    problems.extend(f"{skill_dir.name}: {error}" for error in skill.errors)
    if skill.errors:
        return problems
    name = expected_name if expected_name is not None else skill_dir.name
    _check_name(skill, name, problems)
    _check_description(skill, problems)
    _check_optional_fields(skill, problems)
    if not skill.body.strip():
        problems.append(f"{skill_dir.name}: SKILL.md body is empty")
    _check_resources(skill, problems, repo_root)
    return problems


def check_skill_folders(root: Path, expected_names: set[str] | None = None, repo_root: Path | None = None) -> list[str]:
    """Return every format problem found across the skill folders under `root`."""
    problems: list[str] = []
    if not root.is_dir():
        return [f"{root}: missing skills directory"]
    found = {path.parent.name for path in root.glob("*/SKILL.md")}
    for name in sorted(found):
        problems.extend(check_skill_folder(root / name, name, repo_root))
    if expected_names is not None:
        for missing in sorted(expected_names - found):
            problems.append(f"{root}: missing skill folder '{missing}'")
        for extra in sorted(found - expected_names):
            problems.append(f"{root}: uncataloged skill folder '{extra}'")
    return problems
