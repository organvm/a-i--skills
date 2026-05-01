# Domain Ontology — Education (general; Jessica-domain TBD)

**Stratum:** 1 (Ontology)
**Domain:** Education (broad; Jessica's specific intersection TBD)
**Created:** 2026-04-25
**Status:** Schema-stable; Jessica-specific entries flagged TBD

## Question

What is the domain made of?

## Entities

| Canonical name | Variants | Definition | Boundary case |
|---|---|---|---|
| Learner | student, participant, member | Person engaged in learning process | Learner ≠ customer (commercial); learning continues outside transactions |
| Educator | teacher, facilitator, instructor, coach | Person guiding learning | Educator ≠ trainer (skills focus); ≠ mentor (relationship-bound); overlapping but distinct |
| Curriculum | program, course, syllabus | Sequenced learning content | Curriculum ≠ method (curriculum is content; method is delivery) |
| Pedagogy | teaching method, approach | The how of teaching | Pedagogy is method-class; methodology is specific instance |
| Cohort | class, group, cohort | Synchronous learner-group | Cohort vs solo-learner is structural distinction |
| Outcome | learning outcome, competency | What learner can do after | Outcome ≠ grade (grade is metric; outcome is capability) |
| Assessment | evaluation, test, demonstration | Evidence collection of learning | Assessment ≠ judgment (assessment can be formative or summative) |
| Sticks (TBD) | _Jessica's project name_ | _entity TBD per collaborator_jessica.md_ | _TBD whether Sticks is curriculum / cohort / platform_ |
| Relationship-domain content (TBD) | _Jessica's domain anchor_ | _per DIWS schema v2.2 future-engagement reference_ | _TBD intersection with education_ |

## Relations

| Relation | Source → Target | Semantics | Cardinality |
|---|---|---|---|
| delivers | Educator → Curriculum | Educator instantiates curriculum for learner | 1:N |
| enrolls-in | Learner → Curriculum | Learner commits to curriculum participation | N:M |
| applies | Pedagogy → Curriculum | Method shapes content delivery | 1:N |
| evaluates | Assessment → Outcome | Assessment evidences outcome | N:1 |

## Primitives

- **Learner** — atomic unit of pedagogy
- **Educator** — atomic unit of guidance
- **Pedagogical move** — atomic teaching action (one explanation, one question, one feedback cycle)
- **Outcome unit** — atomic capability gain

## Canonical vocabulary

- **Pedagogy** (lowercase as concept; capitalized in product names)
- **Curriculum** (singular; plural is "curricula")
- **K-12** (hyphenated; lowercase elsewhere)
- **Higher ed** (lowercase; "higher education" in formal contexts)
- **Cohort-based** (vs course-based) — meaningful distinction in commerce
- **Sticks** (TBD — Jessica's project; capitalization TBD on confirmation)

## Boundary cases — what's NOT education domain

- **Pure entertainment** — adjacent; edutainment is the bridge
- **Therapy** — adjacent; education in psychology IS this domain, but therapeutic delivery is not
- **Religious instruction** — adjacent and contested; depends on framing (educational vs catechetical)
- **Pure credentialing** (cert exams without teaching) — adjacent commercial domain

## Authoritative sources

- *Pedagogy of the Oppressed* (Freire) — critical pedagogy canon
- *Make It Stick* (Brown / Roediger / McDaniel) — cognitive science of learning canon
- *Drive* (Pink) — motivation in learning canon (cross-domain)
- Edutainment-creator-economy emerging literature (TBD specific sources)
- _Jessica's specific influences — TBD per collaborator engagement_

## Validation gate

A fresh agent reading this file alone can answer "what is X in this education domain?" for any term used in subsequent strata. Jessica-specific terms are flagged TBD; this is acceptable for pre-active state.

## Changelog

- 2026-04-25 — initial fill (proof-instance; Jessica-domain stub)
