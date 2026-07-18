---
name: systemic-ingestion-normalization
description: Phase 4 of the pentaphase structural-overhaul protocol. Purges redundancies, enriches and aligns legacy entities to the new schema, executes phased ingestion into the new environment, and audits integrity. Use when the user invokes phase 4 of an overhaul, asks to "migrate the data" or "ingest into the new system", or has a configured environment ready to accept legacy entities. Consumes phase-3-environment-spec.md; produces phase-4-ingestion-report.md.
license: MIT
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
argument-hint: <working-directory containing phase-3 environment spec>
---

# Phase 4: Normalization & Systemic Ingestion

You are migrating legacy entities into the configured environment. The
`phase-3-environment-spec.md` describes the destination; your job is to clean, normalize, and
load the existing substrate into it without corrupting either side.

## Preconditions

- `<working-dir>/substrate-context.md` exists.
- `<working-dir>/phase-1-landscape-report.md` exists (for the source-side asset inventory).
- `<working-dir>/phase-2-taxonomy-model.md` exists (for the target schema).
- `<working-dir>/phase-3-environment-spec.md` exists and has passed gate 3.
- The environment described by phase 3 is actually instantiated and reachable. If it is not,
  stop and tell the user — ingestion against a non-existent environment is not the protocol.
- Read all four files in full before starting.

## Four work streams

### Stream 1 — Purge Redundancies

Filter out duplicate, obsolete, or non-standard system inputs from the legacy substrate.

For each pass:

- **Pass name** — what's being filtered (exact duplicates / fuzzy duplicates / obsolete /
  non-standard / corrupted)
- **Detection method** — how items are identified (hash equality, fuzzy match with threshold,
  age beyond N days, schema-conformance check, manual review)
- **Action** — delete / archive / quarantine / merge / preserve-with-flag
- **Counts** — items examined, items matched, items actioned
- **Sample** — 3–5 example items that were actioned, for spot-checking

Always preserve a record of what was purged. Append-only purge logs prevent unrecoverable
mistakes; never hard-delete without an archive.

### Stream 2 — Enrich & Align

Apply the mandatory attributes to all legacy entities before migration.

For each enrichment pass:

- **Target attribute** — which phase-2 attribute is being filled
- **Source** — where the value comes from (existing legacy field, derivation, lookup,
  default, manual)
- **Coverage** — what fraction of legacy entities can be enriched automatically
- **Manual queue** — what fraction needs human input, and how it's surfaced

Critical enrichments that almost always need attention:

- Universal-schema attributes added in phase 2 that didn't exist in legacy (e.g., `owner` if
  the legacy substrate didn't track ownership)
- Status/state normalization (legacy free-text status → new enum)
- Identifier reconciliation (legacy IDs → new id space, with a mapping table preserved)
- Relationship rebuilding (legacy implicit links → explicit relationships)

For every enrichment that touches data, retain a "before/after" record so the audit can verify
no value was changed silently.

### Stream 3 — Execute Ingestion

Transfer items into the new environment using structured, phased batches.

Phase the ingestion explicitly:

- **Phase 4a — Pilot batch**: small, representative slice (1–5% of items). Run through the full
  validation pipeline. Inspect for errors. Adjust enrichment / validation rules if needed.
- **Phase 4b — Bulk batches**: remainder, in batches sized to fit memory and to allow rollback
  on per-batch errors. Document batch size and concurrency.
- **Phase 4c — Tail / edge cases**: items that failed earlier batches and were surfaced for
  manual handling.

For each batch, log:

- Batch ID
- Item count attempted
- Item count succeeded
- Item count rejected (with rejection reason categories)
- Wall-clock duration
- Any rollback or remediation taken

Ingestion runs MUST be idempotent — if a batch fails halfway, re-running it must not duplicate
already-ingested items.

### Stream 4 — Audit Integrity

Run automated and manual checks to ensure zero data corruption.

Automated checks:

- **Count parity** — legacy items in scope vs. new items present (allowing for purge counts)
- **Identifier mapping completeness** — every legacy ID maps to a new ID (or is documented as
  intentionally dropped)
- **Schema conformance** — every new entity passes phase-3 validation rules
- **Relationship integrity** — every relationship has both endpoints present; no orphans
- **Sample fidelity** — random sample of N items, deep-compared between legacy and new

Manual checks:

- **Stakeholder spot-check** — operational role(s) named in `substrate-context.md` review a
  small sample and confirm fidelity
- **Edge-case review** — any item that required special handling during enrichment is reviewed
  by a human

Integrity audit must produce a verdict: PASS / PASS-WITH-CAVEATS / FAIL. A FAIL verdict means
ingestion is rolled back to the pre-ingestion snapshot.

## Composing phase-4-ingestion-report.md

Combine the four streams into a single file at `<working-dir>/phase-4-ingestion-report.md`.
Structure:

```markdown
# Phase 4 — Ingestion Report

**Substrate:** <name>
**Date range:** YYYY-MM-DD to YYYY-MM-DD
**Preconditions:** Read substrate-context.md, phase-1, phase-2, phase-3
**Postconditions:** Ready for Phase 5 (governance-evolution-protocol)

## 1. Purge passes

[per-pass summaries with counts]

## 2. Enrichment passes

[per-pass summaries with coverage]

## 3. Ingestion batches

### 3.1 Pilot
[batch log]

### 3.2 Bulk
[per-batch logs]

### 3.3 Tail / edge cases
[per-item or per-category log]

## 4. Integrity audit

### 4.1 Automated checks
[results table]

### 4.2 Manual checks
[stakeholder sign-offs, edge-case reviews]

### 4.3 Verdict
PASS | PASS-WITH-CAVEATS | FAIL — with reasoning

## 5. Open questions for Phase 5

[explicit list of operational concerns or governance gaps surfaced during ingestion]
```

## Gate criteria (auditor will check)

The report passes Phase 4's gate iff:

1. **At least one purge pass** is documented (even if zero items matched — the pass establishes
   that the question was asked).
2. **Universal-schema attributes are enriched on 100% of ingested entities** — no entity
   missing a required field.
3. **Pilot batch was run before bulk batches** — explicit, in that order, with errors from
   the pilot triggering enrichment/validation adjustments before bulk.
4. **Count parity holds** — legacy_in_scope − purged = new_present (within a documented
   tolerance, ideally 0).
5. **Integrity audit verdict is present and is PASS or PASS-WITH-CAVEATS** — a FAIL verdict
   means ingestion did not complete; the report should not exist in its final form yet.
6. **Open questions for Phase 5 section is present**.

## Anti-patterns

- **Don't skip the pilot batch.** Bulk-loading without piloting is how silent corruption
  enters the new environment at scale.
- **Don't enrich destructively.** Every enrichment must be reversible from the audit log; if
  you can't reverse it, you can't safely re-run it.
- **Don't silently drop items that fail validation.** They go to a quarantine queue with a
  reason code, not /dev/null.
- **Don't declare PASS before stakeholder spot-check.** Automated checks verify schema
  conformance; humans verify semantic fidelity. Both are required.

## See also

- `references/deduplication-strategies.md` — exact, fuzzy, and semantic duplicate detection
- `references/integrity-audits.md` — count parity, mapping completeness, sample fidelity patterns
