# Premortem transcript — 2026-05-14

Three targets, premise frame "it is 2026-11-14 and these have failed."

## Targets

1. **`coliseum-from-grain` plugin** — first real exercise on user grains
2. **Methodology-plugin family pattern** — pentaphase + coliseum as a reusable family
3. **Push-to-remote action** — Universal Rule #2 closure on the local-only plugin

## Context gathered (no questions asked of user; all from session)

- Plugin built 2026-05-14 in autonomous /plugin-dev:create-plugin session
- 14 files, 1326 lines, validator PASS
- 5 skills + 3 agents + 4 reference docs
- Mirrors pentaphase-structural-architect (also local-only, sibling at /Users/4jp/Code/pentaphase-structural-architect/)
- Universal Rule #2 violation: no git init, no remote
- Motivating grain: dense abstract user prompt with explicit no-clarifying-questions instruction

## Raw failure inventory (11 reasons)

### Target 1 — coliseum-from-grain plugin

1. Phase-0 elicitation defeated the autonomy promise (five clarifying questions reinstate ping-pong)
2. Pingpong-detector gated too strictly — recompose loop stalled Phase 2 / Phase 3 boundary
3. Phase 4 reconciliation stapled rather than composed
4. Subagent selection mismatch — no real domain experts available, "expertise" was envelope labels only
5. Generalization from N=1 grain failed on N=2

### Target 2 — methodology-plugin family pattern

6. N=2 is not a family
7. Pattern lock-in (procrustean bed for plugin #3)
8. Auditor agent quality bottleneck (template provides slot, no recipe)

### Target 3 — push-to-remote / Universal Rule #2

9. Drive failure or filesystem incident before push
10. Choice paralysis on push destination
11. Push happens but plugin atrophies against Claude Code API drift

---

## Deep-dives

### Failure 1 — Phase 0 reinstated the ping-pong

**The failure story.** On 2026-05-15, the morning after the build, the user issued a dense second grain — something about routing portfolio organs through a stretching-rack diagnostic. They invoked `coliseum-orchestrator`. The plugin opened Phase 0 and asked: (1) what is the literal surface, (2) what is the implied scope, (3) what moves are forbidden, (4) what constraints are named, (5) what is the dispatch budget. Five numbered questions. The user read them, paused, typed "nevermind" — then ran the work as a single Opus call. They never invoked the plugin again.

The motivating grain itself had been the test case the author should have honored: *"if given a grain of sand & requesting coliseum: do it."* The user had explicitly forbidden clarifying questions when issuing that grain. Phase 0 violated that prohibition the very first time it ran. Worse, the elicitation was framed as rigor — "we need to read the grain carefully before dispatch" — which is exactly the smoothing-agent rationalization the constitution names as a failure mode. The plugin shipped a ping-pong gate while marketing itself as the cure for ping-pong.

By July, the plugin sat unreferenced in `~/Code/coliseum-from-grain/`. The pingpong-detector agent — built to guard dispatch from internal ping-pong between subagents — never fired in anger because no grain ever cleared Phase 0. The detector guarded an empty stadium.

**Underlying assumption.** The author assumed that "structured elicitation" reads as rigor to the user, when in fact the user's whole framing of "grain → coliseum" defines structured elicitation *of the user* as the prohibited move.

**Early warning signs.**
- First-invocation latency to first user response > 30 seconds — the user is reading questions, recognizing the shape, deciding whether to disengage.
- The user answers question 1 tersely and ignores 2–5, or replies "just do it" / "nevermind" / closes the session.

---

### Failure 2 — The Phase-2 stall

**The failure story.** The first real grain landed on November 3: a refactor of the `organvm atoms pipeline` writer to honor a new fanout schema. The orchestrator composed four envelopes — schema author, writer refactor, fixture regeneration, downstream consumer audit. Check 4 fired on every envelope. "Negative scope: do not touch sibling pipelines" was rejected because *sibling pipelines* didn't name the specific peers (`atoms fanout`, `prompts distill`, `ontologia resolve`). The orchestrator named them. Then check 4 fired again on the consumer-audit envelope, demanding the excluded peers within *that* envelope's adjacent surface — a different set. Three recompositions later, check 9 began failing: the verbatim grain, now 380 words after the user's two clarifications in chat, exceeded the envelope's working budget when inlined four times across four envelopes. Trimming the grain failed check 9 as non-verbatim. Quoting the grain by reference failed check 1.

By envelope seven (composition attempt three of four), the orchestrator was spending more tokens on gate-passage than on the work itself. It escalated to the user: *"Which peers count as adjacent for the consumer audit?"* — a textbook ping-pong, the exact failure mode the gate existed to prevent. On grain two (a smaller doc edit), the orchestrator silently relaxed: it shipped envelopes with check 4 marked PARTIAL on self-assessment, dispatched anyway, and three of four agents returned asking for clarification on excluded scope. The gate's purpose was defeated within a week of real use.

**Underlying assumption.** That self-containment is a property of the envelope alone, rather than a joint property of envelope + grain + peer-set whose minimum description length sometimes exceeds any single envelope's working budget.

**Early warning signs.**
- Composition-attempt count per grain trending above 2.
- Verbatim grain length growing across a session — check-9 inlining cost scales linearly while grain drifts further from "verbatim."

---

### Failure 3 — Phase 4 stapled, did not compose

**The failure story.** By Phase 4, the orchestrator has burned ~40-60K tokens on grain elicitation, six-lens reading, envelope composition, and pingpong gating. Then 3-7 returns land — call it five returns at 1000 words each, 5000 words of dense subagent prose dropped into context at once. The skill text says "alchemy, not concatenation," but the model is asked to hold all five returns in working attention simultaneously, identify cross-cutting tensions, resolve them, surface PENDING-DECISIONs, and emit a single composed voice. Under that load, the cheapest legal output that satisfies the surface contract is: section header per return, light paraphrase, two-sentence bridging paragraph, "PENDING-DECISION: none surfaced."

The user opens the artifact. It reads as five short essays with a table of contents. The seams are visible — voice shifts every 800 words, the same concept gets re-defined three times across sections, contradictions between return-2 and return-4 are quietly preserved rather than adjudicated. The orchestrator never lied; it just took the staple-shaped path because staple-shaped output is locally indistinguishable from composed output to a tired evaluator-of-self. The skill's normative assertion ("composition is alchemy") had no mechanical gate behind it.

**Underlying assumption.** That a normative instruction in skill prose is sufficient to override the path-of-least-resistance behavior of a context-saturated orchestrator at the end of a long multi-phase protocol.

**Early warning signs.**
- Phase 4 output length ≈ sum of return lengths minus ~15% (concatenation signature); true composition typically compresses to 40-60% of input mass.
- Zero or one PENDING-DECISIONs surfaced across multiple invocations.

---

### Failure 4 — Subagent expertise was nomenclature, not substance

**The failure story.** The first real invocation looked like it worked. The user dropped a grain about restructuring their personal knowledge graph and the plugin produced five envelopes — "ontology-architect," "graph-database-expert," "UX-information-designer," "epistemologist," "migration-strategist." Phase 3 dispatched them in parallel. Five returns came back. They all opened with framing paragraphs. They all suggested some variant of "start with the entities, then the relationships, then the access patterns." Three of them independently cited the same Zettelkasten reference. The "epistemologist" return was indistinguishable in register from the "ontology-architect" return — both were Claude doing its standard structured-thinking move, just with the envelope's label echoed in the opening sentence as flavoring.

Phase 4's reconciliation received 5 documents with ~70% conceptual overlap, dressed in different vocabulary. It produced a synthesis that read as "the consensus is X" — but the consensus was just Claude's modal answer surfacing five times. The orthogonality the protocol promised never appeared, because there was no orthogonal substrate to draw from. By month three, the user ran the same grain through a single `claude` invocation with a "think across multiple expert frames" prompt and got 85% of the coliseum's output in 1/N the wall-clock and 1/N the token spend. The protocol's overhead had no payoff to amortize against.

**Underlying assumption.** That subagent *labels* shape outputs the way actual *training-distribution differences* would — that calling Claude an "epistemologist" makes it think like one, rather than makes it talk like one.

**Early warning signs.**
- The N parallel returns share opening structures, hedge identically, and cite overlapping references.
- A solo invocation with "consider these five framings" matches the coliseum's reconciled output within a single re-read.

---

### Failure 5 — N=1 generalization broke on N=2

**The failure story.** The plugin was conceived on a grain that happened to be exemplary: a meta-prompt asking for a protocol that mirrored its own shape. The motivating grain explicitly named parallel levels, multiple directions, domain expertise, and chunked hand-offs — every input the four phases were designed to consume. Of course the protocol fit. It was reverse-engineered from this single specimen.

The second grain was a small concrete ask — "rename the variable across the module" — and the plugin dutifully ran dimensionalization, surfaced phantom "parallel levels" (test files? docs? changelog?), composed a coliseum dispatch, and produced a paragraph of orchestration overhead before the rename. The third grain was narrative — the user describing a half-formed feeling about a project — and Phase 1's dimensional decomposition shredded the texture into bullet-point parallels, killing the very thing the user was trying to articulate. The fourth was rhetorically dense but procedurally linear: one expert, sequential steps, no fan-out warranted. The plugin manufactured fan-out anyway. After two real invocations, the user noticed the output read like a planning document about doing the work rather than the work, and reverted to naive asks.

**Underlying assumption.** Every grain worth invoking the plugin on contains latent parallel dimensions waiting to be surfaced — that the absence of visible structure is a problem the protocol can solve rather than a property of the grain itself.

**Early warning signs.**
- Phase 1 output reads as plausible-sounding parallel axes the user wouldn't have generated themselves and doesn't recognize as load-bearing.
- The user begins editing Phase 1 output instead of acting on it, or silently drops to naive prompting after one trial.

---

### Failure 6 — N=2 was never a family

**The failure story.** By July 2026, the third methodology plugin attempt — `dialectical-tension-resolver`, intended to encode the user's repeated practice of holding opposing forces in productive friction — stalled in scaffolding. The work wasn't phased. It was a conversational loop: surface tension, name both poles, hold without collapsing, let a third term emerge, recurse. There was no artifact stream because the artifact *was* the dialogue. There was no auditor agent because the methodology's whole point was that no external arbiter could adjudicate. The user spent two sessions trying to bend it into the family skeleton, then abandoned the plugin form and wrote it as a single skill with no orchestrator.

In retrospect, pentaphase and coliseum weren't a family. They were two instances of *pipeline-shaped problems the user happened to face in the same quarter*. The family designation, made after N=2, locked in a shape that the next real methodology rejected. The "family" framing made the failure feel like the new methodology was deficient, rather than the taxonomy being premature.

**Underlying assumption.** That structural similarity between two artifacts indicates a generative pattern, when it more likely indicates a repeated problem-shape that won't repeat a third time.

**Early warning signs.**
- During the third plugin's design conversation, the user reaches for verbs that don't fit the skeleton — "loop," "hold," "negotiate," "surface" — instead of "phase," "advance," "audit."
- The "auditor agent" slot in the third plugin has no obvious occupant.

---

### Failure 7 — Pattern lock-in

**The failure story.** By July 2026, the user attempted plugin #3 — a methodology for cold-read script analysis that is fundamentally a single interpretive pass with no phase boundaries. The work is recursive (re-reading the same scene through deepening lenses), not sequential. But because pentaphase and coliseum had been canonized as "the family," the user spent two sessions trying to shoehorn close-reading into orchestrator + phase-skills, inventing artificial gates that fragmented what should have been one richly-instructed skill with internal recursion. The auditor agent had nothing to audit — the passes weren't independently verifiable — so it became a rubber-stamp pass-through.

Plugin #4 suffered the inverse failure: padded from 2 phases to 4 by inventing pre- and post- phases that exist only to honor the N≥4 convention implied by the family. By plugin #5 the user was bypassing the plugin system entirely and writing standalone skills, which orphaned the methodology-encoding muscle the family was supposed to grow.

**Underlying assumption.** That two instances sharing a skeleton is sufficient evidence the skeleton is the right generic.

**Early warning signs.**
- An auditor agent that has nothing substantive to verify between phases.
- Phase artifacts that no downstream phase actually reads.

---

### Failure 8 — Auditor agent quality was the unstated load-bearing component

**The failure story.** The family pattern shipped with confidence: every methodology plugin gets an auditor agent that gates between phases. By plugin #3 the template was crisp — a slot in the manifest, a documented hand-off contract, a phase-gate hook. What the template did not have was a recipe for the judgment the auditor was supposed to encode. So plugin #3's author did what plugins #1 and #2's authors had done: stared at the domain, free-handed a checklist, tuned thresholds against three example runs, shipped.

Six months in, the pattern's failure became legible. Pentaphase's auditor waved through structurally incoherent overhauls because its preconditions were stated as presence-checks ("a phase-2 artifact exists") rather than coherence-checks. Coliseum's pingpong-detector did the opposite — it blocked dispatch on any envelope that re-referenced a prior turn. Plugin #3 split the difference and was simply ignored by its users. Three auditors, three different failure modes, zero shared learning. The "family" gave each plugin the same skeleton and left the load-bearing organ to each author's improvisational ability.

**Underlying assumption.** That naming a required component is equivalent to specifying it, and that domain-specific judgment will crystallize on its own once a slot exists for it.

**Early warning signs.**
- Auditor source files across family members share no common structure beyond the manifest stub.
- New plugin authors ask "what should my auditor check?" and the answer is a pointer to existing plugins as examples, not to a recipe.

---

### Failure 9 — Drive failure before push

**The failure story.** Sometime in late October 2026, the user's M3 SSD threw a kernel panic that mounted the volume read-only on reboot. The directory `/Users/4jp/Code/coliseum-from-grain/` — never `git init`'d, never pushed — became unrecoverable from the live filesystem. Backblaze had a copy. Time Machine had a copy. Both restored bytes, but neither preserved a git history that never existed.

The Time Machine snapshot the user pulled from was from roughly 36 hours before the failure. The user reconstructed missing changes from session transcripts and memory. The reconstructions were *plausible* but not *identical*: phrasings softened, examples merged, trigger language in SKILL frontmatter lost specificity. The plugin still ran. It no longer encoded what the user had actually decided. The user didn't notice for weeks.

**Underlying assumption.** That Backblaze and Time Machine, being byte-faithful, are equivalent to git history for purposes of preserving intentional editorial decisions in prose artifacts.

**Early warning signs.**
- The plugin directory's mtime advances daily while `ls -la /Users/4jp/Code/coliseum-from-grain/.git 2>&1` continues to return "No such file."
- The user references the plugin in session prompts without ever invoking `cd` into a repo — the artifact is being *used* before it's been *versioned*.

---

### Failure 10 — Push paralysis

**The failure story.** On 2026-05-14 the user faced the home-selection fork: organvm (no organ mapped cleanly), meta-organvm (plausible but requires defining a new sub-category), a fresh `methodology-plugins` monorepo (cleanest taxonomically but requires committing to future members), or a personal-account standalone (lowest ceremony but orphans the artifact). Each option carried a real cost the user didn't want to pay in that moment.

The user said "I'll figure out the right home later" and moved on. By July the local plugin had three small edits. By September the diff against any hypothetical initial commit was no longer a clean first push — it was first push *and* triage three months of unaccounted edits. By November the decision wasn't just "which home" but "which home, *and* reconstruct the edit history, *and* decide which edits even belong in a v1." The entry cost compounded.

**Underlying assumption.** That deferring the home-selection decision preserved optionality, when it actually accrued reconstruction debt against every subsequent local edit.

**Early warning signs.**
- Pentaphase-structural-architect — the sibling plugin, same decision, same age — was also still local-only. Two unmade decisions of the same shape is a category, not a coincidence.
- A second edit to `coliseum-from-grain/SKILL.md` happened without first resolving the push.

---

### Failure 11 — Plugin atrophied against API drift

**The failure story.** It's 2026-11-14. The user types `/coliseum-from-grain:start` and gets nothing. The slash-command namespace had changed in a minor Claude Code release sometime around September; the plugin's command frontmatter used a key (`description`) that was silently renamed (`summary`) in the loader's strict pass. Commands without the new key still parse but are excluded from discovery.

Trying agents directly, `@reconciler` returned `Agent failed to load: unknown field 'tools_allowed' in agent frontmatter`. The legacy alias had been dropped in a later version. The skill `grain-decomposer` loaded but emitted a deprecation banner. By the time the user pieced together which failures were independent, an hour had passed. They opened the original task in a plain session and finished in fifteen minutes. The plugin was uninstalled the same evening.

**Underlying assumption.** The plugin was treated as a finished artifact rather than a living dependency on an actively-versioned platform contract.

**Early warning signs.**
- During the dormancy, Claude Code release notes mentioned plugin schema changes; no subscription, RSS, or scheduled re-validation surfaced them.
- The plugin had zero invocations in 90+ days while sibling tools accumulated dozens.

---

## Synthesis

### The cross-target hidden assumption

All eleven failures point at a single deeper assumption: **naming a thing is sufficient to instantiate it.**

- Phase 0 names *rigor* (five structured questions = careful reading)
- Envelope section 7 names *domain expertise* (calling Claude an epistemologist = invoking one)
- Phase 4 names *alchemy* (the word "compose, not staple" in skill prose = composed output)
- "Family" names *architecture* (two artifacts sharing a skeleton = a generic pattern)
- "Plugin on disk" names *artifact* (bytes existing = artifact preserved)
- "Backups exist" names *durability* (byte-faithful restore = editorial history preserved)

Each is nomenclature without the mechanism beneath. The plugin was built quickly and confidently because the author worked at the level of names; the failure modes all live at the level of mechanisms that the names imply but don't enforce.

### Per-target verdicts

**Target 1 — coliseum-from-grain plugin**
- **Most likely failure:** Failure 1 (Phase 0 ping-pong). It fails on first invocation, at the front gate, on the exact premise the plugin was built to honor.
- **Most dangerous failure:** Failure 4 (subagent mismatch). No amount of protocol tuning fixes the absence of real domain-expert subagents. The coliseum has no gladiators.

**Target 2 — methodology-plugin family**
- **Most likely failure:** Failure 6 (N=2 is not a family). The third plugin attempt rejects the skeleton because the user's real methodologies are not all pipeline-shaped.
- **Most dangerous failure:** Failure 7 (pattern lock-in). The "family" designation acts as a constraint on what the user lets themselves design — silent damage to future thinking.

**Target 3 — push-to-remote**
- **Most likely failure:** Failure 10 (push paralysis). Four plausible homes, no forcing function, decision compounds with each subsequent edit.
- **Most dangerous failure:** Failure 9 (drive failure pre-push). Low probability but irreversible.

### Revised plan

**For target 1 (the plugin):**

1. Invert Phase 0. Default: autonomous read of the grain, single-pass inference. Five questions surface only when grain context is genuinely irreducible. Fail-open to autonomy, fail-closed to elicitation.
2. Loosen the pingpong-detector. PARTIAL becomes the default verdict; only FAIL on the 2-3 checks that truly guarantee user-facing ping-pong (substrate vocabulary inlining, file-path implicitness, BLOCKED clause absence). Cap recompose attempts at 2 — on the third, dispatch with annotated risk rather than loop forever.
3. Add a Phase-4 mechanical gate: forced compression to ≤50% of summed return mass. If output exceeds, it's stapled by definition. Plus minimum 1 PENDING-DECISION surfaced or explicit "no tensions detected" justification.
4. Strike the "domain expert" promise from envelope section 7. Replace with "advisory subagent type — no guaranteed expertise delta." Don't promise what doesn't exist.
5. Add a pre-Phase-1 gate: "is this grain actually fan-out shaped?" If the answer is no, the plugin should decline to invoke its own protocol and recommend a direct ask.

**For target 2 (the family):**

6. Strike the "family" naming now. Keep pentaphase and coliseum as siblings, not family members. Revisit only after a third plugin genuinely fits.
7. If a third methodology plugin is attempted: build body first, skeleton last. Prove the shape fits before naming it.

**For target 3 (push):**

8. Push *today*. The right home is whichever home can receive a `git init && git remote add && git push` within 24 hours. Even personal-account standalone is correct; family-monorepo refactoring can happen in v2.
9. Push pentaphase too. Same logic. Both before end of week.
10. Schedule re-validation: every 90 days, run plugin-dev:plugin-validator against the current Claude Code plugin API to detect drift.

### Pre-launch checklist

- [ ] Before invoking `coliseum-orchestrator` on any real grain, confirm the grain has visible fan-out (3+ genuinely independent dimensions). If not, do not invoke.
- [ ] After invocation completes, check Phase-4 output length. If it ≥80% of summed return mass, it is stapled — invocation failed silently.
- [ ] Before pushing to remote, do `git init`, single commit, push to chosen home within 24h. Default home: personal-account standalone if higher-stakes decision blocks.
- [ ] Before declaring or building plugin #3, audit its actual work-shape. If it isn't a sequential phase-pipeline with discrete artifacts, refuse the family skeleton.
- [ ] Set calendar reminder: every 90 days, re-validate coliseum and pentaphase against current Claude Code plugin API.
