# Entity classification strategies

Pick the strategy that fits your substrate. Most substrates use 1–2 of these in combination.

## By function (most common)

Group entities by what they DO in the system. Examples: "Document", "Comment", "Task",
"User", "Event".

- **Strength:** maps cleanly to operational behavior; easy to teach.
- **Weakness:** can fragment a single conceptual entity if it has multiple functions.
- **When to use:** substrate has clear functional separation; participants reason about
  behavior more than essence.

## By lifecycle

Group entities by their lifecycle pattern. Examples: "Long-lived Reference" vs. "Short-lived
Transactional" vs. "Append-only Log".

- **Strength:** lifecycle determines storage strategy, retention policy, access tier — so
  classifying by lifecycle aligns with technical concerns.
- **Weakness:** can group functionally-different entities together; doesn't always map to
  user mental models.
- **When to use:** substrate is dominated by data with heterogeneous lifecycles (e.g., some
  permanent, some ephemeral); compliance or storage cost matters.

## By origin

Group entities by where they come from. Examples: "User-Generated", "System-Generated",
"Imported", "Derived".

- **Strength:** clarifies trust and validation requirements; user-generated needs more
  validation than system-generated.
- **Weakness:** origin can be fluid (e.g., user-edits-system-generated).
- **When to use:** substrate has a strong provenance-or-quality axis; auditing matters.

## By audience

Group entities by who is allowed to see them. Examples: "Internal", "Customer-Facing",
"Public", "Restricted".

- **Strength:** maps directly to access framework; reduces complexity of permission rules.
- **Weakness:** can split functionally-identical entities just by audience.
- **When to use:** substrate has strict visibility constraints (compliance, security,
  marketing).

## By stability

Group entities by how often they change. Examples: "Static Reference", "Slowly-Changing",
"High-Velocity".

- **Strength:** maps to caching, replication, and indexing strategies.
- **Weakness:** stability can change over time; reclassification is expensive.
- **When to use:** performance is a primary concern; substrate has heterogeneous change
  rates.

## Composite (multi-axis)

Use two strategies as orthogonal axes. E.g., "Function × Audience" gives a 2D grid where
each cell is an entity class.

- **Strength:** captures more nuance than single-axis.
- **Weakness:** explodes the class count; can be over-classified.
- **When to use:** single-axis strategies leave you with too many "Misc" entities.

## Sanity checks for any classification

After picking a strategy and drafting classes, verify:

1. **Coverage** — every asset from phase 1's inventory maps to exactly one class. Any
   unclassifiable items signal an incomplete strategy or a missing class.
2. **Distinctness** — for any two classes, there is at least one boundary case that clearly
   belongs to one and not the other. If not, the classes will collapse in practice.
3. **Vocabulary fit** — class names use the substrate's own vocabulary. If you're inventing
   labels, you're probably over-classifying.
4. **Population balance** — no single class holds >70% of entities (probably under-classified)
   and no class holds <1% (probably over-classified).
5. **Future-fit** — anticipated new entities (the substrate's roadmap) map cleanly into
   existing classes.

## When to refactor classes

If during phase 3+ you find that a class never has any class-specific attributes, never
participates in any relationship distinctly, and is never accessed differently from
another class — collapse them. Conversely, if a class accumulates many distinct attributes
or access rules for sub-populations, split it.

Refactoring classes after phase 4 ingestion is expensive — get this right in phase 2.
