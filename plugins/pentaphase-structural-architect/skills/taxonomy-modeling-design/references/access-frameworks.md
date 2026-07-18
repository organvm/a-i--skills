# Access framework patterns

Pick the simplest framework that captures the substrate's actual access requirements.
Complexity that isn't enforced becomes drift.

## Owner-only

The simplest model: each entity has exactly one owner; only the owner can read or modify it.

- **When to use:** personal substrates (individual notes, drafts).
- **Strengths:** trivially enforced; no permission UI needed.
- **Weaknesses:** breaks under collaboration; doesn't scale beyond one user.

## Owner + role tiers

Owner has full control; defined roles get read or read-write access.

- **Tiers:** typical sets are {owner, editors, viewers, public} or {owner, team, org, world}.
- **When to use:** team substrates with clear collaboration patterns.
- **Strengths:** fits most enterprise tools; well-understood.
- **Weaknesses:** doesn't handle attribute-level access; coarse granularity.

## Role-based access control (RBAC)

Permissions are assigned to roles; users inherit role permissions.

- **When to use:** medium-sized organizations with stable role definitions.
- **Strengths:** scales to many users; auditing is straightforward.
- **Weaknesses:** roles can multiply ("admin", "super-admin", "regional-admin", "regional-super-admin")
  and become hard to maintain.

## Attribute-based access control (ABAC)

Access is computed from attributes of the user, the entity, and the context (time, location,
purpose).

- **When to use:** complex compliance requirements (HIPAA, GDPR with purpose limitation);
  large organizations with dynamic role membership.
- **Strengths:** very expressive; can encode complex policies.
- **Weaknesses:** harder to reason about; debugging access denials is painful.

## Capability-based

Access is granted via unforgeable tokens (capabilities); possessing the token grants the
permission encoded in it.

- **When to use:** substrates that share entities with external parties; substrates that
  need delegation.
- **Strengths:** delegation and revocation are first-class.
- **Weaknesses:** users must understand capability passing; debugging requires tracing
  capability flow.

## Tier definitions to declare

For any framework you choose, declare per entity class:

- **Visibility tiers** — who can see entities of this class? (Often: world, org, team,
  owner-only, or some subset.)
- **Modification tiers** — who can modify entities of this class? (Usually a subset of
  visibility — modifiers must also be viewers.)
- **Lifecycle-action tiers** — who can archive, delete, or restore? (Usually narrower than
  modification — typically owner + admin only.)
- **Schema-extension tiers** — who can add/change attributes on this class? (Usually system
  admin only.)
- **Access-grant tiers** — who can grant access to others? (Owner, plus possibly delegates.)

## Audit policy declarations

For each entity class, declare:

- **Logged events** — create, read, update, delete, share, archive — which subset is logged.
- **Log retention** — how long the log is kept (regulatory minimums apply).
- **Log access** — who can see the audit log itself.
- **Tamper resistance** — append-only? cryptographically signed? checksummed?

For substrates with compliance requirements, the audit policy is often more important than
the access tiers themselves.

## Mapping to existing systems

If the substrate will live in an existing system (database, CMS, repo, SaaS), prefer that
system's native permission model over inventing a new one. Inventing means re-implementing
audit, debugging tools, and admin UI — usually not worth it.

Exception: if the existing system's model is the documented friction in phase 1, redesign
of access IS the overhaul. In that case, declare the new model explicitly and account for
the migration of existing permissions in phase 4.
