# Skills Marketplace Unification — Master Plan

**Date:** 2026-05-23
**Repo:** `~/Code/organvm/a-i--skills`
**Triggered by:** session-opening directive — "this repo is trouble; the plugins/skills/tools infra developed by me and the skills via anthropic we evolved all need to be brought together in one location; we need a marketplace for anthropic, openai, gemini, opencode, openclaw, etc. all connecting"
**Reference exemplar:** https://github.com/VoltAgent/awesome-agent-skills

## Premise

The marketplace nucleus is already on disk: `.claude-plugin/marketplace.json` (12K populated), `distributions/{claude,codex,extensions/gemini,direct,collections}`, `plugins/` (2 plugins), `skills/` (42 source), `staging/` (12 incoming). What is missing is (a) the **transmutation protocol** that turns a foreign skill into a local-canonical skill, (b) the **federation model** that consumes other providers' marketplaces, and (c) the **canonical skill shape** asserted as the template every skill must converge to.

The session-prior `transcript-promotion` skill (`7df346f`) is the de-facto canonical template: `SKILL.md + scripts/ + references/ + examples/` with series-aware cross-links and a pitfall register (TP-NN).

## Four-phase logical order (bottom-up, empirical-first)

### Phase 1 — Audit (this session)

**Goal:** know the real shape distribution of all 161 skills in `distributions/claude/skills/` before asserting any canonical.

**Method:**
- For each skill dir under `distributions/claude/skills/`, classify shape:
  - `T0`: SKILL.md only
  - `T1`: SKILL.md + (scripts/ OR references/ OR examples/)
  - `T2`: SKILL.md + two of three subdirs
  - `T3`: SKILL.md + all three subdirs (canonical)
- Emit `audit/2026-05-23-skill-shape-distribution.tsv` (skill_name, tier, has_scripts, has_references, has_examples, has_provenance)
- Aggregate counts per tier; surface T3 examples beyond transcript-promotion if any.

**Output:** structural gap map persisted in `audit/`.

### Phase 2 — Fold

**Goal:** codify the canonical pattern from the audit's best examples and operationalize last session's work as the marketplace's first installed pattern.

**Steps:**
- Promote `~/.claude/plans/2026-05-20-{statusline,hooks,subagents}-options-reference.md` (three engine logs) into `a-i--skills/docs/engine-logs/` — they document Claude Code surfaces that skills must respect.
- Register the TP-NN pitfall-register concept (from `transcript-promotion/references/known-promotion-pitfalls.md`) as a marketplace-level convention: every skill that ships scripts MAY emit `references/known-pitfalls.md` with TP-NN entries.
- Cross-link transcript-promotion's pattern into `MARKETPLACE.md` (Phase 3) as the canonical exemplar.

### Phase 3 — README (the unification document)

**Goal:** author `a-i--skills/MARKETPLACE.md` asserting (now that audit + fold have proved them):
- The four-phase protocol: ingest → localize → fanout → register
- The canonical skill shape (T3) with transcript-promotion linked as exemplar
- The federation model: marketplace consumes Anthropic / OpenAI / Gemini / OpenCode / VoltAgent / etc.
- The transmutation pipeline diagram (see session message)
- Provenance requirement (`provenance.yaml`) for every ingested skill

### Phase 4 — Ingest VoltAgent (live validation)

**Goal:** first real exercise of the protocol. Clone VoltAgent/awesome-agent-skills into `staging/awesome-agent-skills/`, run the ingest script against 3-5 picked skills end-to-end, capture surprises into pitfalls. The validation must produce working `scripts/ingest-foreign-skill.sh`, `scripts/localize-skill.sh`, `scripts/fanout-skill.sh`, `scripts/register-skill.sh` as byproducts of empirical discovery.

## Status

- [ ] Phase 1 audit (in flight)
- [ ] Phase 2 fold
- [ ] Phase 3 README
- [ ] Phase 4 VoltAgent ingest

Plan ships as artifact (Universal Rule #5: plans are artifacts → commit + push).
