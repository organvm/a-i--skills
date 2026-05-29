#!/usr/bin/env python3
"""Migration Executor

Defensive mutation engine that processes migration_manifest.json operations
with batch atomicity, collision detection, git-aware moves, idempotent
rollback, and "Flag, Don't Fix" import depth detection.
"""

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SEED_YAML_TEMPLATE = """state: LOCAL
governance_version: 1
dependencies: []
description: ""
owner: ""
"""

IRF_TEMPLATE = """# Identity Reference File

- **Repository:** {repo_name}
- **Governance State:** LOCAL
- **Governance Version:** 1
- **GitHub Issue:** <pending>
- **Remote Origin:** <pending>
- **Triple-Reference Checksum:** <pending>
- **Last Verified:** {timestamp}
"""

INTERVENTION_TEMPLATE = """# Manual Intervention Required — Import Path Review

The following files contain relative imports that may be broken after migration:

| File | Line | Import Statement | Likely Fix |
|------|------|-----------------|------------|
{rows}

Review and update import paths before committing.
"""

MISSING_REFERENCES_MD = """# Missing Triple-Reference Components

The following resources need to be created manually:

1. **GitHub Issue:** Create an issue at https://github.com/<owner>/<repo>/issues
   - Title: "Track governance migration to {state}"
   - Body: "This issue tracks the migration of {repo} to {state} state..."

2. **IRF (Identity Reference File):** Create `IRF.md` in the repository root with:
   - Repository name
   - Governance state
   - GitHub issue URL
   - Triple-reference checksum
"""


def compute_dir_hash(directory: Path) -> str:
    """Compute SHA-256 of sorted, concatenated file contents."""
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
    """Get git tree SHA for HEAD."""
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


def run_git_mv(source: Path, target: Path) -> bool:
    """Execute git mv with collision check."""
    if target.exists():
        print(f"  COLLISION: {target} already exists", file=sys.stderr)
        return False
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        result = subprocess.run(
            ["git", "mv", str(source), str(target)],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode != 0:
            print(f"  GIT MV FAILED: {result.stderr.strip()}", file=sys.stderr)
            return False
        return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def run_mv(source: Path, target: Path) -> bool:
    """Execute standard mv with collision check."""
    if target.exists():
        print(f"  COLLISION: {target} already exists", file=sys.stderr)
        return False
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        shutil.move(str(source), str(target))
        return True
    except OSError as e:
        print(f"  MV FAILED: {e}", file=sys.stderr)
        return False


def run_init(directory: Path) -> bool:
    """Initialize git repo and create baseline seed.yaml."""
    try:
        subprocess.run(
            ["git", "init"], cwd=str(directory),
            capture_output=True, text=True, timeout=10,
        )
        seed_path = directory / "seed.yaml"
        if not seed_path.exists():
            seed_path.write_text(SEED_YAML_TEMPLATE)
        subprocess.run(
            ["git", "add", "."], cwd=str(directory),
            capture_output=True, text=True, timeout=10,
        )
        return True
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return False


def detect_import_depth_changes(directory: Path, depth_change: int) -> list[dict[str, str]]:
    """Detect files with relative imports that may need updating."""
    flagged = []
    import_patterns = [
        "from ..", "from .", "import ..",
        "require('../", "require('./", "require('..",
    ]

    for ext in (".py", ".js", ".ts", ".jsx", ".tsx"):
        for f in directory.rglob(f"*{ext}"):
            if ".git" in f.parts:
                continue
            try:
                lines = f.read_text().splitlines()
                for i, line in enumerate(lines, 1):
                    stripped = line.strip()
                    if any(pat in stripped for pat in import_patterns):
                        likely_fix = suggest_fix(stripped, depth_change)
                        flagged.append({
                            "file": str(f.relative_to(directory)),
                            "line": str(i),
                            "import_statement": stripped,
                            "likely_fix": likely_fix,
                        })
            except (OSError, UnicodeDecodeError):
                continue

    return flagged


def suggest_fix(import_line: str, depth_change: int) -> str:
    """Suggest a likely fix for a relative import."""
    if "from .." in import_line:
        extra_dots = "." * depth_change
        return import_line.replace("from ..", f"from .{extra_dots}..", 1)
    if "from ." in import_line:
        extra_dots = "." * depth_change
        return import_line.replace("from .", f"from .{extra_dots}", 1)
    if "require('../" in import_line:
        extra = "../" * depth_change
        return import_line.replace("require('../", f"require('{extra}../", 1)
    return "Review import path depth"


def write_intervention_file(directory: Path, flagged: list[dict[str, str]]):
    """Write MANUAL_INTERVENTION_REQUIRED.md to target directory."""
    rows = "\n".join(
        f"| {f['file']} | {f['line']} | `{f['import_statement']}` | `{f['likely_fix']}` |"
        for f in flagged
    )
    content = INTERVENTION_TEMPLATE.format(rows=rows)
    (directory / "MANUAL_INTERVENTION_REQUIRED.md").write_text(content)


def write_missing_references(target: Path, repo_name: str, state: str, has_gh_cli: bool):
    """Generate dual reference output for missing triple-reference components."""
    md_path = target / "MISSING_REFERENCES.md"
    md_path.write_text(MISSING_REFERENCES_MD.format(repo=repo_name, state=state))

    if has_gh_cli:
        sh_path = target / "MISSING_REFERENCES_CMDS.sh"
        sh_content = f"""#!/bin/bash
# Auto-generated commands for creating missing triple-reference components
# Repository: {repo_name}
# Target State: {state}

# Create GitHub tracking issue
gh issue create \\
  --title "Governance Migration: {repo_name} → {state}" \\
  --body "This issue tracks the migration of {repo_name} to {state} state."

echo "Issue created. Now create IRF.md in the repository root."
"""
        sh_path.write_text(sh_content)
        sh_path.chmod(0o755)


def has_gh_cli() -> bool:
    """Check if GitHub CLI is available."""
    try:
        result = subprocess.run(
            ["gh", "--version"], capture_output=True, text=True, timeout=5,
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def execute_operation(op: dict[str, Any], execute: bool) -> dict[str, Any] | None:
    """Execute a single migration operation. Returns rollback entry or None."""
    op_id = op["operation_id"]
    source = Path(op["source_path"])
    target = Path(op["target_path"])
    op_type = op["type"]
    depth_change = op.get("depth_change", 0)

    print(f"  [{op_id}] {op_type}: {source} → {target}")

    if not execute:
        return None

    pre_hash = None
    if op_type in ("git_mv", "noop"):
        pre_hash = get_git_tree_sha(source)
    else:
        pre_hash = compute_dir_hash(source)

    if pre_hash is None:
        pre_hash = hashlib.sha256(b"unknown").hexdigest()

    success = False
    if op_type == "noop":
        success = True
    elif op_type == "git_mv":
        success = run_git_mv(source, target)
    elif op_type == "mv":
        success = run_mv(source, target)
    elif op_type == "init":
        success = run_init(source)
        if success:
            target = source

    if not success:
        print(f"  [{op_id}] FAILED", file=sys.stderr)
        return None

    if execute and depth_change >= 1 and op_type != "noop":
        flagged = detect_import_depth_changes(target, depth_change)
        if flagged:
            write_intervention_file(target, flagged)
            print(f"  [{op_id}] Flagged {len(flagged)} files for import review")

    if execute and op.get("requires_init") and op_type == "mv":
        run_init(target)

    inverse_action = "noop"
    if op_type == "git_mv":
        inverse_action = f"git mv {target} {source}"
    elif op_type == "mv":
        inverse_action = f"mv {target} {source}"
    elif op_type == "init":
        inverse_action = f"rm -rf {source}/.git {source}/seed.yaml"

    return {
        "rollback_id": f"rb_{op_id.split('_')[1]}",
        "forward_operation_id": op_id,
        "inverse_action": inverse_action,
        "pre_state_hash": pre_hash,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "rolled_back": False,
    }


def undo_operation(rollback_entry: dict[str, Any]) -> bool:
    """Undo a single operation using the rollback ledger."""
    if rollback_entry.get("rolled_back"):
        return True

    action = rollback_entry["inverse_action"]
    print(f"  Undoing: {action}")

    parts = action.split()
    if parts[0] == "git" and parts[1] == "mv":
        try:
            result = subprocess.run(
                ["git", "mv", parts[2], parts[3]],
                capture_output=True, text=True, timeout=30,
            )
            if result.returncode == 0:
                rollback_entry["rolled_back"] = True
                return True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
    elif parts[0] == "mv":
        try:
            shutil.move(parts[1], parts[2])
            rollback_entry["rolled_back"] = True
            return True
        except OSError:
            pass
    elif parts[0] == "rm":
        for path in parts[2:]:
            p = Path(path)
            if p.exists():
                if p.is_dir():
                    shutil.rmtree(p, ignore_errors=True)
                else:
                    p.unlink(missing_ok=True)
        rollback_entry["rolled_back"] = True
        return True

    return False


def main():
    parser = argparse.ArgumentParser(description="Migration Executor")
    parser.add_argument("--manifest", type=Path, required=True,
                        help="Path to migration_manifest.json")
    parser.add_argument("--execute", action="store_true",
                        help="Perform mutations (default: dry-run)")
    parser.add_argument("--undo", action="store_true",
                        help="Reverse the rollback ledger")
    args = parser.parse_args()

    if not args.manifest.exists():
        print(f"Error: Manifest not found: {args.manifest}", file=sys.stderr)
        sys.exit(1)

    manifest = json.loads(args.manifest.read_text())
    operations = manifest.get("operations", [])

    if not operations:
        print("No operations in manifest.")
        sys.exit(0)

    batch_id = f"batch_{int(datetime.now(timezone.utc).timestamp())}"
    rollback_path = Path("rollback_manifest.json")

    if args.undo:
        if not rollback_path.exists():
            print("Error: No rollback manifest found.", file=sys.stderr)
            sys.exit(1)

        rollback = json.loads(rollback_path.read_text())
        undone = 0
        for entry in rollback.get("operations", []):
            if not entry.get("rolled_back"):
                if undo_operation(entry):
                    undone += 1
                else:
                    print(f"  Failed to undo {entry['rollback_id']}", file=sys.stderr)

        rollback["status"] = "UNDO_COMPLETED"
        rollback_path.write_text(json.dumps(rollback, indent=2))
        print(f"Undone {undone} operations.")
        sys.exit(0)

    mode = "EXECUTE" if args.execute else "DRY-RUN"
    print(f"Migration Executor [{mode}]")
    print(f"Batch: {batch_id}")
    print(f"Operations: {len(operations)}")
    print()

    gh_available = has_gh_cli()
    rollback_entries = []
    failed_at = None

    for i, op in enumerate(operations):
        entry = execute_operation(op, args.execute)

        if entry is None and args.execute:
            failed_at = i
            print(f"\nBatch FAILED at operation {op['operation_id']}")
            print("Auto-triggering rollback for prior operations...")

            for rb in rollback_entries:
                undo_operation(rb)

            rollback_data = {
                "batch_id": batch_id,
                "status": "FAILED",
                "operations": rollback_entries,
            }
            rollback_path.write_text(json.dumps(rollback_data, indent=2))
            print(f"Rollback complete. Rollback manifest written to {rollback_path}")
            sys.exit(1)

        if entry:
            rollback_entries.append(entry)

        if args.execute and entry:
            target = Path(op["target_path"])
            if target.exists() and not (target / "seed.yaml").exists():
                state = "LOCAL"
                for s in ("GRADUATED", "PUBLIC_PROCESS", "CANDIDATE", "LOCAL"):
                    if s in str(target):
                        state = s
                        break
                write_missing_references(target, op["source_path"].split("/")[-1], state, gh_available)

    if args.execute:
        rollback_data = {
            "batch_id": batch_id,
            "status": "COMPLETED",
            "operations": rollback_entries,
        }
        rollback_path.write_text(json.dumps(rollback_data, indent=2))
        print(f"\nBatch COMPLETED. Rollback manifest written to {rollback_path}")
    else:
        print(f"\nDry-run complete. No mutations performed.")
        print(f"Run with --execute to apply {len(operations)} operations.")


if __name__ == "__main__":
    main()
