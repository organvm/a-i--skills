# Parallel dimensions — how to read multi-axis structure in a grain

The user's grain stated: "each prompt suggests multiple parallel levels in all directions needing domain specific knowledge expertise." This document specifies what "multiple parallel levels in all directions" means operationally and how to read for it.

## The premise

A prompt that looks small on the surface is rarely small in implication. Compact phrasings are dense compressions; the prompt-reader's job is to decompress them into the dimensions they encode without paraphrasing the prompt away.

A dimension, in this plugin's vocabulary, is an *axis of work the grain implies* — distinct from peers such that work along it can proceed without coupling to work along peers, and requires expertise distinct from peers.

## The six reading lenses

Reading a grain for its dimensions means passing the grain through six lenses, each of which surfaces a different kind of dimension. Strong dimensions emerge from multiple lenses; weak candidates emerge from only one. The grain-reader agent and the dimension-surfacing skill both use these lenses systematically.

### Lens 1: Domain

What distinct knowledge fields does this implicate? Common domains: legal, security, design, infrastructure, content, ontology, data engineering, governance, accessibility, performance.

If a grain says "ship a feature that lets users export their data," the domain lens surfaces at minimum: data engineering (the export itself), security (auth and access control), legal (GDPR-style compliance), design (the export-trigger UX), ops (storage and rate-limiting). Five domain dimensions from one grain.

### Lens 2: Stakeholder

Whose perspectives are implicated? Roles: user, operator, auditor, contributor, downstream consumer, regulator, ally, adversary.

A grain that names a stakeholder by negation ("don't make the human do the operational work") implies the operator dimension as one of the work axes. A grain that mentions an audience implies that audience as a stakeholder lens.

### Lens 3: Time horizon

What lives across different temporal scales? Immediate (this dispatch), medium (this week's iteration), long (governance that persists).

Different temporal scales often map to different kinds of work: immediate is execution-bound, medium is architectural, long is constitutional. A grain that names a long-term constraint ("rules are additive — never overwrite") implies a constitutional/governance dimension distinct from the immediate-execution dimension.

### Lens 4: Substrate layer

What technical or material layers does the grain span? Data model, API, UI, deployment, observability, documentation, operational runbook.

A grain that names a system-wide concern usually spans multiple layers. Each layer needs its own expertise — the data-model person is not the UI person is not the deployment person.

### Lens 5: Failure mode

What distinct failure modes need separately mitigating? Correctness, latency, security, ergonomics, cost, drift, ambiguity, decay.

Failure modes are dimensions in the sense that mitigating each requires its own specialist work. A grain that says "no ping-pong" is naming an ergonomics-and-cost failure mode (round-trip cost) explicitly — the no-pingpong dimension is therefore an axis the coliseum must include.

### Lens 6: Forbidden moves

What does the grain say "not" about, and what dimension does that "not" name by negation?

The "not" lens is the most often missed. A grain that lists forbidden moves is, by listing them, naming dimensions. "Not task, not series, not stream, not load, not cycle" — each of those names a confusable neighbor, and the work of distinguishing the assignment primitive from each neighbor is itself a dimension (encoded in `why-not-task-series-stream.md`).

## What makes two dimensions truly independent

Two dimensions are independent — peer in a parallel set — when:

1. **No execution-time coupling.** Subagent A's execution does not need to wait on or read from subagent B's execution.
2. **No success-criterion overlap.** A's success criteria and B's success criteria do not share an observable; they can each be evaluated alone.
3. **No expertise collapse.** A and B require genuinely different expertise — the same agent would not be best for both.
4. **No paraphrase relation.** A is not a rephrasing of B at a different level of abstraction.

When any of these four hold the other direction, the candidate dimensions are not yet peers; they are either coupled (collapse them) or in a sequence (one becomes a Phase-4 follow-up).

## The pruning principle

Initial lens-passes produce more candidates than the dispatch budget allows (3–7). Pruning is mandatory. The pruning rule:

- Where two candidates share expertise and overlap in success criteria → collapse to one.
- Where one is a sub-step of another → drop the sub-step.
- Where one is a rephrasing → drop the rephrasing.
- Where one is scope creep beyond what the grain implies → drop the scope creep.

The pruning log is part of the Phase-1 artifact precisely so that pruning decisions are auditable.

## The most common collapse error

The most common error in dimensional reading is **collapsing "stakeholder + domain" into one dimension** when they are actually two. Example: a grain implies both legal and a user-perspective lens; the analyst writes "user-facing legal" as one dimension, when in reality the legal-expert work (compliance analysis) and the user-facing work (UX writing for the disclosure) are different domains with different success criteria. Two dimensions, not one.

The corollary: when you see a hyphenated dimension name, suspect it. Hyphens often mark a collapse that should be a split.

## The most common explosion error

The most common error in the other direction is **lens-pass output retained as dimensions without pruning**. Each lens produces 2–4 candidates; six lenses produce 12–24 candidates; if all are retained, the "coliseum" has 20 assignments that overlap heavily and dispatch wastes tokens. Prune aggressively. The dispatch budget exists to force the pruning.

## Related references

- `assignment-anatomy.md` — what each surfaced dimension will be composed into
- `handoff-envelope-spec.md` — the encoding the surfaced dimensions become
- `why-not-task-series-stream.md` — boundary discipline that pruning relies on
