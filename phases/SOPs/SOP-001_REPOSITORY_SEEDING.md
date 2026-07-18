# SOP-001: Repository Seeding Procedure

## Purpose
Standard procedure for adding seed.yaml to new repos

## When
- New repo created in organvm ecosystem
- Repo missing seed.yaml found during audit

## Steps

### 1. Create seed.yaml
```bash
cd /Users/4jp/Workspace/organvm/[REPO_NAME]
$EDITOR seed.yaml
```

### 2. Required Fields
```yaml
name: [repo-name]
description: [one-line description]
organ: [I|II|III|IV|V|VI|VII|Meta]
org: organvm-[i-vii]-theoria
scale: [σ_E|σ_O|σ_P]
status: [LOCAL|CANDIDATE|PUBLIC_PROCESS|GRADUATED]

# Optional
dependencies:
  - repo: [other-repo]
    assets:
      - [asset-glob]

entry_points:
  cli: [module:function]
  pipeline: [module:function]

primitives:
  - [primitive-1]
  - [primitive-2]

capabilities:
  - [capability-name]: "[description]"

patches:
  - [patch-file.yaml]
```

### 3. Create CLAUDE.md
```bash
touch CLAUDE.md
$EDITOR CLAUDE.md
```

### 4. Required CLAUDE.md Sections
```markdown
# CLAUDE.md — [Repo Name]

## Identity
- **Repo:** organvm-[organ]/[name]
- **Organ:** [Organ Name]
- **Scale:** [σ_E|σ_O|σ_P]
- **IRF:** [IRF-XXX-NNN]
- **Design spec:** [link to spec doc]

## Architecture
[Architecture description]

## Commands
[CLI commands]

## Development
[Dev setup]

## Dependencies
[Dependencies]

## Key Constraints
[Constraints]

## Structure
[Directory structure]
```

### 5. Commit
```bash
git add seed.yaml CLAUDE.md
git commit -m "seed: add seed.yaml and CLAUDE.md"
```

---

## Verification
```bash
# Verify seed.yaml is valid YAML
python3 -c "import yaml; yaml.safe_load(open('seed.yaml'))"

# Verify CLAUDE.md exists and has content
wc -l CLAUDE.md  # Should be > 20 lines
```

---

## Owner
- **Responsible**: Repo owner (specified in seed.yaml)
- **Oversight**: organvm-corpvs-testamentvm

---

## Exceptions
- External contrib repos may have different structure
- Bench repos don't require seeding
- Archived repos marked NO_SEED

---

*Version: 1.0.0*
*Last updated: 2026-04-26*