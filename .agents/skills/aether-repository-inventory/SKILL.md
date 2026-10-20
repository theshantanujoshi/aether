---
name: aether-repository-inventory
description: "Inventory the full Git-visible working tree before creating an Aether repository graph. Use to establish revision, included files, directories, exclusions, and node counts. For relationship analysis use aether-repository-relations."
---

# Repository inventory

Establish what the graph represents before placing nodes in space.

1. Identify the checkout, branch or commit, dirty worktree state, observation time, and requested inclusion rules. Use the current working tree unless the user specified a revision.
2. Enumerate Git-visible files, including untracked nonignored files, and their parent directories. Exclude `.git`, virtual environments, and generated output by default. State any submodule or sparse-checkout limits.
3. Assign stable repository-relative IDs. Record file versus directory, depth, and extension or category. Do not read secret contents to classify nodes.
4. Compare inventory totals with the graph input. Distinguish measured file totals from any display cap or filtered view.
5. Pass the inventory to `aether-repository-relations` and `aether-repository-graph-3d`. Report revision, method, counts, exclusions, and missing coverage.

For this kit, `scripts/render_repository_graph.py` performs the default Git-visible inventory as part of rendering. Its JSON counts and output header are evidence for the generated artifact, not for an unrelated repository.
