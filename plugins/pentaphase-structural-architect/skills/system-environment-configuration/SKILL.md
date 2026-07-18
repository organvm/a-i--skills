---
name: system-environment-configuration
description: Phase 3 of the pentaphase structural-overhaul protocol. Translates the taxonomy model into objective technical criteria, evaluates candidate mechanisms or frameworks, instantiates the chosen architecture, and programs validation rules. Use when the user invokes phase 3 of an overhaul, asks to "select a system" or "configure the environment", or has a taxonomy model and is ready to choose technology. Consumes phase-2-taxonomy-model.md; produces phase-3-environment-spec.md.
license: MIT
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
argument-hint: <working-directory containing phase-2 taxonomy model>
---

# Phase 3: System Selection & Environment Configuration

You are translating a conceptual taxonomy into a concrete environment. The
`phase-2-taxonomy-model.md` defines what the substrate IS conceptually; your job is to choose the
mechanism that will hold it, build the schema into that mechanism, and seat validation rules so
non-compliant items are rejected at entry.

## Preconditions

- `<working-dir>/substrate-context.md` exists.
- `<working-dir>/phase-1-landscape-report.md` exists (for scale and friction context).
- `<working-dir>/phase-2-taxonomy-model.md` exists and has passed gate 2.
- Read all three files in full before starting.

## Four work streams

### Stream 1 — Translate Requirements

Convert the taxonomy model into objective, measurable technical criteria. For each criterion:

- **Name** — short label
- **Source** — which part of phase 1 or phase 2 this comes from
- **Type** — capacity / performance / integration / governance / cost / operational
- **Threshold** — minimum acceptable value (be quantitative; "fast enough" is not a threshold)
- **Weight** — importance relative to other criteria (e.g., must-have / should-have / nice-to-have)

Example criterion families to consider:

- Scale (entity count, write rate, storage volume, growth projection)
- Query patterns (point lookups, range scans, joins, full-text, vector similarity)
- Concurrency (simultaneous readers/writers, lock contention tolerance)
- Schema flexibility (rigid vs. evolutive, online migration support)
- Access control granularity (row/column/field-level, attribute-based)
- Audit requirements (immutable log, point-in-time recovery, retention)
- Integration surface (API protocols, webhook support, CDC, MCP-compatibility)
- Operational fit (existing team skill, hosting model, total cost of ownership)
- Compliance posture (data residency, encryption-at-rest, certification)

Aim for 8–20 criteria. Fewer means you'll have a weak basis to decide on. More means you're
chasing decoration over deciding.

### Stream 2 — Evaluate Mechanisms

Benchmark candidate engines or frameworks against the criteria.

For each candidate (typically 2–4):

- **Name + version**
- **Category** — relational DB / document store / graph / object storage / CMS / repo /
  spreadsheet / specialized SaaS / custom
- **Scoring** — for each criterion, score "meets / partial / fails" with a brief rationale
- **Total cost** — license, infrastructure, operational time, integration cost
- **Lock-in risk** — how reversible is the choice if it turns out wrong
- **Existing-substrate compatibility** — how much of the current substrate can be migrated
  vs. rebuilt

Pick a winner. State the decision with reasoning. Be explicit about which criteria the winner
fails or only partially meets, and what the mitigation is for each.

### Stream 3 — Instantiate Architecture

Build the designed taxonomy directly into the chosen environment. Document the steps:

- **Schema declarations** — DDL, schema files, configuration manifests, etc., for every entity
  class and universal-schema attribute from phase 2
- **Relationship implementations** — foreign keys, link tables, embedded documents, graph edges,
  etc., one per phase-2 relationship
- **Access control implementations** — role/permission/policy declarations matching the phase-2
  access framework
- **Index strategy** — what indexes exist for what query patterns
- **Initial state** — empty / seeded with reference data / migrated subset

Provide actual code/config (not just descriptions). The artifact should be reproducible — a new
operator should be able to instantiate the environment from this section alone.

### Stream 4 — Enforce Validation Rules

Program automated checks to reject non-compliant items at entry. For each rule:

- **Layer** — schema-level (e.g., NOT NULL constraints) / application-level (validation
  functions) / pipeline-level (ingestion checks)
- **Trigger** — when the rule fires (on insert, on update, on read, on schedule)
- **Behavior** — reject / coerce / warn / quarantine
- **Failure handling** — what happens to rejected items (DLQ, error log, return to sender)

Cover at minimum:

- Universal-schema attribute validation (id format, ownership existence, status enum)
- Class-specific required attribute validation
- Relationship integrity (orphan detection, cardinality enforcement)
- Access tier consistency (no items written to a tier the writer can't access)

## Composing phase-3-environment-spec.md

Combine the four streams into a single file at `<working-dir>/phase-3-environment-spec.md`.
Structure:

```markdown
# Phase 3 — Environment Spec

**Substrate:** <name>
**Date:** YYYY-MM-DD
**Preconditions:** Read substrate-context.md, phase-1-landscape-report.md, phase-2-taxonomy-model.md
**Postconditions:** Ready for Phase 4 (systemic-ingestion-normalization)

## 1. Selection criteria

[full criteria table]

## 2. Mechanism evaluation

[per-candidate scoring + decision with rationale]

## 3. Instantiation

### 3.1 Schema declarations
[code/config]

### 3.2 Relationships
[code/config]

### 3.3 Access controls
[code/config]

### 3.4 Indexes
[code/config]

### 3.5 Initial state
[empty / seeded / migrated subset]

## 4. Validation rules

[per-rule cards organized by layer]

## 5. Open questions for Phase 4

[explicit list of decisions deferred to ingestion]
```

## Gate criteria (auditor will check)

The spec passes Phase 3's gate iff:

1. **At least 8 selection criteria** are defined with thresholds and weights.
2. **At least 2 candidate mechanisms** were evaluated, with explicit scoring against criteria.
3. **A winner is declared** with explicit rationale; criteria the winner fails or partially meets
   are named with mitigations.
4. **Schema declarations exist for every entity class** from phase 2 — no class is silently
   dropped during instantiation.
5. **Validation rules cover universal schema, class-specific requireds, relationship integrity,
   and access-tier consistency** at minimum.
6. **Open questions for Phase 4 section is present**.

## Anti-patterns

- **Don't choose the mechanism before the criteria.** Reverse-engineering criteria to fit a
  pre-chosen tool defeats the phase. If a mechanism is genuinely pre-decided, document why and
  short-circuit Stream 2 with a one-paragraph rationale.
- **Don't silently drop entity classes.** If a class doesn't fit the chosen mechanism cleanly,
  surface the friction — either redesign the taxonomy or pick a different mechanism.
- **Don't defer validation to "we'll add it later".** Validation rules ARE the entry gate; if
  they're absent at instantiation, ingestion will pollute the new environment with bad data.
- **Don't skip indexes.** Phase 1's value metrics (especially speed) imply specific query
  patterns. Index for them now, not after performance regressions.

## See also

- `references/selection-criteria.md` — common criterion families with example thresholds
- `references/validation-rules.md` — validation patterns by mechanism category
