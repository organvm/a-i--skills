# SOP-007: CLAUDE.md Generation Procedure

## Purpose
Standard procedure for generating CLAUDE.md files for repositories, ensuring consistent documentation structure across the organvm workspace.

## When
- New repository creation (with seed.yaml)
- Missing CLAUDE.md discovered during audit
- Manual regeneration requested
- On demand via `organvm generate claude <repo>`

---

## CLAUDE.md Structure

```
┌─────────────────────────────────────────────────────────────────────┐
│              STANDARD CLAUDE.md SECTIONS                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                 │
│  # CLAUDE.md — <REPO NAME>                                       │
│                                                                 │
│  ## Identity                                                    │
│  ## Architecture                                               │
│  ## Commands                                                   │
│  ## Development                                               │
│  ## Dependencies                                              │
│  ## Key Constraints                                            │
│  ## Structure                                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Generation Micro-Steps

### Phase 1: Identity Extraction

```
┌─────────────────────────────────────────────────────────────────┐
│ GENERATION MICRO-STEP 7.1.1: IDENTITY EXTRACTION              │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: yaml.parse + git                 TIMEOUT: 5s            │
│ SOURCE: seed.yaml                                           │
│ FIELDS: name, description, organ, scale, IRF, status        │
└─────────────────────────────────────────────────────────────────┘
```

#### Identity Template

```markdown
## Identity

- **Repo:** {{repo_full_name}}
- **Organ:** {{organ_name}} ({{organ_greek}})
- **Scale:** {{scale}}
- **IRF:** {{IRF}}
- **Status:** {{status}}
- **Governance:** {{governance_state}}
```

#### Organ Greek Mapping

```python
GREEK_NAMES = {
    "I": "Theoria",
    "II": "Kerygma",
    "III": "Publica",
    "IV": "Taxis",
    "V": "Ops",
    "VI": "Koinonia",
    "VII": "Kerygma",
    "Meta": "Meta"
}

GREEK_SYMBOLS = {
    "I": "θ",
    "II": "κ",
    "III": "π",
    "IV": "τ",
    "V": "ω",
    "VI": "κο",
    "VII": "ν",
    "Meta": "μ"
}
```

---

### Phase 2: Architecture Extraction

```
┌─���───────────────────────────────────────────────────────────────┐
│ GENERATION MICRO-STEP 7.2.1: ARCHITECTURE EXTRACTION             │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: read + glob                     TIMEOUT: 10s             │
│ SOURCE: README.md, docs/, src/                               │
│ EXTRACT: Overview, key components, tech stack               │
└─────────────────────────────────────────────────────────────────┘
```

#### Architecture Template

```markdown
## Architecture

{{#if tech_stack}}
### Tech Stack
{{tech_stack}}

{{/if}}
{{#if overview}}
### Overview
{{overview}}

{{/if}}
{{#if components}}
### Components
{{components}}

{{/if}}
```

#### Component Extraction

```python
def extract_components(path: str) -> list[str]:
    """Extract key components from directory structure."""
    components = []
    src_path = Path(path) / "src"
    
    if src_path.exists():
        for item in src_path.iterdir():
            if item.is_dir():
                components.append(f"- `{item.name}/`")
            elif item.is_file() and item.suffix in ['.py', '.ts', '.js']:
                components.append(f"- `{item.name}`")
    
    return components
```

---

### Phase 3: Commands Extraction

```
┌─────────────────────────────────────────────────────────────────┐
│ GENERATION MICRO-STEP 7.3.1: COMMANDS EXTRACTION                 │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: read + glob                     TIMEOUT: 10s             │
│ SOURCE: package.json, pyproject.toml, Makefile, CLI modules     │
│ EXTRACT: CLI commands, scripts, npm scripts                   │
└─────────────────────────────────────────────────────────────────┘
```

#### Commands Template

```markdown
## Commands

{{#if cli_commands}}
### CLI
{{cli_commands}}

{{/if}}
{{#if npm_scripts}}
### Scripts
{{npm_scripts}}

{{/if}}
{{#if make_targets}}
### Make
{{make_targets}}

{{/if}}
```

#### Commands Extraction Script

```python
import json
import tomli

def extract_commands(path: str) -> dict:
    """Extract commands from various config files."""
    commands = {"cli": [], "scripts": [], "make": []}
    path = Path(path)
    
    # package.json
    if (path / "package.json").exists():
        pkg = json.loads((path / "package.json").read_text())
        commands["scripts"] = pkg.get("scripts", {})
    
    # pyproject.toml
    if (path / "pyproject.toml").exists():
        try:
            proj = tomli.loads((path / "pyproject.toml").read_text())
            scripts = proj.get("project", {}).get("scripts", {})
            commands["cli"] = scripts
        except:
            pass
    
    # Makefile
    if (path / "Makefile").exists():
        content = (path / "Makefile").read_text()
        targets = re.findall(r'^(\w+):', content, re.MULTILINE)
        commands["make"] = targets
    
    return commands
```

---

### Phase 4: Development Extraction

```
┌─────────────────────────────────────────────────────────────────┐
│ GENERATION MICRO-STEP 7.4.1: DEVELOPMENT EXTRACTION            │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: read + glob                     TIMEOUT: 10s             │
│ SOURCE: README.md, CONTRIBUTING.md, .github/                 │
│ EXTRACT: Setup instructions, testing, contribution guidelines│
└─────────────────────────────────────────────────────────────────┘
```

#### Development Template

```markdown
## Development

### Setup
{{setup_instructions}}

### Testing
{{testing_instructions}}

### Linting
{{linting_instructions}}
```

#### Development Extraction Script

```python
def extract_development(path: str) -> dict:
    """Extract development instructions."""
    dev = {"setup": "", "testing": "", "linting": ""}
    path = Path(path)
    
    # README.md
    readme = path / "README.md"
    if readme.exists():
        content = readme.read_text()
        
        # Extract setup
        if "## Setup" in content:
            start = content.find("## Setup")
            end = content.find("\n## ", start + 1) or len(content)
            dev["setup"] = content[start:end].strip()
        
        # Extract testing
        if "## Test" in content:
            start = content.find("## Test")
            end = content.find("\n## ", start + 1) or len(content)
            dev["testing"] = content[start:end].strip()
    
    return dev
```

---

### Phase 5: Dependencies Extraction

```
┌─────────────────────────────────────────────────────────────────┐
│ GENERATION MICRO-STEP 7.5.1: DEPENDENCIES EXTRACTION          │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: read + yaml                     TIMEOUT: 5s             │
│ SOURCE: seed.yaml, requirements.txt, package.json            │
│ EXTRACT: Internal deps, external deps, organ dependencies    │
└─────────────────────────────────────────────────────────────────┘
```

#### Dependencies Template

```markdown
## Dependencies

{{#if internal_deps}}
### Internal
{{internal_deps}}

{{/if}}
{{#if external_deps}}
### External
{{external_deps}}

{{/if}}
```

#### Dependencies Extraction Script

```python
import yaml
import json

def extract_dependencies(path: str) -> dict:
    """Extract dependencies."""
    deps = {"internal": [], "external": []}
    path = Path(path)
    
    # seed.yaml
    seed = path / "seed.yaml"
    if seed.exists():
        data = yaml.safe_load(seed.read_text())
        for dep in data.get("dependencies", []):
            repo = dep.get("repo", "")
            if "organvm" in repo:
                deps["internal"].append(f"- [{repo}](../{repo})")
            else:
                deps["external"].append(f"- {repo}")
    
    return deps
```

---

### Phase 6: Structure Generation

```
┌─────────────────────────────────────────────────────────────────┐
│ GENERATION MICRO-STEP 7.6.1: STRUCTURE GENERATION             │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: tree + glob                    TIMEOUT: 10s             │
│ SOURCE: Directory listing                                   │
│ GENERATE: Tree representation                              │
└─────────────────────────────────────────────────────────────────┘
```

#### Structure Template

```markdown
## Structure

```
{{directory_tree}}
```
```

#### Structure Generation Script

```python
def generate_tree(path: str, max_depth: int = 3) -> str:
    """Generate directory tree."""
    output = []
    root = Path(path)
    
    def walk(dir_path: Path, prefix: str = "", depth: int = 0):
        if depth > max_depth:
            return
        
        items = sorted(dir_path.iterdir(), key=lambda x: (not x.is_dir(), x.name))
        for i, item in enumerate(items):
            if item.name.startswith('.'):
                continue
            
            connector = "└── " if i == len(items) - 1 else "├── "
            output.append(f"{prefix}{connector}{item.name}")
            
            if item.is_dir():
                new_prefix = prefix + ("    " if i == len(items) - 1 else "│   ")
                walk(item, new_prefix, depth + 1)
    
    output.append(root.name + "/")
    walk(root)
    
    return "\n".join(output)
```

---

## Complete Generation

```
┌─────────────────────────────────────────────────────────────────┐
│ GENERATION MICRO-STEP 7.7.1: COMPLETE GENERATION               │
├─────────────────────────────────────────────────────────────────┤
│ TOOL: composite                     TIMEOUT: 30s               │
│ RUNS ALL MICRO-STEPS AND ASSEMBLES COMPLETE FILE              │
└─────────────────────────────────────────────────────────────────┘
```

#### Generation Script

```python
def generate_claude_md(repo_path: str) -> str:
    """Generate complete CLAUDE.md."""
    
    # Phase 1: Identity
    seed_data = load_seed_yaml(repo_path)
    identity = generate_identity_section(seed_data)
    
    # Phase 2: Architecture
    architecture = generate_architecture_section(repo_path)
    
    # Phase 3: Commands
    commands = generate_commands_section(repo_path)
    
    # Phase 4: Development
    development = generate_development_section(repo_path)
    
    # Phase 5: Dependencies
    dependencies = generate_dependencies_section(repo_path)
    
    # Phase 6: Structure
    structure = generate_structure_section(repo_path)
    
    # Assemble
    content = f"""# CLAUDE.md — {seed_data['name']}

{identity}
{architecture}
{commands}
{development}
{dependencies}
{structure}
"""
    
    return content
```

---

## Template File

```
┌────────────────────���─���──────────────────────────────────────────┐
│              CLAUDE.MD TEMPLATE                                  │
├─────────────────────────────────────────────────────────────────┤
│  /templates/CLAUDE.md.template                              │
└─────────────────────────────────────────────────────────────────┘
```

```markdown
# CLAUDE.md — {{name}}

## Identity
- **Repo:** {{org}}/{{name}}
- **Organ:** {{organ}} ({{organ_greek}})
- **Scale:** {{scale}}
- **IRF:** {{IRF}}
- **Status:** {{status}}

## Architecture
{{architecture}}

## Commands
{{commands}}

## Development
{{development}}

## Dependencies
{{dependencies}}

## Key Constraints
{{constraints}}

## Structure
```
{{structure}}
```
```

---

## Validation

```bash
# Validate CLAUDE.md completeness
organvm validate claude <repo>

# Checks:
# □ Has all required sections
# □ Has minimum line count (50+)
# ✓ Has IRF reference
# ✓ Has seed.yaml reference
```

---

## Owner

- **Responsible**: organvm-IV-taxis/agent--claude-smith
- **Oversight**: organvm-corpvs-testamentvm

---

*Last updated: 2026-04-26*
*Version: 1.0.0*
*SOP-007: CLAUDE.md Generation Procedure*