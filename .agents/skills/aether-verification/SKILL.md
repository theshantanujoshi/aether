---
name: aether-verification
description: "Verify Aether skill outputs, user-approval boundaries, and repository graph coverage against current sources. Use before claiming an activity recap, persistent memory, backup, or full-repository 3D graph is complete."
---

# Aether verification

Check each requested outcome against current evidence. Read `../aether-workflow/references/evidence.md` first.

1. Record the task scope, source identity, revision or observation time, and requested deliverables. Separate specifications, source-backed facts, inferences, and observed output.
2. For activity work, trace a sample of recap or memory claims to approved material. Verify rejected and redacted sentinels are absent from persistent files, exports, and backup paths in scope.
3. For a repository graph, compare Git-visible inventory to the embedded node list, inspect representative containment and reference edges, and confirm the artifact identifies exclusions and worktree state.
4. Run `python scripts/validate_agent_kit.py` for kit structure and `python -m unittest discover -s scripts -p 'test_*.py'` for renderer behavior. Inspect any generated HTML in a browser when available; tests do not prove its visual quality.
5. Return a requirement-by-requirement result with commands, observed results, gaps, and unverified viewer behavior. Do not claim a complete scan from a sampled file list or infer runtime relationships from layout.

Use synthetic fixtures for automated tests. Do not read unrelated private sources or upload graph artifacts during verification.
