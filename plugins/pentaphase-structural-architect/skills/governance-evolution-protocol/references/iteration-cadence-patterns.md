# Iteration cadence patterns

A governance charter that can't change is a charter that ages badly. A governance charter
that changes constantly is a charter that no one trusts. Pick a cadence that matches the
substrate's volatility.

## Cadence by substrate volatility

| Substrate volatility | Recommended cadence | Example |
|---|---|---|
| **Stable reference** (taxonomy, lookups) | Annual review | Country code list; product categories |
| **Operational** (workflows, processes) | Quarterly review | Sales pipeline stages; support ticket types |
| **High-velocity** (engineering systems, fast-moving products) | Monthly review + on-demand | Microservice schemas; feature-flag definitions |
| **Compliance-driven** (legal, regulatory) | Tied to regulatory cycle (often annual) + on-demand on regulatory change | HIPAA-covered substrates |

Default if uncertain: quarterly review with on-demand triggers for unscheduled review.

## Triggers for unscheduled review

The cadence is the floor, not the ceiling. These events force a review outside the cadence:

- **New compliance requirement** — regulatory change, new contractual obligation.
- **Sustained metric degradation** — any value-metric at warning threshold for > 2 cadence
  periods.
- **Critical incident** — substrate-related production incident at severity ≥ S2.
- **Scope expansion** — substrate is being applied to a new domain it wasn't designed for.
- **Departure of key role** — primary owner of the substrate leaves; verify governance
  doesn't depend on tacit knowledge.
- **External integration** — a new system begins consuming the substrate; reverify access
  tiers and audit policy.

For each trigger, declare the response procedure: who is paged, what review is conducted,
on what timeline.

## Amendment process

Every change to the charter or the taxonomy is a versioned amendment. The process:

1. **Proposal** — drafted as an amendment document referencing the section being changed,
   with reasoning. Lives initially in a "proposed" state.
2. **Review** — circulated to a defined review group (the operational roles named in
   `substrate-context.md` plus any external stakeholders). Review window is typically 5–10
   business days.
3. **Ratification** — approval mechanism: consent (no objections), majority vote, or named
   approver depending on substrate. Declare which.
4. **Publication** — amendment is merged into the charter. New version number is assigned.
   Old version is archived but remains queryable.
5. **Communication** — affected operational roles are notified with a one-paragraph summary
   of what changed and what they need to do differently.

## Versioning

Use semantic versioning for the charter:

- **Major** (v1 → v2) — breaking changes to entity classes, access tiers, or core
  protocols. Affects ingestion or downstream consumers.
- **Minor** (v1.0 → v1.1) — additive changes (new entity classes, new optional attributes,
  new monitoring). Backward-compatible.
- **Patch** (v1.0 → v1.0.1) — clarifications, typo fixes, documentation improvements; no
  semantic change.

Each amendment lists the version it produces and the version it supersedes.

## Rollback policy

For each amendment that turns out to cause regressions:

- **Detection threshold** — what evidence triggers rollback consideration (incident,
  metric degradation, stakeholder objection).
- **Rollback authority** — who can authorize rollback.
- **Rollback procedure** — for charter-level amendments, revert to the prior version. For
  taxonomy or schema amendments, rolling back may require data migration; document that
  procedure.
- **Post-mortem** — every rollback produces a post-mortem entry in the amendment log
  explaining what was attempted, what went wrong, and what would need to change for the
  amendment to be re-attempted.

## Amendment log structure

Each amendment-log entry:

```markdown
### Amendment YYYY-MM-DD — vN.M.P → vN.M.(P+1) — <short title>

**Type:** major | minor | patch
**Scope:** which sections of the charter changed
**Reason:** why this change was needed (link to trigger if unscheduled)
**Reviewed by:** [list of roles]
**Ratified by:** [name or role]
**Effective date:** YYYY-MM-DD
**Communication:** how affected roles were notified
**Diff summary:** [brief description of what changed]
```

If the amendment is later rolled back, append a "Rollback" subsection with date, reason,
and post-mortem reference.

## Anti-patterns

- **Don't pick a cadence and abandon it.** A skipped review is a signal that the cadence
  is wrong (too frequent or too infrequent), not that this review can be skipped.
- **Don't make every amendment a major version.** Reserve major for breaking changes;
  otherwise version numbers stop carrying information.
- **Don't allow amendments without reasoning.** Every amendment-log entry has a "Reason"
  field for a reason — future maintainers need to understand intent.
- **Don't centralize all amendments.** Spreading amendment authority across roles (e.g.,
  schema amendments owned by tech, access-policy amendments owned by ops) prevents one
  bottleneck from becoming the rate-limiter for the whole charter.
