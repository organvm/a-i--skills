# Canonical Relay-Injection Phrase

The minimal text to inject into a fresh agent's context to signal "this is a
relay, pick up from the pointer." Use the shortest variant that fits the
situation.

## Minimal form (≤30 tokens)

```
Continue from relay at <pointer-path>. <state-line>.
```

Substitute `<pointer-path>` with an absolute path to a pickup file (see
`pickup-paths.md`). Substitute `<state-line>` from the table below.

## State-line vocabulary

| State line | When to use |
|---|---|
| `quiet pickup — no in-flight work` | Prior session closed cleanly; pointer documents context only |
| `mid-task — see Next Actions for current step` | Work in progress; receiving agent should resume from pointer's Next Actions section |
| `error-recovery — prior session failed at <step>` | Previous attempt errored; pointer documents what was tried |
| `bridge-attach — no transcript inheritance` | Teleport / cross-session attach; local transcript starts cold |

## No-pointer-yet variant (≤25 tokens)

When no pointer file has been written but you still want to inject scope
context:

```
Cold ground — see <closeout-path> for prior session's scope.
```

Substitute `<closeout-path>` with the most recent closeout file at the
relevant scope (e.g., `~/.claude/plans/closeout-{YYYY-MM-DD}-{scope-slug}.md`).

## Usage notes

- The phrase is **inject-only**: paste into the receiving agent's first
  prompt. Do not embed in the pointer file itself — the pointer carries
  substance, the phrase carries routing.
- Receiving agent reads the pointer file as its first action. The phrase
  tells it to do so; the pointer file carries the work.
- For richer context transfer (≥500 tokens), use `standard-envelope.md` as
  the pointer file's body.
- The state line classifies **what kind of pickup** (quiet / mid-task /
  error / bridge), not **what's pending**. What's pending lives in the
  pointer's Next Actions section.
