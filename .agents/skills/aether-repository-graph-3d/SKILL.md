---
name: aether-repository-graph-3d
description: "Generate and verify an interactive local 3D repository graph from an Aether inventory and source-backed relations. Use when the user wants to look around the whole repository. For gathering files and edges use the inventory and relations skills first."
---

# 3D repository graph

Render a navigable perspective view of the actual repository, with an equivalent searchable text list. The support script is `scripts/render_repository_graph.py`.

## Workflow

1. Use `aether-repository-inventory` and `aether-repository-relations` to establish file coverage and edge semantics. Name the requested output path; default to `output/repository-graph.html` in the target checkout.
2. Run `python scripts/render_repository_graph.py --root <checkout> --output <html-path>`. The script embeds only relative paths and graph metadata in standalone HTML; it makes no network request and reads text files only to find explicit references.
3. Inspect the artifact counts, revision, generated time, and exclusions. Confirm containment and reference edges have separate legend entries. The 3D coordinates encode layout only, never evidence.
4. Check search, file-list fallback, keyboard controls, visible focus, and reduced-motion behavior. The graph must remain understandable without dragging or animation. W3C's [WCAG 2.2](https://www.w3.org/TR/WCAG22/) calls for text alternatives and keyboard operation.
5. Open the HTML in a local browser when available and inspect a representative viewport. If browser viewing is unavailable, run `scripts/test_render_repository_graph.py` and report that visual inspection remains unverified.

Do not add a web server, dashboard, CDN script, or analytics. Do not include source contents, credentials, absolute local paths, or inferred call edges in the exported artifact. Tell the user that filenames can reveal private project structure before they share it externally. Report the artifact path, counts, interactions checked, and any exclusions.
