---
name: export-session-archive
description: Exports all reports and session transcripts to markdown in a structured archive. Bundles Claude plans, session transcripts, SpecStory history, organized session files, and reports/audits/summaries into a dated export directory with manifest. Triggers on export sessions, archive transcripts, backup reports, or session documentation requests.
---

## Purpose

Export all AI session artifacts (plans, transcripts, reports) from workspace and code directories into a structured markdown archive with manifest. This skill consolidates scattered session data into a single portable export.

## When to Use

- User requests to export sessions, transcripts, or reports
- Archiving session history before cleanup or migration
- Creating a backup of all AI interaction artifacts
- Preparing session data for analysis or review

## Export Structure

The export creates a dated directory with five categories:

```
export-YYYY-MM-DD/
├── MANIFEST.md                    # Auto-generated manifest with counts
├── plans/                         # Claude Code plans (~/.claude/plans/)
├── transcripts/
│   ├── claude/                    # Claude session transcripts (.claude/sessions/)
│   └── specstory/                 # SpecStory history (.specstory/history/)
├── sessions/                      # Organized session files (*/sessions/)
└── reports/                       # Reports, audits, evaluations, summaries
```

## Execution

To export all session artifacts, run the bundled script:

```bash
scripts/export-session-archive.sh [output-dir] [workspace-root] [code-root]
```

Arguments:
- `output-dir`: Export destination (default: `~/export-$(date +%Y-%m-%d)`)
- `workspace-root`: Workspace directory (default: `~/Workspace`)
- `code-root`: Code directory (default: `~/Code`)

Example:

```bash
# Export to default location
scripts/export-session-archive.sh

# Export to custom location
scripts/export-session-archive.sh /path/to/archive ~/MyWorkspace ~/MyCode
```

## What Gets Exported

| Category | Source Pattern | File Types |
|----------|---------------|------------|
| Plans | `~/.claude/plans/*.md` | All plan files |
| Claude transcripts | `**/.claude/sessions/**/*.md` | transcript.md, prompts.md, review.md |
| SpecStory sessions | `**/.specstory/history/**/*.md` | Session history files |
| Organized sessions | `**/sessions/**/*.md` (excluding .specstory, .claude, .codex) | Session documentation |
| Reports | `**/*{report,audit,evaluation,closeout,summary}*.md` | Reports and summaries |

## Exclusions

The following are explicitly excluded:
- `node_modules/` directories
- `.git/` directories
- Session files already under `.specstory/`, `.claude/`, or `.codex/` (to avoid double-counting in reports category)

## Output

The script prints a summary table and generates `MANIFEST.md` with:
- Export date
- Directory structure with file counts
- Total file count
- Source directory mapping
- Notes on export scope
