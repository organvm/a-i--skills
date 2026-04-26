# SOP-006: Phase Transition Procedure

## Purpose
Standard procedure for transitioning repositories through multiverse phases (1-1A through 4-4B), the 10-path architecture for repo development lifecycle.

## When
- Starting new repo development
- Phase gate review
- On demand via `organvm phase transition <repo>`

---

## Phase Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│              MULTIVERSE PHASE SYSTEM                            │
│                                                             │
│    PHASE 1 (Content)                                         │
│    ├─ 1A: Landing Page                                      │
│    ├─ 1B: Sales/Technical Split                            │
│    └─ 1C: Pitch Deck                                        │
│                                                             │
│    PHASE 2 (Architecture)                                    │
│    ├─ 2A: Full Repository Architecture                     │
│    └─ 2B: Natural Center Bootstrap                          │
│                                                             │
│    PHASE 3 (Execution)                                       │
│    ├─ 3A: Fullstack Production                             │
│    └─ 3B: Lean MVP                                         │
│                                                             │
│    PHASE 4 (Depth)                                          │
│    ├─ 4A: Operator Grade                                   │
│    └─ 4B: Dissertation Grade                              │
│                                                             │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Phase Micro-Transitions

### Phase 1: Content Development

```
┌─────────────────────────────────────────────────────────────────┐
│ PHASE TRANSITION MICRO-STEP 6.1.1: 1A → 1B                    │
├─────────────────────────────────────────────────────────────────┤
│ SOURCE: phase1-1A-landing-page                               │
│ TARGET: phase1-1B-sales-technical-split                     │
│ TRIGGER: Single-page content complete                       │
└─────────────────────────────────────────────────────────────────┘
```

#### 1A → 1B Criteria

| Criterion | Evidence |
|------------|-----------|
| Landing page exists | `landing-page/index.html` |
| Content wireframes | 3+ wireframes in Figma |
| User personas defined | `content/personas.md` |
| Value proposition drafted | `content/value-prop.md` |
| Phase review passed | Gate 1A approval |

---

```
┌─────────────────────────────────────────────────────────────────┐
│ PHASE TRANSITION MICRO-STEP 6.1.2: 1B → 1C                    │
├──────────────────────────────��──────────────────────────────────┤
│ SOURCE: phase1-1B-sales-technical-split                     │
│ TARGET: phase1-1C-pitch-deck                              │
│ TRIGGER: Sales/tech split content complete                │
└─────────────────────────────────────────────────────────────────┘
```

#### 1B → 1C Criteria

| Criterion | Evidence |
|------------|-----------|
| Sales content | `content/sales-deck.md` |
| Technical content | `content/technical-spec.md` |
| Audience analysis | `content/audience.md` |
| Messaging hierarchy | `content/messaging.md` |
| Phase review passed | Gate 1B approval |

---

### Phase 2: Architecture Development

```
┌─────────────────────────────────────────────────────────────────┐
│ PHASE TRANSITION MICRO-STEP 6.2.1: 1C → 2A                    │
├─────────────────────────────────────────────────────────────────┤
│ SOURCE: phase1-1C-pitch-deck                              │
│ TARGET: phase2-2A-repo-architecture                        │
│ TRIGGER: Pitch deck approved, dev starts                   │
└─────────────────────────────────────────────────────────────────┘
```

#### 1C → 2A Criteria

| Criterion | Evidence |
|------------|-----------|
| Pitch approved | Stakeholder sign-off |
| Architecture doc | `docs/architecture.md` |
| Tech stack selected | `docs/technology.md` |
| Repo structure defined | `.github/templates/` |
| CI/CD pipeline | `.github/workflows/` |
| Phase review passed | Gate 2A approval |

---

```
┌─────────────────────────────────────────────────────────────────┐
│ PHASE TRANSITION MICRO-STEP 6.2.2: 2A → 2B                    │
├─────────────────────────────────────────────────────────────────┤
│ SOURCE: phase2-2A-repo-architecture                        │
│ TARGET: phase2-2B-natural-center-bootstrap               │
│ TRIGGER: Core architecture stable                      │
└─────────────────────────────────────────────────────────────────┘
```

#### 2A → 2B Criteria

| Criterion | Evidence |
|------------|-----------|
| Core services | `src/services/` implemented |
| API contracts | `docs/api-contracts.md` |
| Database schema | `schema/` defined |
| Auth flow | `src/auth/` working |
| Phase review passed | Gate 2B approval |

---

### Phase 3: Execution

```
┌─────────────────────────────────────────────────────────────────┐
│ PHASE TRANSITION MICRO-STEP 6.3.1: 2B → 3A                    │
├─────────────────────────────────────────────────────────────────┤
│ SOURCE: phase2-2B-natural-center-bootstrap               │
│ TARGET: phase3-3A-fullstack-production                    │
│ TRIGGER: Bootstrap stable, ready for production          │
└─────────────────────────────────────────────────────────────────┘
```

#### 2B → 3A Criteria

| Criterion | Evidence |
|------------|-----------|
| All endpoints | `src/api/` all implemented |
| Database migrations | `migrations/` ready |
| Tests passing | `pytest` 80%+ coverage |
| Security audit | No critical issues |
| Performance baseline | Benchmarks exist |
| Phase review passed | Gate 3A approval |

---

```
┌─────────────────────────────────────────────────────────────────┐
│ PHASE TRANSITION MICRO-STEP 6.3.2: 2B → 3B                    │
├─────────────────────────────────────────────────────────────────┤
│ SOURCE: phase2-2B-natural-center-bootstrap               │
│ TARGET: phase3-3B-lean-mvp                              │
│ TRIGGER: MVP scope defined, quick win needed              │
└─────────────────────────────────────────────────────────────────┘
```

#### 2B → 3B (MVP Path) Criteria

| Criterion | Evidence |
|------------|-----------|
| MVP features | `docs/mvp-features.md` |
| Core 3 features | Implementation started |
| Quick feedback loop | User testing plan |
| Phase review passed | Gate 3B approval |

---

### Phase 4: Depth

```
┌─────────────────────────────────────────────────────────────────┐
│ PHASE TRANSITION MICRO-STEP 6.4.1: 3A/B → 4A               │
├─────────────────────────────────────────────────────────────────┤
│ SOURCE: phase3-3A-fullstack-production OR 3B-lean-mvp      │
│ TARGET: phase4-4A-operator-grade                         │
│ TRIGGER: Production stable, operator needs                │
└─────────────────────────────────────────────────────────────────┘
```

#### 3A/B → 4A Criteria

| Criterion | Evidence |
|------------|-----------|
| Production deployed | Live URL exists |
| Operator docs | `docs/operators.md` |
| Runbooks | `docs/runbooks.md` |
| Monitoring | Dashboard configured |
| Alerting | PagerDuty/Slack configured |
| Phase review passed | Gate 4A approval |

---

```
┌─────────────────────────────────────────────────────────────────┐
│ PHASE TRANSITION MICRO-STEP 6.4.2: 4A → 4B               │
├─────────────────────────────────────────────────────────────────┤
│ SOURCE: phase4-4A-operator-grade                         │
│ TARGET: phase4-4B-dissertation-grade                   │
│ TRIGGER: Research/academic needs                        │
└─────────────────────────────────────────────────────────────────┘
```

#### 4A → 4B Criteria

| Criterion | Evidence |
|------------|-----------|
| Operator feedback | Issues addressed |
| Research outline | `docs/research-outline.md` |
| Academic sources | Bibliography complete |
| Methodology | `docs/methodology.md` |
| Phase review passed | Gate 4B approval |

---

## Transition Execution

```
┌─────────────────────────────────────────────────────────────────┐
│ TRANSITION MICRO-STEP 6.5.1: PHASE MIGRATION                     │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: git + filesystem             TIMEOUT: 30s              │
│ ACTIONS:                                                   │
│   1. Archive current phase docs                            │
│   2. Create new phase READMEs                              │
│   3. Update seed.yaml phase field                          │
│   4. Commit with phase tag                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### Transition Script

```bash
#!/bin/bash
# transition.sh

SOURCE="$1"
TARGET="$2"
REPO="$3"

echo "Transitioning $REPO: $SOURCE → $TARGET"

# 1. Archive current phase
mkdir -p "$REPO/docs/phases/"
cp -r "$REPO/docs/phase*" "$REPO/docs/phases/archive/"

# 2. Copy new phase template
cp -r "phases/$TARGET" "$REPO/docs/"

# 3. Update seed.yaml
yq -i ".phase = '$TARGET'" "$REPO/seed.yaml"

# 4. Commit
git -C "$REPO" add .
git -C "$REPO" commit -m "chore: phase transition $SOURCE → $TARGET"
```

---

## Gate Review Checklist

```
┌─────────────────────────────────────────────────────────────────┐
│                   GATE REVIEW CHECKLIST                     │
├─────────────────────────────────────────────────────────────────┤
│                                                             │
│ □ All criteria evidence present                              │
│ □ Code review passed (if applicable)                       │
│ □ Documentation reviewed                                   │
│ □ Stakeholder sign-off obtained                           │
│ □ No blocking issues                                     │
│ □ Test coverage sufficient                              │
│ □ Security review passed (Phase 3+)                    │
│ □ Performance reviewed (Phase 3+)                       │
│                                                             │
│ DECISION: APPROVE | REJECT | CONDITIONAL                   │
│                                                             │
└─────────────────────────────────────────────────────────────────┘
```

---

## Phase Decision Matrix

```
┌─────────────────────────────────────────────────────────────────────┐
│              PHASE DECISION BY USE CASE                       │
├─────────────────────────────────┬───────────────────────────┤
│ USE CASE                        │ RECOMMENDED PATH           │
├─────────────────────────────────┼───────────────────────────┤
│ Landing page for product         │ 1A → 1B                │
│ Investor pitch                  │ 1A → 1B → 1C            │
│ Full SaaS product               │ 1A → 1B → 2A → 2B → 3A │
│ Internal tool                  │ 1A → 2A → 2B → 3B → 4A  │
│ Research project               │ 1A → 1C → 2A → 2B → 4B  │
│ Quick prototype                │ 1A → 2A → 3B             │
│ Library/SDK                   │ 1A → 2A → 2B → 3A → 4A  │
└─────────────────────────────────┴───────────────────────────┘
```

---

## Owner

- **Responsible**: Repo owner + organvm-IV-taxis/agent--claude-smith
- **Approver**: Phase gate reviewer
- **Oversight**: organvm-vii-kerygma/system-governance-framework

---

*Last updated: 2026-04-26*
*Version: 1.0.0*
*SOP-006: Phase Transition Procedure*