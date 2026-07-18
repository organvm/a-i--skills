# Common friction archetypes

Use these as prompts when scanning for friction. Most substrates have several of these.

## Bottleneck — single point of contention

A single resource (person, system, queue, gate) that all flow passes through.

- **Symptom:** items pile up before this point; throughput is bounded by this resource's capacity.
- **Diagnostic:** if you removed/duplicated this resource, would throughput meaningfully rise?
- **Examples:** one approver for all PRs; one mailbox for all incoming requests; one engineer
  who knows the deploy ritual.

## Gap — missing handoff

A handoff that should exist but doesn't, so items stall or silently fail to advance.

- **Symptom:** items reach a stage and just sit; no one is paged; no one is responsible.
- **Diagnostic:** trace a sample item to its current stage. Who advances it next? If the
  answer is "no one in particular", it's a gap.
- **Examples:** ticket created, no one assigned; document drafted, no one reviews; PR opened,
  no review SLA.

## Inefficiency — doable but costly

Items advance, but the path is more expensive than necessary in time, effort, or money.

- **Symptom:** participants complain about specific recurring overhead; workarounds emerge.
- **Diagnostic:** measure the cost of one cycle. Is more than ~30% spent on coordination/ceremony
  rather than substantive work?
- **Examples:** five-meeting ritual to ship a one-line config change; manual data entry across
  two systems that don't sync.

## Drift — semantic divergence

Same concept means different things in different places, leading to mismatch and rework.

- **Symptom:** stakeholders use the same word for different things, or different words for the
  same thing; miscommunication is frequent.
- **Diagnostic:** ask three stakeholders to define a key term. If you get three answers, drift
  is present.
- **Examples:** "active" status means different things in CRM vs. billing system; "customer"
  means different things to sales vs. support.

## Silo — unconnected substrates

A substrate exists in parallel with another that should be connected, and the disconnection
causes duplicate work.

- **Symptom:** information is captured in two places and they get out of sync.
- **Diagnostic:** ask what the canonical source for X is. If you get conflicting answers, X
  is siloed.
- **Examples:** product catalog in spreadsheet AND in CMS; runbook in wiki AND in
  README.

## Coordination cost — too many actors

Multiple actors are required to advance an item, and coordination dominates execution.

- **Symptom:** more time is spent coordinating than doing.
- **Diagnostic:** count the actors required to advance one item. >5 typically signals
  coordination cost.
- **Examples:** quarterly review involving 12 reviewers; deploy requiring sign-off from
  4 teams.

## Quality leak — items pass through without validation

Items pass through stages without any validation, so quality issues only surface downstream.

- **Symptom:** errors are caught late, after they have propagated; rework is expensive.
- **Diagnostic:** find a recent quality incident. How far downstream was it caught? If it
  could have been caught at the entry stage, you have a quality leak at entry.
- **Examples:** data ingested without schema check; PRs merged without test runs; documents
  published without proofreading.

## Stale ownership — owner has moved on

The named owner is no longer doing the work, but ownership wasn't transferred.

- **Symptom:** the owner is unresponsive, or the owner is "the team" with no individual
  accountable.
- **Diagnostic:** for each owner of record, verify they're still active. >10% stale ownership
  is a structural problem.
- **Examples:** files owned by departed employees; processes "owned by ops" with no
  individual responsible.

## Hidden dependency — undocumented coupling

Item A depends on item B, but the dependency isn't recorded anywhere; changes to B silently
break A.

- **Symptom:** unexpected breakage when something seemingly unrelated changes.
- **Diagnostic:** ask "what would break if we deleted X?" If the answer requires a 30-minute
  archaeology session, dependency on X is hidden.
- **Examples:** dashboards depending on undocumented column names; scripts depending on
  specific cron schedules.
