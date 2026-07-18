---
name: landscape-discovery-audit
description: Phase 1 of the pentaphase structural-overhaul protocol. Inventories assets, maps current flow, identifies friction, and defines value metrics for any substrate. Use when the user invokes phase 1 of an overhaul, requests a baseline audit, asks to "discover the landscape" of a system, or wants to understand current state before redesigning. Produces phase-1-landscape-report.md.
license: MIT
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
argument-hint: <working-directory containing substrate-context.md>
---

# Phase 1: Landscape Discovery & Baseline Audit

You are conducting the discovery phase of a structural overhaul. The `substrate-context.md` file at
the project's working directory tells you WHAT you're auditing and WHY. Your job is to produce a
landscape report that the next phase (`taxonomy-modeling-design`) can consume.

## Preconditions

- Working directory exists and contains `substrate-context.md`.
- If `substrate-context.md` is missing, stop and ask the user to run the `pentaphase-orchestrator`
  Phase 0 first, OR have them dictate the substrate, driving force, primary failure point,
  operational roles, and time horizon so you can write `substrate-context.md` yourself.

Read `substrate-context.md` in full before starting any work stream.

## Four work streams

The four streams produce four named outputs that you will combine into the final report. Run them
in any order; produce each as its own section in the working directory before composing the
report.

### Stream 1 — Inventory Assets

Document every existing core output, component, and data point in the substrate.

For each asset, capture:

| Field | Required | Notes |
|---|---|---|
| Name | yes | Canonical name in the system, plus any aliases |
| Location | yes | Absolute path, URL, registry id, or coordinates |
| Owner | yes | Person, team, or role responsible |
| State | yes | active / archived / deprecated / orphaned / unknown |
| Last touched | yes | ISO date if discoverable; otherwise "unknown" |
| Size / scale | yes | rows, files, bytes, or domain-native unit |
| Dependencies | optional | Other assets this one depends on |
| Notes | optional | Anything anomalous worth flagging |

Output as a markdown table or sectioned list. Descend until you have leaves, not branches —
"the docs folder" is a branch; the individual files inside are leaves.

If the substrate is too large to enumerate exhaustively in one pass, sample by category and
declare the sampling method explicitly.

### Stream 2 — Map Current Flow

Track how items travel from creation to final archive. For each distinct flow:

- **Trigger** — what initiates the flow (event, schedule, human action)
- **Stages** — ordered list of states the item passes through
- **Actors** — who or what advances each stage (human role, automation, hybrid)
- **Handoffs** — where state passes between actors (these are the friction-prone points)
- **Termination** — how the flow ends (archive, deletion, escalation, abandonment)
- **Volume** — items per unit time (or backlog depth if flow is irregular)

If multiple distinct flows exist, document each separately. Number them. Use prose, ASCII
diagrams, or sequence lists — whichever is clearest.

### Stream 3 — Identify Friction

Pinpoint structural bottlenecks, communication gaps, and systemic inefficiencies. For each:

- **Friction point** — specific, named, located in the flow
- **Type** — bottleneck / gap / inefficiency / drift / silo / coordination cost / quality leak
- **Frequency** — how often it bites (every event, weekly, monthly, sporadic)
- **Impact** — cost in time, money, quality, morale, opportunity
- **Root cause hypothesis** — your best read on the underlying mechanism

Resist generic complaints. "Slow process" is not a friction point. "Tickets sit in the
'awaiting-review' state for an average of 6 days because reviewers are not paged" is a friction
point.

### Stream 4 — Define Value Metrics

Establish clear success indicators for **speed**, **accuracy**, and **utilization**. At minimum,
one metric per dimension. For each:

- **Name**
- **Definition** — what is measured, how, with what tool
- **Current baseline** — current value with measurement method and date
- **Target** — where we need to be after the overhaul
- **Cadence** — how often it's measured
- **Threshold** — value at which an alert/escalation fires (optional but recommended)

Metrics must be measurable. "Better UX" is not a metric. "Time from ticket creation to first
response, p50, in minutes" is.

## Composing phase-1-landscape-report.md

Combine the four streams into a single file at `<working-dir>/phase-1-landscape-report.md`.
Structure:

```markdown
# Phase 1 — Landscape Report

**Substrate:** <name from substrate-context.md>
**Date:** YYYY-MM-DD
**Preconditions:** Read substrate-context.md (path)
**Postconditions:** Ready for Phase 2 (taxonomy-modeling-design)

## 1. Executive summary

3–5 sentences on the substrate's current shape and biggest pain.

## 2. Assets inventory

[full table or sectioned list]

## 3. Current flow map

[per-flow sections]

## 4. Friction register

[per-friction-point list]

## 5. Value metrics

[per-metric definitions with baselines]

## 6. Open questions for Phase 2

[explicit list of gaps, ambiguities, or decisions deferred to taxonomy design]
```

## Gate criteria (auditor will check)

The report passes Phase 1's gate iff:

1. **Asset coverage ≥ 80%** — no major asset class missing. If sampling was used, the sampling
   method is declared.
2. **At least one flow mapped end-to-end** — from trigger to termination, with stages, actors,
   and handoffs.
3. **Friction register has ≥ 3 named points** — each with a type, a frequency, an impact, and a
   root cause hypothesis.
4. **Value metrics cover speed AND accuracy dimensions** — each with a current baseline and a
   target. Utilization is encouraged but not required.
5. **Open questions for Phase 2 section is present** — even if empty (an explicit "no open
   questions" is acceptable; an absent section is not).

If you cannot meet a gate criterion, flag the gap explicitly in the "Open questions" section
and surface it to the user before invoking the next phase.

## Anti-patterns

- **Don't invent assets you can't verify.** If something might exist, mark it "suspected — needs
  confirmation" rather than asserting it.
- **Don't smooth over confusion.** If two roles claim ownership of the same asset, document the
  conflict — that IS the friction point.
- **Don't skip flow mapping by saying "it's complicated".** If it's complicated, that's a Phase 2
  problem to solve. Map what's there.
- **Don't propose solutions in this phase.** Solutions belong in Phase 2 (taxonomy) or Phase 3
  (environment). Phase 1 is descriptive only.

## See also

- `references/inventory-templates.md` — sample inventory tables for common substrate types
- `references/friction-patterns.md` — common friction archetypes with examples
- `references/value-metrics-frameworks.md` — speed/accuracy/utilization metric libraries
