# SOP-008: Dependency Mapping Procedure

## Purpose
Standard procedure for mapping, validating, and managing dependencies across the organvm workspace, ensuring the dependency graph remains acyclic and well-formed.

## When
- New dependency addition
- Audit (SOP-002)
- Dependency resolution failure
- On demand via `organvm deps map <repo>`

---

## Dependency Types

```
┌─────────────────────────────────────────────────────────────────────┐
│              DEPENDENCY TYPE SYSTEM                         │
├─────────────────────────────────────┬───────────────────┤
│ TYPE                              │ DESCRIPTION        │
├─────────────────────────────────────┼───────────────────┤
│ explicit                         │ Declared in        │
│                                 │ seed.yaml         │
│ implicit                        │ Import/require    │
│                                 │ statements       │
│ workflow                       │ CI/CD pipeline    │
│                                 │ references       │
│ asset                          │ File/asset       │
│                                 │ references       │
└─────────────────────────────────────┴───────────────────┘
```

---

## Mapping Micro-Steps

### Phase 1: Discovery

```
┌─────────────────────────────────────────────────────────────────┐
│ MAPPING MICRO-STEP 8.1.1: EXPLICIT DEPENDENCY DISCOVERY   │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: yaml.parse                  TIMEOUT: 5s            │
│ SOURCE: seed.yaml dependencies                        │
│ OUTPUT: List of explicit dependencies            │
└─────────────────────────────────────────────────────────────────┘
```

```python
def discover_explicit_deps(seed_path: str) -> list[dict]:
    """Discover explicit dependencies from seed.yaml."""
    deps = []
    
    with open(seed_path) as f:
        data = yaml.safe_load(f)
    
    for dep in data.get("dependencies", []):
        deps.append({
            "type": "explicit",
            "repo": dep["repo"],
            "assets": dep.get("assets", []),
            "optional": dep.get("optional", False)
        })
    
    return deps
```

---

```
┌─────────────────────────────────────────────────────────────────┐
│ MAPPING MICRO-STEP 8.1.2: IMPLICIT DEPENDENCY DISCOVERY │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: grep + parse                  TIMEOUT: 30s         │
│ SOURCE: requirements.txt, package.json, imports          │
│ OUTPUT: List of implicit dependencies                │
└─────────────────────────────────────────────────────────────────┘
```

#### Python Imports

```python
import re

PYTHON_IMPORT_PATTERN = re.compile(r'^(?:from|import)\s+([\w.]+)', re.MULTILINE)

def discover_python_deps(repo_path: str) -> list[str]:
    """Discover implicit Python dependencies."""
    deps = set()
    path = Path(repo_path)
    
    for py_file in path.glob("**/*.py"):
        if str(py_file).startswith(".venv/"):
            continue
        
        content = py_file.read_text()
        for match in PYTHON_IMPORT_PATTERN.finditer(content):
            module = match.group(1).split('.')[0]
            # Skip local modules
            if not module.startswith('_') and module not in {'organvm'}:
                deps.add(module)
    
    return list(deps)
```

#### JavaScript Imports

```python
JS_IMPORT_PATTERN = re.compile(r"(?:import|require)\s*['\"]([^'\"]+)['\"]", re.MULTILINE)

def discover_js_deps(repo_path: str) -> list[str]:
    """Discover implicit JS dependencies."""
    deps = set()
    path = Path(repo_path)
    
    for js_file in path.glob("**/*.{js,ts,mjs}"):
        content = js_file.read_text()
        for match in JS_IMPORT_PATTERN.finditer(content):
            module = match.group(1)
            if not module.startswith('.') and not module.startswith('@') is None:
                deps.add(module.split('/')[0])
    
    return list(deps)
```

---

```
┌─────────────────────────────────────────────────────────────────┐
│ MAPPING MICRO-STEP 8.1.3: WORKFLOW DEPENDENCY DISCOVERY  │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: yaml.parse + read             TIMEOUT: 10s           │
│ SOURCE: .github/workflows/*                           │
│ OUTPUT: List of workflow dependencies             │
└─────────────────────────────────────────────────────────────────┘
```

```python
def discover_workflow_deps(repo_path: str) -> list[dict]:
    """Discover workflow dependencies."""
    deps = []
    path = Path(repo_path) / ".github" / "workflows"
    
    if not path.exists():
        return deps
    
    for wf in path.glob("*.yml"):
        data = yaml.safe_load(wf.read_text())
        
        # Check uses statements
        for job in data.get("jobs", {}).values():
            for step in job.get("steps", []):
                if "uses" in step:
                    action = step["uses"].split("@")[0]
                    deps.append({
                        "type": "workflow",
                        "action": action,
                        "file": str(wf.name)
                    })
    
    return deps
```

---

### Phase 2: Resolution

```
┌─────────────────────────────────────────────────────────────────┐
│ MAPPING MICRO-STEP 8.2.1: DEPENDENCY RESOLUTION                 │
├─────────────────────────────────────────────��───────────────────┤
│ TOOL: path.resolve                 TIMEOUT: 10s           │
│ VERIFY: All dependencies exist                        │
│ OUTPUT: Resolution map with status                  │
└─────────────────────────────────────────────────────────────────┘
```

```python
WORKSPACE_ROOT = Path("/Users/4jp/Workspace/organvm")

def resolve_dependency(repo: str) -> dict:
    """Resolve a single dependency."""
    # Check if it's an organvm repo
    organvm_path = WORKSPACE_ROOT / repo
    if organvm_path.exists():
        return {"found": True, "path": str(organvm_path), "type": "internal"}
    
    # External - would need package manager resolution
    return {"found": False, "path": None, "type": "external"}

def resolve_all_dependencies(deps: list[dict]) -> list[dict]:
    """Resolve all dependencies."""
    results = []
    
    for dep in deps:
        result = resolve_dependency(dep["repo"])
        result.update({
            "declared_repo": dep["repo"],
            "declared_type": dep["type"]
        })
        results.append(result)
    
    return results
```

---

### Phase 3: Graph Construction

```
┌─────────────────────────────────────────────────────────────────┐
│ MAPPING MICRO-STEP 8.3.1: GRAPH CONSTRUCTION                   │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: composite                     TIMEOUT: 30s           │
│ BUILD: Full dependency graph (DAG)                       │
│ OUTPUT: Graph in DOT + JSON format                        │
└─────────────────────────────────────────────────────────────────┘
```

```python
def build_dependency_graph(workspace: str) -> tuple[dict, list[list[str]]]:
    """Build complete dependency graph."""
    graph = {}
    repos = []
    
    # Collect all repos
    for repo_path in Path(workspace).iterdir():
        if not repo_path.is_dir():
            continue
        
        seed = repo_path / "seed.yaml"
        if not seed.exists():
            continue
        
        repos.append(repo_path.name)
        
        # Get dependencies
        data = yaml.safe_load(seed.read_text())
        deps = [d["repo"] for d in data.get("dependencies", [])]
        graph[repo_path.name] = deps
    
    return graph, detect_cycles(graph)
```

---

### Phase 4: Cycle Detection

```
┌─────────────────────────────────────────────────────────────────┐
│ MAPPING MICRO-STEP 8.4.1: CYCLE DETECTION                      │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: dfs                       TIMEOUT: O(V+E)             │
│ VERIFY: No cycles in dependency graph                    │
│ OUTPUT: Any cycles found (should be none)                  │
└─────────────────────────────────────────────────────────────────┘
```

```python
def detect_cycles(graph: dict[str, list[str]]) -> list[list[str]]:
    """Detect cycles using DFS."""
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {node: WHITE for node in graph}
    parent = {node: None for node in graph}
    cycles = []
    
    def dfs(node: str) -> bool:
        color[node] = GRAY
        for neighbor in graph.get(node, []):
            if color.get(neighbor, WHITE) == GRAY:
                cycle = [neighbor, node]
                curr = parent[node]
                while curr != neighbor:
                    cycle.append(curr)
                    curr = parent[curr]
                cycles.append(cycle)
                return True
            elif color.get(neighbor, WHITE) == WHITE:
                parent[neighbor] = node
                if dfs(neighbor):
                    return True
        color[node] = BLACK
        return False
    
    for node in graph:
        if color[node] == WHITE:
            dfs(node)
    
    return cycles
```

---

### Phase 5: Impact Analysis

```
┌─────────────────────────────────────────────────────────────────┐
│ MAPPING MICRO-STEP 8.5.1: IMPACT ANALYSIS                    │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: graph traversal                TIMEOUT: O(V+E)          │
│ INPUT: Changed repo                                       │
│ OUTPUT: All repos that depend on it (downstream)            │
│        All repos it depends on (upstream)                │
└─────────────────────────────────────────────────────────────────┘
```

```python
def analyze_impact(repo: str, graph: dict[str, list[str]]) -> dict:
    """Analyze dependency impact."""
    
    # Find all downstream (repos that depend on this repo)
    downstream = []
    
    def find_downstream(current: str):
        for node, deps in graph.items():
            if current in deps and node not in downstream:
                downstream.append(node)
                find_downstream(node)
    
    # Find all upstream (repos this repo depends on)
    upstream = graph.get(repo, [])
    
    find_downstream(repo)
    
    return {
        "repo": repo,
        "upstream": upstream,
        "downstream": downstream,
        "impact_score": len(downstream)
    }
```

---

## Graph Visualization

```
┌─────────────────────────────────────────────────────────────────┐
│              DEPENDENCY GRAPH FORMATS                        │
├─────────────────────────────────────┬───────────────────┤
│ FORMAT                            │ TOOL             │
├─────────────────────────────────────┼───────────────────┤
│ DOT (GraphViz)                   │ graphviz          │
│ Mermaid                         │ mermaid           │
│ JSON                           │ json.dumps       │
│ CSV                             │ csv.writer       │
└─────────────────────────────────────┴───────────────────┘
```

#### DOT Export

```python
def export_dot(graph: dict[str, list[str]]) -> str:
    """Export dependency graph as DOT."""
    lines = ["digraph dependencies {"]
    lines.append('  rankdir=LR;')
    lines.append('  node [shape=box];')
    
    for repo, deps in graph.items():
        for dep in deps:
            lines.append(f'  {repo} -> {dep};')
    
    lines.append("}")
    return "\n".join(lines)
```

#### Mermaid Export

```python
def export_mermaid(graph: dict[str, list[str]]) -> str:
    """Export dependency graph as Mermaid."""
    lines = ["graph LR;"]
    
    for repo, deps in graph.items():
        for dep in deps:
            lines.append(f"  {repo}[{repo}] --> {dep}[{dep}]")
    
    return "\n".join(lines)
```

---

## Owner

- **Responsible**: organvm-IV-taxis/agent--claude-smith
- **Oversight**: organvm-corpvs-testamentvm

---

*Last updated: 2026-04-26*
*Version: 1.0.0*
*SOP-008: Dependency Mapping Procedure*