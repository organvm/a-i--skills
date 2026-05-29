#!/usr/bin/env python3
"""Ecosystem Autopsy Scanner

Traverses the ecosystem, maps current governance state, reads seed.yaml
dependencies, builds a directed graph, topologically sorts operations,
and generates autopsy_report.json and migration_manifest.json.
"""

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

# Hardened skip list — directories to never traverse
SKIP_DIRS = {
    ".git", "node_modules", "__pycache__", "venv", ".venv", "env",
    ".archive", ".recovery", ".serena", ".whisper", ".lh", ".openhand",
    ".specstory", ".temp", ".vscode", ".gemini", ".claude", ".codex",
    ".cache", ".Trash", "Library", "Applications", ".local/share",
}

VALID_STATES = {"LOCAL", "CANDIDATE", "PUBLIC_PROCESS", "GRADUATED"}
SEED_FILENAME = "seed.yaml"
IRF_FILENAME = "IRF.md"

DEFAULT_SCAN_PATHS = [
    Path.home() / "Workspace",
    Path.home() / "Code",
    Path.home() / "Documents",
]


def compute_dir_hash(directory: Path) -> str:
    """Compute SHA-256 of sorted, concatenated file contents in a directory."""
    h = hashlib.sha256()
    files = sorted(
        f for f in directory.rglob("*")
        if f.is_file() and ".git" not in f.parts
    )
    for f in files:
        h.update(str(f.relative_to(directory)).encode())
        try:
            h.update(f.read_bytes())
        except (PermissionError, OSError):
            pass
    return h.hexdigest()


def get_git_tree_sha(directory: Path) -> str | None:
    """Get git tree SHA for HEAD if directory is a git repo."""
    import subprocess
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD^{tree}"],
            cwd=str(directory),
            capture_output=True, text=True, timeout=10,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return None


def is_git_repo(directory: Path) -> bool:
    """Check if directory contains a valid .git."""
    return (directory / ".git").exists()


def get_remote_origin(directory: Path) -> str | None:
    """Get git remote origin URL if configured."""
    import subprocess
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=str(directory),
            capture_output=True, text=True, timeout=10,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return None


def get_last_commit_timestamp(directory: Path) -> str | None:
    """Get ISO 8601 timestamp of last commit."""
    import subprocess
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%ci"],
            cwd=str(directory),
            capture_output=True, text=True, timeout=10,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return None


def read_seed_yaml(directory: Path) -> dict[str, Any] | None:
    """Read and validate seed.yaml from a repository root."""
    seed_path = directory / SEED_FILENAME
    if not seed_path.exists():
        return None
    try:
        with open(seed_path) as f:
            data = yaml.safe_load(f)
        if not isinstance(data, dict):
            return None
        return data
    except (yaml.YAMLError, OSError):
        return None


def classify_repo(directory: Path) -> dict[str, Any]:
    """Classify a directory's governance state and metadata."""
    result: dict[str, Any] = {
        "path": str(directory),
        "name": directory.name,
        "is_git_repo": is_git_repo(directory),
        "has_seed": False,
        "has_irf": (directory / IRF_FILENAME).exists(),
        "remote_origin": None,
        "state": None,
        "governance_version": None,
        "dependencies": [],
        "last_commit": None,
        "pre_state_hash": None,
        "violations": [],
    }

    if result["is_git_repo"]:
        result["remote_origin"] = get_remote_origin(directory)
        result["last_commit"] = get_last_commit_timestamp(directory)
        result["pre_state_hash"] = get_git_tree_sha(directory)
    else:
        result["pre_state_hash"] = compute_dir_hash(directory)

    seed = read_seed_yaml(directory)
    if seed:
        result["has_seed"] = True
        state = seed.get("state")
        if state in VALID_STATES:
            result["state"] = state
        else:
            result["violations"].append(f"Invalid state in seed.yaml: {state!r}")
        result["governance_version"] = seed.get("governance_version")
        result["dependencies"] = seed.get("dependencies", [])
    else:
        result["violations"].append("Missing seed.yaml")

    if not result["has_irf"]:
        result["violations"].append("Missing IRF.md")

    if result["is_git_repo"] and not result["remote_origin"]:
        result["violations"].append("No remote origin configured")

    return result


def scan_directory(root: Path, depth: int = 2) -> list[dict[str, Any]]:
    """Scan a root directory for repositories and non-repo directories."""
    repos = []
    if not root.exists() or not root.is_dir():
        return repos

    for entry in root.iterdir():
        if not entry.is_dir() or entry.name in SKIP_DIRS:
            continue
        if entry.name.startswith("."):
            continue

        if is_git_repo(entry) or any(entry.iterdir()):
            repos.append(classify_repo(entry))

        # Recurse one level deeper for nested org directories
        if depth > 0:
            repos.extend(scan_directory(entry, depth - 1))

    return repos


def build_dependency_graph(repos: list[dict[str, Any]]) -> dict[str, list[str]]:
    """Build a directed graph of repo dependencies."""
    path_to_name = {r["path"]: r["name"] for r in repos}
    graph: dict[str, list[str]] = {r["name"]: [] for r in repos}

    for repo in repos:
        for dep in repo.get("dependencies", []):
            dep_path = str(Path(repo["path"]).parent / dep)
            dep_name = path_to_name.get(dep_path)
            if dep_name and dep_name in graph:
                graph[repo["name"]].append(dep_name)
            elif dep_name is None:
                repo["violations"].append(f"UNRESOLVED_DEPENDENCY: {dep}")

    return graph


def topological_sort(graph: dict[str, list[str]]) -> list[str]:
    """Topological sort so dependencies come before consumers."""
    visited = set()
    order = []
    temp_mark = set()

    def visit(node: str):
        if node in temp_mark:
            return  # cycle detected, skip
        if node in visited:
            return
        temp_mark.add(node)
        for dep in graph.get(node, []):
            visit(dep)
        temp_mark.remove(node)
        visited.add(node)
        order.append(node)

    for node in graph:
        if node not in visited:
            visit(node)

    return order


def compute_priority(repo: dict[str, Any]) -> int:
    """Compute migration priority score."""
    state_scores = {"GRADUATED": 40, "PUBLIC_PROCESS": 30, "CANDIDATE": 20, "LOCAL": 10, None: 5}
    score = state_scores.get(repo.get("state"), 5)

    if repo.get("violations"):
        score += 10

    if not repo.get("is_git_repo"):
        score += 5

    return score


def determine_operation(repo: dict[str, Any], target_root: Path) -> dict[str, Any] | None:
    """Determine the migration operation for a repo."""
    source = Path(repo["path"])
    current_state = repo.get("state")

    if current_state in VALID_STATES:
        target_dir = target_root / current_state / source.name
    else:
        target_dir = target_root / "LOCAL" / source.name

    if source == target_dir:
        return {
            "operation_id": "",
            "priority": compute_priority(repo),
            "source_path": str(source),
            "target_path": str(target_dir),
            "type": "noop",
            "depth_change": 0,
        }

    depth_change = len(target_dir.parts) - len(source.parts)

    if repo["is_git_repo"]:
        op_type = "git_mv"
    else:
        op_type = "mv"

    return {
        "operation_id": "",
        "priority": compute_priority(repo),
        "source_path": str(source),
        "target_path": str(target_dir),
        "type": op_type,
        "depth_change": abs(depth_change),
        "is_untracked_dir": not repo["is_git_repo"],
        "requires_init": not repo["is_git_repo"] and not repo["has_seed"],
    }


def generate_manifest(
    repos: list[dict[str, Any]],
    ecosystem_root: Path,
    graph: dict[str, list[str]],
) -> list[dict[str, Any]]:
    """Generate the migration manifest with topologically sorted operations."""
    sorted_names = topological_sort(graph)
    name_to_repo = {r["name"]: r for r in repos}

    operations = []
    for i, name in enumerate(sorted_names):
        repo = name_to_repo.get(name)
        if not repo:
            continue
        op = determine_operation(repo, ecosystem_root)
        if op:
            op["operation_id"] = f"op_{i + 1:03d}"
            operations.append(op)

    operations.sort(key=lambda o: o["priority"], reverse=True)
    for i, op in enumerate(operations):
        op["operation_id"] = f"op_{i + 1:03d}"

    return operations


def main():
    parser = argparse.ArgumentParser(description="Ecosystem Autopsy Scanner")
    parser.add_argument(
        "--workspace", nargs="+", type=Path, default=DEFAULT_SCAN_PATHS,
        help="Directories to scan (default: ~/Workspace ~/Code ~/Documents)",
    )
    parser.add_argument("--output", type=Path, default=Path("autopsy_report.json"),
                        help="Output path for autopsy report")
    parser.add_argument("--manifest", type=Path, default=Path("migration_manifest.json"),
                        help="Output path for migration manifest")
    args = parser.parse_args()

    all_repos = []
    for root in args.workspace:
        all_repos.extend(scan_directory(root))

    graph = build_dependency_graph(all_repos)
    operations = generate_manifest(all_repos, args.workspace[0], graph)

    violations = [v for r in all_repos for v in r.get("violations", [])]
    orphans = [r for r in all_repos if not r["has_seed"] and not r["has_irf"]]

    report = {
        "scan_timestamp": datetime.now(timezone.utc).isoformat(),
        "ecosystem_roots": [str(p) for p in args.workspace],
        "total_repos": len(all_repos),
        "git_repos": sum(1 for r in all_repos if r["is_git_repo"]),
        "non_repo_dirs": sum(1 for r in all_repos if not r["is_git_repo"]),
        "states": {s: sum(1 for r in all_repos if r.get("state") == s) for s in VALID_STATES},
        "violations": violations,
        "orphans": [{"path": r["path"], "name": r["name"]} for r in orphans],
        "repos": all_repos,
    }

    manifest = {
        "ecosystem_root": str(args.workspace[0]),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "operations": operations,
    }

    with open(args.output, "w") as f:
        json.dump(report, f, indent=2)
    print(f"Autopsy report written to {args.output}")

    with open(args.manifest, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"Migration manifest written to {args.manifest}")

    print(f"\nSummary: {len(all_repos)} repos scanned, {len(violations)} violations, {len(orphans)} orphans")


if __name__ == "__main__":
    main()
