---
name: aether-verification
description: "Use this skill when you are about to claim that an Aether recap, memory file, backup, or repository graph is complete: check every requirement against current sources, prove rejected and redacted material is absent from durable artifacts, and reconcile graph nodes with the Git-visible inventory. It reports requirement-by-requirement results with the commands run and what stays unverified. Trigger it at the end of any Aether task that produces a deliverable. For the graph workflow use aether-repository-inventory first."
license: MIT
metadata:
  aether-kit-version: "0.2.0"
  aether-skill-version: "1.0"
---

# Aether verification

Check each requested outcome against current evidence. Read `references/evidence.md` first.

## Workflow

1. Record the task scope, source identity, revision or observation time, and requested deliverables. Separate specifications, source-backed facts, inferences, and observed output.
2. For activity work, trace a sample of recap or memory claims to approved material. Verify rejected and redacted sentinels are absent from persistent files, exports, and backup paths in scope.
3. For a repository graph, compare Git-visible inventory to the embedded node list, inspect representative containment and reference edges, and confirm the artifact identifies exclusions and worktree state.
4. Run `python scripts/validate_agent_kit.py` for kit structure and `python -m unittest discover -s scripts -p 'test_*.py'` for renderer behavior when you are working inside the Aether kit repository. Inspect any generated HTML in a browser when available; tests do not prove its visual quality.
5. Return a requirement-by-requirement result with commands, observed results, gaps, and unverified viewer behavior. Do not claim a complete scan from a sampled file list or infer runtime relationships from layout.

## Gotchas

- "The test passed" is not the same as "the artifact is correct". The renderer tests prove inventory and embedding behavior; only a browser view proves the 3D view, focus order, and search work.
- Absence must be demonstrated. Search the durable artifacts for the sentinel and show the result, rather than reporting that the item was not written.
- A sampled check is a sample. Report it as a sample, and say how much of the material was actually inspected.
- A file that exists is not a file that is correct. Confirm the content matches the current revision before calling the output verified.

## Guardrails

Use synthetic fixtures for automated tests. Do not read unrelated private sources or upload graph artifacts during verification.
