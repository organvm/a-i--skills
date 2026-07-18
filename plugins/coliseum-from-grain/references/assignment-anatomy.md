# Anatomy of an autonomous work assignment

The unit this plugin encodes is the **autonomous work assignment**. This document specifies what it is, what it is made of, and what makes it cohere as a primitive distinct from neighboring units.

## Definition

An autonomous work assignment is a unit of work that carries enough of its own context to be executed by a recipient who has no other knowledge of the originating situation, judged complete by the recipient (against named success criteria) without consultation with the originator, and bounded such that a recipient could not, in good faith, expand the work beyond the assignment's stated scope.

The three load-bearing words are **autonomous** (the recipient does not bounce back), **work** (it produces an artifact), and **assignment** (it is bestowed with scope, not assumed).

## The seven structural elements

Every assignment, examined under microscope, contains seven structural elements. The 9-section envelope in `handoff-envelope-spec.md` is the *encoding* of these elements; the elements themselves are the *primitive*:

### 1. Identity

A stable referent — the assignment can be named and referred to. Without identity, the assignment cannot be tracked, audited, or referenced by peer assignments in the coliseum.

### 2. Scope (bivalent)

Scope is bivalent: it has a positive face (what is to be produced) and a negative face (what is explicitly not to be produced). Most failure modes of single-face scope come from leaving the negative face implicit — the recipient, in the absence of explicit exclusion, expands the work into adjacent territory.

### 3. Context

The information the recipient needs that is not derivable from the prompt alone. Context is the largest contributor to envelope size and the most common site of insufficiency. A failed envelope almost always failed at context.

### 4. Success criteria

Observable conditions under which the assignment is complete. Observable means: a third party, looking at the return artifact, can verify completion without asking the originator. Unobservable success criteria are a sign that scope is not yet operationalized.

### 5. Constraints (capabilities and prohibitions)

What the recipient may use (allowed tools, allowed approaches) and what is forbidden (e.g., "no destructive operations," "no fetching from external URLs," "no modifying files outside this directory"). Constraints carve out the action space inside which the recipient is autonomous.

### 6. Return contract

Where the work goes when finished and what shape it takes. Specifies path, structure, length budget. The return contract is what closes the assignment back into the coliseum — without it, returns are unmergeable.

### 7. Handoff envelope

The metadata layer that connects this assignment to its originating grain and its peer dimensions. Includes the verbatim grain, the dimension served, pointers to peer artifacts, and the BLOCKED clause that handles unresolvable obstacles without forcing the recipient to ping-pong.

## What makes the assignment "autonomous"

Autonomy is not a property of the recipient; it is a property of the envelope. A recipient can be highly capable and still ping-pong, if the envelope is insufficient. A recipient can be modest in capability and not ping-pong, if the envelope is complete.

The autonomy test is operational: hand the envelope to a stranger; if the stranger could complete it without asking, the envelope is autonomy-grade. If the stranger would have to ask "what did you mean by X" or "where is Y" or "is Z in scope," the envelope is leaky.

## What makes it "work"

Work means the assignment produces an artifact. An artifact is the externalized residue of the assignment — something readable, auditable, mergeable, transmittable. An assignment that produces only a mental shift in the recipient (e.g., "understand the codebase") is not an assignment; it has no completion test.

## What makes it an "assignment"

An assignment is bestowed, not chosen. The recipient does not negotiate scope; the recipient accepts the envelope as-given (or returns a BLOCKED block if it is genuinely unexecutable). This is what distinguishes assignment from collaboration. Collaboration is bidirectional and renegotiable; assignment is unidirectional and fixed-at-handoff.

This is also why the plugin's no-pingpong constraint is structural, not stylistic. Ping-pong reintroduces collaboration into a unit that was meant to be assignment. Once collaboration enters, the force-multiplication dies — every clarification round is a round-trip cost, and N round-trips across M assignments is the dispatch architecture collapsing back into a single serial conversation.

## Cardinality

An assignment is exactly one envelope sent to exactly one recipient producing exactly one return artifact. Multi-recipient assignments are not assignments — they are dispatches (the next level up). Multi-return assignments are not assignments — they are workflows (lower level).

A coliseum is a *set* of assignments dispatched in parallel. The coliseum has cardinality; the assignment does not.

## When an assignment is the wrong primitive

If the work to be done is genuinely sequential (B must wait for A), do not force assignment shape onto it. Sequence is a different primitive (sequence, series, pipeline). The autonomous-assignment primitive is the right encoding when the work is genuinely parallelizable across independent dimensions. Forcing assignment shape onto serial work loses the force-multiplication and creates dispatch-log fiction.

If the work to be done is small enough that a single direct execution by the orchestrator is faster than envelope-composition + dispatch + reconciliation overhead, do that. The assignment primitive carries protocol cost; that cost is paid only when the parallel-dispatch yield is greater.

## Related references

- `handoff-envelope-spec.md` — the 9-section encoding of these seven elements
- `why-not-task-series-stream.md` — boundary distinctions to neighboring units
- `parallel-dimensions.md` — the multi-axis structure that makes a coliseum legitimate
