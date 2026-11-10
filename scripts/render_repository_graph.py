"""Repository-root entry point for the graph renderer bundled with the skill.

The implementation lives with its skill so the skill folder stays portable:

    .agents/skills/aether-repository-graph-3d/scripts/render_repository_graph.py

This wrapper runs that module, so `python scripts/render_repository_graph.py
--root . --output output/repository-graph.html` keeps working from the root of
a checkout.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SKILL_SCRIPT = ROOT / ".agents/skills/aether-repository-graph-3d/scripts/render_repository_graph.py"


def load_renderer():
    """Load the skill-bundled renderer module."""
    if not SKILL_SCRIPT.is_file():
        raise SystemExit(f"missing skill renderer: {SKILL_SCRIPT}")
    spec = importlib.util.spec_from_file_location("aether_render_repository_graph", SKILL_SCRIPT)
    if spec is None or spec.loader is None:
        raise SystemExit(f"cannot load skill renderer: {SKILL_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    sys.dont_write_bytecode = True
    spec.loader.exec_module(module)
    return module


renderer = load_renderer()


if __name__ == "__main__":
    raise SystemExit(renderer.main())
