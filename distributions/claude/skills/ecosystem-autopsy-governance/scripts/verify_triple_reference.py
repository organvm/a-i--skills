#!/usr/bin/env python3
"""Triple-Reference Auditor

Validates that migrated repositories meet ecosystem governance standards:
seed.yaml state enum, IRF presence, valid remote origin, and GitHub issue
tracking link. Exits 0 on compliance, 1 with violation_report.md on failure.
"""

import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

VALID_STATES = {"LOCAL", "CANDIDATE", "PUBLIC_PROCESS", "GRADUATED"}
SEED_FILENAME = "seed.yaml"
IRF_FILENAME = "IRF.md"
ROLLBACK_MANIFEST = "rollback_manifest.json"

DEFAULT_SCAN_PATHS = [
    Path.home() / "Workspace",
    Path.home() / "Code",
    Path.home() / "Documents",
]


def check_seed_yaml(directory: Path) -> tuple[bool, str, dict[str, Any] | None]:
    """Validate seed.yaml exists and contains valid state."""
    seed_path = directory / SEED_FILENAME
    if not seed_path.exists():
        return False, "Missing seed.yaml", None

    try:
        with open(seed_path) as f:
            data = yaml.safe_load(f)
        if not isinstance(data, dict):
            return False, "seed.yaml is not a valid mapping", None

        state = data.get("state")
        if state not in VALID_STATES:
            return False, f"Invalid state in seed.yaml: {state!r}", data

        return True, "OK", data
    except (yaml.YAMLError, OSError) as e:
        return False, f"Cannot read seed.yaml: {e}", None


def check_irf(directory: Path) -> tuple[bool, str, str | None]:
    """Validate IRF.md exists and contains required fields."""
    irf_path = directory / IRF_FILENAME
    if not irf_path.exists():
        return False, "Missing IRF.md", None

    try:
        content = irf_path.read_text()
    except OSError as e:
        return False, f"Cannot read IRF.md: {e}", None

    required_fields = [
        "Repository:", "Governance State:", "GitHub Issue:",
        "Remote Origin:", "Triple-Reference Checksum:", "Last Verified:",
    ]
    missing = [f for f in required_fields if f not in content]
    if missing:
        return False, f"IRF.md missing fields: {', '.join(missing)}", content

    return True, "OK", content


def check_remote_origin(directory: Path) -> tuple[bool, str, str | None]:
    """Validate git remote origin is configured and accessible."""
    if not (directory / ".git").exists():
        return False, "Not a git repository", None

    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=str(directory),
            capture_output=True, text=True, timeout=10,
        )
        if result.returncode != 0:
            return False, "No remote origin configured", None

        url = result.stdout.strip()
        return True, "OK", url
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False, "git command not available", None


def check_github_issue(irf_content: str) -> tuple[bool, str]:
    """Validate GitHub issue URL in IRF resolves."""
    if not irf_content:
        return False, "No IRF content to check"

    url_match = re.search(r"https://github\.com/[^/]+/[^/]+/issues/\d+", irf_content)
    if not url_match:
        return False, "No GitHub issue URL found in IRF.md"

    url = url_match.group(0)
    if "<pending>" in url or "pending" in url.lower():
        return False, "GitHub issue URL is still pending"

    try:
        result = subprocess.run(
            ["gh", "issue", "view", url, "--json", "state"],
            capture_output=True, text=True, timeout=15,
        )
        if result.returncode == 0:
            return True, "OK"
        return False, f"GitHub issue not accessible: {result.stderr.strip()}"
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False, "gh CLI not available — cannot verify issue (manual check required)"


def check_state_consistency(seed_data: dict[str, Any] | None, irf_content: str | None) -> tuple[bool, str]:
    """Validate state in seed.yaml matches state in IRF.md."""
    if not seed_data or not irf_content:
        return False, "Cannot compare — missing seed or IRF"

    seed_state = seed_data.get("state", "")
    irf_state_match = re.search(r"Governance State:\s*(\S+)", irf_content)
    if not irf_state_match:
        return False, "Cannot extract state from IRF.md"

    irf_state = irf_state_match.group(1)
    if seed_state != irf_state:
        return False, f"State mismatch: seed.yaml={seed_state}, IRF.md={irf_state}"

    return True, "OK"


def check_checksum(directory: Path, irf_content: str | None) -> tuple[bool, str]:
    """Validate triple-reference checksum."""
    if not irf_content:
        return False, "No IRF content"

    checksum_match = re.search(r"Triple-Reference Checksum:\s*([a-f0-9]+)", irf_content)
    if not checksum_match:
        return False, "No checksum found in IRF.md"

    stored_checksum = checksum_match.group(1)
    if stored_checksum == "<pending>":
        return False, "Checksum is still pending"

    seed_path = directory / SEED_FILENAME
    seed_content = seed_path.read_text() if seed_path.exists() else ""

    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=str(directory),
            capture_output=True, text=True, timeout=10,
        )
        remote_url = result.stdout.strip() if result.returncode == 0 else ""
    except (subprocess.TimeoutExpired, FileNotFoundError):
        remote_url = ""

    computed = hashlib.sha256(
        (irf_content + seed_content + remote_url).encode()
    ).hexdigest()

    if stored_checksum != computed:
        return False, f"Checksum mismatch: stored={stored_checksum[:12]}..., computed={computed[:12]}..."

    return True, "OK"


def verify_repo(directory: Path) -> dict[str, Any]:
    """Run all checks on a single repository."""
    result: dict[str, Any] = {
        "path": str(directory),
        "name": directory.name,
        "checks": {},
        "passed": True,
        "violations": [],
    }

    checks = [
        ("seed_yaml", check_seed_yaml(directory)),
    ]

    seed_ok, seed_msg, seed_data = checks[0][1]
    result["checks"]["seed_yaml"] = {"passed": seed_ok, "message": seed_msg}
    if not seed_ok:
        result["passed"] = False
        result["violations"].append(f"seed.yaml: {seed_msg}")

    irf_ok, irf_msg, irf_content = check_irf(directory)
    result["checks"]["irf"] = {"passed": irf_ok, "message": irf_msg}
    if not irf_ok:
        result["passed"] = False
        result["violations"].append(f"IRF.md: {irf_msg}")

    remote_ok, remote_msg, remote_url = check_remote_origin(directory)
    result["checks"]["remote_origin"] = {"passed": remote_ok, "message": remote_msg}
    if not remote_ok:
        result["passed"] = False
        result["violations"].append(f"Remote origin: {remote_msg}")

    if irf_content:
        issue_ok, issue_msg = check_github_issue(irf_content)
        result["checks"]["github_issue"] = {"passed": issue_ok, "message": issue_msg}
        if not issue_ok:
            result["passed"] = False
            result["violations"].append(f"GitHub issue: {issue_msg}")

    state_ok, state_msg = check_state_consistency(seed_data, irf_content)
    result["checks"]["state_consistency"] = {"passed": state_ok, "message": state_msg}
    if not state_ok:
        result["passed"] = False
        result["violations"].append(f"State consistency: {state_msg}")

    checksum_ok, checksum_msg = check_checksum(directory, irf_content)
    result["checks"]["checksum"] = {"passed": checksum_ok, "message": checksum_msg}
    if not checksum_ok:
        result["passed"] = False
        result["violations"].append(f"Checksum: {checksum_msg}")

    return result


def find_migrated_repos() -> list[Path]:
    """Find repos from the most recent rollback manifest."""
    manifest_path = Path(ROLLBACK_MANIFEST)
    if not manifest_path.exists():
        return []

    try:
        manifest = json.loads(manifest_path.read_text())
    except (json.JSONDecodeError, OSError):
        return []

    targets = []
    for op in manifest.get("operations", []):
        inverse = op.get("inverse_action", "")
        if "git mv" in inverse or "mv " in inverse:
            parts = inverse.split()
            if len(parts) >= 3:
                targets.append(Path(parts[1]))

    return targets


def scan_ecosystem(roots: list[Path]) -> list[Path]:
    """Scan ecosystem roots for git repositories."""
    repos = []
    for root in roots:
        if not root.exists():
            continue
        for entry in root.rglob("*.git"):
            repo_dir = entry.parent
            if repo_dir not in repos:
                repos.append(repo_dir)
        for entry in root.iterdir():
            if entry.is_dir() and (entry / ".git").exists():
                repos.append(entry)
    return repos


def generate_violation_report(results: list[dict[str, Any]], ecosystem_wide: bool) -> str:
    """Generate markdown violation report."""
    timestamp = datetime.now(timezone.utc).isoformat()
    report = f"""# Triple-Reference Violation Report

Generated: {timestamp}
Scope: {'Ecosystem-wide' if ecosystem_wide else 'Migrated batch'}
Total Checked: {len(results)}
Passed: {sum(1 for r in results if r['passed'])}
Failed: {sum(1 for r in results if not r['passed'])}

---

"""

    for r in results:
        if not r["passed"]:
            report += f"## {r['name']} (`{r['path']}`)\n\n"
            for v in r["violations"]:
                report += f"- {v}\n"
            report += "\n"

    return report


def main():
    parser = argparse.ArgumentParser(description="Triple-Reference Auditor")
    parser.add_argument("--dir", type=Path, help="Verify a single repository/directory")
    parser.add_argument("--ecosystem-wide", action="store_true",
                        help="Scan all ecosystem roots")
    parser.add_argument("--manifest", type=Path,
                        help="Path to rollback_manifest.json (default: ./rollback_manifest.json)")
    parser.add_argument("--scan-paths", nargs="+", type=Path, default=DEFAULT_SCAN_PATHS,
                        help="Ecosystem roots to scan (with --ecosystem-wide)")
    args = parser.parse_args()

    results = []

    if args.dir:
        results.append(verify_repo(args.dir))
    elif args.ecosystem_wide:
        repos = scan_ecosystem(args.scan_paths)
        for repo in repos:
            results.append(verify_repo(repo))
    else:
        repos = find_migrated_repos()
        if not repos:
            print("No migrated repos found in rollback manifest.", file=sys.stderr)
            sys.exit(1)
        for repo in repos:
            if repo.exists():
                results.append(verify_repo(repo))

    passed = sum(1 for r in results if r["passed"])
    failed = sum(1 for r in results if not r["passed"])

    for r in results:
        status = "PASS" if r["passed"] else "FAIL"
        print(f"  [{status}] {r['name']}")
        if not r["passed"]:
            for v in r["violations"]:
                print(f"    - {v}")

    print(f"\nResults: {passed} passed, {failed} failed")

    if failed > 0:
        report_name = "ecosystem_violation_report.md" if args.ecosystem_wide else "violation_report.md"
        report = generate_violation_report(results, args.ecosystem_wide)
        Path(report_name).write_text(report)
        print(f"Violation report written to {report_name}")
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
