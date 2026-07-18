# SOP-003: Governance Promotion Procedure

## Purpose
Standard procedure for promoting repositories through governance states from LOCAL → CANDIDATE → PUBLIC_PROCESS → GRADUATED.

## When
- Repo meets criteria for next governance state
- Weekly governance review
- On demand via `organvm governance promote <repo>`

## Governance State Machine

```
┌─────────────────────────────────────────────────────────────────────┐
│              GOVERNANCE STATE MACHINE                        │
│                                                             │
│   ┌──────────┐     ┌──────────────┐     ┌───────────────┐ │
│   │  LOCAL  │────▶│ CANDIDATE  │────▶│PUBLIC_PROCESS│──────┐ │
│   │ (Start) │     │            │     │             │      │ │
│   └──────────┘     └──────────────┘     └───────────────┘      │ │
│        ▲                                                  │ │
│        │                                                  ▼ │
│        │                 ┌──────────────┐     ┌───────────┐ │
│        └────────────────│  REJECTED    │◀────│GRADUATED │ │
│                       │ (rollback)   │     │(terminal)│ │
│                       └──────────────┘     └───────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Micro-Promotion Steps

### Phase 1: Pre-Promotion Assessment

```
┌─────────────────────────────────────────────────────────────────┐
│ PROMOTION MICRO-STEP 3.1.1: STATE ELIGIBILITY CHECK    │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: yaml + git status          TIMEOUT: 10s         │
│ PREREQUISITE: Current status, commit history,        │
│            tests passing, documentation complete   │
└─────────────────────────────────────────────────────────────────┘
```

#### Eligibility Matrix

| Current State | Target State | Prerequisites |
|--------------|-------------|---------------|
| LOCAL | CANDIDATE | ✓ seed.yaml complete<br>✓ CLAUDE.md complete<br>✓ Basic tests pass<br>✓ Initial commit exists |
| CANDIDATE | PUBLIC_PROCESS | ✓ Scale assigned<br>✓ Organ confirmed<br>✓ IRF assigned<br>✓ Unit tests pass<br>✓ Basic docs |
| PUBLIC_PROCESS | GRADUATED | ✓ All capabilities defined<br>✓ Primitives documented<br>✓ Entry points working<br>✓ Integration tests pass<br>✓ Full documentation |
| GRADUATED | - | Terminal state - no promotion |

---

```
┌─────────────────────────────────────────────────────────────────┐
│ PROMOTION MICRO-STEP 3.1.2: CRITERIA VALIDATION             │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: criteria_check             TIMEOUT: 5s            │
│ VALIDATE EACH CRITERIA:                               │
│   □ All required fields present                   │
│   □ Tests passing (unit + integration)              │
│   □ Documentation complete                        │
│   □ No critical issues in latest audit           │
│   □ Dependencies resolved                        │
└─────────────────────────────────────────────────────────────────┘
```

---

### Phase 2: Promotion Execution

```
┌─────────────────────────────────────────────────────────────────┐
│ PROMOTION MICRO-STEP 3.2.1: SEED.YAML UPDATE               │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: edit                      TIMEOUT: 5s              │
│ ACTION: Update status field in seed.yaml                │
└─────────────────────────────────────────────────────────────────┘
```

#### Step-by-Step

```bash
# 1. Navigate to repo
cd /Users/4jp/Workspace/organvm/<repo-name>

# 2. Read current seed.yaml
cat seed.yaml

# 3. Identify current status
current_status: $(grep "^status:" seed.yaml | cut -d' ' -f2)

# 4. Update to target status
sed -i '' "s/^status:.*/status: <TARGET_STATUS>/" seed.yaml

# 5. Commit with conventional commit
git add seed.yaml
git commit -m "chore: promote from $current_status to <TARGET_STATUS>"
```

---

```
┌─────────────────────────────────────────────────────────────────┐
│ PROMOTION MICRO-STEP 3.2.2: CLAUDE.md UPDATE                    │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: edit                      TIMEOUT: 5s              │
│ ACTION: Update status badge in CLAUDE.md                   │
└─────────────────────────────────────────────────────────────────┘
```

#### CLAUDE.md Status Badge Update

```markdown
# Previously
[![Status: LOCAL](https://img.shields.io/badge/Status-LOCAL-yellow)]

# Updated
[![Status: CANDIDATE](https://img.shields.io/badge/Status-CANDIDATE-blue)]
```

---

```
┌─────────────────────────────────────────────────────────────────┐
│ PROMOTION MICRO-STEP 3.2.3: DEPENDENCY UPDATE (if needed)     │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: yaml.edit                 TIMEOUT: 10s             │
│ ACTION: Add new dependencies (GRADUATED only)              │
└───────────────────────────���─────────────────────────────────────┘
```

#### For PUBLIC_PROCESS → GRADUATED

```yaml
# Add to seed.yaml
dependencies:
  - repo: organvm-IV-taxis/agent--claude-smith
    assets:
      - agents/*.md
  - repo: organvm-corpvs-testamentvm
    assets:
      - governance/*

entry_points:
  cli: src.cli:main
  pipeline: src.pipeline:execute
  api: src.api:app
```

---

### Phase 3: Post-Promotion Verification

```
┌─────────────────────────────────────────────────────────────────┐
│ PROMOTION MICRO-STEP 3.3.1: STATE VERIFICATION               │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: yaml.parse + git log        TIMEOUT: 10s            │
│ VERIFY: New status persisted correctly                │
│        Latest commit shows promotion              │
│        All validations pass                    │
└─────────────────────────────────────────────────────────────────┘
```

#### Verification Script

```bash
#!/bin/bash
# verify_promotion.sh

REPO="$1"
EXPECTED="$2"

echo "Verifying promotion for $REPO to $EXPECTED..."

# Check seed.yaml status
actual=$(grep "^status:" "$REPO/seed.yaml" | cut -d' ' -f2)
if [ "$actual" != "$EXPECTED" ]; then
    echo "FAILED: Expected $EXPECTED, got $actual"
    exit 1
fi

# Check commit message
last_commit=$(git -C "$REPO" log -1 --format=%s)
if ! echo "$last_commit" | grep -q "promote.*$EXPECTED"; then
    echo "WARNING: Commit message doesn't reflect promotion"
fi

echo "SUCCESS: Promotion verified to $EXPECTED"
```

---

```
┌─────────────────────────────────────────────────────────────────┐
│ PROMOTION MICRO-STEP 3.3.2: REGRESSION PREVENTION               │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: pytest + git status        TIMEOUT: 60s            │
│ RUN: Full test suite for affected repos              │
│ CHECK: No failures in dependency chain          │
└─────────────────────────────────────────────────────────────────┘
```

---

### Phase 4: Registry Notification

```
┌─────────────────────────────────────────────────────────────────┐
│ PROMOTION MICRO-STEP 3.4.1: REGISTRY UPDATE                 │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: mcp + git                  TIMEOUT: 15s           │
│ ACTION: Update global registry with new status            │
│        Notify dependent repos                      │
└─────────────────────────────────────────────────────────────────┘
```

#### Notification Schema

```python
def notify_promotion(repo: str, from_state: str, to_state: str):
    # Update organvm-IV-taxis/agent--claude-smith registry
    registry.update({
        "repo": repo,
        "status": to_state,
        "promoted_at": iso_timestamp(),
        "previous": from_state
    })
    
    # Find all repos depending on this repo
    dependents = find_dependents(repo)
    
    # Notify each dependent
    for dependent in dependents:
        notify(dependent, {
            "type": "dependency_promoted",
            "repo": repo,
            "from": from_state,
            "to": to_state
        })
```

---

## Promotion Criteria by State

### LOCAL → CANDIDATE

| Criterion | Test | Weight |
|-----------|------|--------|
| seed.yaml exists | `test -f seed.yaml` | REQUIRED |
| name field valid | `^name: .+$` | REQUIRED |
| description field | `^description: .+$` | REQUIRED |
| organ field valid | `^organ: [I-VII\|Meta]+$` | REQUIRED |
| status = LOCAL | `^status: LOCAL$` | REQUIRED |
| Initial commit | `git log -1` passes | REQUIRED |
| Git remote configured | `git remote -v` | REQUIRED |

### CANDIDATE → PUBLIC_PROCESS

| Criterion | Test | Weight |
|-----------|------|--------|
| All LOCAL criteria | All pass | REQUIRED |
| org field valid | `^org: organvm-.+$` | REQUIRED |
| scale field valid | `^scale: [σ_E\|σ_O\|σ_P]$` | REQUIRED |
| IRF assigned | `^IRF: IRF-[A-Z]{3}-[0-9]{3}$` | REQUIRED |
| Unit tests pass | `pytest --tb=short` | REQUIRED |
| Basic documentation | README.md ≥ 100 lines | REQUIRED |
| No critical audit issues | `organvm audit --severity=CRITICAL` | REQUIRED |

### PUBLIC_PROCESS → GRADUATED

| Criterion | Test | Weight |
|-----------|------|--------|
| All CANDIDATE criteria | All pass | REQUIRED |
| capabilities defined | `^capabilities:` present | REQUIRED |
| primitives defined | `^primitives:` present | REQUIRED |
| dependencies resolved | No unmet deps | REQUIRED |
| entry_points defined | `^entry_points:` present | REQUIRED |
| Integration tests | `pytest tests/integration` | REQUIRED |
| Full documentation | CLAUDE.md ≥ 200 lines | REQUIRED |
| Performance baseline | Benchmarks exist | REQUIRED |
| Security review | No CVEs | REQUIRED |

---

## Rollback Procedure

```
┌─────────────────────────────────────────────────────────────────┐
│ PROMOTION MICRO-STEP 3.5.1: STATE ROLLBACK                     │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: git revert + yaml.edit        TIMEOUT: 20s            │
│ TRIGGER: Test failure, documentation gap, security issue    │
│ CAUTION: Only to CANDIDATE, never from GRADUATED directly  │
└─────────────────────────────────────────────────────────────────┘
```

#### Rollback Command

```bash
# Rollback to previous state
organvm governance rollback <repo> --to=<previous_state>

# This will:
# 1. Revert seed.yaml status
# 2. Revert CLAUDE.md badge
# 3. Create rollback commit
# 4. Notify dependents
# 5. Log rollback reason
```

---

## Owner

- **Responsible**: Repo owner (specified in seed.yaml)
- **Approver**: organvm-vii-kerygma/system-governance-framework
- **Oversight**: organvm-corpvs-testamentvm

---

## Exceptions

### Cannot Rollback From GRADUATED
- Once GRADUATED, repo represents production contract
- Must go through full re-promotion process
- Requires explicit approval from governance org

### Emergency Rollback (Critical Security)
- Security issues can bypass normal process
- Requires immediate action with post-hoc documentation
- Must notify all dependents within 1 hour

---

## Audit Trail

All promotions logged in:

```bash
# Query promotion history
organvm governance history <repo>

# Output:
# ┌────────────┬─────────┬──────────────────┬────────────┐
# │ Timestamp │ From    │ To               │ Commit    │
# ├────────────┼─────────┼──────────────────┼────────────┤
# │ 2026-04-26│ LOCAL   │ CANDIDATE        │ abc123def │
# │ 2026-04-27│ CANDIDATE│ PUBLIC_PROCESS  │ ghi456jkl│
# │ 2026-04-28│ PUBLIC_ │ GRADUATED       │ mno789pqr│
# └────────────┴─────────┴──────────────────┴────────────┘
```

---

*Last updated: 2026-04-26*
*Version: 1.0.0*
*SOP-003: Governance Promotion Procedure*