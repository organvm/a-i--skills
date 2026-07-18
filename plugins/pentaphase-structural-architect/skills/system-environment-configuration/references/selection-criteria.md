# Selection criteria families

Use these as a starting palette. Cut criteria that don't apply; add substrate-specific criteria
the palette doesn't cover.

## Capacity

- **Entity count ceiling** — how many entities the mechanism handles before performance degrades.
  Threshold: 10× the projected count at end of phase-1's time horizon.
- **Storage volume ceiling** — bytes the mechanism can hold. Threshold: 10× current substrate
  storage.
- **Per-entity payload size** — max size of a single entity. Threshold: must accommodate the
  largest entity from phase-1's inventory.
- **Growth rate accommodation** — sustained writes per second the mechanism can absorb without
  backpressure. Threshold: 10× current p99 write rate.

## Performance

- **Read latency p50/p99** — for typical query patterns identified in phase-1's value metrics.
- **Write latency p50/p99** — for the dominant write pattern.
- **Concurrent reader count** — supported simultaneous readers without degradation.
- **Concurrent writer count** — supported simultaneous writers without lock contention.

## Query expressiveness

- **Point lookup** — by primary key. Universal requirement.
- **Range scan** — by sortable attribute (timestamp, numeric).
- **Equality filter** — by indexed attribute.
- **Multi-attribute filter** — combinations.
- **Joins / lookups** — across entity classes.
- **Full-text search** — across textual content.
- **Vector similarity** — for semantic search; only if substrate has embeddings.
- **Aggregation** — sum, count, group-by, percentile.
- **Window functions** — running totals, leads/lags.
- **Graph traversal** — multi-hop relationship walks; only if substrate is graph-shaped.

## Schema flexibility

- **Online schema change** — can attributes be added without downtime?
- **Backfill support** — when an attribute is added, can existing rows be backfilled cleanly?
- **Soft-delete support** — does the mechanism distinguish "marked deleted" from "purged"?
- **Versioning support** — can entity versions coexist? Is point-in-time recovery available?
- **Polymorphism** — can a single class hold heterogeneous shapes (sparse attributes)?

## Access control granularity

- **Entity-level** — minimum.
- **Attribute-level** — for substrates with sensitive attributes within otherwise-public entities.
- **Row-level / record-level** — for substrates where some rows are restricted within an
  otherwise-shared table.
- **Tenant isolation** — for multi-tenant substrates.

## Audit & compliance

- **Audit log** — automatic logging of who did what, when.
- **Log immutability** — append-only with tamper detection.
- **Retention controls** — programmable retention periods.
- **PII tooling** — discovery, classification, redaction.
- **Data residency** — geographic constraints on where data lives.
- **Encryption at rest** — and key management story.
- **Encryption in transit** — TLS for all client-server communication.
- **Certifications** — SOC2, HIPAA, ISO 27001, etc., as required.

## Integration surface

- **API protocols** — REST, GraphQL, gRPC, native client SDK.
- **Change-data-capture (CDC)** — for downstream consumers needing event streams.
- **Webhook outputs** — for event-driven consumers.
- **MCP compatibility** — for AI-agent access.
- **Bulk import/export** — for migration in/out.
- **Backup/restore** — automated, scheduled, tested.

## Operational fit

- **Existing team skill** — does the operational team already know this mechanism?
- **Hosting model** — self-hosted / managed / SaaS; preferences and constraints.
- **Total cost of ownership** — license + infrastructure + operational time + integration cost.
- **Vendor health** — for proprietary mechanisms, vendor stability and roadmap.
- **Community size** — for open-source mechanisms, ecosystem and community support.
- **Lock-in risk** — how reversible is the choice if it turns out wrong.

## Threshold-setting protocol

For each criterion, set a threshold that is:

- **Measurable** — you can verify it with a benchmark or a docs page.
- **Relevant** — derived from phase-1 (current scale + value metrics) or phase-2 (taxonomy
  shape), not from generic best practice.
- **Honest** — set based on actual need, not aspirational growth that won't materialize.

Weight each criterion {must / should / nice}. Must-have failures eliminate a candidate
outright. Should-have failures require explicit mitigation. Nice-to-have failures are noted
but tolerated.
