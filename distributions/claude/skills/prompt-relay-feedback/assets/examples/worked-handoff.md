---
type: prompt-relay-envelope
version: 1.0
date: 2026-05-21
from: codex + session 7f3a1c08
to: claude (next session)
scope: <repo-root>/
phase: BUILD
compression_level: medium
---

# Relay Envelope — Type-check failures in payment module

**From:** Codex session 7f3a1c08 | **Date:** 2026-05-21 | **Phase:** BUILD

## Inject phrase used to land this handoff

```
Continue from relay at ~/.claude/plans/2026-05-21-handoff-payment-typecheck.md. mid-task — see Next Actions for current step.
```

## Current State

| Item | State on disk |
|---|---|
| `<repo-root>/src/payment/types.ts` | Modified — 3 new type definitions |
| `<repo-root>/src/payment/charge.ts` | Modified — signature change for `chargeCard()` |
| `<repo-root>/src/payment/__tests__/charge.test.ts` | Unchanged — tests not yet updated |
| `tsc --noEmit` | Currently failing — 4 errors in `charge.test.ts` |

## Completed Work

- [x] Added `PaymentMethod` discriminated union to `types.ts`
- [x] Refactored `chargeCard()` to accept `PaymentMethod` instead of raw string
- [x] Verified runtime behavior unchanged (manual run of `pnpm run pay:demo`)

## Key Decisions

| Decision | Rationale |
|---|---|
| Used discriminated union over enum + payload object | Type safety at call sites; pattern matches existing `OrderStatus` shape in `<repo-root>/src/orders/types.ts` |
| Did NOT update tests yet | User asked for production-code refactor in isolation; test updates queued for handoff to Claude (architecture-aware test rewrites) |

## Critical Context

- The `chargeCard()` callers in `<repo-root>/src/checkout/` were updated
  mechanically. Six call sites; all touch the same shape.
- The Stripe integration in `<repo-root>/src/payment/stripe.ts` was
  deliberately NOT touched — it has its own type layer that maps
  `PaymentMethod` to Stripe's API. That mapping needs strategic review.

## Next Actions

1. Update `<repo-root>/src/payment/__tests__/charge.test.ts` to use the new
   `PaymentMethod` shape. The 4 errors `tsc --noEmit` surfaces are the
   test-side mismatches.
2. Review `<repo-root>/src/payment/stripe.ts` for the discriminated-union
   mapping question — flagged as a strategic decision Codex deferred.
3. Run `pnpm test src/payment` and verify green before pushing.

## Risks & Warnings

- Branch `<branch-name>` is local-only; not pushed yet. No external blast radius.
- The `chargeCard()` signature change is breaking — if any external consumer
  imports it (verify with `grep -r "chargeCard" <repo-root>/`), they'll need
  updates too.

## Reference

- **Closeout (Codex session):** `~/bound/.Codex/plans/closeout-2026-05-21-payment-typecheck-codex.md`
- **Related plans:** `<repo-root>/.claude/plans/2026-05-20-payment-refactor.md` (parent plan)
- **Related memory entries:** `feedback_discriminated_union_preference`, `project_artifact_2026_05_21_payment_refactor`

## Compression note

This is a **medium** envelope. Receiving agent token budget needed: ~600
tokens to fully absorb. If picking up cold, you can skip to "Next Actions"
and treat the rest as optional context.

---

**Note for documentation readers:** This file is a worked example pinned
beside the templates it demonstrates. All paths use `<repo-root>`,
`<branch-name>` as placeholders — this is **not live state**. The session ID
`7f3a1c08` and the payment-module scenario are fictional. Use this file to
see how `canonical-phrase.md` and `standard-envelope.md` compose into a
real-shaped handoff.
