# pentaphase-structural-architect

A Claude Code plugin that operationalizes a five-phase methodology for any structural overhaul.

## What it is

This plugin treats "restructuring a system" as a directed protocol with five gated phases:

```
substrate → discovery → modeling → configuration → ingestion → governance → governed-substrate
              │            │             │              │            │
            gate-1      gate-2         gate-3         gate-4       gate-5
```

Each phase is a skill. Each gate is enforced by an agent. Each artifact produced by phase N is
the input to phase N+1, so the protocol is self-composing once the substrate-context is captured.

The methodology is **substrate-agnostic** — apply it to a documentation system, an asset registry,
a code monorepo, a knowledge base, an operational workflow, or any domain that needs the chaos-to-
governance arc.

## Components

| Type | Name | Purpose |
|---|---|---|
| Skill | `pentaphase-orchestrator` | Threads all five phases end-to-end with handoffs |
| Skill | `landscape-discovery-audit` | Phase 1 — inventory, flow map, friction, value metrics |
| Skill | `taxonomy-modeling-design` | Phase 2 — entity classes, attributes, relationships, access tiers |
| Skill | `system-environment-configuration` | Phase 3 — selection criteria, mechanism choice, instantiation, validation rules |
| Skill | `systemic-ingestion-normalization` | Phase 4 — deduplication, enrichment, batch ingestion, integrity audit |
| Skill | `governance-evolution-protocol` | Phase 5 — codified protocols, onboarding, monitoring, iteration cadence |
| Agent | `structural-integrity-auditor` | Verifies gate criteria at every phase boundary |

## Installation

### Local-only test install

```bash
claude --plugin-dir /Users/4jp/Code/pentaphase-structural-architect
```

### Project-scoped install

Copy or symlink the plugin into a project's `.claude-plugin/` directory and the plugin will be
discoverable when Claude Code runs from that project.

### Marketplace publication

Publish by adding an entry to the appropriate `marketplace.json` and pushing to a discoverable
repository host. (No marketplace entry yet — local-only at version 0.1.0.)

## Usage patterns

### A. Full protocol (most common)

When you're about to overhaul a real system end-to-end, invoke the orchestrator:

```
/pentaphase-structural-architect:pentaphase-orchestrator
```

It will:

1. Elicit substrate context (system name, driving force, primary failure point, operational roles, time horizon)
2. Anchor a working directory for the overhaul project
3. Walk the five phase-skills in sequence, invoking the integrity auditor at each gate
4. Leave behind a complete artifact stream you can refer back to

### B. Single-phase invocation

When you only need one phase (e.g., you already have a taxonomy and just need an ingestion plan):

```
/pentaphase-structural-architect:systemic-ingestion-normalization
```

The phase skill will read whatever prior-phase artifacts exist in the project's working directory
and produce its own output. If a required prior artifact is missing, the skill will tell you what
it needs.

### C. Audit only

When you want a verdict on an existing artifact without running any phase work:

Invoke the `structural-integrity-auditor` agent and point it at the artifact path.

## Working-directory layout

Each overhaul project gets its own directory (default: `<cwd>/pentaphase-overhauls/<substrate-slug>/`):

```
<substrate-slug>/
├── substrate-context.md           # input — set in phase 0 by the orchestrator
├── phase-1-landscape-report.md
├── phase-2-taxonomy-model.md
├── phase-3-environment-spec.md
├── phase-4-ingestion-report.md
├── phase-5-governance-charter.md
└── audit-log.md                   # cumulative auditor sign-offs
```

This layout is documented per skill and enforced by the orchestrator.

## Design philosophy

Three constraints shaped the architecture:

1. **System-first over anecdote-first.** Each phase is defined as a structured input/output schema,
   not as a free-form chat about restructuring. The artifacts are first-class.
2. **Generative, not prescriptive.** The skills do not impose a vocabulary on your substrate. They
   ask you to name your entities, your friction, your metrics — then they thread those names
   through the remaining phases.
3. **Gated, not waterfall.** The integrity auditor sits at every phase boundary. A failed gate is
   not a soft warning — it stops the protocol until the gap is named or remediated.

## Adapting the framework

The plugin's `pentaphase-orchestrator` opens with the same three questions the methodology calls
for in its conclusion:

- What business function is driving this structural overhaul?
- Who are the primary operational roles interacting with this process?
- What is the biggest current failure point you need this new structure to solve?

Answer those, and the protocol takes the substrate from chaotic-current-state to governed-target-state.

## Versioning

- `0.1.0` — initial release: 6 skills, 1 agent, gate-driven protocol.

## License

MIT.
