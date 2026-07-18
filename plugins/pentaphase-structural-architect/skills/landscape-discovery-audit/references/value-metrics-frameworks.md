# Value metric frameworks

Choose at least one metric per dimension. Customize names to match the substrate's vocabulary.

## Speed dimension

- **Cycle time** — wall-clock time from item creation to terminal state. Report p50 and p90.
- **Lead time** — wall-clock time from request to first delivery. Report p50 and p90.
- **Time-in-stage** — wall-clock time spent in each stage of the flow. Surface stages with
  outlier dwell times.
- **Time-to-first-response** — time from creation to first human/system action. Strong
  predictor of perceived responsiveness.
- **Throughput** — items completed per unit time (per day, per week). Track trend, not just
  absolute value.
- **Backlog age** — for items still in flight, the age distribution. p90 backlog age is a
  good leading indicator of approaching burnout.

## Accuracy dimension

- **Defect rate** — fraction of items that require rework after their initial pass.
- **Validation pass rate** — fraction of items that pass automated entry validation on first
  submission.
- **Stakeholder agreement rate** — for items requiring multi-party agreement, fraction
  approved without modification.
- **Reopen rate** — fraction of items that return to an earlier stage after reaching a later
  one (signals premature advancement).
- **Schema conformance** — fraction of items that fully populate required attributes.
- **Cross-system consistency** — for items represented in multiple systems, fraction that
  match across systems.

## Utilization dimension

- **Active vs. archived ratio** — fraction of substrate items currently in active states.
- **Owner coverage** — fraction of items with a current, active owner.
- **Search hit rate** — fraction of search queries that return relevant results.
- **Read frequency distribution** — distribution of how often items are accessed; long-tail
  items signal underutilization.
- **Storage efficiency** — bytes of substrate per active item; trending up signals bloat.
- **Last-touched distribution** — how recently items were modified; useful for finding
  candidates for archival.

## Quality-of-life dimension (optional but recommended)

- **Operator satisfaction** — periodic NPS-style survey to operational roles.
- **New-user onboarding time** — time from new operator's start date to their first
  unsupervised completed cycle.
- **Documentation coverage** — fraction of operations covered by current documentation.

## Threshold patterns

For each metric, set thresholds:

- **Target** — the value you're trying to reach (used in phase 5 monitoring).
- **Warning** — the value at which a watch is triggered.
- **Critical** — the value at which an incident response triggers.

Example for cycle time: target p90 ≤ 48h, warning at p90 > 72h, critical at p90 > 120h.

## Anti-patterns

- **Don't measure what you can't act on.** A metric with no improvement lever is decoration.
- **Don't measure too many things.** 5–10 metrics maintained is more useful than 30 metrics
  ignored.
- **Don't forget to baseline.** A metric without a baseline cannot show improvement.
- **Don't average away the tails.** Means hide the actual problem; track p50 AND p90.
