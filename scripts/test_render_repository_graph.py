"""Behavior checks for the local repository graph renderer."""

from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

import render_repository_graph as renderer


class RepositoryGraphTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        (self.root / ".gitignore").write_text("output/\n.venv/\n", encoding="utf-8")
        (self.root / "docs").mkdir()
        (self.root / "docs/guide.md").write_text("Guide\n", encoding="utf-8")
        (self.root / "README.md").write_text("See docs/guide.md for details.\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(self.root), "add", ".gitignore", "README.md", "docs/guide.md"], check=True)
        subprocess.run([
            "git", "-C", str(self.root), "-c", "user.name=Aether Test",
            "-c", "user.email=test@example.invalid", "-c", "commit.gpgsign=false",
            "commit", "-qm", "fixture",
        ], check=True)
        (self.root / "notes.txt").write_text("Untracked, visible file\n", encoding="utf-8")
        (self.root / ".venv").mkdir()
        (self.root / ".venv/secret.txt").write_text("not in graph", encoding="utf-8")

    def test_inventory_and_reference_evidence(self) -> None:
        output = self.root / "output/repository-graph.html"
        data = renderer.graph(self.root, output)
        ids = {node["id"] for node in data["nodes"]}
        self.assertEqual(ids, {".", ".gitignore", "README.md", "docs", "docs/guide.md", "notes.txt"})
        self.assertEqual(data["meta"]["file_count"], 4)
        self.assertTrue(data["meta"]["working_tree_modified"])
        self.assertIn({"source": "README.md", "target": "docs/guide.md", "kind": "references", "line": 1}, data["edges"])
        self.assertNotIn(".venv/secret.txt", ids)
        self.assertNotIn("output/repository-graph.html", ids)

    def test_standalone_html_and_safe_embedding(self) -> None:
        data = renderer.graph(self.root, self.root / "output/repository-graph.html")
        html = renderer.render(data)
        self.assertIn('id="graph-data"', html)
        self.assertIn('id="file-list"', html)
        self.assertIn('id="show-references"', html)
        self.assertNotIn('<script src=', html)
        embedded = re.search(r'<script type="application/json" id="graph-data">(.*?)</script>', html, re.S)
        self.assertIsNotNone(embedded)
        self.assertEqual(len(json.loads(embedded.group(1))["nodes"]), len(data["nodes"]))
        self.assertNotIn("</script>", renderer.safe_json({"unsafe": "</script>"}))

    def test_command_writes_openable_artifact(self) -> None:
        output = self.root / "output/repository-graph.html"
        result = subprocess.run([
            sys.executable, str(Path(renderer.__file__)), "--root", str(self.root),
            "--output", str(output),
        ], capture_output=True, text=True, check=True)
        self.assertTrue(output.is_file())
        self.assertIn("4 files", result.stdout)
        self.assertIn("Repository Atlas", output.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
