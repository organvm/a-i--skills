#!/usr/bin/env bash
set -euo pipefail

# prompt-relay.sh
# Receives feedback from an external agent and formats it for local processing.
#
# Usage: prompt-relay.sh <action> [options]
#   Actions:
#     receive   - Receive and parse feedback from external agent
#     format    - Format feedback into structured relay envelope
#     respond   - Generate response prompt for external agent
#     status    - Show relay status and pending items
#
# Options:
#   --from <agent-name>     Source agent identifier
#   --to <agent-name>       Target agent identifier
#   --session <session-id>  Session identifier for tracking
#   --file <path>           Path to feedback file
#   --output <path>         Output file path

ACTION="${1:-status}"
shift || true

# Parse options
FROM_AGENT=""
TO_AGENT=""
SESSION_ID=""
FILE_PATH=""
OUTPUT_PATH=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --from) FROM_AGENT="$2"; shift 2 ;;
        --to) TO_AGENT="$2"; shift 2 ;;
        --session) SESSION_ID="$2"; shift 2 ;;
        --file) FILE_PATH="$2"; shift 2 ;;
        --output) OUTPUT_PATH="$2"; shift 2 ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

# Defaults
FROM_AGENT="${FROM_AGENT:-unknown-agent}"
SESSION_ID="${SESSION_ID:-$(date +%Y%m%d-%H%M%S)}"
RELAY_DIR="${HOME}/.prompt-relay"
FEEDBACK_DIR="${RELAY_DIR}/feedback"
RESPONSE_DIR="${RELAY_DIR}/responses"

mkdir -p "$FEEDBACK_DIR" "$RESPONSE_DIR"

case "$ACTION" in
    receive)
        if [ -z "$FILE_PATH" ]; then
            echo "Error: --file required for receive action"
            exit 1
        fi
        
        if [ ! -f "$FILE_PATH" ]; then
            echo "Error: File not found: $FILE_PATH"
            exit 1
        fi
        
        # Parse feedback file
        FEEDBACK_ID="FB-${SESSION_ID}-$(date +%s)"
        OUTPUT_FILE="${FEEDBACK_DIR}/${FEEDBACK_ID}.md"
        
        cat > "$OUTPUT_FILE" << EOF
# Feedback Relay Envelope

## Metadata
- **Feedback ID**: ${FEEDBACK_ID}
- **Session ID**: ${SESSION_ID}
- **From Agent**: ${FROM_AGENT}
- **To Agent**: ${TO_AGENT:-local-agent}
- **Received**: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
- **Status**: PENDING

## Feedback Content
$(cat "$FILE_PATH")

## Processing Notes
- [ ] Acknowledge receipt
- [ ] Parse action items
- [ ] Generate response
- [ ] Close feedback loop
EOF
        
        echo "Feedback received: ${OUTPUT_FILE}"
        echo "Feedback ID: ${FEEDBACK_ID}"
        ;;
        
    format)
        if [ -z "$FILE_PATH" ]; then
            echo "Error: --file required for format action"
            exit 1
        fi
        
        if [ ! -f "$FILE_PATH" ]; then
            echo "Error: File not found: $FILE_PATH"
            exit 1
        fi
        
        # Format as structured relay envelope
        cat << EOF
---
type: prompt-relay-envelope
version: 1.0
---

# Prompt Relay Envelope

## Routing
- **From**: ${FROM_AGENT}
- **To**: ${TO_AGENT:-local-agent}
- **Session**: ${SESSION_ID}
- **Timestamp**: $(date -u +"%Y-%m-%dT%H:%M:%SZ")

## Payload
$(cat "$FILE_PATH")

## Instructions
Process the above feedback and generate a response using the respond action.
Include the session ID and feedback ID in your response for tracking.
EOF
        ;;
        
    respond)
        # Generate response prompt template
        cat << EOF
# Response Prompt for External Agent

## Context
- **Session ID**: ${SESSION_ID}
- **Responding To**: ${FROM_AGENT}
- **Timestamp**: $(date -u +"%Y-%m-%dT%H:%M:%SZ")

## Response Format

Provide your response in the following structure:

\`\`\`markdown
# Response Envelope

## Metadata
- **Response ID**: [Generate unique ID]
- **Session ID**: ${SESSION_ID}
- **From**: [Your agent name]
- **To**: ${FROM_AGENT}
- **Timestamp**: [Current timestamp]
- **In Response To**: [Feedback ID being addressed]

## Response Content
[Your response here]

## Action Items
- [ ] [List any action items]
- [ ] [List follow-up items]

## Status
[COMPLETE | PARTIAL | NEEDS_CLARIFICATION]
\`\`\`

## Guidelines
1. Address each point from the original feedback
2. Be specific about what was changed or decided
3. Note any items that need further discussion
4. Include the session ID for tracking
EOF
        ;;
        
    status)
        echo "=== Prompt Relay Status ==="
        echo "Relay directory: ${RELAY_DIR}"
        echo ""
        
        FEEDBACK_COUNT=$(ls "$FEEDBACK_DIR"/*.md 2>/dev/null | wc -l | tr -d ' ')
        RESPONSE_COUNT=$(ls "$RESPONSE_DIR"/*.md 2>/dev/null | wc -l | tr -d ' ')
        
        echo "Feedback received: ${FEEDBACK_COUNT}"
        echo "Responses sent: ${RESPONSE_COUNT}"
        echo ""
        
        if [ "$FEEDBACK_COUNT" -gt 0 ]; then
            echo "Recent feedback:"
            ls -t "$FEEDBACK_DIR"/*.md 2>/dev/null | head -5 | while read -r f; do
                basename "$f"
            done
        fi
        ;;
        
    *)
        echo "Unknown action: ${ACTION}"
        echo "Usage: prompt-relay.sh <receive|format|respond|status> [options]"
        exit 1
        ;;
esac
