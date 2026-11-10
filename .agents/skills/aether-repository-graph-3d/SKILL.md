---
name: aether-repository-graph-3d
description: "Use this skill when the user wants to generate and check an interactive, standalone 3D graph of a Git repository with a searchable text view, a keyboard-reachable file list, and separate legend entries for containment and reference edges. It runs the bundled renderer to write one local HTML file and makes no network request. Trigger it to explore a whole repository visually or to confirm the graph artifact's counts, exclusions, and accessibility behavior. Gather files and edges with the inventory and relations skills first."
license: MIT
compatibility: Requires Python 3.10 or newer and Git; writes one standalone local HTML file.
metadata:
  aether-kit-version: "0.2.0"
  aether-skill-version: "1.0"
---

# 3D repository graph

Render a navigable perspective view of the actual repository, with an equivalent searchable text list.

## Bundled resources

- **`scripts/render_repository_graph.py`** — Reads the checkout with Git and writes one standalone HTML artifact.
- **`assets/graph.html`** — The template the renderer fills with local graph data.

## Workflow

1. Use `aether-repository-inventory` and `aether-repository-relations` to establish file coverage and edge semantics. Name the requested output path; default to `output/repository-graph.html` in the target checkout.
2. Run `python scripts/render_repository_graph.py --root <checkout> --output <html-path>` from this skill directory. The script embeds only relative paths and graph metadata in standalone HTML; it makes no network request and reads text files only to find explicit references.
3. Inspect the artifact counts, revision, generated time, and exclusions. Confirm containment and reference edges have separate legend entries. The 3D coordinates encode layout only, never evidence.
4. Check search, file-list fallback, keyboard controls, visible focus, and reduced-motion behavior. The graph must remain understandable without dragging or animation. W3C's [WCAG 2.2](https://www.w3.org/TR/WCAG22/) calls for text alternatives and keyboard operation.
5. Open the HTML in a local browser when available and inspect a representative viewport. If browser viewing is unavailable, report that visual inspection remains unverified instead of substituting a test result.

## Gotchas

- The script's output path is relative to the repository root it resolves, not to the shell's working directory. Pass an absolute path when the output must land elsewhere.
- The artifact embeds file names. That is useful for the user and risky for sharing, so say so before the file leaves the machine.
- The renderer never infers edges from layout or proximity. If the user wants call or import relations, that is a separate, evidence-backed step.
- A generated file changes the working tree. Exclude the output path so the graph does not measure its own artifact.

## Guardrails

Do not add a web server, dashboard, CDN script, or analytics. Do not include source contents, credentials, absolute local paths, or inferred call edges in the exported artifact. Tell the user that filenames can reveal private project structure before they share it externally.

## Report

Return the artifact path, counts, interactions checked, and any exclusions.
