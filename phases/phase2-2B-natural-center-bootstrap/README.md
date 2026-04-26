# PHASE 2B: Natural Center Bootstrap ($PROC_NATURAL_CENTER_BOOTSTRAP)

## Metadata
- **Phase**: 2B
- **Decision**: Formalize Natural Center as computable object
- **Status**: DRAFT
- **Created**: 2026-04-26
- **Parent**: PHASE_2_ARCHITECTURE

## The Ask

The Natural Center is the platonic ideal form beneath client adaptations — the "DNA clone" theory made mathematical.

## Definition: Natural Center

```
Natural Center (NC) = The invariant form + variable parameters

Where:
- invariant form = the core logic that doesn't change per persona
- variable parameters = the dimensions that adapt to client
- Ideal Yearning = the attractor state the client moves toward
- Gate Register = the transition mechanism
```

## Mathematical Formalization

### Core Object

```
NC = {
  I: Invariant Form (set of rules that never change)
  P: Parameter Space (dimensions of variation)
  Y: Ideal Yearning (attractor state)
  G: Gate Register (transition function)
  T: Temporal Axis (how NC evolves over time)
}
```

### Invariant Form (I)

```
I = {
  r1: Input → Processing → Output (no jargon in output)
  r2: Every output traces to input (bridge_to)
  r3: Voice matches persona's register (not generic)
  r4: Anti-orphan: no floating references
  r5: Scaffold → Curate → Ship (2-step verification)
}
```

### Parameter Space (P)

```
P = {
  p1: Domain (fitness/chess/wellness/business)
  p2: Vocabulary (client-specific terms)
  p3: Analogies (metaphors that land)
  p4: Register (logos/ethos/pathos/kairos)
  p5: Gate Type (battle/ritual/gift/trial/council/quest)
  p6: Depth Tolerance (ELI5/TLDR/full/appendix)
}
```

### Ideal Yearning (Y)

```
Y = {
  current_state: client现状
  target_state: where_client_wants_to_be
  motivation: why_they_care
  metric: how_we_measure_progress
}
```

### Gate Register (G)

```
G = {
  gate_type: one of [battle|ritual|gift|trial|council|quest|training_arc]
  entry_condition: what_activates_the_gate
  transition: how_client_moves_through
  exit_condition: what_completes_the_gate
  next_gate: what's_after_this
}
```

### Transition Function

```
transform(input, NC, client_persona) → output

Where:
- input = raw internal artifact
- NC = Natural Center (invariant + params)
- client_persona = parameter overrides
- output = client-facing storefront surface
```

## Extraction Algorithm

```
ALGORITHM: Extract_Natural_Center(client_transcripts)

INPUT: Set of client conversation transcripts
OUTPUT: Computed Natural Center

STEP 1: Tokenize all transcripts
STEP 2: Extract vocabulary frequency (client terms)
STEP 3: Extract analogical patterns (metaphors)
STEP 4: Identify ideal yearning (attractor state)
STEP 5: Identify gate register (transition mechanism)
STEP 6: Compare across transcripts → find_invariants
STEP 7: Return NC = {I, P, Y, G, T}
```

## Computable Representation

```typescript
interface NaturalCenter {
  invariant: InvariantForm;
  parameterSpace: ParameterSpace;
  yearning: IdealYearning;
  gates: GateRegister[];
  temporal: TemporalEvolution;
}

interface InvariantForm {
  rules: Rule[];
  verify(artifact: Artifact): boolean;
}

interface ParameterSpace {
  dimensions: Map<string, DimensionConfig>;
  adapt(persona: Persona, nc: NaturalCenter): NaturalCenter;
}

interface IdealYearning {
  current: State;
  target: State;
  motivation: string;
  metric: Metric;
}

interface GateRegister {
  type: GateType;
  entry: Condition;
  transition: Transition;
  exit: Condition;
}
```

## Natural Center Bootstrap Pipeline

```
1. COLLECT_CLIENT_TRANSCRIPTS
   ↓
2. RUN_EXTRACTION_ALGORITHM
   ↓
3. COMPUTE_NC_PARAMETERS
   ↓
4. VALIDATE_INVARIANTS (must hold across 3+ transcripts)
   ↓
5. DEPLOY_TO_SERVICE
   ↓
6. USE_AS_TRANSFORMATION_ENGINE
```

## Service Integration

| Method | Service | Function |
|---|---|---|
| Extract | corpus-service | Compute NC from transcripts |
| Store | lexicon-service | Save computed NCs |
| Transform | storefront-service | Apply NC to artifacts |

## Decision Log

| Decision | Choice | Rationale |
|---|---|---|
| Formalization | Mathematical object | Computable, testable |
| Invariants | 5 core rules | Minimum viable |
| Parameter Space | 6 dimensions | Complete coverage |
| Yearning | State-based | Progress measurable |
| Gates | Enum-based | Clear transitions |

## Generated Files

`phase2-2B-natural-center-bootstrap/SPEC.md`
`phase2-2B-natural-center-bootstrap/algorithm.md`
`phase2-2B-natural-center-bootstrap/types.ts`
`phase2-2B-natural-center-bootstrap/pipeline.md`