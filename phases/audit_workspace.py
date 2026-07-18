#!/usr/bin/env python3
"""
Full Workspace Audit Script
Extracts metadata from all seed.yaml files in organvm/
"""
import os
import yaml
from pathlib import Path

ROOT = Path("/Users/4jp/Workspace/organvm")

def get_seed_data(repo_path):
    seed_file = repo_path / "seed.yaml"
    if not seed_file.exists():
        return None
    try:
        with open(seed_file) as f:
            return yaml.safe_load(f)
    except:
        return None

def get_claude_summary(repo_path):
    claude_file = repo_path / "CLAUDE.md"
    if claude_file.exists():
        return claude_file.stat().st_size
    return 0

results = []
for repo_dir in sorted(ROOT.iterdir()):
    if not repo_dir.is_dir():
        continue
    
    seed = get_seed_data(repo_dir)
    claude_size = get_claude_summary(repo_dir)
    
    name = repo_dir.name
    
    if seed:
        results.append({
            "name": name,
            "organ": seed.get("organ", "?"),
            "status": seed.get("status", "?"),
            "scale": seed.get("scale", "?"),
            "has_seed": True,
            "has_claude": claude_size > 0,
            "claude_size": claude_size
        })
    else:
        results.append({
            "name": name,
            "organ": "NO_SEED",
            "status": "NO_SEED",
            "scale": "NO_SEED",
            "has_seed": False,
            "has_claude": claude_size > 0,
            "claude_size": claude_size
        })

# Print CSV
print("name,organ,status,scale,has_seed,has_claude,claude_size")
for r in results:
    print(f"{r['name']},{r['organ']},{r['status']},{r['scale']},{r['has_seed']},{r['has_claude']},{r['claude_size']}")
