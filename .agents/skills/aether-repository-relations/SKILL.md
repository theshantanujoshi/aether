---
name: aether-repository-relations
description: "Use this skill when you need to derive graph edges that can be defended: containment from real parent directories, and reference edges from paths or skill names that actually appear in a file, with the source file and matched target recorded. It keeps import, call, and runtime relations absent unless they are separately verified. Trigger it between aether-repository-inventory and aether-repository-graph-3d, and when someone asks how files in a repository relate to each other."
license: MIT
metadata:
  aether-kit-version: "0.2.0"
  aether-skill-version: "1.0"
---

# Repository relationships

Give each graph edge a verifiable meaning.

## Workflow

1. Start with `aether-repository-inventory` and preserve its revision and file scope.
2. Derive containment edges from actual parent directories. For reference edges, match explicit repo-relative paths or canonical skill paths found in text files to an inventoried target. Record the source file and matched target.
3. Add import, call, or runtime edges only after checking relevant source syntax or execution evidence. Keep these relation types distinct; absence of a parser means they remain unmeasured.
4. Deduplicate edges by source, target, and type. Keep direction explicit. Label sampled or unresolved references as omitted rather than drawing speculative links.
5. Verify representative edges against the actual files, then hand stable IDs and evidence to `aether-repository-graph-3d`.

## Gotchas

- A path mentioned in prose is a reference, not a dependency. The edge records that the text names the file, nothing more.
- Duplicate mentions of the same target are one edge. Record the first line that matched rather than a weight per mention.
- A file that is not inventoried cannot be a target. Excluded paths stay out of the graph instead of dangling.
- Unresolved or sampled references belong in the report as omissions, not in the graph as inferred edges.

## Report

The default renderer includes containment and explicit references only. It does not infer architecture from file proximity or node layout. Report relation counts, method, examples checked, and omitted edge types.
