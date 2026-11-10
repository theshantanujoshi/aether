---
name: aether-repository-inventory
description: "Use this skill when you need to establish exactly what a repository graph will contain before any layout is drawn: the checkout, revision, dirty worktree state, observation time, Git-visible files and directories, exclusions, and node IDs. It separates measured totals from display filters. Trigger it whenever a full-repository view is requested for the current working tree or a named revision, and before any claim about how complete a graph is. For edges use aether-repository-relations."
license: MIT
metadata:
  aether-kit-version: "0.2.0"
  aether-skill-version: "1.0"
---

# Repository inventory

Establish what the graph represents before placing nodes in space.

## Workflow

1. Identify the checkout, branch or commit, dirty worktree state, observation time, and requested inclusion rules. Use the current working tree unless the user specified a revision.
2. Enumerate Git-visible files, including untracked nonignored files, and their parent directories. Exclude `.git`, virtual environments, and generated output by default. State any submodule or sparse-checkout limits.
3. Assign stable repository-relative IDs. Record file versus directory, depth, and extension or category. Do not read secret contents to classify nodes.
4. Compare inventory totals with the graph input. Distinguish measured file totals from any display cap or filtered view.
5. Pass the inventory to `aether-repository-relations` and `aether-repository-graph-3d`. Report revision, method, counts, exclusions, and missing coverage.

## Gotchas

- Untracked but nonignored files are part of the working tree. Leaving them out makes the graph describe a commit rather than the checkout.
- Exclusions are part of the result. `.git`, virtual environments, and generated output are skipped by default, and the graph must say so.
- A sparse checkout or submodule makes "all files" smaller than the upstream repository. Name the limit instead of implying full coverage.
- Directory and file counts are different measures. A count of files that includes directories overstates coverage.

## Report

For the kit, `scripts/render_repository_graph.py` performs the default Git-visible inventory as part of rendering. Its JSON counts and output header are evidence for the generated artifact, not for an unrelated repository.
