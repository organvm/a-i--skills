# PHASE 1B: Sales One-Pager + Technical Split

## Metadata
- **Phase**: 1B
- **Decision**: Sales one-pager + Technical split
- **Status**: DRAFT
- **Created**: 2026-04-26
- **Parent**: PHASE_1_CONTENT

## The Ask

Two documents:
1. **Sales One-Pager** — For non-technical buyers/stakeholders
2. **Technical Spec** — For engineers/technical decision-makers

## Structure: Sales One-Pager

```
1. THE TRANSFORMATION (headline + 2 subs)
2. THE PAIN (what's broken, quantified)
3. THE SOLUTION (how it works, metaphor)
4. THE PROOF (case studies, ROI)
5. THE OFFER (pricing, guarantee)
6. THE ASK (CTA)
```

### Sales One-Pager Specs
- **Length**: 1 page (letter size, print-ready)
- **Words**: 300-500
- **Tone**: Warm, confident, human
- **Jargon**: Zero — translate everything
- **Visual**: Headers, bullets, 1-2 graphics

## Structure: Technical Spec

```
1. SYSTEM ARCHITECTURE
   - High-level diagram
   - Component list
   - Data flow

2. API SURFACE
   - Endpoints (REST)
   - Authentication
   - Rate limits

3. DEPLOYMENT
   - Infrastructure
   - Scaling model
   - Regions

4. SECURITY
   - Auth model
   - Encryption
   - Compliance

5. PERFORMANCE
   - SLAs
   - Latency targets
   - Throughput

6. INTEGRATION
   - Webhooks
   - SDKs
   - Third-party deps
```

### Technical Spec Specs
- **Length**: 5-10 pages
- **Format**: Markdown (source) → PDF (distribution)
- **Diagrams**: Mermaid or ASCII
- **Audience**: CTO, engineering lead
- **Style**: Precise, quantified

## Decision Log

| Decision | Choice | Rationale |
|---|---|---|
| Split | Yes | Different audiences |
| Sales tone | Warm, jargon-free | Human connection |
| Tech style | Quantified, precise | Engineering trust |
| Diagrams | Mermaid | Editable, versionable |
| Distribution | PDF for tech | Formal review |

## Next Phase

From 1B → goes to:
- **2A**: Full repo architecture (sales enables)
- **2B**: Natural Center bootstrap (tech spec formalizes)

---

## Generated Files

`phase1-1B-sales-technical-split/sales-one-pager.md`
`phase1-1B-sales-technical-split/technical-spec.md`
`phase1-1B-sales-technical-split/README.md`