# Agent Handoff: Skills Marketplace Unification

**From:** Claude job `beeff468` | **Date:** 2026-05-23 | **Phase:** 0+1+2a EXECUTED → 3+4 PENDING
**Work home:** `~/Code/organvm/a-i--skills/` (master branch `main`, 0/0 parity)
**Authoritative plan:** `~/Code/organvm/a-i--skills/.claude/plans/2026-05-23-skills-marketplace-unification.md`

---

## Current State (verify on pickup)

**Both touched repos: 0/0 parity at session close.**

| Repo | Last SHA | Pushed | Verify |
|---|---|---|---|
| `~/Code/organvm/a-i--skills` | `f9c3ceb` | ✅ origin/main | `git -C ~/Code/organvm/a-i--skills rev-parse HEAD` |
| `~/Workspace/4444J99/domus-semper-palingenesis` | `b8495ed`+ | ✅ origin/master | `git -C ~/Workspace/4444J99/domus-semper-palingenesis rev-parse HEAD` |

Note: domus may have advanced past `b8495ed` — sibling sessions commit there constantly. The audit-window commit `947742a` landed after mine; expect more.

**Files on disk (verify with `ls`):**
- `~/Code/organvm/a-i--skills/.claude/plans/2026-05-23-skills-marketplace-unification.md` (master plan, 4 phases)
- `~/Code/organvm/a-i--skills/audit/2026-05-23-skill-shape-distribution.tsv` (161-skill tier classification)
- `~/Code/organvm/a-i--skills/audit/2026-05-23-unified-inventory.md` (685-line all-surface catalog)
- `~/Code/organvm/a-i--skills/docs/engine-logs/{README.md, 2026-05-20-{statusline,hooks,subagents}-options-reference.md}` (engine logs promoted from `~/.claude/plans/`)
- `~/.claude/plans/2026-05-20-{statusline,hooks,subagents}-options-reference.md` (now BREADCRUMB STUBS, not the original content)
- `~/.claude/projects/-Users-4jp/memory/feedback_relocation_breadcrumb_protocol.md`
- `~/.claude/projects/-Users-4jp/memory/feedback_chezmoi_add_during_rebase_race.md`

**Safety branch (insurance, may delete):** `safety/2026-05-23-breadcrumb-stubs` in domus at orphan `9db1c44`.

## Completed Work

- [x] **Phase 0** — Unified inventory of every skill/agent/command/plugin surface (in-repo: 9 dirs; cross-system: Codex 21, Gemini 27, OpenCode 7, Cursor 11+3). 685-line catalog at `audit/2026-05-23-unified-inventory.md`.
- [x] **Phase 1** — Shape audit of 161 skills in `distributions/claude/skills/`. Result: T0=53 (33%), T1=90 (56%, 89 of 90 carry `references/` only), T2=15 (9%, 14 of 15 are `scripts+references`), **T3=3 canonical** (`artifact-resurfacing`, `transcript-promotion`, `webapp-testing`). TSV at `audit/2026-05-23-skill-shape-distribution.tsv`.
- [x] **Phase 2a** — Engine logs (statusLine / Hooks / Subagents) promoted from `~/.claude/plans/` to `~/Code/organvm/a-i--skills/docs/engine-logs/`. Breadcrumb stubs left at original location per new universal protocol.
- [x] **Universal rule codified** — `feedback_relocation_breadcrumb_protocol.md`: every reorganization emits TWO outputs (artifact at new home + breadcrumb at old location).
- [ ] **Phase 2b** — Fold transcript-promotion's pattern (T3 canonical) into MARKETPLACE.md as exemplar; promote pitfall-register (TP-NN) concept to marketplace-level convention.
- [ ] **Phase 3** — Author `~/Code/organvm/a-i--skills/MARKETPLACE.md` asserting the four-phase protocol (ingest → localize → fanout → register), the canonical-shape model, and the federation model.
- [ ] **Phase 4** — Clone VoltAgent/awesome-agent-skills into `staging/awesome-agent-skills/`; run ingest of 3-5 skills end-to-end; codify `scripts/ingest-foreign-skill.sh`, `scripts/localize-skill.sh`, `scripts/fanout-skill.sh`, `scripts/register-skill.sh` as byproducts.

## Key Decisions (do not re-litigate)

| Decision | Rationale |
|---|---|
| Logic order: Audit → Fold → README → Ingest (bottom-up empirical-first) | User explicitly chose all four levers in this logic order ("logic orders"); respects accumulated rules #32 (discover empirically) + #41 (audit before building). |
| "Gather all under our wings before chickens hatched or counted" reframed Phase 1 from canonical-declaration to inventory-first | User directive against premature canonical declaration. |
| Engine logs PROMOTED (moved, not copied) with breadcrumb stubs | They are marketplace context, not home-scope ad-hoc plans. Breadcrumbs preserve search habits & cross-references. |
| Stub format = full markdown file (NOT symlink) | `~/.claude/plans/` is indexed by `INDEX.md`; stubs preserve `.md` extension + grep-by-habit; chezmoi tracks them through source. |
| `chezmoi add` required (not just Write+autosync) per [[auto-sync-path-pattern-asymmetry]] | The sibling-session-discovered amendment to [[edit-vs-write-auto-sync-asymmetry]] supersedes the older Write-fires-but-Edit-doesn't framing. |
| Safety branch left in place even after recovery | Insurance; orphan `9db1c44` survives reflog gc this way until next session confirms cherry-pick durability. |
| **OPEN — DO NOT DECIDE WITHOUT USER:** canonical-shape model | Three options posed (tier-by-kind A/B/C, uniform T3, capability-tagged) but user deferred to "all of the above—logic orders". The canonical-shape question itself was deferred when audit showed species differentiation. **Next session must surface this to user before Phase 3.** |

## Critical Context

- **`a-i--skills/.claude-plugin/marketplace.json` already exists** (12K populated). Marketplace nucleus is on disk; the repo is further along than "this repo is trouble" framing suggested.
- **`distributions/` already has the multi-distribution backbone**: `claude/`, `codex/`, `extensions/gemini/`, `direct/`, `collections/{by-category,by-purpose,by-complexity}/`. Phase 4's `fanout` script extends this; doesn't invent it.
- **`staging/` is the inbound dock** — currently holds 23 entries (12 `*.skill` files + 2 Anthropic zips + reference docs). Phase 4's `ingest` script writes here.
- **Reference exemplar**: `https://github.com/VoltAgent/awesome-agent-skills` (user's preferred ingest target for Phase 4).
- **T3 canonical species (full SKILL.md + scripts/ + references/ + examples/) is rare (3 of 161)**. The marketplace grew by species, not toward uniform shape. Treat each tier as legitimate; force-marching T3 onto T0 advisory skills adds ceremonial empty dirs.
- **Sibling session activity in `domus` source is high** — between session start and close, 4+ commits landed from other agents. Memory rule #12 (verify before acting) is load-bearing here, not optional.
- **`chezmoi add` does NOT check `.git/rebase-merge/`** — see `feedback_chezmoi_add_during_rebase_race.md`. Pre-check: `[ -z "$(git -C ~/Workspace/4444J99/domus-semper-palingenesis symbolic-ref HEAD 2>&1 | grep -v refs/)" ]` (HEAD must be on a branch).

## Next Actions (in order)

1. **Surface canonical-shape decision to user.** Three options previously posed:
   - **Tier-by-kind (A/B/C)** — recommended: Advisory (T0 ok), Reference-pack (T1 with references/ required), Tooled (T3 full canonical required). 14 T2 skills become the enforcement gap.
   - **Uniform T3** — force all 161 to canonical. Adds ~480 empty ceremonial subdirs.
   - **Capability-tagged** — drop tier language; frontmatter declares capabilities; marketplace surfaces filters.
2. **Once decided: write `~/Code/organvm/a-i--skills/MARKETPLACE.md`** asserting:
   - The four-phase protocol (ingest → localize → fanout → register) with diagram
   - Canonical-shape model (whichever was chosen)
   - Federation model (how marketplace consumes Anthropic / OpenAI / Gemini / OpenCode / VoltAgent)
   - Provenance requirement (`provenance.yaml` for every ingested skill)
   - Pointer to the three T3 exemplars (`transcript-promotion` as primary template)
3. **Phase 4 execution:**
   - `cd ~/Code/organvm/a-i--skills/staging && git clone https://github.com/VoltAgent/awesome-agent-skills awesome-agent-skills`
   - Pick 3-5 skills covering different formats (Anthropic-skill, Cursor-rule, plain-MD, etc.)
   - Walk one through end-to-end manually, capturing each transform as a script (`ingest`, `localize`, `fanout`, `register`)
   - Record surprises in `skills/tools/transcript-promotion/references/known-promotion-pitfalls.md` (or new sibling pitfall register if generalizing)

## Risks & Warnings

- **Sibling sessions are actively committing to domus chezmoi-source.** Verify HEAD attached to branch before any `chezmoi add`. The reflog-as-hidden-actor pattern WILL fire — assume it.
- **Three working-tree mods in `a-i--skills` are NOT mine** (AGENTS.md, CLAUDE.md, GEMINI.md modified + 2 atuin-preview files deleted). Do not stage or commit them without user direction — they were present at session start.
- **`MEMORY.md` is under a 200-line budget** per SPEC-020 §5.2 hub-atom restructure (sibling session restructured 367→127 lines mid-our-session). Keep additive entries terse.
- **Canonical-shape decision is the bottleneck** — Phase 3 cannot start without it; Phase 4 cannot start without Phase 3's protocol assertion.
- **VoltAgent ingest may surface foreign-license / attribution issues** the marketplace doesn't yet handle (provenance.yaml schema doesn't currently include license field).
- **Anthropic's `distributions/claude/skills` symlinks to `~/.claude/skills`** — modifying source skill dirs propagates instantly to the runtime. Test changes in a feature branch.

## Coordination (multi-agent active)

```yaml
coordination:
  task: "Skills Marketplace Unification"
  agents_active_at_handoff:
    - id: claude-beeff468  # this session (closing)
      scope: "Phase 0/1/2a — inventory, audit, engine-log promotion"
      status: closing
      owns_at_close: []  # nothing locked

    - id: claude-unknown   # sibling sessions writing to domus
      scope: "domus chezmoi-source memory/plans propagation"
      status: ongoing
      observable_via: "git log ~/Workspace/4444J99/domus-semper-palingenesis"
      conflict_evidence: "947742a landed AFTER my b8495ed during my close window"

  shared_state:
    domus_master_head: "b8495ed at my close; may advance"
    a_i_skills_main_head: "f9c3ceb at my close"

  conflict_zones:
    - path: "~/.claude/projects/-Users-4jp/memory/MEMORY.md"
      rule: "append_only — always re-read before edit; never replace_all; respect ≤200-line budget"
    - path: "~/Workspace/4444J99/domus-semper-palingenesis (chezmoi source)"
      rule: "verify HEAD on branch before chezmoi add; check .git/rebase-merge/ via git symbolic-ref HEAD"
    - path: "~/Code/organvm/a-i--skills/.claude-plugin/marketplace.json"
      rule: "coordinator_only — only the agent executing Phase 3 should modify"
    - path: "~/Code/organvm/a-i--skills/distributions/"
      rule: "exclusive per skill — fanout writes are per-skill; no two agents fanout same skill concurrently"
```

## Recovery Protocol (if you're picking up cold)

1. **Verify current state:** `git -C ~/Code/organvm/a-i--skills log --oneline -3` should show `f9c3ceb feat(marketplace): Phase 0...` at HEAD (or descendant).
2. **Read the canonical plan:** `cat ~/Code/organvm/a-i--skills/.claude/plans/2026-05-23-skills-marketplace-unification.md`
3. **Read the audit:** `cat ~/Code/organvm/a-i--skills/audit/2026-05-23-skill-shape-distribution.tsv | head -20`
4. **Verify breadcrumbs survived:** `head -5 ~/.claude/plans/2026-05-20-statusline-options-reference.md` should show `title: MOVED — statusLine Options Reference`. If it shows the original "Claude Code statusLine — Complete Options Reference + Extension Roadmap", then chezmoi reverted them — re-execute the `chezmoi add` step from the rebase-race memory.
5. **Confirm canonical-shape decision is still open** by asking the user before Phase 3.
6. **Continue from Next Actions §1.**

## Pointer for cross-agent discovery

A pointer file at `~/.Codex/handoffs/2026-05-23-skills-marketplace-unification-pointer.md` references this canonical document. Codex / Gemini / OpenCode agents looking for pending work should check `~/.Codex/handoffs/` first; this file is the substrate.
