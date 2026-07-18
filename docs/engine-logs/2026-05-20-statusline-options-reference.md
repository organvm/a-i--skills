---
title: Claude Code statusLine — Complete Options Reference + Extension Roadmap
date: 2026-05-20
scope: home (~/.claude/settings.json)
status: reference
related:
  - ~/.claude/settings.json (current statusLine at line ~349)
  - https://code.claude.com/docs/en/statusline.md
  - https://code.claude.com/docs/en/settings.md
  - https://json.schemastore.org/claude-code-settings.json
---

# Claude Code statusLine — Complete Options Reference

## Why this file exists

The user asked "I want to see every option available" for the statusLine. This file captures the full surface (every settings field, every JSON payload field, every execution behavior) plus a gap analysis of what the current statusLine uses versus what's available — and a proposed extension roadmap.

This is a reference document, not an implementation plan in the strict sense, but it lives under `plans/` to:
1. Honor the home-scope plan discipline (`~/.claude/plans/YYYY-MM-DD-{slug}.md`).
2. Serve as the design substrate for future statusLine extensions (Section G below).

Cross-organ note: this is not project work; the durable form belongs at the home scope, not in any organ.

---

## A. The `statusLine` settings object — every field

```json
{
  "statusLine": {
    "type": "command",
    "command": "~/.claude/statusline.sh",
    "padding": 2,
    "refreshInterval": 5,
    "hideVimModeIndicator": false
  }
}
```

| Field | Type | Default | What it does |
|---|---|---|---|
| `type` | string | — | **Only `"command"` is supported.** No `static`, `disabled`, etc. To turn it off, delete the block or use `/statusline`. |
| `command` | string | — | Script path (supports `~/`) or inline shell command. Receives JSON on stdin. |
| `padding` | number | `0` | Extra leading horizontal spacing (chars). Relative indent, not absolute. |
| `refreshInterval` | seconds | unset | Re-runs on a timer **in addition to** event triggers. Min `1`. Set this if you want a live clock, countdown, or background-subagent updates while you're idle. |
| `hideVimModeIndicator` | bool | `false` | Suppress the built-in `-- INSERT --` line. Set `true` if you render `vim.mode` yourself. |

**Companion setting:** `subagentStatusLine` — same shape, but renders per-subagent rows. Each row receives a JSON object with `tasks[]` array (id, name, type, status, description, label, startTime, tokenCount, tokenSamples, cwd) and you emit one JSON-line per row: `{"id":"<task-id>","content":"<row body>"}`. Empty `content` hides the row.

---

## B. The full stdin JSON payload — every field

```json
{
  "cwd": "/path",
  "session_id": "abc123",
  "session_name": "feature-rename",
  "transcript_path": "/path/to/transcript.jsonl",
  "version": "2.1.90",
  "model": {
    "id": "claude-opus-4-7",
    "display_name": "Opus"
  },
  "workspace": {
    "current_dir": "/path",
    "project_dir": "/launch/path",
    "added_dirs": ["/extra/dir"],
    "git_worktree": "feature-xyz",
    "repo": {
      "host": "github.com",
      "owner": "anthropics",
      "name": "claude-code"
    }
  },
  "output_style": { "name": "default" },
  "cost": {
    "total_cost_usd": 0.0123,
    "total_duration_ms": 45000,
    "total_api_duration_ms": 2300,
    "total_lines_added": 156,
    "total_lines_removed": 23
  },
  "context_window": {
    "total_input_tokens": 15500,
    "total_output_tokens": 1200,
    "context_window_size": 200000,
    "used_percentage": 8,
    "remaining_percentage": 92,
    "current_usage": {
      "input_tokens": 8500,
      "output_tokens": 1200,
      "cache_creation_input_tokens": 5000,
      "cache_read_input_tokens": 2000
    }
  },
  "exceeds_200k_tokens": false,
  "effort": { "level": "high" },
  "thinking": { "enabled": true },
  "rate_limits": {
    "five_hour":  { "used_percentage": 23.5, "resets_at": 1738425600 },
    "seven_day":  { "used_percentage": 41.2, "resets_at": 1738857600 }
  },
  "vim": { "mode": "NORMAL" },
  "agent": { "name": "security-reviewer" },
  "pr": {
    "number": 1234,
    "url": "https://github.com/anthropics/claude-code/pull/1234",
    "review_state": "pending"
  },
  "worktree": {
    "name": "my-feature",
    "path": "/path/.claude/worktrees/my-feature",
    "branch": "worktree-my-feature",
    "original_cwd": "/path",
    "original_branch": "main"
  }
}
```

### Field-by-field

| Path | What it is |
|---|---|
| `cwd` | Current working dir. Same as `workspace.current_dir`. |
| `session_id` | Stable per session — use it for cache filenames. |
| `session_name` | Set via `--name` or `/rename`. **Absent if unnamed.** |
| `transcript_path` | JSONL transcript path. |
| `version` | Claude Code version. |
| `model.id` | E.g. `claude-opus-4-7`. |
| `model.display_name` | E.g. `Opus`. |
| `workspace.current_dir` | Where you are now. |
| `workspace.project_dir` | Where Claude Code launched. |
| `workspace.added_dirs[]` | Dirs added via `/add-dir` or `--add-dir`. |
| `workspace.git_worktree` | Git-worktree name (any linked worktree, not just `--worktree` sessions). **Absent in main tree.** |
| `workspace.repo.{host,owner,name}` | Git remote metadata. **Absent without `origin`.** |
| `output_style.name` | Current output style (e.g. `explanatory`). |
| `cost.total_cost_usd` | Client-side estimate (≠ billing). |
| `cost.total_duration_ms` | Wall-clock session ms. |
| `cost.total_api_duration_ms` | Time waiting on API. |
| `cost.total_lines_{added,removed}` | Code diff totals. |
| `context_window.total_input_tokens` | Live total (as of v2.1.132); cumulative before. |
| `context_window.total_output_tokens` | Output tokens last response. |
| `context_window.context_window_size` | `200000` or `1000000`. |
| `context_window.used_percentage` | 0–100, input-only. **May be null early.** |
| `context_window.remaining_percentage` | 0–100. **May be null early.** |
| `context_window.current_usage.input_tokens` | Fresh input. |
| `context_window.current_usage.output_tokens` | Last response output. |
| `context_window.current_usage.cache_creation_input_tokens` | Cache writes. |
| `context_window.current_usage.cache_read_input_tokens` | Cache hits. |
| `exceeds_200k_tokens` | Bool — fixed 200k threshold even on 1M-ctx models. |
| `effort.level` | `low` · `medium` · `high` · `xhigh` · `max`. **Absent if model lacks effort.** |
| `thinking.enabled` | Extended-thinking flag. |
| `rate_limits.five_hour.{used_percentage,resets_at}` | Pro/Max subscribers only. |
| `rate_limits.seven_day.{used_percentage,resets_at}` | Pro/Max subscribers only. |
| `vim.mode` | `NORMAL` · `INSERT` · `VISUAL` · `VISUAL LINE`. **Absent if vim disabled.** |
| `agent.name` | When `--agent` or agent settings active. |
| `pr.number` / `pr.url` | Open PR for current branch. **Removed once PR closes/merges.** |
| `pr.review_state` | `approved` · `pending` · `changes_requested` · `draft`. |
| `worktree.name` · `path` · `branch` · `original_cwd` · `original_branch` | Populated during `--worktree` sessions. `branch` and `original_branch` may be absent for hook-based worktrees. |

### Absent vs null — handle both

- **Absent** when context doesn't apply (no PR, no vim, not a subscriber, no worktree).
- **null** when the field exists but data isn't ready yet (`context_window.current_usage` is null pre-first-API-call and again right after `/compact`).

Defensive access patterns:

- **jq:** `.context_window.used_percentage // 0`
- **python:** `(data.get('context_window') or {}).get('used_percentage') or 0`
- **node:** `data?.context_window?.used_percentage ?? 0`

---

## C. Execution behavior

| Property | Value |
|---|---|
| **Event triggers** | New assistant message · `/compact` completion · permission-mode change · vim-mode toggle |
| **Debounce** | 300ms |
| **Cancellation** | New event mid-run cancels the in-flight script |
| **Token cost** | **Zero** — local execution, no API |
| **Hidden during** | Autocomplete · help menu · permission prompt |
| **Failure mode** | Non-zero exit / no output / hang → blank statusLine (no error shown unless `--debug`) |

---

## D. Colors & ANSI

| Format | Supported | Notes |
|---|---|---|
| ANSI 256-color (`\033[38;5;N m`) | Yes | Current implementation already uses this. |
| ANSI truecolor (`\033[38;2;R;G;B m`) | Yes | Terminal-dependent. |
| OSC 8 hyperlinks (`\033]8;;URL\a TEXT \033]8;;\a`) | Yes (terminal-dependent) | iTerm2/Kitty/WezTerm yes; **Terminal.app no**. Force with `FORCE_HYPERLINK=1 claude`. |

Claude Code **does not strip** escapes — they pass through. Width is finite; long lines truncate or wrap. Notifications/MCP-error toasts share the row right-edge.

---

## E. Environment variables

There is **no** documented `$CLAUDE_*` env-var contract for statusLine. The script inherits your shell environment (`$HOME`, `$PATH`, etc.) and receives all session data **only via stdin**. The single documented env-var is `FORCE_HYPERLINK=1` for OSC 8 detection override.

---

## F. Current statusLine state (verified 2026-05-20)

Verified at `~/.claude/settings.json` `statusLine` block. Currently renders:

| Used | Field |
|---|---|
| ✓ | `workspace.current_dir` (truncated to last 3 segments if depth > 4, `~`-substituted) |
| ✓ | `model.display_name` |
| ✓ | `context_window.remaining_percentage` |
| ✓ | (shells out to local `git` for branch + porcelain status — staged/modified/deleted/untracked counts) |
| ✓ | local clock (HH:MM via `date`) |

Tokyo Night palette via ANSI 256-color codes:
- Directory: `\033[38;5;111m` (blue `#7aa2f7`)
- Git branch: `\033[38;5;141m` (purple)
- Git status counts: `\033[38;5;210m` (red)
- Model: `\033[38;5;179m` (yellow)
- Time + ctx: `\033[38;5;146m` (grey)

Settings fields **not currently set**: `padding`, `refreshInterval`, `hideVimModeIndicator`.

JSON-payload fields **not currently consumed**: everything except the 3 above.

---

## G. Extension roadmap (prioritized)

Each entry: what it adds, which field(s) to wire in, expected payload-absence handling.

### Tier 1 — High signal-to-noise (recommended first)

1. **Effort badge** — `effort.level`
   - Why: user toggles effort with `/effort`; current level isn't visible anywhere else.
   - Absence: don't render if `effort` is missing.
   - Render: `effort:high` in yellow.

2. **PR badge** — `pr.number` + `pr.review_state`
   - Why: one glance tells you if a branch is review-ready.
   - Absence: omit if `pr` absent (no open PR on branch).
   - Render: `PR#1234 ✓` (✓=approved, !=changes_requested, ?=pending, ⋯=draft).

3. **Worktree name** — `worktree.name` OR `workspace.git_worktree`
   - Why: user spawns many background jobs in worktrees — disambiguation.
   - Absence: omit if main tree.
   - Render: append after branch name with distinct color.

### Tier 2 — Useful when stretching sessions

4. **Session name** — `session_name`
   - Why: branched conversations are hard to tell apart.
   - Render: `[session-name]` slot between branch and model.

5. **Rate-limit %** — `rate_limits.five_hour.used_percentage`
   - Why: pacing signal before hitting the wall.
   - Absence: omit for non-subscribers.
   - Render: `5h:23%` in muted color, red if >80%.

6. **Output style name** — `output_style.name`
   - Why: easy to forget you're in `explanatory` vs `default`.
   - Render: only show if non-default.

### Tier 3 — Nice-to-have

7. **Cost** — `cost.total_cost_usd`
   - Render: `$0.42` in grey, subtle.

8. **Context-window size flag** — `context_window.context_window_size`
   - Render: small `1M` badge if size == 1000000, else nothing.

9. **Vim mode** — `vim.mode` + set `hideVimModeIndicator: true`
   - Why: replaces ugly built-in `-- INSERT --` with palette-consistent rendering.
   - Render: colored mode tag matching palette.

10. **Agent name** — `agent.name`
    - Render when a subagent is the renderer (separate from `subagentStatusLine`).

---

## H. Implementation pattern (proposed extension)

The current script already has a Python block that extracts a handful of fields. Extension would:

1. Extend the Python extractor to pull additional fields (10 lines).
2. Add render-branch blocks for each new field (guard on absence).
3. Compose final `printf` with new optional segments interpolated.

No restructure needed — the existing architecture (Python-extracts-then-bash-renders) accommodates this cleanly. Estimated diff size: ~40 lines added to the inline `command`.

---

## I. Troubleshooting cheatsheet

| Symptom | Likely cause |
|---|---|
| Blank statusLine | Script not executable · writes to stderr not stdout · workspace trust not accepted · `disableAllHooks: true` |
| Stale data | Long-running script cancelled mid-run · cache file persists across sessions (use `session_id`, not `$$`) |
| Garbled output | Malformed escape sequence · truncation on narrow terminal · multi-line output |
| OSC 8 links not clickable | Terminal.app · SSH-stripping · try `FORCE_HYPERLINK=1` |
| `--` or `0` showing | Field was null/absent — add `// 0` fallback |

Debug with `claude --debug` to see the script's exit code and stderr.

---

## J. Next-action options for the user

- **No-op**: file saved for future reference.
- **Extend statusLine**: pick fields from Tier 1/2/3 above; this plan provides the extraction + render scaffold.
- **Set `refreshInterval`**: turn on time-based refresh (clock, rate-limit countdown).
- **Build `subagentStatusLine`**: separate companion config for per-subagent row rendering.

Plan persists at `~/.claude/plans/2026-05-20-statusline-options-reference.md`. Auto-synced via `domus-memory-sync` → chezmoi → GitHub.
