---
name: governance-evolution-protocol
description: Phase 5 of the pentaphase structural-overhaul protocol. Codifies operational protocols, onboards the ecosystem of participants, programs behavior monitoring, and establishes an iteration cadence so the substrate evolves rather than calcifies. Use when the user invokes phase 5 of an overhaul, asks to "establish governance" or "lock in the protocols", or has completed ingestion and is ready to declare the substrate operational. Consumes phase-4-ingestion-report.md; produces phase-5-governance-charter.md, which closes the protocol.
license: MIT
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
argument-hint: <working-directory containing phase-4 ingestion report>
---

# Phase 5: Governance, Optimization & Evolution

You are sealing the substrate into an operational state with explicit governance. The
`phase-4-ingestion-report.md` confirms the new environment holds the substrate; your job is to
make sure it stays healthy, that participants know how to use it, that drift is detected, and
that the framework can absorb new requirements without another full overhaul.

This phase produces the artifact that closes the protocol. After phase 5 passes its gate, the
substrate is in governed-target-state.

## Preconditions

- `<working-dir>/substrate-context.md` exists.
- `<working-dir>/phase-1-landscape-report.md` exists.
- `<working-dir>/phase-2-taxonomy-model.md` exists.
- `<working-dir>/phase-3-environment-spec.md` exists.
- `<working-dir>/phase-4-ingestion-report.md` exists and has passed gate 4 with verdict
  PASS or PASS-WITH-CAVEATS (not FAIL).
- Read all five files in full before starting.

## Four work streams

### Stream 1 — Codify Protocols

Document strict operational rules for system upkeep and modification.

For each protocol:

- **Name** — short, memorable label
- **Scope** — what part of the substrate or its lifecycle this governs
- **Rule** — the imperative statement of the protocol
- **Why** — the reason the rule exists (what failure mode it prevents — link back to phase 1
  friction or phase 4 audit findings where applicable)
- **Enforcement mechanism** — how compliance is detected (automated check / review gate /
  retro)
- **Exception process** — who can grant exceptions and on what evidence

Cover at minimum these protocol families:

- **Entry rules** — how new items are admitted (validation, review, attribution)
- **Modification rules** — who can change what, under what review
- **Lifecycle rules** — when items transition between states (active → archived → deleted)
- **Schema evolution rules** — how attributes are added, deprecated, removed
- **Access change rules** — how visibility/modification tiers are altered
- **Audit rules** — what is logged, retained, surfaced for review

### Stream 2 — Onboard Ecosystem

Train all participants on ingestion rules and system navigation.

For each operational role from `substrate-context.md`:

- **Role**
- **What they do in the new environment** — their day-to-day surface
- **Required onboarding** — docs, walkthroughs, training sessions, paired sessions
- **First-week checklist** — concrete tasks that confirm they can operate
- **Escalation path** — who they contact when stuck

Produce or reference:

- A short orientation document (link or embed)
- A reference for common operations (cookbook of "how do I X")
- A glossary mapping legacy vocabulary to the new taxonomy (this prevents the most common form
  of post-migration confusion)

### Stream 3 — Analyze Behaviors

Monitor system performance, retrieval speed, and operational failures.

For each metric defined in phase 1's value metrics:

- **Metric name** (carry over from phase 1)
- **New baseline** — value as of phase 5 start
- **Target** (carry over from phase 1)
- **Current vs. target** — gap analysis
- **Monitoring instrument** — dashboard, query, alert, periodic report
- **Owner** — who watches this
- **Cadence** — daily / weekly / monthly review

Add new metrics that became relevant during ingestion or that the new environment makes
measurable for the first time. For each new metric, declare why it was added.

Define escalation thresholds — at what metric value does an incident-response trigger fire.

### Stream 4 — Iterate Framework

Refine the underlying structure periodically to absorb new organizational needs.

Define the iteration cadence:

- **Review cadence** — how often the governance charter itself is reviewed (quarterly is
  typical; annual is the floor for non-trivial substrates)
- **Triggers for unscheduled review** — events that force a review outside the cadence (new
  compliance requirement, sustained metric degradation, scope expansion, key role departure)
- **Amendment process** — how the charter or taxonomy is changed (proposal → review → ratify
  → publish), and who is in the loop
- **Versioning** — how charter and taxonomy versions are named and archived
- **Rollback policy** — how amendments are reversed if they cause regressions

Explicitly forbid silent change. Every change to the charter or the taxonomy is a versioned
amendment with reasoning attached.

## Composing phase-5-governance-charter.md

Combine the four streams into a single file at `<working-dir>/phase-5-governance-charter.md`.
Structure:

```markdown
# Phase 5 — Governance Charter

**Substrate:** <name>
**Date:** YYYY-MM-DD (initial)
**Charter version:** v1.0
**Preconditions:** Read substrate-context.md, phase-1, phase-2, phase-3, phase-4
**Postconditions:** Substrate is in governed-target-state; protocol is closed.

## 1. Operational protocols

[per-protocol cards organized by family]

## 2. Onboarding plan

[per-role sections with checklists]

## 3. Behavior monitoring

[per-metric definitions with current vs. target and monitoring instrument]

## 4. Iteration cadence

[review cadence, unscheduled-review triggers, amendment process, versioning, rollback]

## 5. Amendment log

[empty at v1.0; future amendments append here in dated entries]

## 6. Closure declaration

The substrate <name> is in governed-target-state as of YYYY-MM-DD. The protocol of
pentaphase-structural-architect v0.1.0 is closed. Further changes occur via the iteration
cadence in section 4.
```

## Gate criteria (auditor will check)

The charter passes Phase 5's gate iff:

1. **At least one protocol per family** is documented (entry, modification, lifecycle, schema
   evolution, access change, audit). Six minimum.
2. **Every operational role** named in `substrate-context.md` has an onboarding section with a
   first-week checklist.
3. **Every phase-1 value metric** has been carried into Phase 5's monitoring section with a new
   baseline.
4. **Iteration cadence is specified** with a review cadence, an amendment process, and a
   rollback policy.
5. **Closure declaration is present** and dates the substrate's transition to governed-target-state.
6. **Open questions section is NOT present** — Phase 5 closes open questions; if any remain,
   they become inaugural amendment-log entries instead.

## Anti-patterns

- **Don't write protocols nobody will read.** If a protocol is more than 3 sentences, it is
  unlikely to be enforced. Compress to the rule, the why, and the enforcement.
- **Don't leave onboarding to "self-serve documentation".** Every role needs a named human
  contact for the first week of operation. Documentation is the long tail; the contact is the
  foundation.
- **Don't define monitoring without an owner.** A metric without an owner is a metric without a
  watcher.
- **Don't make the charter unamendable.** A charter that can't change is a charter that ages
  badly. Iteration cadence is non-optional.
- **Don't declare closure if integrity audit was FAIL.** Phase 4's gate already prevents this,
  but verify explicitly before writing the closure declaration.

## See also

- `references/iteration-cadence-patterns.md` — review-cadence patterns with examples
