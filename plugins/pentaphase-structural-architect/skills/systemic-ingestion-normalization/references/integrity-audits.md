# Integrity audit patterns

Run all of these. Skipping any one is how silent corruption survives the migration.

## 1. Count parity

The canonical first audit. Verifies that everything that should have moved did move.

```
legacy_in_scope - items_purged - items_quarantined = items_present_in_new_environment
```

If this equation does not hold (within a documented tolerance), ingestion is incomplete or
duplicated.

- **How to compute:** count from source, count from destination, subtract purges and
  quarantine reads from source-side.
- **Tolerance:** ideally 0. If non-zero, document why and verify the discrepancy is in the
  expected direction.

## 2. Identifier mapping completeness

For every legacy ID in scope, verify a corresponding new ID exists (or the legacy item is
documented as intentionally not migrated).

- **How to compute:** join legacy-id table to new-id mapping table on legacy-id; flag rows
  with no match.
- **Output:** list of un-mapped legacy IDs with reasons (intentionally dropped vs.
  unintentionally lost).

## 3. Schema conformance

For every entity in the new environment, verify it passes phase-3's validation rules.

- **How to compute:** run validation rules against every new entity (sampling is acceptable
  for very large substrates, but document the sample size and method).
- **Output:** counts of violations by rule. Zero is the goal.

## 4. Relationship integrity

For every relationship in the new environment, verify both endpoints exist.

- **How to compute:** for each foreign key, count rows where the referenced row does not
  exist. For each link table, count rows where either side is missing.
- **Output:** orphan counts by relationship. Zero is the goal.

## 5. Cardinality consistency

For each phase-2 relationship with declared cardinality, verify the actual data respects it.

- **How to compute:** for 1:1 relationships, count cases where one side has multiple
  entries on the other. For 1:N relationships, verify the "1" side has exactly 1.
- **Output:** violations by relationship type.

## 6. Sample fidelity

Take a random sample of N items. For each, deep-compare the new record against the legacy
record (after applying the documented enrichment transformations).

- **How to compute:** stratified random sample (across entity classes). For each, verify
  every attribute matches the expected post-enrichment value.
- **Sample size:** at minimum 100 items, or √(total_items) for very large substrates.
- **Output:** items with mismatches, with the specific attribute that diverged.

## 7. Stakeholder spot-check

Each operational role from `substrate-context.md` reviews a small sample (5–10 items
relevant to their role) and signs off that the items are usable in the new environment.

- **How to record:** include sign-off in `phase-4-ingestion-report.md` Section 4.2 with
  role, person (or anonymized), date, and any caveats raised.

## 8. Edge-case review

Every item that went through manual handling during enrichment is reviewed by a human (the
person who handled it OR an independent reviewer).

- **How to record:** a list in the audit section with item ID, what was special, who
  reviewed, sign-off.

## 9. Reverse query

A regression-style check: for a representative set of legacy queries, run the equivalent
query against the new environment and compare results.

- **Method:** select 10–20 queries that operational roles run regularly. Translate to the
  new environment. Run both. Diff results.
- **Output:** queries with diverging results, with explanation (intentional change vs.
  unintentional regression).

## 10. Performance baseline

Capture the value-metric baselines defined in phase 1, measured against the new
environment.

- **Method:** run the metric collection for one full cadence cycle (e.g., a week if metrics
  are weekly). Record values.
- **Output:** baseline table that becomes the input to phase 5's monitoring section.

## Verdict assembly

After running all audits, the verdict is:

- **PASS** — all 10 audits passed within tolerance; stakeholder sign-offs received.
- **PASS-WITH-CAVEATS** — minor discrepancies documented; user explicitly accepts; remediation
  items listed.
- **FAIL** — any of: count parity miss > tolerance; schema conformance < 100%; relationship
  orphans present; stakeholder rejection; reverse-query regression on critical queries.

A FAIL verdict triggers rollback to the pre-ingestion snapshot. The rollback procedure must
be documented in phase 3's environment spec — if it isn't, ingestion shouldn't have started.

## Documentation in the report

Phase 4's report Section 4 should include:

- A table of audits with audit name, method, result, and verdict.
- Stakeholder sign-offs as quoted lines.
- Edge-case reviews as a numbered list.
- The final verdict with reasoning.

If verdict is PASS-WITH-CAVEATS, list the caveats as inaugural entries for phase 5's
amendment log.
