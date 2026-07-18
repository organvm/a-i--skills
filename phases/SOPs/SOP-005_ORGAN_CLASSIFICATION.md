# SOP-005: Organ Classification Procedure

## Purpose
Standard procedure for classifying repositories into the seven-organs-plus-Meta system, ensuring consistent taxonomy across the entire organvm workspace.

## When
- New repository creation
- Audit discovering unclassified repos
- On demand via `organvm classify <repo>`

---

## Organ Taxonomy

```
┌─────────────────────────────────────────────────────────────────────┐
│                    ORGANVM ORGAN SYSTEM                       │
├─────┬───────────────┬──────────────┬─────────────────────────┤
│ ORG │ GREEK TERM   │ ENGLISH     │ FUNCTION               │
├─────┼─────────────┼────────────┼─────────────────────────┤
│ I   │ Theoria    │ Knowledge  │ Ontology, taxonomy     │
│ II  │ Kerygma    │ Creative  │ Content, expression    │
│ III │ Publica    │ Publishing│ Distribution, public    │
│ IV  │ Taxis      │ Orchestration│ Agents, coordination │
│ V   │ Ops       │ Operations│ Tools, infrastructure  │
│ VI   │ Koinonia   │ Community │ Social, collaboration  │
│ VII  │ Kerygma    │ Governance│ Law, standards       │
│ Meta │ Meta      │ Meta     │ Cross-organ, system     │
└─────┴─────────────┴────────────┴─────────────────────────┘
```

---

## Organ Characteristics

### ORGAN-I: Theoria (Knowledge)

```
┌─────────────────────────────────────────────────────────────────┐
│ ORGAN-I: THEORIA - ONTOLOGY & TAXONOMY                        │
├─────────────────────────────────────────────────────────────────┤
│ Symbol: θ (theta)                                         │
│ Domain: Ontological structures, knowledge graphs            │
│ Repos: ~26                                               │
│ Flagship: organvm-ontologia                               │
│ Scale typical: σ_E → σ_O                                  │
│ Keywords: ontology, taxonomy, schema, knowledge, IRF        │
└─────────────────────────────────────────────────────────────────┘
```

| Characteristic | Value |
|----------------|-------|
| Primary function | Knowledge organization |
| Typical output | Schemas, taxonomies, definitions |
| Dependencies | Minimal (self-contained) |
| CI needs | Low |
| Public facing | Rare |

**Example repos:**
- `organvm-ontologia`
- `nexus--babel-alexandria`
- `schema-definitions`
- `linguistic-atomization-framework`

---

### ORGAN-II: Kerygma (Creative)

```
┌─────────────────────────────────────────────────────────────────┐
│ ORGAN-II: KERYGMA - CREATIVE & EXPRESSION                       │
├───────────────────────────────────��─────────────────────────────┤
│ Symbol: κ (kappa)                                           │
│ Domain: Creative output, algorithmic art, essays              │
│ Repos: ~32                                                 │
│ Flagship: sema-metra--alchemica-mundi                       │
│ Scale typical: σ_E                                         │
│ Keywords: creative, art, essay, narrative, pipeline          │
└─────────────────────────────────────────────────────────────────┘
```

| Characteristic | Value |
|----------------|-------|
| Primary function | Creative generation |
| Typical output | Art, essays, narratives |
| Dependencies | Minimal (standalone) |
| CI needs | Custom |
| Public facing | Sometimes |

**Example repos:**
- `sema-metra--alchemica-mundi`
- `alchemical-synthesizer`
- `essay-pipeline`
- `materia-collider`

---

### ORGAN-III: Publica (Publishing)

```
┌─────────────────────────────────────────────────────────────────┐
│ ORGAN-III: PUBLICA - DISTRIBUTION & PUBLISHING                  │
├─────────────────────────────────────────────────────────────────┤
│ Symbol: π (pi)                                             │
│ Domain: Publishing, distribution, syndication                 │
│ Repos: ~32                                                 │
│ Flagship: kerygma-pipeline                                │
│ Scale typical: σ_O → σ_P                                   │
│ Keywords: publish, syndicate, distribution, RSS, POSSE        │
└─────────────────────────────────────────────────────────────────┘
```

| Characteristic | Value |
|----------------|-------|
| Primary function | Content distribution |
| Typical output | Published content, feeds |
| Dependencies | Moderate |
| CI needs | High (reliability) |
| Public facing | Often |

**Example repos:**
- `kerygma-pipeline`
- `content-engine--asset-amplifier`
- `distribution-strategy`
- `vox--publica`

---

### ORGAN-IV: Taxis (Orchestration)

```
┌─────────────────────────────────────────────────────────────────┐
│ ORGAN-IV: TAXIS - ORCHESTRATION & AGENTS                    │
├─────────────────────────────────────────────────────────────────┤
│ Symbol: τ (tau)                                            │
│ Domain: Multi-agent systems, orchestration, workflows      │
│ Repos: ~22                                                 │
│ Flagship: agent--claude-smith                              │
│ Scale typical: σ_O → σ_P                                   │
│ Keywords: agent, orchestration, workflow, MCP, swarm        │
└─────────────────────────────────────────────────────────────────┘
```

| Characteristic | Value |
|----------------|-------|
| Primary function | Orchestration |
| Typical output | Executed workflows |
| Dependencies | High |
| CI needs | Very high |
| Public facing | Sometimes |

**Example repos:**
- `agent--claude-smith`
- `orchestration-start-here`
- `recursive-engine--generative-entity`
- `tool-interaction-design`

---

### ORGAN-V: Ops (Operations)

```
┌─────────────────────────────────────────────────────────────────┐
│ ORGAN-V: OPS - TOOLS & INFRASTRUCTURE                       │
├─────────────────────────────────────────────────────────────────┤
│ Symbol: ω (omega)                                         │
│ Domain: CLI tools, utilities, infrastructure                │
│ Repos: ~6                                                 │
│ Flagship: call-function--ontological                      │
│ Scale typical: σ_O → σ_P                                  │
│ Keywords: cli, tool, utility, infrastructure           │
└─────────────────────────────────────────────────────────────────┘
```

| Characteristic | Value |
|----------------|-------|
| Primary function | Operations |
| Typical output | CLI tools |
| Dependencies | Minimal |
| CI needs | Medium |
| Public facing | Sometimes |

**Example repos:**
- `call-function--ontological`
- `system-dashboard`
- `analytics-engine`
- `commerce--meta`

---

### ORGAN-VI: Koinonia (Community)

```
┌─────────────────────────────────────────────────────────────────┐
│ ORGAN-VI: KOINONIA - COMMUNITY & SOCIAL                          │
├─────────────────────────────────────────────────────────────────┤
│ Symbol: κο (kappa-omicron)                                   │
│ Domain: Social features, collaboration, community            │
│ Repos: ~6                                                  │
│ Flagship: community-hub                                    │
│ Scale typical: σ_O                                           │
│ Keywords: community, social, collaboration, portal         │
└─────────────────────────────────────────────────────────────────┘
```

| Characteristic | Value |
|----------------|-------|
| Primary function | Community building |
| Typical output | Platforms, portals |
| Dependencies | Moderate |
| CI needs | Medium |
| Public facing | Often |

**Example repos:**
- `community-hub`
- `stakeholder-portal`
- `salon-archive`
- `koinonia-db`

---

### ORGAN-VII: Kerygma (Governance)

```
┌─────────────────────────────────────────────────────────────────┐
│ ORGAN-VII: KERYGMA - GOVERNANCE & STANDARDS                      │
├─────────────────────────────────────────────────────────────────┤
│ Symbol: ν (nu)                                               │
│ Domain: Standards, governance, law                         │
│ Repos: ~6                                                  │
│ Flagship: system-governance-framework                      │
│ Scale typical: σ_O                                          │
│ Keywords: governance, standard, policy, law, FR, SOP          │
└─��─��─────────────────────────────────────────────────────────────┘
```

| Characteristic | Value |
|----------------|-------|
| Primary function | Governance |
| Typical output | Standards, procedures |
| Dependencies | None |
| CI needs | Low |
| Public facing | Rare |

**Example repos:**
- `system-governance-framework`
- `rules-system-bound`
- `public-process`
- `cvrsvs-honorvm`

---

### META: Meta-Organvm

```
┌─────────────────────────────────────────────────────────────────┐
│ META: META-ORGANVM - CROSS-ORGAN SYSTEM                      │
├─────────────────────────────────────────────────────────────────┤
│ Symbol: μ (mu)                                             │
│ Domain: System-level, cross-organ                           │
│ Repos: ~13                                                │
│ Flagship: organvm-corpvs-testamentvm                        │
│ Scale typical: σ_E → σ_P                                 │
│ Keywords: system, cross-organ, registry, meta               │
└─────────────────────────────────────────────────────────────────┘
```

| Characteristic | Value |
|----------------|-------|
| Primary function | System operation |
| Typical output | System infrastructure |
| Dependencies | All organs |
| CI needs | High |
| Public facing | Rare |

**Example repos:**
- `organvm-corpvs-testamentvm`
- `organvm-mcp-server`
- `organvm-aerarium`
- `a-i--skills`

---

## Classification Micro-Steps

### Phase 1: Path Analysis

```
┌─────────────────────────────────────────────────────────────────┐
│ CLASSIFICATION MICRO-STEP 5.1.1: PATH PARSING               │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: path.parse                  TIMEOUT: 1s              │
│ INPUT: Repo name, directory path, git remote              │
│ EXTRACT: Organ signals from name, path patterns           │
└─────────────────────────────────────────────────────────────────┘
```

#### Name Pattern Analysis

```python
ORGAN_SIGNALS = {
    "theoria": "I", "ontology": "I", "knowledge": "I",
    "kerygma": "II", "creative": "II", "content": "II",
    "publica": "III", "publish": "III", "distribution": "III",
    "taxis": "IV", "orchestration": "IV", "agent": "IV",
    "ops": "V", "tool": "V", "cli": "V",
    "koinonia": "VI", "community": "VI", "social": "VI",
    "governance": "VII", "standard": "VII", "rule": "VII",
    "meta": "Meta", "system": "Meta", "corpus": "Meta"
}

def classify_from_name(name: str) -> str | None:
    """Infer organ from repo name."""
    name_lower = name.lower()
    for signal, organ in ORGAN_SIGNALS.items():
        if signal in name_lower:
            return organ
    return None
```

---

```
┌─────────────────────────────────────────────────────────────────┐
│ CLASSIFICATION MICRO-STEP 5.1.2: DIRECTORY ANALYSIS         │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: ls + glob                   TIMEOUT: 3s              │
│ INPUT: Directory structure, file types, key files           │
│ ANALYZE: src/, tests/, docs/, .github/ patterns            │
└─────────────────────────────────────────────────────────────────┘
```

#### Directory Pattern Analysis

```python
DIRECTORY_PATTERNS = {
    ("src/", "agents/"): "IV",
    ("src/", "workflows/"): "IV",
    ("tests/",): "IV",
    ("docs/", "essays/"): "II",
    ("content/", "pieces/"): "III",
    ("schema/", "ontology/"): "I",
    ("governance/", "policies/"): "VII",
    ("tools/", "cli/"): "V",
    ("community/", "social/"): "VI",
}

def classify_from_directory(path: str) -> str | None:
    """Infer organ from directory structure."""
    dirs = set(Path(path).iterdir())
    for pattern, organ in DIRECTORY_PATTERNS.items():
        if all(p in dirs for p in pattern):
            return organ
    return None
```

---

### Phase 2: Content Analysis

```
┌─────────────────────────────────────────────────────────────────┐
│ CLASSIFICATION MICRO-STEP 5.2.1: README ANALYSIS            │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: read + nlp                   TIMEOUT: 5s              │
│ INPUT: README.md, seed.yaml description                   │
│ EXTRACT: Domain keywords, purpose, audience             │
└─────────────────────────────────────────────────────────────────┘
```

#### Text Content Analysis

```python
PURPOSE_KEYWORDS = {
    "generate": "II", "create": "II", "compose": "II",
    "publish": "III", "distribute": "III", "syndicate": "III",
    "orchestrate": "IV", "coordinate": "IV", "manage": "IV",
    "define": "I", "structure": "I", "model": "I",
    "govern": "VII", "enforce": "VII", "validate": "V",
    "connect": "VI", "collaborate": "VI", "share": "VI",
}

def classify_from_purpose(text: str) -> str | None:
    """Infer organ from purpose text."""
    # Simplified keyword matching
    words = text.lower().split()
    for word, organ in PURPOSE_KEYWORDS.items():
        if word in words:
            return organ
    return None
```

---

```
┌─────────────────────────────────────────────────────────────────┐
│ CLASSIFICATION MICRO-STEP 5.2.2: DEPENDENCY ANALYSIS         │
├─────────────────────────���─���─────────────────────────────────────┤
│ TOOL: read + graph                TIMEOUT: 5s              │
│ INPUT: requirements.txt, package.json, seed.yaml deps        │
│ ANALYZE: Dependency graph, import patterns              │
└─────────────────────────────────────────────────────────────────┘
```

#### Dependency Analysis

```python
ORGAN_DEPENDENCIES = {
    "I": ["ontologia", "schema", "taxonomy", "knowledge"],
    "II": ["creative", "art", "essay", "narrative"],
    "III": ["publish", "syndicate", "rss", "feed"],
    "IV": ["agent", "orchestrate", "workflow", "mcp"],
    "V": ["cli", "tool", "utility"],
    "VI": ["community", "social", "portal"],
    "VII": ["governance", "standard", "policy"],
}

def classify_from_dependencies(deps: list[str]) -> str | None:
    """Infer organ from dependency names."""
    dep_string = " ".join(deps).lower()
    for keyword, organ in ORGAN_DEPENDENCIES.items():
        if any(kw in dep_string for kw in keyword):
            return organ
    return None
```

---

### Phase 3: Composite Classification

```
┌─────────────────────────────────────────────────────────────────┐
│ CLASSIFICATION MICRO-STEP 5.3.1: WEIGHTED COMPOSITE         │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: composite                  TIMEOUT: 10s             │
│ WEIGHT: Path 40%, Directory 20%, Purpose 25%, Deps 15%    │
│ OUTPUT: Classification + confidence score                 │
└─────────────────────────────────────────────────────────────────┘
```

#### Weighted Classification Algorithm

```python
def classify_repo(path: str) -> dict:
    """Run complete classification."""
    weights = {"path": 0.40, "directory": 0.20, "purpose": 0.25, "dependencies": 0.15}
    scores = {organ: 0.0 for organ in VALID_ORGANS}
    
    # Path analysis (40%)
    organ = classify_from_name(Path(path).name)
    if organ:
        scores[organ] += weights["path"]
    
    # Directory analysis (20%)
    organ = classify_from_directory(path)
    if organ:
        scores[organ] += weights["directory"]
    
    # Purpose analysis (25%)
    readme_path = Path(path) / "README.md"
    if readme_path.exists():
        organ = classify_from_purpose(readme_path.read_text())
        if organ:
            scores[organ] += weights["purpose"]
    
    # Dependency analysis (15%)
    deps = extract_dependencies(path)
    organ = classify_from_dependencies(deps)
    if organ:
        scores[organ] += weights["dependencies"]
    
    # Return highest scoring organ
    best_organ = max(scores, key=scores.get)
    confidence = scores[best_organ]
    
    return {
        "organ": best_organ,
        "confidence": confidence,
        "all_scores": scores
    }
```

---

## Classification Decision Tree

```
┌─────────────────────────────────────────────────────────────────┐
│              CLASSIFICATION DECISION TREE                    │
├─────────────────────────────────────────────────────────────────┤
│                                                         │
│  START: New repository discovered                        │
│    │                                                   │
│    ▼                                                   │
│  ┌─────────────────┐                                   │
│  │ Has seed.yaml?  │───NO──▶ Classify by seed.yaml organ │
│  └────────┬────────┘                                  │
│          │YES                                          │
│          ▼                                            │
│  ┌─────────────────┐                                   │
│  │ seed.yaml has   │───YES──▶ Use seed.yaml organ    │
│  │ organ field?   │                                   │
│  └────────┬────────┘                                  │
│          │NO                                           │
│          ▼                                            │
│  ┌─────────────────┐                                   │
│  │ Name contains   │───YES──▶ Use name signal         │
│  │ organ signal?  │                                   │
│  └────────┬────────┘                                  │
│          │NO                                           │
│          ▼                                            │
│  ┌─────────────────┐                                   │
│  │ Directory has   │───YES──▶ Use directory pattern│
│  │ pattern?      │                                   │
│  └────────┬────────┘                                  │
│          │NO                                           │
│          ▼                                            │
│  ┌─────────────────┐                                   │
│  │ README has     │───YES──▶ Use purpose keywords  │
│  │ keywords?     │                                   │
│  └────────┬────────┘                                  │
│          │NO                                           │
│          ▼                                            │
│  ┌─────────────────┐                                   │
│  │ Dependencies  │───YES──▶ Use dependency graph │
│  │ indicate?    │                                   │
│  └────────┬────────┘                                  │
│          │NO                                           │
│          ▼                                            │
│  ESCALATE: Request manual classification               │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## Verification

```bash
# Verify organ classification
organvm classify verify <repo>

# Output:
# {
#   "organ": "IV",
#   "confidence": 0.85,
#   "method": "weighted_composite",
#   "all_scores": {"I": 0.0, "II": 0.1, "III": 0.0, "IV": 0.85, "V": 0.0, "VI": 0.0, "VII": 0.0, "Meta": 0.05}
# }
```

---

## Manual Override

```bash
# Override classification (requires justification)
organvm classify set <repo> --organ=IV --reason="Multi-agent orchestration system"

# This will:
# 1. Update seed.yaml organ field
# 2. Move repo to correct directory if needed
# 3. Log override with reason
# 4. Update registry
```

---

## Owner

- **Responsible**: organvm-IV-taxis/agent--claude-smith
- **Approver**: organvm-vii-kerygma/system-governance-framework
- **Oversight**: organvm-corpvs-testamentvm

---

*Last updated: 2026-04-26*
*Version: 1.0.0*
*SOP-005: Organ Classification Procedure*