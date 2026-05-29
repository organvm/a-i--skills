---
type: prompt-relay-envelope
version: 1.0
date: <YYYY-MM-DD>
from: <agent + session short-id>
to: <target agent or "next session in this scope">
scope: <absolute path of working scope>
phase: <FRAME | SHAPE | BUILD | PROVE | DONE>
compression_level: <minimal | medium | full>
---

# Relay Envelope — <one-line subject>

**From:** <agent + session> | **Date:** <YYYY-MM-DD> | **Phase:** <phase>

## Current State

Verified-on-disk only. No unverified claims. Use a table for path × state pairs.

| Item | State on disk |
|---|---|
| ... | ... |

## Completed Work

- [x] ...
- [x] ...

## Key Decisions

| Decision | Rationale |
|---|---|
| ... | ... |

## Critical Context

Constraints, sensitive content, sibling-process notes, time-pressure markers.
Anything the receiving agent needs to know to avoid stepping on a tripwire.

## Next Actions

Numbered, for the receiving agent. Concrete enough that the receiver can act
without re-deriving.

1. ...
2. ...

## Risks & Warnings

- Reversibility constraints (git-tracked? rollback-safe?)
- External-system effects (already pushed? notifications fired?)
- Sensitive-content reminders (PHI, credentials, etc.)

## Reference

- **Closeout (this session):** `<path>`
- **Related plans:** `<paths>`
- **Related memory entries:** `<names>`

## Compression note

This is a **<minimal | medium | full>** envelope. Receiving agent token
budget needed: ~<N> tokens to fully absorb. If picking up cold, you can skip
to "Next Actions" and treat the rest as optional context.
