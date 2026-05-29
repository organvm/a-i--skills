# Prompt Relay Protocol

## Overview

The prompt relay protocol enables structured feedback exchange between AI agents operating in different contexts or sessions. It provides a standardized envelope format for routing, tracking, and processing feedback.

## Envelope Structure

Every relay message uses this structure:

```markdown
---
type: prompt-relay-envelope
version: 1.0
---

# Prompt Relay Envelope

## Routing
- **From**: [Source agent identifier]
- **To**: [Target agent identifier]
- **Session**: [Session ID for tracking]
- **Timestamp**: [ISO 8601 timestamp]

## Payload
[Feedback content, instructions, or response]

## Instructions
[Processing instructions for the receiving agent]
```

## Feedback Categories

### 1. Code Review Feedback
- Specific file and line references
- Suggested changes
- Rationale for changes

### 2. Architecture Feedback
- System design observations
- Pattern recommendations
- Trade-off analysis

### 3. Process Feedback
- Workflow improvements
- Communication gaps
- Coordination needs

### 4. Quality Feedback
- Testing gaps
- Documentation issues
- Performance concerns

## Response Status Codes

| Status | Meaning | Action Required |
|--------|---------|-----------------|
| COMPLETE | Feedback fully addressed | Close loop |
| PARTIAL | Partially addressed | Follow-up needed |
| NEEDS_CLARIFICATION | Unclear feedback | Request clarification |
| DEFERRED | Valid but not now | Schedule for later |
| REJECTED | Disagree with feedback | Provide rationale |

## Session Tracking

Each session gets a unique ID: `YYYYMMDD-HHMMSS`
Each feedback gets a unique ID: `FB-{SESSION_ID}-{TIMESTAMP}`
Each response gets a unique ID: `RESP-{SESSION_ID}-{TIMESTAMP}`

## Best Practices

1. **Include context**: Always reference the original feedback ID
2. **Be specific**: Reference files, lines, and concrete examples
3. **Track status**: Update feedback status as items are addressed
4. **Close loops**: Mark feedback as complete when resolved
5. **Preserve history**: Keep all relay envelopes for audit trail
