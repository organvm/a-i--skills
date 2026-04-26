# PHASE 1C: Pitch Deck Narrative (10-12 Slides)

## Metadata
- **Phase**: 1C
- **Decision**: Pitch deck narrative
- **Status**: DRAFT
- **Created**: 2026-04-26
- **Parent**: PHASE_1_CONTENT

## The Ask

A narrative-driven pitch deck (10-12 slides) that tells a story, not just presents features. Built either as:
- **Option C1**: Marp-renderable Markdown → PDF/HTML
- **Option C2**: Direct HTML/Keynote outline

## Slide Structure

| Slide | Content | Words |
|:---:|---|---|
| 1 | **Title** — The transformation | 8 |
| 2 | **The Problem** — Quantified pain | 30 |
| 3 | **The Metaphor** — What's broken, visualized | 40 |
| 4 | **The Solution** — The insight | 50 |
| 5 | **How It Works** — 3 steps | 75 |
| 6 | **Proof #1** — Case study A | 60 |
| 7 | **Proof #2** — Case study B | 60 |
| 8 | **The Model** — Pricing/revenue | 40 |
| 9 | **The Ask** — What we need | 30 |
| 10 | **The Team** — Why us | 40 |
| 11 | **The Vision** — What's next | 50 |
| 12 | **Contact** — CTA | 10 |

**Total**: ~500 words → ~8 minutes spoken

## Narrative Arc

```
ACT 1: THE WORLD IS BROKEN (slides 1-3)
   - Establish the pain
   - Name the enemy
   - Quantify the cost
   
ACT 2: THE HERO ARRIVES (slides 4-5)
   - The insight/solution
   - How it works
   
ACT 3: PROOF (slides 6-7)
   - Real evidence
   - Social proof
   
ACT 4: THE DEAL (slides 8-9)
   - Economics
   - The ask
   
ACT 5: THE CALL (slides 10-12)
   - Team authority
   - Vision
   - Contact
```

## Design Guidance

| Element | Guideline |
|---|---|
| **Typography** | Headers: bold, sans; Body: readable serif |
| **Color** | Primary + accent + white space |
| **Graphics** | 1 per slide max, data when possible |
| **Animation** | None (distraction) |
| **Transitions** | Fade only |

## Rendering Options

### Option C1: Marp Markdown
```markdown
---
marp: true
theme: default
---

# SLIDE 1 TITLE
```

### Option C2: HTML Outline
```html
<section data-slide="1"><h1>TRANSFORMATION</h1></section>
```

## Key Principles

1. **One message per slide** 
2. **Visual > text**
3. **Story > features**
4. **Quantify > qualifiers** ("3x" not "much better")
5. **End on CTA** — never leave the audience hanging

## Decision Log

| Decision | Choice | Rationale |
|---|---|---|
| Format | Markdown→HTML | Editable, versionable |
| Slides | 12 max | Attention span |
| Tone | Narrative arc | Stories sell |
| Proof | Two case studies | Social validation |

## Next Phase

From 1C → goes to:
- **2A**: Repo architecture (if selling externally)
- **2B**: Natural Center bootstrap (if formalizing)

---

## Generated Files

`phase1-1C-pitch-deck/slides-01-12.md`
`phase1-1C-pitch-deck/arc-structure.md`
`phase1-1C-pitch-deck/RENDER_INSTRUCTIONS.md`