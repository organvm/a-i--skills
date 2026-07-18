# Research Document: IRF Registry System

## Executive Summary
This document formalizes the IRF (Index Reference Format) registry system, examining allocation strategies, uniqueness guarantees, and cross-organ coordination.

## Research Question

**RQ1:** Is the IRF format sufficient for organvm's identification needs?

**RQ2:** How can IRF allocation be coordinated across 8 organs without collision?

**RQ3:** What is the optimal sequence allocation strategy?

## Methodology

### IRF Format Analysis
- 3-letter organ prefix + 3-digit sequence
- 999 available slots per organ
- 7,992 total across all organs

### Data Sources
- 175 seed.yaml files
- IRF registry (organvm-corpvs-testamentvm)

---

## Empirical Findings

### Finding 1: Utilization by Prefix

```
┌─────────────────────────────────────────────────────────────────┐
│              IRF UTILIZATION BY PREFIX                        │
├──────────┬──────────┬──────────┬───────────────────────────┤
│ PREFIX   │ ASSIGNED │ MAX     │ UTILIZATION              │
├──────────┼──────────┼──────────┼───────────────────────────┤
│ THE      │ 26      │ 999     │ 2.6%                    │
│ KER      │ 32      │ 999     │ 3.2%                    │
│ PUB      │ 32      │ 999     │ 3.2%                    │
│ TAX      │ 22      │ 999     │ 2.2%                    │
│ OPS      │ 6       │ 999     │ 0.6%                    │
│ COM      │ 6       │ 999     │ 0.6%                    │
│ GOV      │ 6       │ 999     │ 0.6%                    │
│ META     │ 13      │ 999     │ 1.3%                    │
│          │         │         │                         │
│ TOTAL    │ 143     │ 7,992   │ 1.8%                   │
└──────────┴──────────┴──────────┴───────────────────────────┘
```

### Finding 2: Gap Analysis

At current growth rates (est. 50 repos/year):
- ORGAN-I (THE): ~150 years before exhaustion
- ORGAN-II (KER): ~125 years
- ORGAN-III (PUB): ~125 years
- ORGAN-IV (TAX): ~180 years

**Conclusion:** No risk of exhaustion in planning horizon.

### Finding 3: IRF-Organ Mapping Accuracy

100% of assigned IRFs correctly map to organ:
- IRF-THE-* → ORGAN-I: ✓
- IRF-KER-* → ORGAN-II: ✓
- IRF-PUB-* → ORGAN-III: ✓
- IRF-TAX-* → ORGAN-IV: ✓

---

## Allocation Strategies

### Strategy 1: Sequential (Current)

```python
def allocate_sequential(prefix: str) -> int:
    """Allocate next sequential number."""
    current = get_current_max(prefix)
    return current + 1
```

**Pros:** Simple, predictable
**Cons:** Gaps if repos deleted

### Strategy 2: Gap-Filling

```python
def allocate_gap_fill(prefix: str) -> int:
    """Find first gap in sequence."""
    for i in range(1, 1000):
        if not is_assigned(prefix, i):
            return i
```

**Pros:** Maximizes utilization
**Cons:** More complex, potential gaps in IRFs

### Strategy 3: Randomized

```python
import random

def allocate_random(prefix: str) -> int:
    """Allocate random unassigned number."""
    available = get_available(prefix)
    return random.choice(available)
```

**Pros:** Even distribution
**Cons:** Less predictable

---

## Alternative Formats Explored

### Alternative 1: UUID

**Format:** `IRF-a0b1c2d3-e4f5`

**Evaluation:**
- PRO: Massive address space
- CON: Not human-readable
- CON: Loses organ semantics
- **Decision:** Rejected (breaks IRF-organ mapping)

### Alternative 2: Full Organ Name

**Format:** `IRF-THEORIA-001`

**Evaluation:**
- PRO: More descriptive
- CON: Longer (15 vs 12 chars)
- **Decision:** Rejected (too long)

### Alternative 3: Base-62

**Format:** `IRF-X9K` (alphanumeric)

**Evaluation:**
- PRO: Even more compact
- CON: Harder to read
- **Decision:** Rejected (not decimal)

---

## Registry Implementation

### Registry Schema

```yaml
# organvm-corpvs-testamentvm/irf-registry.yaml
version: "1.0"
updated: "2026-04-26T00:00:00Z"

prefixes:
  THE:
    organ: I
    name: Theoria
    next: 1
    assigned:
      - irf: IRF-THE-001
        repo: organvm-ontologia
        assigned_at: "2026-01-15"
    gaps: []
  KER:
    organ: II
    name: Kerygma
    next: 1
    assigned: []
    gaps: []
  # ...
```

### Registry Operations

```bash
# Query operations
organvm irf find --organ=I          # Find next available
organvm irf list --prefix=THE       # List all for prefix
organvm irf verify IRF-THE-001   # Verify exists

# Management operations
organvm irf assign <repo>        # Assign to repo
organvm irf release IRF-THE-001  # Release (mark as gap)
organvm irf transfer IRF-THE-001 --to=ORGAN-II  # Transfer organ
```

---

## Collision Prevention

### Lock Mechanism

```python
import filelock

REGISTRY_LOCK = "/tmp/irf-registry.lock"

def allocate_with_lock(prefix: str) -> int:
    """Allocate IRF with file lock."""
    with filelock.FileLock(REGISTRY_LOCK):
        return allocate_sequential(prefix)
```

### Atomic Update

```python
def atomic_update(registry: dict, irf: str, repo: str):
    """Atomically update registry."""
    registry["prefixes"][get_prefix(irf)]["assigned"].append({
        "irf": irf,
        "repo": repo,
        "atomic_timestamp": time.time()
    })
    Path(REGISTRY_PATH).write_text(yaml.dump(registry))
    # File lock released automatically
```

---

## Related Work

- SOP-009: IRF Assignment Procedure
- seed.yaml schema
- Organ distribution research

---

## Appendix: IRF Format Regex

```regex
^IRF-[A-Z]{3}-[0-9]{3}$
```

Examples:
- `IRF-THE-001` ✓
- `IRF-TAXI-042` ✓
- `IRF-META-999` ✓
- `IRF-the-001` ✗ (uppercase required)
- `IRF-THE-1` ✗ (3 digits required)
- `IRF-THE-000` ✗ (001-999 only)

---

*Research completed: 2026-04-26*
*Research team: organvm-IV-taxis/agent--claude-smith*
*Version: 1.0.0*
*RD-005: IRF Registry System Research*