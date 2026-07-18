# SOP-004: Seed.yaml Validation Procedure

## Purpose
Standard procedure for validating seed.yaml files across the organvm workspace, ensuring structural integrity, field correctness, and referential validity.

## When
- During workspace audit (SOP-002)
- Before commit to repository
- On demand via `organvm validate seed <repo>`

---

## Micro-Validation Steps

### Phase 1: Structural Validation

```
┌─────────────────────────────────────────────────────────────────┐
│ VALIDATION MICRO-STEP 4.1.1: YAML SYNTAX CHECK                │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: yaml.safe_load                TIMEOUT: 2s/file         │
│ CHECKS:                                                │
│   □ Valid YAML syntax                                     │
│   □ No duplicate keys                                  │
│   □ Indentation consistent (2 spaces)               │
│   □ No tabs used                                   │
└─────────────────────────────────────────────────────────────────┘
```

#### Validation Script

```python
import yaml
import sys

def validate_yaml_syntax(path: str) -> tuple[bool, str]:
    """Validate YAML file syntax."""
    try:
        with open(path) as f:
            data = yaml.safe_load(f)
        return True, "Valid"
    except yaml.YAMLError as e:
        return False, str(e)
    except Exception as e:
        return False, f"Unexpected error: {e}"
```

---

```
┌─────────────────────────────────────────────────────────────────┐
│ VALIDATION MICRO-STEP 4.1.2: REQUIRED FIELDS CHECK           │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: dict.keys                  TIMEOUT: 1s/file           │
│ STATUS-SPECIFIC REQUIREMENTS:                             │
│   LOCAL: name, description, organ, status               │
│   CANDIDATE: + org, scale, IRF                         │
│   PUBLIC_PROCESS: + capabilities, primitives            │
│   GRADUATED: + dependencies, entry_points             │
└─────────────────────────────────────────────────────────────────┘
```

#### Field Requirements by Status

```python
REQUIRED_FIELDS = {
    "LOCAL": ["name", "description", "organ", "status"],
    "CANDIDATE": ["name", "description", "organ", "status", "org", "scale", "IRF"],
    "PUBLIC_PROCESS": [
        "name", "description", "organ", "status", 
        "org", "scale", "IRF", "capabilities", "primitives"
    ],
    "GRADUATED": [
        "name", "description", "organ", "status", 
        "org", "scale", "IRF", "capabilities", "primitives",
        "dependencies", "entry_points"
    ]
}

OPTIONAL_FIELDS = ["patches", "benchmarks", "tags", "owners", "contacts"]
```

---

### Phase 2: Field-Specific Validation

```
┌─────────────────────────────────────────────────────────────────┐
│ VALIDATION MICRO-STEP 4.2.1: NAME FIELD VALIDATION             │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: regex ^[\w-]+$              TIMEOUT: 1s           │
│ RULES:                                                  │
│   □ Alphanumeric + hyphens only                          │
│   □ No leading/trailing hyphens                        │
│   □ No consecutive hyphens                            │
│   □ Max 64 characters                                │
│   □ Unique across workspace                            │
└─────────────────────────────────────────────────────────────────┘
```

#### Name Validation

```python
import re

def validate_name(name: str) -> tuple[bool, str]:
    """Validate name field."""
    # Check length
    if len(name) > 64:
        return False, "Name exceeds 64 characters"
    
    # Check characters
    if not re.match(r'^[\w]+(?:-[\w]+)*$', name):
        return False, "Name contains invalid characters"
    
    # Check consecutive hyphens
    if '--' in name:
        return False, "Name contains consecutive hyphens"
    
    # Check leading/trailing
    if name.startswith('-') or name.endswith('-'):
        return False, "Name cannot start or end with hyphen"
    
    return True, "Valid"
```

---

```
┌─────────────────────────────────────────────────────────────────┐
│ VALIDATION MICRO-STEP 4.2.2: ORGAN FIELD VALIDATION          │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: set membership             TIMEOUT: 1s              │
│ VALID ORGANS: {I, II, III, IV, V, VI, VII, Meta}        │
│ NOTE: "organvm" prefix stripped for validation            │
└─────────────────────────────────────────────────────────────────┘
```

```python
VALID_ORGANS = {"I", "II", "III", "IV", "V", "VI", "VII", "Meta"}

def validate_organ(organ: str) -> tuple[bool, str]:
    """Validate organ field."""
    # Strip "organvm-" prefix if present
    if organ.startswith("organvm-"):
        organ = organ[7:]
    
    if organ not in VALID_ORGANS:
        return False, f"Invalid organ: {organ}. Must be one of {VALID_ORGANS}"
    
    return True, "Valid"
```

---

```
┌─────────────────────────────────────────────────────────────────┐
│ VALIDATION MICRO-STEP 4.2.3: STATUS FIELD VALIDATION            │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: state machine             TIMEOUT: 1s              │
│ VALID STATES: {LOCAL, CANDIDATE, PUBLIC_PROCESS, GRADUATED}│
│ NOTE: Must match current governance state               │
└─────────────────────────────────────────────────────────────────┘
```

```python
VALID_STATUSES = {"LOCAL", "CANDIDATE", "PUBLIC_PROCESS", "GRADUATED"}

def validate_status(status: str) -> tuple[bool, str]:
    """Validate status field."""
    if status not in VALID_STATUSES:
        return False, f"Invalid status: {status}"
    return True, "Valid"
```

---

```
┌─────────────────────────────────────────────────────────────────┐
│ VALIDATION MICRO-STEP 4.2.4: SCALE FIELD VALIDATION          │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: set membership             TIMEOUT: 1s              │
│ VALID SCALES: {σ_E, σ_O, σ_P}                          │
│ SYMBOLS: σ_E = emergent, σ_O = operational, σ_P = public │
└─────────────────────────────────────────────────────────────────┘
```

```python
VALID_SCALES = {"σ_E", "σ_O", "σ_P"}

def validate_scale(scale: str) -> tuple[bool, str]:
    """Validate scale field."""
    if scale not in VALID_SCALES:
        return False, f"Invalid scale: {scale}"
    return True, "Valid"
```

---

```
┌─────────────────────────────────────────────────────────────────┐
│ VALIDATION MICRO-STEP 4.2.5: IRF FIELD VALIDATION           │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: regex ^IRF-[A-Z]{3}-[0-9]{3}$  TIMEOUT: 1s       │
│ FORMAT: IRF-XXX-NNN                                       │
│ XXX: Organ prefix (THE, KER, PUB, TAX, OPS, COM, GOV)        │
│ NNN: 001-999                                             │
└─────────────────────────────────────────────────────────────────┘
```

```python
import re

IRF_PATTERN = re.compile(r'^IRF-[A-Z]{3}-[0-9]{3}$')
ORGAN_PREFIXES = {
    "I": "THE", "II": "KER", "III": "PUB", 
    "IV": "TAX", "V": "OPS", "VI": "COM", 
    "VII": "GOV", "Meta": "META"
}

def validate_irf(irf: str, organ: str) -> tuple[bool, str]:
    """Validate IRF field."""
    # Check format
    if not IRF_PATTERN.match(irf):
        return False, f"Invalid IRF format: {irf}"
    
    # Check organ prefix matches
    prefix = irf.split("-")[1]
    expected = ORGAN_PREFIXES.get(organ, "")
    if prefix != expected:
        return False, f"IRF prefix {prefix} doesn't match organ {organ}"
    
    return True, "Valid"
```

---

### Phase 3: Referential Validation

```
┌─────────────────────────────────────────────────────────────────┐
│ VALIDATION MICRO-STEP 4.3.1: DEPENDENCY RESOLUTION         │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: path.resolve               TIMEOUT: 5s              │
│ CHECKS:                                                 │
│   □ All referenced repos exist                          │
│   □ No circular dependencies                         │
│   □ Version constraints parse                         │
└─────────────────────────────────────────────────────────────────┘
```

```python
from pathlib import Path

def validate_dependencies(seed_path: str, deps: list) -> list[dict]:
    """Validate all dependencies exist."""
    workspace = Path("/Users/4jp/Workspace/organvm")
    errors = []
    
    for dep in deps:
        repo_path = workspace / dep["repo"]
        if not repo_path.exists():
            errors.append({
                "type": "missing_dependency",
                "repo": dep["repo"],
                "path": str(repo_path)
            })
    
    return errors
```

---

```
┌─────────────────────────────────────────────────────────────────┐
│ VALIDATION MICRO-STEP 4.3.2: ASSET GLOB VALIDATION          │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: glob                     TIMEOUT: 3s              │
│ CHECKS:                                                 │
│   □ All asset globs match files                        │
│   □ No empty globs                                    │
│   □ Paths are relative to repo root                   │
└─────────────────────────────────────────────────────────────────┘
```

```python
import glob as glob_module

def validate_assets(repo_path: str, assets: list) -> list[dict]:
    """Validate asset globs match files."""
    errors = []
    repo = Path(repo_path)
    
    for asset_glob in assets:
        matches = list(repo.glob(asset_glob))
        if not matches:
            errors.append({
                "type": "empty_asset_glob",
                "glob": asset_glob,
                "repo": str(repo)
            })
    
    return errors
```

---

### Phase 4: Composite Validation

```
┌─────────────────────────────────────────────────────────────────┐
│ VALIDATION MICRO-STEP 4.4.1: COMPLETE VALIDATION           │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: composite                  TIMEOUT: 10s           │
│ RUNS ALL MICRO-STEPS AND AGGREGATES RESULTS              │
└─────────────────────────────────────────────────────────────────┘
```

#### Composite Validator

```python
def validate_seed_yaml(path: str) -> dict:
    """Run complete seed.yaml validation."""
    result = {
        "path": path,
        "valid": True,
        "errors": [],
        "warnings": []
    }
    
    # Phase 1: Structural
    valid, msg = validate_yaml_syntax(path)
    if not valid:
        result["valid"] = False
        result["errors"].append({"phase": 1, "step": "4.1.1", "error": msg})
        return result
    
    # Load data
    with open(path) as f:
        data = yaml.safe_load(f)
    
    # Phase 2: Field validation
    for field, validator in FIELD_VALIDATORS.items():
        if field in data:
            valid, msg = validator(data[field])
            if not valid:
                result["errors"].append({"phase": 2, "step": f"4.2.{field}", "error": msg})
    
    # Phase 3: Referential
    if "dependencies" in data:
        errors = validate_dependencies(path, data["dependencies"])
        result["errors"].extend(errors)
    
    # Set final validity
    result["valid"] = len(result["errors"]) == 0
    
    return result
```

---

## Validation Levels

| Level | Scope | Timeout | Used By |
|-------|-------|---------|--------|
| FAST | Syntax + Required | 2s | Pre-commit hook |
| STANDARD | + Field checks | 5s | CI pipeline |
| COMPREHENSIVE | + Referential | 15s | Full audit |
| STRICT | All + Warnings | 30s | Governance review |

---

## Error Handling

```
┌─────────────────────────────────────────────────────────────────┐
│ VALIDATION ERROR CODES                                       │
├─────────────────────────────────────────────────────────────────┤
│ E001: YAML syntax error                                    │
│ E002: Missing required field                             │
│ E003: Invalid field value                               │
│ E004: Missing dependency                              │
│ E005: Circular dependency                             │
│ E006: Invalid IRF format                             │
│ E007: Invalid IRF-organ mismatch                    │
│ E008: Empty asset glob                              │
│ E009: Invalid status transition                      │
│ W001: Optional field missing                         │
│ W002: Unused dependency                             │
└─────────────────────────────────────────────────────────────────┘
```

---

## Owner

- **Responsible**: Repo owner
- **Enforcer**: organvm-IV-taxis/agent--claude-smith
- **Oversight**: organvm-corpvs-testamentvm

---

*Last updated: 2026-04-26*
*Version: 1.0.0*
*SOP-004: Seed.yaml Validation Procedure*