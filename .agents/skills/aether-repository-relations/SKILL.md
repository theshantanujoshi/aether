---
name: aether-repository-relations
description: "Find source-backed relationships for an Aether repository graph, separating folder containment and explicit file references from inferred imports, calls, or runtime paths. Use after repository inventory and before 3D rendering."
---

# Repository relationships

Give each graph edge a verifiable meaning.

1. Start with `aether-repository-inventory` and preserve its revision and file scope.
2. Derive containment edges from actual parent directories. For reference edges, match explicit repo-relative paths or canonical skill paths found in text files to an inventoried target. Record the source file and matched target.
3. Add import, call, or runtime edges only after checking relevant source syntax or execution evidence. Keep these relation types distinct; absence of a parser means they remain unmeasured.
4. Deduplicate edges by source, target, and type. Keep direction explicit. Label sampled or unresolved references as omitted rather than drawing speculative links.
5. Verify representative edges against the actual files, then hand stable IDs and evidence to `aether-repository-graph-3d`.

The default renderer includes containment and explicit references only. It does not infer architecture from file proximity or node layout. Report relation counts, method, examples checked, and omitted edge types.
