# Domain Ontology — Wellness / Health

**Stratum:** 1 (Ontology)
**Domain:** Wellness / Health (BODI fitness + Elevate Align brand)
**Created:** 2026-04-25

## Question

What is the domain made of?

## Entities

| Canonical name | Variants | Definition | Boundary case |
|---|---|---|---|
| Practitioner | coach, trainer, healer, therapist | Person delivering wellness service | Practitioner ≠ doctor (clinical practice has separate ontology); ≠ guru (lifestyle vs brand) |
| Client | participant, member, patient | Person receiving wellness service | Client ≠ patient (clinical implication); ≠ subscriber (digital-only) |
| Modality | discipline, practice | Specific approach (yoga, strength training, breathwork, meditation, nutrition, somatic) | Modality ≠ method ≠ system; finer-grain than "wellness" but coarser than specific technique |
| Program | curriculum, protocol | Sequenced delivery of modality(s) over time | Program ≠ session (single instance); ≠ membership (commercial wrapper) |
| Membership | subscription, community | Commercial container for ongoing relationship | Membership ≠ class-pack (transactional); ≠ certification (credential-based) |
| Outcome | result, transformation | What the client achieves | Outcome ≠ feeling (subjective marker); ≠ metric (objective marker) — both can apply |
| Recovery | rest, regeneration | Post-load restoration phase | Distinct from "rest day" — recovery is active state |
| Macro / volume | macronutrient, training volume | Quantitative load (nutrition or exercise) | Macro = nutrient class; volume = weekly tonnage; not interchangeable |
| Mind-body | somatic, psychosomatic | Integrated mind-body practice | Boundary blur with traditional therapy; somatic IS therapy in many schools |
| Funnel | pipeline | Commercial customer-acquisition flow (L1-L4 typically) | Funnel = commercial structure; not a wellness practice |

## Relations

| Relation | Source → Target | Semantics | Cardinality |
|---|---|---|---|
| delivers | Practitioner → Modality | Practitioner offers modality to clients | 1:N |
| participates-in | Client → Program | Client engages with structured offering | N:M |
| measures | Outcome → Metric/Subjective-marker | Outcome instantiates measurable signals | 1:N |
| recovers-from | Recovery → Load | Specific load drives specific recovery requirement | 1:1 by load |
| contains | Membership → Program | Commercial wrapper holds programmatic offering | 1:N |

## Primitives

- **Practitioner** — atomic unit of service-delivery
- **Client** — atomic unit of service-reception
- **Modality** — atomic unit of practice
- **Outcome** — atomic unit of result
- **Time slice** — session / week / month / year (granularities)

## Canonical vocabulary

- **Modality** (lowercase as concept; capitalized in product names)
- **Practitioner** (preferred over "trainer" / "coach" when domain-neutral)
- **BODI** (uppercase — Beachbody re-brand; treat as proper noun)
- **NSCA-CSCS** (Certified Strength and Conditioning Specialist) — credentialing canon
- **ACSM** (American College of Sports Medicine) — credentialing canon
- **Mind-body** (hyphenated; lowercase as concept)
- **Macro** / **macros** (singular = macronutrient; plural = nutrient cluster)

## Boundary cases — what's NOT this domain

- **Clinical medicine** — adjacent domain; HIPAA + licensure requirements; do not blur
- **Pharmaceuticals / supplements as drugs** — adjacent; supplements as wellness protocol IS this domain, but pharmacology is not
- **Religious / spiritual practice** — overlaps with mind-body modalities; distinct in framing (wellness is secular-default)
- **Pure aesthetic** (e.g., bodybuilding-only) — adjacent; visible in this domain but not the domain's purpose
- **Diet culture** (calorie-deficit-only weight-loss without holistic frame) — adjacent and contested

## Authoritative sources

- *NSCA Essentials of Strength Training and Conditioning* — credentialing canon
- *ACSM's Guidelines for Exercise Testing and Prescription* — clinical-adjacent canon
- *Body by Science* (McGuff & Little) — minimum-effective-dose canon
- BODI / Beachbody internal materials — commercial-leader canon
- *Atomic Habits* (Clear) — behavior-change canon (cross-domain)

## Validation gate

A fresh agent reading this file alone can answer "what is X in this wellness domain?" for any term used in subsequent strata without external lookups.

## Changelog

- 2026-04-25 — initial fill (proof-instance for DIWS skill)
