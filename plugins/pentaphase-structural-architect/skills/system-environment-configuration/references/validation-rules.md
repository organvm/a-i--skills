# Validation rule patterns

Validation lives at three layers. Use all three; each catches different failure modes.

## Layer 1 — Schema-level (storage layer)

These rules are enforced by the mechanism itself; they cannot be bypassed by application bugs.

- **Type constraints** — column types, required/optional, length limits.
- **NOT NULL constraints** — every required attribute from phase 2 has NOT NULL on the schema.
- **CHECK constraints** — value ranges, regex patterns for IDs, enum membership.
- **UNIQUE constraints** — natural keys, slugs, externally-meaningful identifiers.
- **FOREIGN KEY constraints** — every relationship from phase 2 enforced at the schema level
  with appropriate ON DELETE / ON UPDATE behavior (matching phase-2's lifecycle coupling).

Schema-level rules are the strongest. Use them aggressively where the mechanism supports them.

## Layer 2 — Application-level (validation functions)

These run on every write attempt before the schema-level rules see the data. They catch what
schema rules can't express — semantic constraints, multi-field invariants, external lookups.

- **Multi-field invariants** — e.g., `end_date >= start_date`, `total = sum(line_items)`.
- **External existence checks** — e.g., owner must exist in the user registry, parent must
  exist in the taxonomy.
- **Permission preconditions** — writer must have permission to write to the target tier.
- **Workflow state guards** — transitions must follow the declared state machine (e.g.,
  active → archived is allowed; deleted → active is not).
- **Idempotency keys** — for mutating endpoints, reject duplicate operations within a
  configurable window.

Implement application validation as composable functions, not inline ifs. This makes them
testable and reusable across endpoints.

## Layer 3 — Pipeline-level (ingestion checks)

These run on bulk loads and CDC streams. They catch what application rules can't see — global
patterns, distributional anomalies, drift over time.

- **Schema-conformance audit** — fraction of records that pass schema validation.
- **Reference-integrity audit** — fraction of foreign-key references that resolve.
- **Distributional checks** — flag if attribute distributions diverge from established
  baselines (e.g., a 10× spike in null rate, an unexpected new enum value).
- **Volume checks** — flag if batch sizes deviate from expected ranges (sudden spikes/drops).
- **Source-system reconciliation** — for CDC, periodic count parity between source and
  destination.

Pipeline-level checks emit metrics, not exceptions. They feed phase-5's monitoring.

## Behavior on failure

For each rule, declare what happens when it fails:

| Behavior | When to use |
|---|---|
| **Reject** | Default for schema and application rules. The write does not succeed; the caller is informed. |
| **Coerce** | When a known-safe transformation can fix the input (e.g., trimming whitespace, casting numeric types). Coercions must be logged. |
| **Warn** | For pipeline-level rules where you want telemetry without blocking. |
| **Quarantine** | For pipeline-level rules where the record might be valid but needs human review. |

Coerce is dangerous because it changes data without the caller's knowledge — use sparingly
and always log.

## Failure handling

Rejected writes need somewhere to go:

- **Synchronous callers** (API requests) — return a structured error with the rule name and
  the failure reason. Never return generic 500s.
- **Asynchronous callers** (bulk loads, CDC) — write to a dead-letter queue (DLQ) with the
  original record and the rejection reason. The DLQ is a substrate of its own and needs an
  owner and a review cadence (declared in phase 5).

## Testing validation rules

For each rule, write at least:

- One test that confirms the rule passes for a known-valid input.
- One test that confirms the rule rejects a known-invalid input.
- One test for boundary conditions (just-valid, just-invalid).

Validation rules without tests are not validation rules; they're hopeful suggestions.
