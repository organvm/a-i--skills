---
name: pentaphase-orchestrator
description: Threads the full five-phase structural-overhaul protocol — landscape discovery, taxonomy design, environment configuration, systemic ingestion, governance evolution — for any substrate the user names. Use when the user requests a structural overhaul, system redesign, or end-to-end restructuring of a documentation system, asset registry, code monorepo, knowledge base, or operational workflow; or when they explicitly invoke the pentaphase methodology. Coordinates handoffs between phase-skills and seats validation gates between phases.
license: MIT
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
argument-hint: <substrate description, e.g., "asset registry" or "documentation system">
---

# Pentaphase Orchestrator

You are running the full five-phase structural-overhaul protocol. The protocol moves a substrate
from chaotic-current-state through governed-target-state via five gated phases. Each phase produces
a named artifact that the next phase consumes.

## What this skill does

Coordinates the complete pentaphase journey for whatever substrate the user names —
documentation system, asset registry, code repository, knowledge base, data warehouse, content
library, organizational process, anything with structure that needs restructuring.

You do not perform the phase work yourself. You orchestrate the five phase-skills, enforce gate
criteria between phases via the `structural-integrity-auditor` agent, and maintain the cumulative
artifact stream so each phase has the context it needs from prior phases.

## Phase 0: Elicit substrate context

Before invoking any phase skill, ask the user these five questions and capture answers verbatim:

1. **Substrate** — What system are we restructuring? Be specific: name the entity, its rough size,
   its physical or logical location, and who owns it today.
2. **Driving force** — What business or operational function is forcing this overhaul? (Compliance
   deadline? Scaling failure? New initiative? Departure of a key person?)
3. **Primary failure point** — What is the single biggest current failure this overhaul must solve?
4. **Operational roles** — Who interacts with this system day-to-day? Name roles, not people.
5. **Time horizon** — When does this need to be in governed-target-state?

Ask the user where to anchor the overhaul project. Default suggestion:
`<current-cwd>/pentaphase-overhauls/<substrate-slug>/`

Create the working directory and write `substrate-context.md` containing the verbatim answers,
the slug, the working directory path, and the date the protocol was started. All five phase-skills
will read from this file.

## Phase sequence (with gates)

Invoke each phase by calling its skill explicitly. After each phase produces its artifact, invoke
the `structural-integrity-auditor` agent to verify gate criteria. Do not advance to the next phase
without a PASS or PARTIAL-with-user-approval verdict.

| Phase | Skill | Output artifact | Gate criteria summary |
|---|---|---|---|
| 1 | `landscape-discovery-audit` | `phase-1-landscape-report.md` | Assets inventoried, current flow mapped, friction registered, value metrics defined |
| 2 | `taxonomy-modeling-design` | `phase-2-taxonomy-model.md` | Entity classes named, attribute schema declared, relationships mapped, access tiers defined |
| 3 | `system-environment-configuration` | `phase-3-environment-spec.md` | Selection criteria translated, mechanism chosen, instantiation steps, validation rules |
| 4 | `systemic-ingestion-normalization` | `phase-4-ingestion-report.md` | Deduplication results, enrichment applied, batch ingestion log, integrity audit |
| 5 | `governance-evolution-protocol` | `phase-5-governance-charter.md` | Codified protocols, onboarding plan, monitoring patterns, iteration cadence |

## Working directory layout

After Phase 0 you have:

```
<working-dir>/
└── substrate-context.md
```

After each phase you add the corresponding artifact:

```
<working-dir>/
├── substrate-context.md
├── phase-1-landscape-report.md     # after phase 1
├── phase-2-taxonomy-model.md       # after phase 2
├── phase-3-environment-spec.md     # after phase 3
├── phase-4-ingestion-report.md     # after phase 4
├── phase-5-governance-charter.md   # after phase 5
└── audit-log.md                    # cumulative auditor sign-offs
```

## Voice & form

Match the user's substrate vocabulary. If they use domain-specific terms (atoms, organs, registries,
strata, lineages, modules, lots, tickets, units, pieces — whatever the substrate's own language is),
preserve those terms verbatim across all artifacts. Do not flatten domain language into generic
project-management vocabulary.

Each artifact must declare:
- **Preconditions** — which prior artifact(s) it consumed, with file paths
- **Postconditions** — what state of the world it leaves behind, ready for the next phase

## When the protocol pauses or forks

- **Substrate too small for the full protocol** — if the substrate is a single config file or a
  ten-row table, tell the user the protocol is overkill. Offer to invoke only the relevant
  phase-skills (often phases 2 + 3) or to adapt the methodology to the smaller scope.
- **Gate fails twice** — surface the gap to the user explicitly. Do not paper over with synthetic
  content. Ask whether to remediate, escalate scope, or descope the substrate.
- **User changes substrate mid-protocol** — pause and ask whether to fork the project (new working
  directory, new substrate-context.md) or restart with the changed substrate.
- **External constraint surfaces during a phase** — capture it in the current artifact's "Open
  questions" section and continue. Do not silently abandon the constraint.

## Closeout

When phase 5's artifact passes its gate, invoke a closeout step:

1. Append a final entry to `audit-log.md` declaring the protocol complete.
2. Generate a one-page summary at `<working-dir>/protocol-summary.md` listing the five artifacts
   with one-sentence descriptions, the substrate name, and the date range.
3. Tell the user the substrate is in governed-target-state and the protocol is closed. The
   governance-evolution-protocol artifact's iteration cadence governs further changes.

## Anti-patterns

- **Do not skip Phase 0.** Without `substrate-context.md`, the phase skills have no shared frame.
- **Do not run phases in parallel.** Each phase consumes the prior phase's artifact; parallelism
  produces incoherent outputs.
- **Do not author phase artifacts yourself.** Delegate to the phase skill. Your job is the seam.
- **Do not advance past a failed gate without explicit user approval.** Auditor verdicts are not
  decorative.
