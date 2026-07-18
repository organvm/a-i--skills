# Why "assignment" is not "task," "series," "stream," "load," or "cycle"

The user's originating grain stated the unit by *negation*: not task, not series, not stream, not load, not cycle. Each negation names a neighboring primitive with which assignment is frequently confused. This document holds the boundaries.

## Assignment vs. task

A **task** is a single bounded action with a single owner. "Update the README." "Add a unit test." "Refactor function X."

An **assignment** is a task **plus an envelope** that carries the context required for the recipient to execute autonomously. The envelope is what makes it more than a task. A task can be barked across the room; an assignment must be self-contained on paper.

The everyday confusion: people use "task" and "assignment" interchangeably. The plugin draws the line: if you are tracking work in a system where each item has a one-line title and an assignee — those are tasks. If each item has a 9-section envelope ready to dispatch to a fresh agent — those are assignments.

## Assignment vs. series

A **series** is a sequence of dependent actions. B cannot begin until A completes. Series carries temporal order as load-bearing structure.

An **assignment** is a *peer* element in a parallel set. Assignments in a coliseum are dispatched simultaneously precisely because they are not series-related. If two named assignments turn out to have a real dependency (B reads A's output), one of them is not a peer assignment — it is a downstream follow-up, and the coliseum has been mis-decomposed.

The everyday confusion: people see N items to do and call it "a series of assignments." If the items have order, they are a series of *tasks* (or steps). Assignments-proper are unordered with respect to each other.

## Assignment vs. stream

A **stream** is a continuous flow of homogeneous events. Each event is small, similar in shape, and processed by a standing handler. Logs, telemetry, message queues — streams.

An **assignment** is discrete, heterogeneous, and bespoke-shaped per dimension. Each assignment has its own envelope; no two assignments are the same in detail. The handler is selected per-assignment (different subagent types for different dimensions), not standing.

The everyday confusion: high-throughput repetitive work is sometimes called "assignments" when it is properly a stream. If the work is the-same-action-on-many-inputs, you want a stream architecture (one handler, many inputs) not a coliseum (many handlers, parallel inputs). Coliseums are for the case of *different* domains in parallel, not *same* domain repeated.

## Assignment vs. load

A **load** is an aggregate weight without internal structure. "I have a heavy load this week" — three meetings, two deadlines, an audit. The load is the sum; the items inside are not addressed structurally.

An **assignment** has internal structure: scope, context, success criteria, etc. It is *not* an undifferentiated weight; it is a named composition.

The everyday confusion: "my assignment load" treats assignments as fungible mass. The plugin treats each assignment as a structured object. Load-thinking and assignment-thinking are different operating modes, and the plugin operates in the latter.

## Assignment vs. cycle

A **cycle** is a repeating loop. Same shape, recurring. Daily standup. Weekly review. Monthly close.

An **assignment** is one-shot. Once executed and reconciled, it is finished. A coliseum can be re-run on a new grain, but each coliseum is its own non-repeating composition.

The everyday confusion: standing work (a weekly review) is sometimes packaged as "an assignment" because it has scope and criteria. If it recurs on a schedule with the same shape, it is a cycle, not an assignment. The plugin would not be the right tool for that — a cron / scheduled-agent system is.

## The negation as constructive definition

By naming what the assignment is *not*, the user has carved out the conceptual space the assignment *is*. The five negations together specify:

- **Not task** → carries an envelope
- **Not series** → peer in a parallel set
- **Not stream** → bespoke per dimension
- **Not load** → has internal structure
- **Not cycle** → one-shot

The intersection of these five negative constraints is precisely the autonomous-work-assignment primitive. The plugin enforces this intersection.

## When you encounter a unit that doesn't fit

When a user request seems to want the assignment primitive but the work is structurally one of the neighbors, do not force the fit. Recognize:

- Truly serial work → use sequential dispatch with explicit dependency; do not pretend it's parallel.
- Repetitive homogeneous work → use a stream architecture; the coliseum overhead is wasted.
- Heavy load with no structure → ask the user to specify the internal structure first; assignment requires it.
- Recurring same-shape work → use the `/schedule` mechanism; assignment is one-shot.

Forcing the wrong primitive onto the work is one of the failure modes the no-flattening rule explicitly forbids.

## Related references

- `assignment-anatomy.md` — the seven structural elements that make the primitive
- `parallel-dimensions.md` — what "peer in a parallel set" requires of the dimensions
- `handoff-envelope-spec.md` — the envelope that distinguishes assignment from task
