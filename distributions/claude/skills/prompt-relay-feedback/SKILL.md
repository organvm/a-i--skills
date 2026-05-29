---
name: prompt-relay-feedback
description: Provides structured prompt relay envelopes for receiving and processing feedback from external AI agents. Handles feedback routing, formatting, response generation, and session tracking across agent boundaries. Triggers on cross-agent feedback, external review comments, multi-agent coordination, or feedback relay requests.
---

## Purpose

Enable structured feedback exchange between AI agents operating in different contexts, sessions, or systems. This skill provides standardized envelope formats, routing protocols, and tracking mechanisms for cross-agent communication.

## When to Use

- Receiving feedback from another AI agent (Codex, Gemini, Claude, etc.)
- Coordinating work across multiple agent sessions
- Processing external review comments or suggestions
- Managing multi-agent workflows with handoff points
- Tracking feedback loops between agents

## Relay Architecture

```
External Agent → [Feedback Envelope] → Local Agent → [Response Envelope] → External Agent
```

Each relay cycle:
1. External agent generates feedback
2. Feedback wrapped in relay envelope
3. Local agent processes feedback
4. Response wrapped in relay envelope
5. Response returned to external agent

## Forward Handoff vs Inbound Feedback

The skill covers two relay directions, which use different storage and tooling:

| Direction | What | Tooling | Storage |
|---|---|---|---|
| **Inbound feedback** | External agent sends review/comments TO local agent | `scripts/prompt-relay.sh receive` | `~/.prompt-relay/feedback/FB-*.md` |
| **Forward handoff** | Local agent passes work TO next session/agent | Direct markdown write (no script) | Target-agent's pickup path (see `assets/pickup-paths.md`) |

### Canonical phrase (forward handoff)

To inject a forward handoff into a fresh agent's context, use the canonical phrase from `assets/canonical-phrase.md`:

```
Continue from relay at <pointer-path>. <state-line>.
```

The `<pointer-path>` is the absolute path to a file containing a filled `assets/standard-envelope.md` template. The `<state-line>` is one of the controlled-vocabulary entries (`quiet pickup`, `mid-task`, etc.).

### Pickup paths

Different target agents look in different places. See `assets/pickup-paths.md` for the per-agent table. Headline:

- Claude → `~/.claude/plans/{date}-handoff-{slug}.md`
- Codex → `~/bound/.Codex/handoffs/{date}-{slug}-pointer.md`

### Standard envelope template

The medium-compression handoff template is `assets/standard-envelope.md`. A worked example is at `assets/examples/worked-handoff.md`.

The existing FB-* inbound-feedback pipeline (sections below) is **unchanged**.

## Receiving Feedback

To receive feedback from an external agent, run:

```bash
scripts/prompt-relay.sh receive \
    --from <agent-name> \
    --session <session-id> \
    --file <path-to-feedback>
```

This creates a structured feedback envelope in `~/.prompt-relay/feedback/` with:
- Unique feedback ID for tracking
- Metadata (source, session, timestamp)
- Original feedback content
- Processing checklist

## Formatting Feedback

To format raw feedback into a relay envelope:

```bash
scripts/prompt-relay.sh format \
    --from <agent-name> \
    --session <session-id> \
    --file <path-to-feedback>
```

Outputs a properly formatted relay envelope to stdout.

## Generating Response Prompts

To generate a response prompt template for replying to external feedback:

```bash
scripts/prompt-relay.sh respond \
    --from <agent-name> \
    --session <session-id>
```

Outputs a structured response prompt that ensures:
- All feedback points are addressed
- Session tracking is maintained
- Response status is clear
- Action items are documented

## Checking Relay Status

To view relay status and pending items:

```bash
scripts/prompt-relay.sh status
```

Shows:
- Total feedback received
- Total responses sent
- Recent feedback files

## Envelope Format

All relay messages follow this structure:

```markdown
---
type: prompt-relay-envelope
version: 1.0
---

# Prompt Relay Envelope

## Routing
- **From**: [Source agent]
- **To**: [Target agent]
- **Session**: [Session ID]
- **Timestamp**: [ISO 8601]

## Payload
[Content]

## Instructions
[Processing instructions]
```

## Response Status Codes

| Status | Meaning |
|--------|---------|
| COMPLETE | Feedback fully addressed |
| PARTIAL | Partially addressed |
| NEEDS_CLARIFICATION | Unclear feedback |
| DEFERRED | Valid but not now |
| REJECTED | Disagree with rationale |

## Session Tracking

- Session ID format: `YYYYMMDD-HHMMSS`
- Feedback ID format: `FB-{SESSION_ID}-{TIMESTAMP}`
- Response ID format: `RESP-{SESSION_ID}-{TIMESTAMP}`

## Best Practices

1. Always include the original feedback ID in responses
2. Reference specific files, lines, and examples
3. Update feedback status as items are addressed
4. Preserve all relay envelopes for audit trail
5. Close feedback loops explicitly

## References

For detailed protocol specification, see `references/relay-protocol.md`.
