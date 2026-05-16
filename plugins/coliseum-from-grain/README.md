# coliseum-from-grain

A Claude Code plugin that encodes the **autonomous-work-assignment primitive** — a unit of work that is *not* task, series, stream, load, or cycle, but a scoped-and-parameterized assignment that carries its own context.

Given a *grain of sand* (a dense or minimal prompt), the plugin surfaces the parallel dimensions implicit in it, composes each dimension as a self-contained assignment with a 9-section handoff envelope, dispatches them in parallel to recommended subagent types, and reconciles the returns into a composed whole.

The constraint throughout: **no prompt ping-pong**. The orchestrator reads the grain autonomously — no front-gate intake — and every dispatched handoff carries enough context that the recipient never has to come back asking "what did you mean by X."

> **Honest limit.** "Domain expert" subagents are not infrastructure that exists. Available subagent types differ in tools and system prompts; they are all general Claude underneath. Treat envelope section 7 (recommended subagent type) as advisory. The force multiplication, if any, comes from independent parallel execution and orthogonal framing — not from imagined expertise.

## What this plugin solves

You issue a dense prompt that plainly implies more work than its surface suggests. The naive failure modes are:

- Ask the user twenty clarifying questions (ping-pong; collapses the coliseum into a serial conversation).
- Pick one obvious interpretation and execute (flattening; abandons the parallel dimensions).
- Decompose into a serial task list and walk it linearly (loses force-multiplication; wastes parallel capacity).

This plugin enforces the third option done right: **dispatch parallel assignments with self-contained envelopes**, then reconcile.

It also enforces a fifth option not listed above: **refuse to invoke the protocol when the grain is not fan-out shaped.** A pre-Phase-1 gate checks whether the grain has ≥3 genuinely independent dimensions. If not, the plugin declines and recommends a single direct ask. Running the four-phase protocol on a grain that doesn't fit produces orchestration overhead with no payoff.

## Architecture

```
coliseum-from-grain/
├── .claude-plugin/
│   └── plugin.json
├── README.md
├── skills/
│   ├── coliseum-orchestrator/       # Phase 0 + threading of phases 1-4
│   ├── dimension-surfacing/         # Phase 1
│   ├── assignment-composition/      # Phase 2
│   ├── coliseum-dispatch/           # Phase 3 (gated by pingpong-detector)
│   └── coliseum-reconciliation/     # Phase 4
├── agents/
│   ├── grain-reader.md              # autonomous dimensional read
│   ├── assignment-composer.md       # autonomous single-envelope draft
│   └── pingpong-detector.md         # mandatory gate before dispatch
└── references/
    ├── assignment-anatomy.md
    ├── why-not-task-series-stream.md
    ├── parallel-dimensions.md
    └── handoff-envelope-spec.md
```

## The four phases

| Phase | Skill | Output artifact |
|---|---|---|
| 1 | `dimension-surfacing` | `phase-1-dimensions.md` |
| 2 | `assignment-composition` | `phase-2-assignments.md` |
| 3 | `coliseum-dispatch` (gated by `pingpong-detector`) | `phase-3-dispatch-log.md` |
| 4 | `coliseum-reconciliation` | `phase-4-composed-whole.md` |

All artifacts land in a per-grain working directory: `coliseum-runs/<grain-slug>-YYYY-MM-DD/`.

## How to invoke

The orchestrator skill is the main entry point. Triggers include:

- A dense prompt whose surface size is small but implied scope is large.
- A prompt that names "grain → coliseum" framing, "autonomous work assignment," "no ping-pong," or "chunk and hand off."
- A request to decompose work into parallel domain expert dispatches.

The skill walks Phase 0 (autonomous grain read + fan-out gate) → Phase 1–4 with the no-pingpong gate seated between Phases 2 and 3, and a mechanical compression gate inside Phase 4.

## The four hard constraints

1. **No prompt ping-pong.** Every assignment must be self-contained. The pingpong-detector agent gates dispatch — calibrated to ship with annotated risk, not stall. Recomposition attempts are capped at 2.
2. **Parallel by default.** Sequential dispatch is the exception, justified by real dependency.
3. **Advisory subagent routing.** Each envelope names a recommended subagent type from the available roster — advisory, not load-bearing. There is no guaranteed expertise delta between subagent types.
4. **Reconciliation, not concatenation.** Phase 4 composes; it does not staple. Enforced mechanically: compressed output ≤50% target, ≥80% flagged as stapled, minimum 1 PENDING-DECISION or explicit justification.

## Legitimate user-touch points

The plugin runs autonomously by default. Phase 0 reads the grain itself; the orchestrator does not begin with a clarifying-question intake. The conductor principle holds: the human directs vision; the system does everything else.

The system touches the user at most three times across a run, and the first is rare:

- **Phase 0 (rare)** — only on irreducible ambiguity (e.g., the grain references "the spec" and two specs exist at known paths and the choice changes which subagents to dispatch). "I'm not sure what you mean" is not such a case.
- **Pre-Phase-1 fan-out gate** — if the grain is not fan-out shaped (≥3 independent dimensions), the plugin declines and recommends a direct ask instead. This is a refusal, not a question — the user can override but the protocol does not proceed by default.
- **Phase 4 PENDING-DECISIONs** — decisions that *cannot* be resolved by the system because they require user vision (two equally-valid design choices, authorization for a destructive op).

## Author

Anthony Padavano — `padavano.anthony@gmail.com`

## License

MIT
