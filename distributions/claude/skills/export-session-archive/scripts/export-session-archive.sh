#!/usr/bin/env bash
set -euo pipefail

# export-session-archive.sh
# Exports all reports and session transcripts to markdown in a structured archive.
#
# Usage: export-session-archive.sh [output-dir] [workspace-root] [code-root]
#   output-dir:    Directory for export (default: ~/export-$(date +%Y-%m-%d))
#   workspace-root: Root workspace directory (default: ~/Workspace)
#   code-root:     Root code directory (default: ~/Code)

OUTPUT_DIR="${1:-$HOME/export-$(date +%Y-%m-%d)}"
WORKSPACE_ROOT="${2:-$HOME/Workspace}"
CODE_ROOT="${3:-$HOME/Code}"

echo "=== Session Archive Export ==="
echo "Output: $OUTPUT_DIR"
echo "Workspace: $WORKSPACE_ROOT"
echo "Code: $CODE_ROOT"
echo ""

# Create directory structure
mkdir -p "$OUTPUT_DIR"/{plans,transcripts/claude,transcripts/specstory,sessions,reports}

# 1. Export Claude plans
echo "Exporting plans..."
if [ -d "$HOME/.claude/plans" ]; then
    cp "$HOME/.claude/plans"/*.md "$OUTPUT_DIR/plans/" 2>/dev/null || true
    PLAN_COUNT=$(ls "$OUTPUT_DIR/plans/"*.md 2>/dev/null | wc -l | tr -d ' ')
    echo "  Plans: $PLAN_COUNT files"
else
    echo "  No plans directory found"
    PLAN_COUNT=0
fi

# 2. Export Claude session transcripts
echo "Exporting Claude transcripts..."
CLAUDE_COUNT=0
for root in "$WORKSPACE_ROOT" "$CODE_ROOT"; do
    if [ -d "$root" ]; then
        find "$root" -path "*/.claude/sessions/*" -name "*.md" 2>/dev/null | while read -r f; do
            session_name=$(echo "$f" | sed 's|.*/.claude/sessions/||' | sed 's|/[^/]*$||')
            mkdir -p "$OUTPUT_DIR/transcripts/claude/$session_name"
            cp "$f" "$OUTPUT_DIR/transcripts/claude/$session_name/"
        done
    fi
done
CLAUDE_COUNT=$(find "$OUTPUT_DIR/transcripts/claude" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
echo "  Claude transcripts: $CLAUDE_COUNT files"

# 3. Export SpecStory sessions
echo "Exporting SpecStory sessions..."
SPECSTORY_COUNT=0
for root in "$WORKSPACE_ROOT" "$CODE_ROOT"; do
    if [ -d "$root" ]; then
        find "$root" -path "*/.specstory/history/*" -name "*.md" 2>/dev/null | while read -r f; do
            session_name=$(echo "$f" | sed 's|.*/.specstory/history/||' | sed 's|/[^/]*$||')
            mkdir -p "$OUTPUT_DIR/transcripts/specstory/$session_name"
            cp "$f" "$OUTPUT_DIR/transcripts/specstory/$session_name/"
        done
    fi
done
SPECSTORY_COUNT=$(find "$OUTPUT_DIR/transcripts/specstory" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
echo "  SpecStory sessions: $SPECSTORY_COUNT files"

# 4. Export organized session files
echo "Exporting session files..."
SESSION_COUNT=0
for root in "$WORKSPACE_ROOT" "$CODE_ROOT"; do
    if [ -d "$root" ]; then
        find "$root" -path "*/sessions/*" -name "*.md" \
            -not -path "*/.specstory/*" \
            -not -path "*/.claude/*" \
            -not -path "*/.codex/*" 2>/dev/null | while read -r f; do
            session_path=$(echo "$f" | sed 's|.*/sessions/||' | sed 's|/[^/]*$||')
            mkdir -p "$OUTPUT_DIR/sessions/$session_path"
            cp "$f" "$OUTPUT_DIR/sessions/$session_path/"
        done
    fi
done
SESSION_COUNT=$(find "$OUTPUT_DIR/sessions" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
echo "  Session files: $SESSION_COUNT files"

# 5. Export reports, audits, evaluations, summaries
echo "Exporting reports..."
REPORT_COUNT=0
for root in "$WORKSPACE_ROOT" "$CODE_ROOT"; do
    if [ -d "$root" ]; then
        find "$root" -maxdepth 5 \
            \( -name "*report*.md" -o -name "*REPORT*.md" \
               -o -name "*evaluation*.md" -o -name "*EVALUATION*.md" \
               -o -name "*audit*.md" -o -name "*AUDIT*.md" \
               -o -name "*CLOSEOUT*.md" -o -name "*closeout*.md" \
               -o -name "*summary*.md" -o -name "*SUMMARY*.md" \) \
            -not -path "*/node_modules/*" \
            -not -path "*/.git/*" \
            -not -path "*/sessions/*" \
            -not -path "*/.specstory/*" \
            -not -path "*/.claude/*" \
            -not -path "*/.codex/*" 2>/dev/null | while read -r f; do
            rel_path=$(echo "$f" | sed "s|^$root/||" | sed 's|/[^/]*$||')
            mkdir -p "$OUTPUT_DIR/reports/$rel_path"
            cp "$f" "$OUTPUT_DIR/reports/$rel_path/"
        done
    fi
done
REPORT_COUNT=$(find "$OUTPUT_DIR/reports" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
echo "  Reports: $REPORT_COUNT files"

# 6. Generate manifest
TOTAL=$((PLAN_COUNT + CLAUDE_COUNT + SPECSTORY_COUNT + SESSION_COUNT + REPORT_COUNT))
cat > "$OUTPUT_DIR/MANIFEST.md" << EOF
# Session Archive Manifest

## Export Date
$(date +%Y-%m-%d)

## Structure
\`\`\`
$(basename "$OUTPUT_DIR")/
├── MANIFEST.md                    # This file
├── plans/                         # Claude Code plans ($PLAN_COUNT files)
├── transcripts/
│   ├── claude/                    # Claude session transcripts ($CLAUDE_COUNT files)
│   └── specstory/                 # SpecStory session history ($SPECSTORY_COUNT files)
├── sessions/                      # Organized session files ($SESSION_COUNT files)
└── reports/                       # Reports, audits, evaluations, summaries ($REPORT_COUNT files)
\`\`\`

## Totals
- **Plans**: $PLAN_COUNT
- **Claude transcripts**: $CLAUDE_COUNT
- **SpecStory sessions**: $SPECSTORY_COUNT
- **Organized sessions**: $SESSION_COUNT
- **Reports**: $REPORT_COUNT
- **Total**: $TOTAL markdown files

## Source Directories
- Plans: \`~/.claude/plans/\`
- Claude transcripts: \`Workspace/**/*.claude/sessions/\`, \`Code/**/*.claude/sessions/\`
- SpecStory: \`Workspace/**/*.specstory/history/\`, \`Code/**/*.specstory/history/\`
- Sessions: \`Workspace/**/sessions/\`, \`Code/**/sessions/\`
- Reports: Scattered across Workspace and Code

## Notes
- All files are markdown (.md)
- Directory structure preserved where applicable
- No binary files included
- No node_modules or .git directories included
EOF

echo ""
echo "=== Export Complete ==="
echo "Total: $TOTAL markdown files"
echo "Location: $OUTPUT_DIR"
echo "Manifest: $OUTPUT_DIR/MANIFEST.md"
