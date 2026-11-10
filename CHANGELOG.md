# Changelog

## [0.2.0] - 2026-11-10

### Added

- Ship a portable skill folder for every skill: frontmatter with `name`, `description`, `license`, optional `compatibility` and `metadata`, plus bundled `references/`, `scripts/`, `assets/`, and `evals/` directories.
- Add per-skill evaluation sets. `evals/evals.json` holds behavior cases with expected output and assertions, and `evals/trigger-queries.json` holds activation cases with near-miss queries. `python scripts/validate_evals.py` reports the coverage of both sets.
- Validate the skill format without third-party dependencies. `python scripts/validate_agent_kit.py` checks names, descriptions, frontmatter fields, instruction size, bundled resource references, and evaluation coverage, and confirms the generated Codex and Claude entries match the canonical skills.
- Document the authoring standard in `docs/skill-format.md` and the checks in `AGENTS.md`.

### Changed

- Rewrite every skill description to state what the skill does and when to use it, and point to the neighbouring skill for near-miss requests.
- Move the graph renderer into its skill at `.agents/skills/aether-repository-graph-3d/scripts/render_repository_graph.py` so the skill folder works on its own. `scripts/render_repository_graph.py` is now a thin entry point that runs it.
- Generate the Claude skill entries from the canonical skill frontmatter, so a Claude user sees the same description that drives activation.
- Mirror the shared evidence contract into the skills that read it, so each skill folder is self-contained.

### Removed

- Drop the optional `scripts/requirements-agentkit.txt` dependency. The validators and the renderer use the standard library only.

## [0.1.0] - 2026-10-20

### Added

- Install Aether's local skills and Codex and Claude agent entries with `npx aether-agent-suite@0.1.0 install`. The installer preserves existing files.
- Build an on-demand, standalone 3D graph of a Git repository with the included Python renderer.
- Use reviewed, source-grounded workflows for activity recaps and user-approved persistent memory.

[0.2.0]: https://github.com/theshantanujoshi/aether/releases/tag/v0.2.0
[0.1.0]: https://github.com/theshantanujoshi/aether/releases/tag/v0.1.0
