# SOP-010: Multi-Repo Orchestration Procedure

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
│ TOOL: read seed.yaml + classify          TIMEOUT: 5s              │
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
    
    # Fallback: classify from path
    return classify_from_path(repo_path)
```

---

### Phase 2: Sequence Allocation

```
┌─────────────────────────────────────────────────────────────────┐
│ ASSIGNMENT MICRO-STEP 9.2.1: SEQUENCE ALLOCATION               │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: counter + lock               TIMEOUT: 10s              │
│ SOURCE: IRF registry                                    │
│ ALLOCATE: Next available sequence for organ               │
│ LOCK: Prevent race conditions                             │
└─────────────────────────────────────────────────────────────────┘
```

#### IRF Registry Structure

```python
# Global IRF Registry
# Stored in: organvm-corpvs-testamentvm/irf-registry.yaml

IRF_REGISTRY = {
    "THE": {"next": 1, "assigned": []},
    "KER": {"next": 1, "assigned": []},
    "PUB": {"next": 1, "assigned": []},
    "TAX": {"next": 1, "assigned": []},
    "OPS": {"next": 1, "assigned": []},
    "COM": {"next": 1, "assigned": []},
    "GOV": {"next": 1, "assigned": []},
    "META": {"next": 1, "assigned": []}
}

def allocate_sequence(organ_prefix: str) -> int:
    """Allocate next sequence for organ."""
    global IRF_REGISTRY
    
    if organ_prefix not in IRF_REGISTRY:
        raise ValueError(f"Unknown organ prefix: {organ_prefix}")
    
    next_seq = IRF_REGISTRY[organ_prefix]["next"]
    
    # Mark as assigned
    IRF_REGISTRY[organ_prefix]["assigned"].append(next_seq)
    IRF_REGISTRY[organ_prefix]["next"] = next_seq + 1
    
    return next_seq
```

---
<minimax:tool_call>
<invoke name="write">
<parameter name="content"># SOP-010: Multi-Repo Orchestration Procedure

## Purpose
Standard procedure for orchestrating operations across multiple repositories in the organvm workspace, enabling coordinated multi-repo workflows.

## When
- Bulk updates across organs
- Coordinated phase transitions
- Dependency chain updates
- Workspace-wide audits
- On demand via `organvm orchestrate <workflow>`

---

## Orchestration Patterns

```
┌─────────────────────────────────────────────────────────────────────┐
│              ORCHESTRATION PATTERNS                         │
├─────────────────────────────���─��─┬───────────────────────────┤
│ PATTERN                         │ DESCRIPTION              │
├─────────────────────────────────┼───────────────────────────┤
│ Sequential                     │ Run in order            │
│ Parallel                      │ Run simultaneously       │
│ Pipeline                      │ Output feeds input      │
│ Fan-out/Fan-in                │ One to many, collect    │
│ Scatter-gather                │ Distribute, aggregate   │
└─────────────────────────────────┴───────────────────────────┘
```

---

## Orchestration Micro-Steps

### Phase 1: Target Selection

```
┌─────────────────────────────────────────────────────────────────┐
│ ORCHESTRATION MICRO-STEP 10.1.1: TARGET SELECTION              │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: glob + filter               TIMEOUT: 30s              │
│ FILTERS: organ, status, scale, pattern                   │
│ OUTPUT: List of target repositories                  │
└─────────────────────────────────────────────────────────────────┘
```

#### Target Selection Script

```python
def select_targets(
    workspace: str,
    organ: str = None,
    status: str = None,
    scale: str = None,
    pattern: str = None
) -> list[str]:
    """Select target repositories based on filters."""
    targets = []
    
    for repo_path in Path(workspace).iterdir():
        if not repo_path.is_dir():
            continue
        
        seed = repo_path / "seed.yaml"
        if not seed.exists():
            continue
        
        data = yaml.safe_load(seed.read_text())
        
        # Apply filters
        if organ and data.get("organ") != organ:
            continue
        if status and data.get("status") != status:
            continue
        if scale and data.get("scale") != scale:
            continue
        if pattern and pattern not in repo_path.name:
            continue
        
        targets.append(str(repo_path))
    
    return targets
```

---

### Phase 2: Execution Planning

```
┌─────────────────────────────────────────────────────────────────┐
│ ORCHESTRATION MICRO-STEP 10.2.1: EXECUTION PLANNING            │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: topological_sort + parallelize   TIMEOUT: 20s           │
│ INPUT: Targets + dependency graph                         │
│ OUTPUT: Execution plan (sequence, parallelization)          │
└─────────────────────────────────────────────────────────────────┘
```

#### Execution Planning Script

```python
def plan_execution(targets: list[str], graph: dict[str, list[str]]) -> dict:
    """Create execution plan."""
    
    # Build execution levels
    levels = []
    remaining = set(targets)
    
    while remaining:
        # Find repos with no dependencies in remaining
        level = []
        for repo in remaining:
            deps = graph.get(repo, [])
            if not any(d in remaining for d in deps):
                level.append(repo)
        
        if not level:
            raise CircularDependencyError("Circular dependency detected")
        
        levels.append(level)
        remaining -= set(level)
    
    return {
        "total": len(targets),
        "levels": levels,
        "parallelizable": [len(l) for l in levels],
        "estimated_time": sum(len(l) * 60 for l in levels)  # Assume 60s per repo
    }
```

---

### Phase 3: Execution

```
┌─────────────────────────────────────────────────────────────────┐
│ ORCHESTRATION MICRO-STEP 10.3.1: PARALLEL EXECUTION            │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: asyncio + subprocess         TIMEOUT: Variable         │
│ INPUT: Execution plan                                 │
│ OUTPUT: Results + logs                                │
└─────────────────────────────────────────────────────────────────┘
```

#### Parallel Execution Script

```python
import asyncio

async def execute_parallel(targets: list[str], command: str) -> list[dict]:
    """Execute command on multiple targets in parallel."""
    
    async def run_on_target(target: str) -> dict:
        proc = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=target
        )
        stdout, stderr = await proc.communicate()
        
        return {
            "target": target,
            "returncode": proc.returncode,
            "stdout": stdout.decode(),
            "stderr": stderr.decode()
        }
    
    # Run all in parallel
    tasks = [run_on_target(t) for t in targets]
    results = await asyncio.gather(*tasks)
    
    return results
```

---

### Phase 4: Aggregation

```
┌─────────────────────────────────────────────────────────────────┐
│ ORCHESTRATION MICRO-STEP 10.4.1: RESULT AGGREGATION               │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: aggregate                  TIMEOUT: 10s              │
│ INPUT: Individual results                              │
│ OUTPUT: Summary + detailed logs                        │
└─────────────────────────────────────────────────────────────────┘
```

#### Aggregation Script

```python
def aggregate_results(results: list[dict]) -> dict:
    """Aggregate execution results."""
    
    summary = {
        "total": len(results),
        "success": 0,
        "failed": 0,
        "errors": []
    }
    
    for result in results:
        if result["returncode"] == 0:
            summary["success"] += 1
        else:
            summary["failed"] += 1
            summary["errors"].append({
                "target": result["target"],
                "error": result["stderr"]
            })
    
    return summary
```

---

## Predefined Workflows

### Workflow 1: Workspace Audit

```bash
organvm orchestrate audit \
  --organ=IV \
  --status=LOCAL \
  --output=audit/results
```

### Workflow 2: Bulk Seed Update

```bash
organvm orchestrate update-seed \
  --field=status \
  --value=CANDIDATE \
  --filter=organ=I
```

### Workflow 3: Dependency Chain Update

```bash
organvm orchestrate update-deps \
  --repo=organvm-iv-taxis/agent--claude-smith
```

### Workflow 4: Multi-Repo Phase Transition

```bash
organvm orchestrate phase-transition \
  --from=1A \
  --to=2A \
  --targets=repos.txt
```

---

## Performance

```
┌─────────────────────────────────────────────────────────────────┐
│              ORCHESTRATION PERFORMANCE                          │
├─────────────────────────────────────┬───────────────────┤
│ METRIC                            │ VALUE              │
├─────────────────────────────────────┼───────────────────┤
│ Max parallel repos                │ 10                 │
│ Timeout per repo                  │ 60s                │
│ Memory per task                   │ 100MB              │
│ Network rate limit                │ 10 req/s          │
└─────────────────────────────────────┴───────────────────┘
```

---

## Owner

- **Responsible**: organvm-IV-taxis/agent--claude-smith
- **Approver**: organvm-vii-kerygma/system-governance-framework
- **Oversight**: organvm-corpvs-testamentvm

---

*Last updated: 2026-04-26*
*Version: 1.0.0*
*SOP-010: Multi-Repo Orchestration Procedure*