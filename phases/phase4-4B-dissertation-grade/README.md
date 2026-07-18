# PHASE 4B: Dissertation-Grade Atlas

## Metadata
- **Phase**: 4B
- **Decision**: Dissertation-grade (research-backed, peer-reviewed sources)
- **Status**: DRAFT
- **Created**: 2026-04-26
- **Parent**: PHASE_4_DEPTH

## The Ask

Full research atlas with:
- Methodological rigor
- Exact peer-reviewed sources (30-80)
- Reading ladder
- Experiment design templates

## Research Atlas Structure

### Pillar 1: Causal Inference

```
The causal model underpinning the transformation engine.
How we prove X → Y (not just correlation).
```

#### Core Sources (Target: 20-30)

| Source | Topic | Citation |
|---|---|---|
| Pearl (2009) | Causal inference theory | *Causality* |
| Morgan & Winship (2014) | Counterfactuals | *Counterfactuals and Causal Inference* |
| Imbens & Rubin (2015) | Causal inference in practice | *Causal Inference for Statistics* |
| Angrist et al. | IV methods | Multiple |

#### Reading Ladder
1. Pearl入门 (Ch. 1-3)
2. Morgan & Winship (Ch. 1-4)
3. Imbens & Rubin (Ch. 12-15)
4. Advanced: Pearl (Ch. 7-11)

### Pillar 2: Unit Economics

```
The economic model underpinning the transformation economy.
How we measure ROI, LTV, CAC.
```

#### Core Sources (Target: 15-25)

| Source | Topic | Citation |
|---|---|---|
| Damodaran | Valuation | *Damodaran on Valuation* |
| bland | Unit economics | Various SaaS papers |
| Huberman | SaaS metrics | *Business Metrics* |

#### Reading Ladder
1. SaaS Metrics 101
2. Unit Economics Basics
3. Customer Economics
4. Advanced: LTV modeling

### Pillar 3: Algorithmic Interface

```
The computational model underpinning the transformation engine.
How we compute, scale, optimize.
```

#### Core Sources (Target: 20-30)

| Source | Topic | Citation |
|---|---|---|
| Manning & Raghavan | Information Retrieval | *Introduction to IR* |
| Goodfellow et al. | Deep Learning | *Deep Learning* |
| Bishop | Pattern Recognition | *Pattern Recognition* |
| Russell & Norvig | AI | *Artificial Intelligence* |

#### Reading Ladder
1. IR Foundations
2. ML Basics
3. Deep Learning Intro
4. Advanced: Transformers

### Constraint-Domain Pillars

| Pillar | What It Covers | Breaking Conditions |
|---|---|---|
| Availability | Uptime, reliability | Infrastructure failure |
| Latency | Response time | Network congestion |
| Privacy | Compliance | GDPR, CCPA violations |
| Security | Attack vectors | Breaches |
| Cost | Operability | Budget overruns |

### Experiment Design Templates

#### Template A/B Testing
```markdown
## Experiment: [Name]

### Hypothesis
[H0]: [Control produces X]
[H1]: [Treatment produces Y > X]

### Design
- Sample: [N]
- Randomization: [method]
- Duration: [days]
- Power: [80%]

### Metrics
- Primary: [metric]
- Secondary: [metrics]
- Guard: [guard metric]

### Analysis
- Method: [t-test/chi-square/Bayesian]
- Significance: [p < 0.05]
```

#### Template: Qualtrics Interview
```markdown
## Interview Protocol: [Name]

### Script
Opening: [intro]
Q1: [question]
Q2: [question]
Q3: [question]

### Analysis
Coding: [method]
Sample: [N]
Duration: [min]
```

## Research Operating System (ROS) Spec

```
┌─────────────────────────────────────────────┐
│           RESEARCH OPERATING SYSTEM         │
│                                             │
│  ┌──────────────┐   ┌──────────────┐       │
│  │   Source     │──▶│   Reading   │──▶│    │
│  │   Library   │   │   Ladder    │   │    │
│  └──────────��───┘   └──────────────┘       │
│         │                 │                 │
│         ▼                 ▼                 │
│  ┌──────────────┐   ┌──────────────┐       │
│  │   Experiment│──▶│   Results   │──▶│    │
│  │   Design    │   │   Analysis  │   │    │
│  └──────────────┘   └──────────────┘       │
│         │                 │                 │
│         └─────────────────┘                 │
│                   │                       │
│                   ▼                       │
│  ┌──────────────────────────────────┐  │
│  │        Publication / Thesis         │  │
│  └──────────────────────────────────┘  │
└─────────────────────────────────────────────┘
```

## Peer-Reviewed Source List (30-80)

### Must-Cite (Target: 15)

1. Pearl, J. (2009). *Causality: Models, Reasoning, and Inference* (2nd ed.). Cambridge.
2. Morgan, S. & Winship, C. (2014). *Counterfactuals and Causal Inference* (2nd ed.). Cambridge.
3. Imbens, G. & Rubin, D. (2015). *Causal Inference for Statistics, Social, and Biomedical Sciences*. Cambridge.
4. Goodfellow, I., Bengio, Y., & Courville, A. (2016). *Deep Learning*. MIT Press.
5. Russell, S. & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson.
... (remaining in development)

## Decision Log

| Decision | Choice | Rationale |
|---|---|---|
| Format | Markdown + BibTeX | Versionable |
| Sources | 30-80 exact | Dissertation standard |
| Ladder | Progressive | Learn in order |
| Templates | Copy-paste | Runnable |

---

## Generated Files

`phase4-4B-dissertation-grade/research-atlas.md`
`phase4-4B-dissertation-grade/pillar-1-causal-inference.md`
`phase4-4B-dissertation-grade/pillar-2-unit-economics.md`
`phase4-4B-dissertation-grade/pillar-3-algorithmic-interface.md`
`phase4-4B-dissertation-grade/experiment-templates.md`
`phase4-4B-dissertation-grade/source-list.bib`