# Inventory templates by substrate type

Use the closest template, adapt to your substrate's vocabulary.

## Document/content substrate (CMS, wiki, knowledge base)

| Title | Path/URL | Owner | State | Last modified | Format | Word count | Linked-from count |
|---|---|---|---|---|---|---|---|

Add a column for "audience" if the substrate has multi-audience scoping.

## Code substrate (monorepo, package collection)

| Module | Path | Owner team | State | Last commit | LoC | Test coverage | Public API surface |
|---|---|---|---|---|---|---|---|

Add a column for "downstream dependents" if you can compute it (lockfile scan, package registry).

## Asset substrate (digital assets, media library)

| Asset id | Storage location | Owner | State | Created | Format | Size (MB) | Usage count |
|---|---|---|---|---|---|---|---|

Add a column for "license" if assets have heterogeneous licensing.

## Workflow/ticket substrate (Jira, Linear, GitHub issues)

| Item id | Project | Owner | State | Created | Type | Priority | Last activity |
|---|---|---|---|---|---|---|---|

Add a column for "blocked-by count" — items with high blocked-by counts are friction
indicators.

## Data substrate (tables, datasets, warehouses)

| Object name | Schema/path | Owner | State | Created | Row count | Storage (MB) | Query freq (last 30d) |
|---|---|---|---|---|---|---|---|

Add a column for "downstream views/dashboards count" — high count means high blast radius
for any change.

## Operational process substrate (workflows, SOPs)

| Process name | Doc location | Owner | State | Last reviewed | Trigger | Frequency | Stakeholders |
|---|---|---|---|---|---|---|---|

Add a column for "automation %" — what fraction of the process is automated vs. manual.

## Sampling protocol (when full enumeration is impractical)

If the substrate is too large to enumerate exhaustively (>10,000 items, or no machine-readable
catalog exists), declare the sampling method:

1. **Stratified sample** — divide by category, sample N per category. Use when categories
   differ in size/risk.
2. **Random sample** — uniform random across the population. Use when categories are unknown
   or uniform.
3. **High-risk sample** — sample only items matching risk criteria (recently modified, owned
   by departed users, in deprecated formats). Use to find friction quickly.

State the sample size, the sampling method, the date, and the confidence level (or
explicitly say "exploratory; no statistical claim").
