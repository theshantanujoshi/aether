"""Render a Git-visible repository as a standalone, interactive 3D graph."""

from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import datetime, timezone
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys


TEMPLATE = Path(__file__).resolve().parents[1] / ".agents/skills/aether-repository-graph-3d/assets/graph.html"
EXCLUDED_PARTS = {".git", ".venv", "__pycache__", "node_modules", "output"}
TEXT_SUFFIXES = {".md", ".py", ".toml", ".txt", ".json", ".yaml", ".yml", ".js", ".ts"}
MAX_REFERENCE_BYTES = 1_000_000
PATH_TOKEN = re.compile(r"(?<![A-Za-z0-9_./-])(?:[A-Za-z0-9_.-]+/)+[A-Za-z0-9_.-]+")


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or f"git {' '.join(args)} failed")
    return result.stdout


def repository_root(path: Path) -> Path:
    return Path(git(path.resolve(), "rev-parse", "--show-toplevel").strip()).resolve()


def inventory(root: Path, output: Path) -> tuple[list[dict], list[dict], dict[str, int]]:
    raw = git(root, "ls-files", "--cached", "--others", "--exclude-standard", "-z")
    files = []
    omitted = {"removed_index_paths": 0, "excluded_entries": 0, "unsafe_entries": 0}
    for item in raw.split("\0"):
        if not item:
            continue
        path = PurePosixPath(item.replace("\\", "/"))
        if path.is_absolute() or ".." in path.parts:
            omitted["unsafe_entries"] += 1
            continue
        if any(part in EXCLUDED_PARTS for part in path.parts):
            omitted["excluded_entries"] += 1
            continue
        actual = root.joinpath(*path.parts)
        if actual.is_symlink():
            omitted["unsafe_entries"] += 1
            continue
        if not actual.is_file():
            omitted["removed_index_paths"] += 1
            continue
        if actual.resolve() == output.resolve():
            omitted["excluded_entries"] += 1
            continue
        files.append(path.as_posix())
    files = sorted(set(files))
    directories = {"."}
    for file in files:
        parent = PurePosixPath(file).parent
        while parent.as_posix() != ".":
            directories.add(parent.as_posix())
            parent = parent.parent
    nodes = [{"id": ".", "label": root.name, "kind": "root", "depth": 0}]
    nodes += [
        {"id": path, "label": PurePosixPath(path).name, "kind": "directory", "depth": len(PurePosixPath(path).parts)}
        for path in sorted(directories - {"."})
    ]
    nodes += [
        {"id": path, "label": PurePosixPath(path).name, "kind": "file", "depth": len(PurePosixPath(path).parts)}
        for path in files
    ]
    edges = []
    for node in nodes[1:]:
        parent = PurePosixPath(node["id"]).parent.as_posix()
        edges.append({"source": parent, "target": node["id"], "kind": "contains"})
    return nodes, edges, omitted


def references(root: Path, nodes: list[dict]) -> list[dict]:
    file_ids = {n["id"] for n in nodes if n["kind"] == "file"}
    directory_ids = {n["id"] for n in nodes if n["kind"] == "directory"}
    known = file_ids | directory_ids
    found = set()
    edges = []
    for source in sorted(file_ids):
        file = root.joinpath(*PurePosixPath(source).parts)
        if file.suffix.lower() not in TEXT_SUFFIXES or file.stat().st_size > MAX_REFERENCE_BYTES:
            continue
        content = file.read_text(encoding="utf-8", errors="replace")
        parent = PurePosixPath(source).parent
        for line_number, line in enumerate(content.splitlines(), 1):
            for match in PATH_TOKEN.finditer(line):
                token = match.group(0).rstrip(".,:;)")
                if token.startswith(("http/", "https/")):
                    continue
                candidates = [PurePosixPath(token).as_posix(), (parent / token).as_posix()]
                for target in candidates:
                    if target in known and target != source and (source, target) not in found:
                        found.add((source, target))
                        edges.append({"source": source, "target": target, "kind": "references", "line": line_number})
                        break
    return edges


def graph(root: Path, output: Path) -> dict:
    nodes, edges, omitted = inventory(root, output)
    edges += references(root, nodes)
    revision = git(root, "rev-parse", "--short", "HEAD").strip()
    dirty = bool(git(root, "status", "--porcelain").strip())
    return {
        "meta": {
            "repository": root.name,
            "revision": revision,
            "working_tree_modified": dirty,
            "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "method": "Git-visible working tree: tracked and untracked nonignored files",
            "excluded": sorted(EXCLUDED_PARTS),
            **omitted,
            "file_count": sum(n["kind"] == "file" for n in nodes),
            "directory_count": sum(n["kind"] == "directory" for n in nodes),
            "reference_count": sum(e["kind"] == "references" for e in edges),
        },
        "nodes": nodes,
        "edges": edges,
    }


def safe_json(data: dict) -> str:
    return json.dumps(data, ensure_ascii=True, separators=(",", ":")).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")


def render(data: dict) -> str:
    template = TEMPLATE.read_text(encoding="utf-8")
    marker = "__AETHER_GRAPH_DATA__"
    if template.count(marker) != 1:
        raise ValueError("Graph template must contain exactly one data marker")
    return template.replace(marker, safe_json(data))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Path inside the target Git repository")
    parser.add_argument("--output", type=Path, default=Path("output/repository-graph.html"), help="HTML artifact path")
    args = parser.parse_args()
    root = repository_root(args.root)
    output = args.output if args.output.is_absolute() else root / args.output
    data = graph(root, output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render(data), encoding="utf-8")
    print(f"Rendered {data['meta']['file_count']} files, {data['meta']['directory_count']} directories, and {data['meta']['reference_count']} references: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
