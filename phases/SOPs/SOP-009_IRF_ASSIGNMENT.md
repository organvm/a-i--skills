# SOP-009: IRF Assignment Procedure

## Purpose
Standard procedure for assigning and managing IRF (Index Reference Format) identifiers across the organvm workspace.

## When
- New repository creation
- Reorganization affecting organ assignment
- Manual IRF reconciliation
- On demand via `organvm irf assign <repo>`

---

## IRF Schema

```
┌─────────────────────────────────────────────────────────────────────┐
│                   IRF FORMAT                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                             │
│   IRF-XXX-NNN                                                │
│    │   │  │                                                  │
│    │   │  └── Sequence (001-999)                             │
│    │   └────── Organ prefix (3 letters)                     │
│    └─────────── Fixed prefix                                  │
│                                                             │
│   Example: IRF-THE-001                                      │
│   Example: IRF-TAXI-042                                      │
│                                                             │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Organ-IRF Mapping

```
┌─────────────────────────────────────────────────────────────────────┐
│              ORGAN-IRF PREFIX MAPPING                            │
├────────┬──────────┬────────┬─────────┬──────────────────────────┤
│ ORGAN  │ GREEK    │ PREFIX │ RANGE   │ EXAMPLE                 │
├────────┼──────────┼────────┼─────────┼──────────────────────────┤
│ I     │ Theoria  │ THE    │ 001-999 │ IRF-THE-001            │
│ II    │ Kerygma  │ KER    │ 001-999 │ IRF-KER-001            │
│ III   │ Publica  │ PUB    │ 001-999 │ IRF-PUB-001            │
│ IV    │ Taxis   │ TAX    │ 001-999 │ IRF-TAX-001            │
│ V     │ Ops      │ OPS    │ 001-999 │ IRF-OPS-001            │
│ VI    │ Koinonia │ COM    │ 001-999 │ IRF-COM-001            │
│ VII   │ Kerygma  │ GOV    │ 001-999 │ IRF-GOV-001            │
│ Meta  │ Meta     │ META   │ 001-999 │ IRF-META-001           │
└────────┴──────────┴────────┴─────────┴──────────────────────────┘
```

---

## Assignment Micro-Steps

### Phase 1: Organ Determination

```
┌─────────────────────────────────────────────────────────────────┐
│ ASSIGNMENT MICRO-STEP 9.1.1: ORGAN DETERMINATION                │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: read seed.yaml                   TIMEOUT: 5s              │
│ SOURCE: seed.yaml organ field                             │
│ OUTPUT: Organ type (I-VII, Meta)                        │
└─────────────────────────────────────────────────────────────────┘
```

```python
def determine_organ(repo_path: str) -> str:
    """Determine organ from seed.yaml."""
    seed = Path(repo_path) / "seed.yaml"
    
    if seed.exists():
        data = yaml.safe_load(seed.read_text())
        return data.get("organ", "Meta")
    
    return "Meta"
```

---

### Phase 2: Prefix Selection

```
┌─────────────────────────────────────────────────────────────────┐
│ ASSIGNMENT MICRO-STEP 9.2.1: PREFIX SELECTION                   │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: dictionary lookup                 TIMEOUT: 1s              │
│ INPUT: Organ type                                           │
│ OUTPUT: IRF prefix                                           │
└─────────────────────────────────────────────────────────────────┘
```

```python
ORGAN_TO_PREFIX = {
    "I": "THE",
    "II": "KER", 
    "III": "PUB",
    "IV": "TAX",
    "V": "OPS",
    "VI": "COM",
    "VII": "GOV",
    "Meta": "META"
}

def get_prefix(organ: str) -> str:
    """Get IRF prefix for organ."""
    return ORGAN_TO_PREFIX.get(organ, "META")
```

---

### Phase 3: Sequence Allocation

```
┌─────────────────────────────────────────────────────────────────┐
│ ASSIGNMENT MICRO-STEP 9.3.1: SEQUENCE ALLOCATION               │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: registry + lock                 TIMEOUT: 10s              │
│ SOURCE: IRF registry                                       │
│ ALLOCATE: Next available sequence for organ                 │
└─────────────────────────────────────────────────────────────────┘
```

```python
IRF_REGISTRY_PATH = "/Users/4jp/Workspace/organvm/organvm-corpvs-testamentvm/irf-registry.yaml"

def allocate_sequence(prefix: str) -> int:
    """Allocate next sequence for prefix."""
    registry = yaml.safe_load(Path(IRF_REGISTRY_PATH).read_text())
    
    next_seq = registry["prefixes"][prefix]["next"]
    registry["prefixes"][prefix]["next"] = next_seq + 1
    
    # Update registry
    Path(IRF_REGISTRY_PATH).write_text(yaml.dump(registry))
    
    return next_seq
```

---

### Phase 4: IRF Assembly

```
┌───────────────────────────────────────────────────────���─��───────┐
│ ASSIGNMENT MICRO-STEP 9.4.1: IRF ASSEMBLY                       │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: string format                  TIMEOUT: 1s               │
│ INPUT: Prefix + sequence                                    │
│ OUTPUT: Complete IRF                                      │
└─────────────────────────────────────────────────────────────────┘
```

```python
def assemble_irf(prefix: str, sequence: int) -> str:
    """Assemble IRF from parts."""
    return f"IRF-{prefix}-{sequence:03d}"
```

---

### Phase 5: Assignment

```
┌─────────────────────────────────────────────────────────────────┐
│ ASSIGNMENT MICRO-STEP 9.5.1: IRF ASSIGNMENT                   │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: edit seed.yaml                TIMEOUT: 5s               │
│ UPDATE: seed.yaml IRF field                                │
│ COMMIT: With IRF assignment                                │
└─────────────────────────────────────────────────────────────────┘
```

```bash
# Assignment command
organvm irf assign organvm-iv-taxis/agent--claude-smith

# Output:
# IRF-TAXI-001 assigned to organvm-iv-taxis/agent--claude-smith
```

---

## Registry Management

### Registry Structure

```yaml
# irf-registry.yaml
version: "1.0"
updated: "2026-04-26"

prefixes:
  THE:
    organ: I
    next: 1
    assigned:
      - irf: IRF-THE-001
        repo: organvm-ontologia
        assigned_at: "2026-01-15"
  # ... etc
```

### Registry Queries

```bash
# Get next available IRF for organ
organvm irf next THE

# Get all IRFs for organ
organvm irf list --organ=IV

# Get IRF details
organvm irf get IRF-TAXI-001
```

---

## Validation Rules

1. **Format:** Must match `^IRF-[A-Z]{3}-[0-9]{3}$`
2. **Prefix:** Must match organ mapping
3. **Sequence:** Must be 001-999 (no reuse)
4. **Uniqueness:** Must be unique across workspace

---

## Owner

- **Responsible**: organvm-IV-taxis/agent--claude-smith
- **Oversight**: organvm-corpvs-testamentvm

---

*Last updated: 2026-04-26*
*Version: 1.0.0*
*SOP-009: IRF Assignment Procedure*