# PHASE 3B: Lean MVP ($MODE = lean)

## Metadata
- **Phase**: 3B
- **Decision**: Lean MVP (fast deployment)
- **Status**: DRAFT
- **Created**: 2026-04-26
- **Parent**: PHASE_3_EXECUTION

## The Ask

Build the minimum viable version that:
- Ships fast (days, not months)
- Tests the core hypothesis
- Can be validated by real users
- Costs minimal to operate

## MVP Scope

| Feature | Priority | Status |
|---|---|---|
| Client storefront render | P0 | CORE |
| Lexicon/persona loading | P0 | CORE |
| Simple deployment | P0 | CORE |
| Contact form/mailto | P1 | REQUIRED |
| Analytics (privacy-first) | P2 | NICE |
| A/B testing | DROP | Later |
| Full CI/CD | P1 | v2 |
| Multiple personas | P1 | v2 |

## Architecture (Lean)

```
┌──────────────────┐
│   Vercel/Netlify  │  (Static hosting)
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│   Next.js App    │  (Server-side rendering)
│  + Lexicon JSON │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Formspree/mailto│  (No backend)
└──────────────────┘
```

## Quick Stack

| Component | Technology | Why |
|---|---|---|
| Framework | Next.js | SSR, fast deploy |
| Styling | Tailwind | Rapid UI |
| Forms | Formspree | No backend |
| Hosting | Vercel | Free tier, fast |
| Analytics | Plausible | Privacy-first |
| Domain | Cloudflare | Cheap |

## Deployment (One Command)

```bash
# Deploy to Vercel
npm i -g vercel
vercel --prod
# Done. URL in 30 seconds.
```

## MVP File Structure

```
/mvp
├── /src
│   ├── /app
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── /components
│   │   ├── Header.tsx
│   │   ├── Hero.tsx
│   │   └── Footer.tsx
│   └── /lib
│       ├── lexicon.ts
│       └── transform.ts
├── /content
│   └── /client-storefront
│       └── (rendered pages)
├── next.config.ts
├── tailwind.config.ts
└── package.json
```

## Cost Calculation

| Service | Free Tier | Paid (Growth) |
|---|---|---|
| Vercel | ✓ | $20/mo |
| Domain | $12/yr | $12/yr |
| Analytics | ✓ | $9/mo |
| Email | ✓ (Formspree) | $9/mo |
| **Total** | **~$12/yr** | **~$50/mo** |

## Validation Metrics

| Metric | Target |
|---|---|
| Time to deploy | < 1 hour |
| First visitor | Day 1 |
| First conversion | Week 1 |
| Cost | < $50/month |

## Decisions Overridden (Deferred)

| Decision | Deferred To |
|---|---|
| Multiple personas | v2 |
| Database | v2 |
| Custom domain auth | v2 |
| Full CI/CD | v2 |
| A/B testing | v3 |

## Decision Log

| Decision | Choice | Rationale |
|---|---|---|
| Stack | Next.js + Vercel | Fastest deploy |
| Database | None (JSON files) | MVP doesn't need |
| Auth | None (mailto) | Focus on value |
| CI/CD | Manual push | Simpler, fine for MVP |
| Hosting | Free tier | Validate before paying |

## Next Phase

From 3B → goes to:
- **4A**: Operator-grade documentation (if validated)

---

## Generated Files

`phase3-3B-lean-mvp/SPEC.md`
`phase3-3B-lean-mvp/deploy-instructions.md`
`phase3-3B-lean-mvp/cost-estimate.md`