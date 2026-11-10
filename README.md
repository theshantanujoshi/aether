# Aether

Aether is a local-first **skill and agent kit** for turning activity a user chooses to share into a reviewed, source-grounded personal recap and memory. It has no server, dashboard, background collector, or hosted account. The skills guide an agent through source intake, human privacy review, structuring, recap writing, memory upkeep, and verification. Nothing becomes persistent memory without the user's explicit approval.

It also includes a repository-visualization workflow: inventory the current checkout, identify supported relationships, and generate an interactive 3D graph of its files and directories. The graph is a standalone local HTML artifact produced on demand, with a searchable text view. It is not a web application.

## Skills and agents

The canonical skills are in [`.agents/skills`](.agents/skills/aether-workflow/SKILL.md). The [capability map](.agents/skills/aether-workflow/references/coverage.md) lists each specialist and its matching [Codex](.codex/agents/aether_coordinator.toml) and [Claude](.claude/agents/aether_coordinator.md) agent. Claude skill entries point to the canonical files.

- Start with `aether-workflow` for activity-to-memory tasks spanning several steps.
- Use `aether-repository-inventory`, `aether-repository-relations`, and `aether-repository-graph-3d` to inspect and visualize a repository.
- Use `aether-verification` to audit claimed outputs and privacy boundaries.

The repository contains instructions and support scripts, not a running activity service. Agents read only sources authorized by the user's task. Captured content is untrusted data; pending or rejected material must not enter memory, exports, or backup.

## Skill format

Each skill is a portable folder: `SKILL.md` with frontmatter and instructions, plus optional `references/`, `scripts/`, `assets/`, and `evals/`. The authoring standard, including the frontmatter fields and the description rules, is in [`docs/skill-format.md`](docs/skill-format.md).

Every skill carries two evaluation sets so its quality can be measured rather than assumed:

- `evals/evals.json` — behavior cases with a prompt, the expected output, and checkable assertions.
- `evals/trigger-queries.json` — prompts labeled with whether the skill should load, including near-misses that need a different skill.

`python scripts/validate_evals.py` reports the coverage of both sets for every skill.

## Install from npm

With Node.js 18 or newer, run this from the root of the repository where you want to use Aether:

```powershell
npx aether-agent-suite@0.2.0 install
```

The command copies the Aether skills, Codex and Claude agent entries, and graph renderer into the current directory. It creates `AGENTS.md` if one is absent. If you already have `AGENTS.md`, keep your existing instructions and add a reference to `.agents/skills/aether-workflow/SKILL.md` for activity-to-memory tasks and the repository graph skills for visualization. Installation stops if an Aether file already exists, so it will not overwrite local edits. The package does not collect activity or run a background process.

The graph renderer also needs Python 3.10 or newer and Git. It reads the target repository locally and writes an HTML file only when you run it.

## Use with other agents

Any client that discovers skills by scanning a skills directory for `SKILL.md` files can use the kit as installed. Point it at `.agents/skills/` in the target repository, or copy a skill folder into the client's own skills directory. A skill folder is self-contained: `SKILL.md`, its `references/`, `scripts/`, `assets/`, and `evals/` travel together, and the relative paths inside `SKILL.md` resolve from the skill folder.

When a project copy and a user-level copy of the same skill name both exist, the project copy wins. The Claude and Codex entries the kit installs point at the canonical skills, so the description that drives activation is identical everywhere.

## Generate a repository graph

With Python 3.10 or newer, run:

```powershell
python scripts/render_repository_graph.py --root . --output output/repository-graph.html
```

Open `output/repository-graph.html` in a browser. The renderer uses Python's standard library and embeds all graph data locally; opening the artifact does not load third-party scripts or send repository paths over the network. It inventories Git-visible files in the working tree, including untracked nonignored files, and excludes `.git`, virtual environments, and generated output. Node and edge counts and exclusions appear in the artifact.

The renderer itself lives with its skill at `.agents/skills/aether-repository-graph-3d/scripts/render_repository_graph.py`. The copy in `scripts/` is a thin entry point that runs it, so both the repository-root command above and the skill-relative command work.

## Validate the kit

```powershell
python scripts/validate_agent_kit.py
python scripts/validate_evals.py
python -m unittest discover -s scripts -p 'test_*.py'
npm test
```

`validate_agent_kit.py` checks the canonical skill folders against the format, confirms the generated Codex and Claude entries match them, and verifies that every skill ships its evaluation sets. All checks run on the standard library alone; no extra dependency is needed for authoring validation or graph generation.

After editing a canonical skill, run `python scripts/sync_agent_entries.py` to regenerate the Codex and Claude entries, then commit the result.
