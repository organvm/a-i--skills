# Deduplication strategies

Deduplication is the largest source of subtle data corruption in migrations. Use multiple
strategies in sequence, from cheapest to most expensive.

## Strategy 1 — Exact-match deduplication

Compare full content (or hash of full content). Items with identical hashes are exact
duplicates.

- **Method:** compute a stable hash of the canonical representation of each item. Group by
  hash. Within each group, keep one and archive the rest.
- **Speed:** fast — single pass.
- **False-positive rate:** zero, by definition (modulo hash collisions).
- **False-negative rate:** high — misses duplicates with trivial differences (extra
  whitespace, different ordering of attributes, different timestamps).
- **When to use:** always run this first.

## Strategy 2 — Canonicalized-exact deduplication

Normalize content before hashing — strip whitespace, sort attributes, round timestamps,
lowercase identifiers.

- **Method:** define a canonicalization function appropriate to the entity class. Apply
  it before hashing. Group by canonical hash.
- **Speed:** fast — single pass after canonicalization.
- **False-positive rate:** depends on canonicalization function. Aggressive canonicalization
  (e.g., removing all whitespace) can collapse semantically distinct items.
- **False-negative rate:** lower than exact match.
- **When to use:** after exact-match, for substrates where content is human-edited.

## Strategy 3 — Fuzzy matching

For each pair of items, compute a similarity score; pairs above a threshold are flagged as
candidate duplicates.

- **Method:** typical algorithms — Jaccard for set-like content, Levenshtein for short
  strings, MinHash for large textual content, embedding cosine similarity for semantic
  similarity.
- **Speed:** O(N²) naive; use blocking (group by an indexable feature first, then compare
  within groups) to reduce.
- **False-positive rate:** depends on threshold; tune by sampling and human review.
- **False-negative rate:** lower than canonicalized-exact.
- **When to use:** for substrates where exact-match catches few duplicates but human
  judgment says many exist.

## Strategy 4 — Semantic deduplication

Use a model to determine whether two items refer to the same concept, even if surface
features differ.

- **Method:** embed each item, cluster embeddings, surface clusters for human review or
  programmatic merging.
- **Speed:** depends on embedding cost; usually batch-able overnight.
- **False-positive rate:** depends on the model and threshold; verify on a sample.
- **False-negative rate:** lowest of all strategies.
- **When to use:** sparingly — for high-value substrates where missed duplicates have real
  cost; never as the sole strategy.

## Action policy

For each duplicate group, decide:

| Action | When to use |
|---|---|
| **Delete duplicates** | Only when duplicates are byte-identical AND have no independent provenance to preserve. |
| **Archive duplicates** | Default — preserves the audit trail; reversible. |
| **Merge duplicates** | When duplicates have complementary attributes (e.g., one has a description, another has tags). Merge into the canonical record; archive the rest. |
| **Flag for review** | When confidence is low; do not auto-action. |

Always preserve the mapping from "old ID → canonical new ID" — phase 4's identifier
reconciliation depends on this.

## Anti-patterns

- **Don't trust automated deduplication blindly.** Sample at every threshold; have a human
  spot-check before auto-actioning.
- **Don't delete without archive.** Reversibility is the protection against bad
  deduplication choices.
- **Don't apply semantic deduplication to small substrates.** The cost-benefit is poor for
  substrates < 10,000 items.
- **Don't stop at one strategy.** Run exact, then canonicalized, then fuzzy in sequence —
  each catches what the previous missed.

## Reporting

For phase-4-ingestion-report.md, the per-pass section should include:

- Strategy used
- Threshold (for fuzzy/semantic)
- Items examined
- Duplicate groups detected
- Action distribution (deleted / archived / merged / flagged)
- Sample of 5–10 actioned groups for spot-checking
