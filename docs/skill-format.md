# Skill format standard

Aether ships portable skill folders. This document is the authoring standard the kit enforces in `scripts/validate_agent_kit.py`. It is written for humans and agents editing this repository; a user who only installs the kit never needs it.

## Folder layout

```
aether-<name>/
├── SKILL.md                  # required: frontmatter and instructions
├── references/               # optional: detail loaded on demand
├── scripts/                  # optional: executable helpers
├── assets/                   # optional: templates and static resources
└── evals/                    # optional: behavior and trigger cases
```

A skill must work when its folder is copied on its own. Bundled scripts, references, and assets travel with the folder, and file references in `SKILL.md` are written relative to the skill root (`scripts/render_repository_graph.py`, `references/guide.md`).

## Frontmatter

`SKILL.md` starts with YAML frontmatter followed by the instructions.

```yaml
---
name: aether-example
description: "Use this skill when the user asks for ... It does ... Trigger it when ..."
license: MIT
compatibility: Requires Python 3.10 or newer and Git.
metadata:
  aether-kit-version: "0.2.0"
  aether-skill-version: "1.0"
---
```

| Field | Required | Rules |
| --- | --- | --- |
| `name` | yes | 1-64 characters, lowercase letters, digits, and single hyphens, must match the folder name |
| `description` | yes | 1-1024 characters, states what the skill does and when to use it |
| `license` | no | short license name |
| `compatibility` | no | at most 500 characters, environment requirements only |
| `metadata` | no | mapping of string keys to string values |
| `allowed-tools` | no | space-separated list of pre-approved tools |

No other fields are allowed.

## Writing the description

The description is the only text an agent sees before it decides whether to load the skill, so it carries the whole triggering burden.

* Lead with an imperative sentence: "Use this skill when ...".
* Say what the skill does and the situation that calls for it.
* Name the situations that look similar but belong to another skill, and point to the neighbour by name.
* Keep it under 1024 characters.

## Writing the instructions

* Prefer a numbered workflow over prose. The workflow is the reusable method, not the answer to one request.
* Add a "Gotchas" section for the corrections an agent would otherwise make: environment facts, naming traps, and the failure that keeps coming back.
* Add a "Report" section that fixes the shape of the final answer.
* Keep the file under 500 lines. Move detail to `references/` and say when to read it.
* Reference bundled files one level deep. Deep chains cost context and break when a file moves.

## Bundled scripts

Scripts live in the skill's own `scripts/` folder and are referenced relative to the skill root.

* No interactive prompts. Accept input through flags, environment variables, or stdin.
* Document the interface in `--help`, with the flags, the defaults, and one example.
* Print structured data to stdout and diagnostics to stderr.
* Use meaningful exit codes and idempotent behavior, because an agent may retry a command.
* Provide a dry run for anything destructive or stateful.

## Evaluation sets

Each skill carries two files that let its quality be measured instead of assumed.

`evals/evals.json` holds behavior cases:

```json
{
  "skill_name": "aether-example",
  "evals": [
    {
      "id": 1,
      "prompt": "A realistic request, with paths and context.",
      "expected_output": "What a good answer contains.",
      "assertions": ["Something checkable about the output"]
    }
  ]
}
```

Keep two or three cases to start, vary the phrasing, and include one case that probes a boundary. Write assertions that a person or a script can check, not impressions.

`evals/trigger-queries.json` holds activation cases as a flat list:

```json
[
  { "query": "A request the skill should handle.", "should_trigger": true },
  { "query": "A similar request that needs a different skill.", "should_trigger": false }
]
```

The near-misses matter more than the obvious positives. A query that shares vocabulary with the skill but needs something else is what proves the description is precise.

Run `python scripts/validate_evals.py` to check the structure and print the coverage of both sets.

## Checks

```powershell
python scripts/validate_agent_kit.py
python scripts/validate_evals.py
python -m unittest discover -s scripts -p 'test_*.py'
```

The validator fails on an invalid name, a missing or oversized description, an unknown frontmatter field, a `SKILL.md` over 500 lines, a resource reference that does not exist, a reference deeper than one level, a missing evaluation set, and a generated Codex or Claude entry that is out of sync with the canonical skill.
