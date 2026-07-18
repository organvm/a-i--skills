# Handoff envelope specification

This document specifies the 9-section envelope that wraps each autonomous-work-assignment for dispatch. The pingpong-detector agent validates each envelope against this spec; envelopes that fail the spec are rejected at the no-pingpong gate.

## The 9 sections (canonical order)

```markdown
### assignment-NNN-<dimension-slug>

**Scope (positive)**:
<one paragraph, concrete, what is to be produced>

**Scope (negative)**:
<adjacent work explicitly excluded — name specific peer concerns being kept out of scope>

**Context the recipient needs**:
<everything the recipient must know to execute; assume zero conversation history>

**Success criteria**:
- [ ] <observable check>
- [ ] <observable check>
- [ ] <observable check>

**Allowed tools**:
<minimal explicit list, e.g., Read, Grep, Write — NOT "all tools">

**Recommended subagent type**:
<agent type from roster> — <one sentence justification>

**Return format**:
- Path: <absolute path to return artifact>
- Structure: <required headings or layout>
- Length budget: <e.g., ≤ 400 words OR ≤ 2 pages>
- Must NOT contain: <explicit exclusions>

**Handoff envelope**:
- Originating grain (verbatim):
  > <quoted grain>
- Dimension served: <name of dimension from Phase-1>
- Peer-context reference: <path to phase-1-dimensions.md>
- BLOCKED clause: If you reach a point where you cannot continue without clarification, write a `BLOCKED` block in your return artifact rather than coming back to ask. Continue with the rest of the assignment if any part remains executable.
```

## Section-by-section guidance

### Identifier (`### assignment-NNN-<dimension-slug>`)

- `NNN` is zero-padded three-digit serial within this coliseum (001, 002, …).
- `<dimension-slug>` is a kebab-case shortening of the dimension name.
- The full identifier is stable across all later phases (dispatch log, return artifacts, reconciliation).

### Scope (positive)

- One paragraph, 3–6 sentences.
- Concrete: name actual artifacts, formats, decisions to be produced.
- Not abstract: avoid "understand," "explore," "investigate." Use produce/write/decide/specify.
- A scope that begins "Help me think about…" is a failed scope — make it operational.

### Scope (negative)

- This is the section most often skipped or boilerplate-filled, and the section most responsible for ping-pong when leaky.
- Name *specific adjacent concerns*. Not "anything outside scope" — list which adjacent dimensions are explicitly out (e.g., "Excludes UX implementation for the same feature, which is dispatched as assignment-004").
- The negative scope reads like a small inventory of what could-but-won't-be-included.

### Context the recipient needs

- The largest section by far.
- Inline anything substrate-specific: if the user uses substrate vocabulary (σ-axis, AMMOI, ORGANVM, IRF), define it inline rather than assume the recipient knows.
- Inline file paths, system names, conventions. The recipient cannot grep the user's mind.
- Include any *previously-rejected approaches* with reasons — this preempts the recipient re-proposing them.

### Success criteria

- Each item is observable: a third party reading the return artifact can verify yes/no without consulting the originator.
- Each item is independently verifiable: do not chain criteria such that "if A then B" — list each as standalone.
- Sufficient as a set: when all are checked, the work is genuinely complete (no implicit additional criteria).
- Aim for 3–6 items. Fewer than 3 usually means under-specification; more than 6 usually means scope creep crept in.

### Allowed tools

- Explicit list of named tools. Examples: `Read, Grep, Write` or `Read, Bash, WebFetch`.
- Default to minimum. If you list `Bash`, you must believe the recipient genuinely needs to run shell commands.
- "All tools" is almost always wrong. The pingpong-detector flags it.
- If destructive operations are forbidden, name that explicitly here (e.g., "Read, Edit — no Bash, no Write of new files").

### Recommended subagent type

- Choose from the available roster at runtime.
- Justify in one sentence: "Explore — because this dimension is read-only research across multiple files."
- If no roster entry fits well, name the gap: "general-purpose, but the ideal would be a domain-specific X agent we lack." This is honesty about fit, not failure.

### Return format

- **Path** — absolute, parent-directory-existing. The dispatch skill creates parent dirs in advance.
- **Structure** — name the required sections or layout. The recipient should not invent the structure; the structure is part of the contract.
- **Length budget** — explicit. "≤ 400 words" or "≤ 2 pages" or "exactly N rows in the table." Open-ended returns cause reconciliation problems.
- **Must NOT contain** — important: forbid executive summaries, forbid scope-expanding recommendations, forbid any framing the reconciliation doesn't want.

### Handoff envelope (the no-pingpong guarantee)

- **Verbatim grain** — quoted, in a blockquote. The recipient should never have to infer the originating intent.
- **Dimension served** — by name. Lets the recipient understand their place in the coliseum.
- **Peer-context reference** — pointer to `phase-1-dimensions.md`. Optional read, but available.
- **BLOCKED clause** — exactly as in the template. The standard wording matters; the recipient must learn that writing BLOCKED is the legitimate move, not coming back.

## Common envelope pathologies

### The "trust me" envelope

> Context the recipient needs: You know what we're working on.

Fail. The recipient does not. Inline everything.

### The "all tools, all welcome" envelope

> Allowed tools: as needed.

Fail. Specify.

### The "vibe-check" success criterion

> Success criteria: The result feels right and addresses the dimension.

Fail. "Feels right" is not observable. Rewrite.

### The "polite" negative scope

> Scope (negative): Anything outside the stated positive scope.

Fail. This is boilerplate. Name actual adjacent concerns being kept out.

### The "we'll figure it out" return format

> Return format: A markdown file with your findings.

Fail. Specify path, structure, length, exclusions.

## When the envelope feels too long

It will. Envelopes are typically 400–1200 words. That is correct. The cost of envelope-length is paid once, by the orchestrator, at composition. The cost is amortized across the parallel dispatch and the absence of ping-pong rounds. A 1200-word envelope that avoids 4 clarification rounds is a win, because each clarification round is hundreds of additional tokens (the recipient's read, the recipient's question, the orchestrator's answer, the recipient's re-read) and serializes work that was supposed to be parallel.

The envelope's length is the price of force-multiplication. Pay it once.

## Related references

- `assignment-anatomy.md` — the seven structural elements this 9-section encoding serves
- `why-not-task-series-stream.md` — why "task" can be barked across the room but "assignment" cannot
- `parallel-dimensions.md` — what makes the dimension being wrapped here a legitimate peer
