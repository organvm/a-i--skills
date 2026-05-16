---
name: taxonomy-modeling-design
description: Phase 2 of the pentaphase structural-overhaul protocol. Classifies entities, standardizes attributes, establishes relationships, and designs the access framework. Use when the user invokes phase 2 of an overhaul, asks to "design the taxonomy" or "model the structure", or has completed a landscape audit and is ready to redesign. Consumes phase-1-landscape-report.md; produces phase-2-taxonomy-model.md.
license: MIT
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
argument-hint: <working-directory containing phase-1 report>
---

# Phase 2: Structural Modeling & Taxonomy Design

You are designing the target-state taxonomy. The `phase-1-landscape-report.md` describes what
exists today; your job is to define the conceptual structure the substrate will inhabit going
forward — the categories, the attributes every item must carry, the relationships items have to
each other, and who is allowed to see or modify what.

## Preconditions

- `<working-dir>/substrate-context.md` exists.
- `<working-dir>/phase-1-landscape-report.md` exists and has passed gate 1 (PASS or
  PARTIAL-with-user-approval).
- Read both files in full before starting.

If phase 1 has not been audited yet, ask the user whether to invoke the
`structural-integrity-auditor` agent first.

## Four work streams

### Stream 1 — Classify Entities

Group similar elements from the assets inventory into logical, universally understood categories.

For each entity class, define:

- **Class name** — singular noun that captures the essence (e.g., "Document", "Ticket", "Asset",
  "Component"). Use the substrate's own vocabulary where possible.
- **Definition** — one sentence stating what membership requires
- **Examples from inventory** — 2–4 specific assets from phase 1 that belong in this class
- **Boundary cases** — assets that *almost* fit but don't (and where they go instead)
- **Estimated population** — rough count of how many instances exist today

Aim for 5–15 classes. Fewer means under-classified (blob categories that won't help). More
means over-classified (categories that will collapse together in practice).

### Stream 2 — Standardize Attributes

Define the mandatory traits, labels, and metadata every item must carry, per entity class.

For each entity class, list:

| Attribute | Type | Required | Validation | Default |
|---|---|---|---|---|
| (e.g., id) | string (uuid) | yes | matches `uuid` regex | generated on create |
| (e.g., owner) | string (user-id) | yes | exists in user registry | — |
| (e.g., created_at) | timestamp | yes | valid ISO-8601 | now() on create |
| (e.g., status) | enum | yes | one of {active, archived, deleted} | active |
| (e.g., tags) | array<string> | no | each tag <= 50 chars | [] |

Distinguish:

- **Universal attributes** that apply to ALL entity classes (id, created_at, owner — common
  cross-class metadata)
- **Class-specific attributes** that apply only to one class

Universal attributes go in a shared "Universal Schema" section; class-specific attributes go
under each class.

### Stream 3 — Establish Relationships

Map out how entity classes connect, depend on, and interact with each other.

For each relationship:

- **From class** → **To class**
- **Cardinality** — 1:1, 1:N, N:1, N:N
- **Name** — verb phrase describing the relationship from the From-class's perspective (e.g.,
  "owns", "references", "supersedes", "blocks")
- **Direction** — directed (one-way) or symmetric (two-way)
- **Lifecycle coupling** — what happens to the To-class instance when the From-class instance
  is deleted/archived (cascade, restrict, set-null, no-op)

Optionally include a textual or ASCII relationship diagram showing the entity classes as nodes
and relationships as edges.

### Stream 4 — Design Access Framework

Determine visibility, ownership levels, and modification rights across tiers.

For each entity class, declare:

- **Visibility tiers** — who can see instances (e.g., public / org-wide / team / owner-only)
- **Modification tiers** — who can modify instances (often more restricted than visibility)
- **Ownership model** — single owner / shared / role-based / committee
- **Delegation rules** — who can transfer ownership and under what conditions
- **Audit policy** — what changes are logged, retained how long

If the substrate has compliance requirements (legal, regulatory, contractual), surface them
explicitly here. Tier definitions should map cleanly to existing role/permission systems where
possible — don't invent a new permission model unless the substrate's existing one is the
problem being solved.

## Composing phase-2-taxonomy-model.md

Combine the four streams into a single file at `<working-dir>/phase-2-taxonomy-model.md`.
Structure:

```markdown
# Phase 2 — Taxonomy Model

**Substrate:** <name>
**Date:** YYYY-MM-DD
**Preconditions:** Read substrate-context.md, phase-1-landscape-report.md
**Postconditions:** Ready for Phase 3 (system-environment-configuration)

## 1. Entity classes

[per-class definitions with examples and boundary cases]

## 2. Universal schema

[attributes that apply to all classes]

## 3. Class-specific schemas

[per-class attribute tables]

## 4. Relationships

[per-relationship cards + optional diagram]

## 5. Access framework

[per-class tier definitions, ownership, audit policy]

## 6. Open questions for Phase 3

[explicit list of decisions deferred to environment configuration —
e.g., "should `status` enum allow custom values per team, or be globally enumerated?"]
```

## Gate criteria (auditor will check)

The model passes Phase 2's gate iff:

1. **Entity classes are exhaustive and mutually exclusive** — every asset from phase 1's
   inventory maps to exactly one class. If any are unclassifiable, declare a "Misc" class
   explicitly with a rule for when items belong there.
2. **Universal schema has ≥ 3 attributes** — at minimum: identity, ownership, lifecycle/state.
3. **Every class-specific attribute has a type and required-ness** — no schema fields with
   undefined types or undefined optionality.
4. **Every relationship has a cardinality and a lifecycle coupling** — no relationship cards
   missing those fields.
5. **Every entity class has both visibility AND modification tiers declared** — even if both
   default to "owner-only" or "public".
6. **Open questions for Phase 3 section is present** — even if empty.

## Anti-patterns

- **Don't import attribute schemas from frameworks you haven't chosen yet.** Phase 3 picks the
  environment. Phase 2 is conceptual — it describes WHAT the taxonomy is, not WHICH database or
  CMS will hold it.
- **Don't collapse entity classes prematurely.** If two classes feel similar but have different
  lifecycles or different access tiers, they are different classes.
- **Don't define attributes the substrate doesn't actually need.** Every attribute is a
  validation cost. Only require what enforces invariants.
- **Don't design access tiers that don't map to a real principal.** Every tier must point to
  identifiable users, roles, or systems — not theoretical actors.

## See also

- `references/classification-strategies.md` — common entity-classification patterns
- `references/access-frameworks.md` — visibility/modification tier patterns by domain
