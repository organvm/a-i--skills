# Governance States

## Overview

The ecosystem enforces a 4-tier governance model. Every repository must declare its state in `seed.yaml` at the repository root. State transitions are explicit, auditable, and require triple-reference alignment.

## State Definitions

### LOCAL

- **Definition:** Repository exists on local disk only. No remote origin configured. No external tracking.
- **Requirements:**
  - `seed.yaml` with `state: LOCAL`
  - Valid `.git` directory (or marked for `INIT_LOCAL`)
- **Transition Path:** LOCAL → CANDIDATE when ready for ecosystem integration.

### CANDIDATE

- **Definition:** Repository has been reviewed and approved for ecosystem inclusion. Remote origin configured. Initial governance scaffolds in place.
- **Requirements:**
  - `seed.yaml` with `state: CANDIDATE`
  - Valid `git remote origin` URL
  - `IRF.md` (Identity Reference File) in repository root
  - GitHub tracking issue created
- **Transition Path:** CANDIDATE → PUBLIC_PROCESS when ready for public review.

### PUBLIC_PROCESS

- **Definition:** Repository is undergoing public governance review. Open to community contribution. Documentation and tests meet ecosystem standards.
- **Requirements:**
  - `seed.yaml` with `state: PUBLIC_PROCESS`
  - Complete triple-reference (IRF, remote, GitHub issue)
  - `CONTRIBUTING.md` present
  - CI/CD pipeline configured
  - All tests passing
- **Transition Path:** PUBLIC_PROCESS → GRADUATED when governance review passes.

### GRADUATED

- **Definition:** Repository has achieved full governance compliance. Production-ready. Subject to ongoing audit via `verify_triple_reference.py --ecosystem-wide`.
- **Requirements:**
  - `seed.yaml` with `state: GRADUATED`
  - Complete triple-reference, verified
  - `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md` present
  - CI/CD pipeline with branch protection
  - All tests passing, coverage threshold met
  - Regular audit schedule configured
- **Degradation Path:** GRADUATED → PUBLIC_PROCESS if violations found during audit.

## Transition Rules

1. **Forward transitions** require explicit human approval and a completed migration manifest.
2. **Backward transitions** (degradation) are triggered automatically by audit violations.
3. **No skipping states.** LOCAL → CANDIDATE → PUBLIC_PROCESS → GRADUATED is the only valid path.
4. **Every transition** must be recorded in the rollback manifest with a `pre_state_hash`.

## Governance Versioning

The `governance_version` field in `seed.yaml` tracks which version of the governance specification the repository conforms to. Current version: `1`.

When the governance specification is updated, repositories must be migrated to the new version through the standard migration process.
