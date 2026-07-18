---
title: Claude Code Hooks — Complete Options Reference
date: 2026-05-20
scope: home (~/.claude/settings.json)
status: reference
extracted_from: /Users/4jp/.claude/projects/-Users-4jp/9cb55c4d-3191-4b61-a8e8-192e4710affb.jsonl
extraction_date: 2026-05-22
related:
  - ~/.claude/settings.json (34-hook census; PreToolUse/SessionStart/etc.)
  - https://code.claude.com/docs/en/hooks.md
  - 2026-05-20-statusline-options-reference.md (LOG #1 sibling)
  - 2026-05-20-subagents-options-reference.md (LOG #3 sibling)
---

# Claude Code Hooks — Complete Options Reference

## Why this file exists

This was delivered inline as "LOG #2" in session `9cb55c4d` (2026-05-20) but never persisted as a file — closeout flagged it as "at risk: inline only". Promoted to a plan file 2026-05-22 under "find their gravitational logical center" authorization, mirroring the precedent set by `2026-05-20-statusline-options-reference.md` (LOG #1).

The content below is the verbatim transcript-canonical reference, extracted via `jq` from the JSONL. Cross-references to "your" / "current setup" refer to the session-author's environment (34-hook census in `~/.claude/settings.json`).

---

## LOG #2 — Hooks: Complete Reference

Sources: https://code.claude.com/docs/en/hooks.md

### A. The hook settings block — every field

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolName|OtherTool|*",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/script.sh",
            "args": ["arg1"],
            "timeout": 600,
            "shell": "bash",
            "async": false,
            "asyncRewake": false,
            "if": "Bash(git *)",
            "statusMessage": "Running validation..."
          }
        ]
      }
    ]
  },
  "disableAllHooks": false
}
```

**Settings location hierarchy** (later overrides earlier within event):

```
Managed policy settings         (org-wide, highest authority)
~/.claude/settings.json         (user-wide)
.claude/settings.json           (project-wide, version-controlled)
.claude/settings.local.json     (project local, gitignored)
Plugin's hooks/hooks.json       (when plugin enabled)
Skill/Agent frontmatter         (component lifetime, narrowest scope)
```

You write hooks at `private_dot_claude/settings.json.tmpl` → renders to `~/.claude/settings.json`. To scope a hook to one plugin only, put it in that plugin's `hooks/hooks.json`.

### B. Handler type field — five values, each with its own schema

```
Field: type      Value          Body fields
                 "command"      command, args?, timeout?, shell?, async?, asyncRewake?, if?, statusMessage?
                 "http"         url, headers?, allowedEnvVars?, timeout?
                 "mcp_tool"     server, tool, input?, timeout?
                 "prompt"       prompt, model?, timeout?
                 "agent"        prompt, timeout?
```

**Path placeholders inside `command` (and `args`):**

- `${CLAUDE_PROJECT_DIR}` → project root at session start
- `${CLAUDE_PLUGIN_ROOT}` → plugin install dir
- `${CLAUDE_PLUGIN_DATA}` → plugin persistent data dir
- `${tool_input.command}`, `${tool_input.file_path}` etc → substituted from current event's payload (also available via stdin)

**Exec form vs shell form:**
- `args` present → spawns directly, no tokenization (safest)
- `args` absent → uses shell (`sh -c` / PowerShell / Git Bash); shell expansion applies

### C. Every hook event — categorized

**Per-session (3):**

| Event | Matcher | Blocks? | Inputs |
|---|---|---|---|
| `SessionStart` | source (`startup`, `resume`, `clear`, `compact`) | no | `source`, `model`, has `CLAUDE_ENV_FILE` |
| `Setup` | flag (`init`, `maintenance`) | no | only fires with `--init-only` / `--maintenance` |
| `SessionEnd` | reason (`clear`, `resume`, `logout`, `prompt_input_exit`) | no | end reason |

**Per-turn (4):**

| Event | Matcher | Blocks? |
|---|---|---|
| `UserPromptSubmit` | (none) | yes (rejects prompt) |
| `UserPromptExpansion` | command/skill name | yes |
| `Stop` | (none) | yes (forces Claude to continue) |
| `StopFailure` | error type (`rate_limit`, `authentication_failed`, `server_error`) | no |

**Per-tool-call (6):**

| Event | Matcher | Blocks? |
|---|---|---|
| `PreToolUse` | tool name | yes (deny/ask/defer/modify-input) |
| `PermissionRequest` | tool name | yes |
| `PermissionDenied` | tool name | no (but can `retry: true`) |
| `PostToolUse` | tool name | no |
| `PostToolUseFailure` | tool name | no |
| `PostToolBatch` | (none) | no |

**Async / observability (12):**

| Event | Matcher |
|---|---|
| `Notification` | notification type |
| `SubagentStart` / `SubagentStop` | agent type |
| `TaskCreated` / `TaskCompleted` | (block-able) |
| `TeammateIdle` | (block-able via `continue: false`) |
| `InstructionsLoaded` | load reason |
| `ConfigChange` | source (`user_settings`, `project_settings`, `local_settings`, `policy_settings`, `skills`) |
| `CwdChanged` | (none) |
| `FileChanged` | literal filenames, `\|`-separated |
| `WorktreeCreate` / `WorktreeRemove` | hook can override default worktree path |
| `PreCompact` / `PostCompact` | trigger (`manual`, `auto`) |
| `Elicitation` / `ElicitationResult` | MCP server name |

### D. Matcher syntax

```
Pattern                          Evaluation
"*", "", or omitted              match all
[a-zA-Z0-9_|]-only string        exact match or |-separated list ("Bash", "Edit|Write")
anything else                    JavaScript regex ("^Notebook", "mcp__memory__.*")
```

MCP tool naming: `mcp__<server>__<tool>`. To match server-wide use regex form: `mcp__memory__.*` (the `.*` is required — `mcp__memory__` alone won't match anything).

### E. Hook stdin JSON payload — common fields received by every hook

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/dir",
  "permission_mode": "default|plan|acceptEdits|auto|dontAsk|bypassPermissions",
  "effort": { "level": "low|medium|high|xhigh|max" },
  "hook_event_name": "PreToolUse",
  "agent_id": "subagent-123",
  "agent_type": "Explore|Plan|general-purpose|<custom>"
}
```

Plus event-specific fields:
- `PreToolUse` / `PostToolUse` → `tool_name`, `tool_input`, `tool_response`
- `UserPromptSubmit` → `prompt`
- `SessionStart` → `source`, `model`
- `FileChanged` → `file_path`, `change_type`
- `CwdChanged` → `new_cwd`, `previous_cwd`
- `InstructionsLoaded` → `file_path`, `load_reason`, `memory_type`
- `PreCompact` / `PostCompact` → `compaction_trigger`, `reason`, `preTokens`
- `StopFailure` → `error_type`, `error_message`
- `Notification` → `notification_type`, `title`, `body`
- `Elicitation` → `mcp_server`, `form_schema`
- `TaskCreated` / `TaskCompleted` → `task_id`, `task_name`, `task_description`, `status`

### F. Hook stdout JSON response — every field

**Universal (all events):**

```json
{
  "continue": true|false,
  "stopReason": "User-facing message when continue=false",
  "suppressOutput": false,
  "systemMessage": "Warning shown to user",
  "terminalSequence": "\033]777;notify;Title;Body\007"
}
```

**Top-level decision pattern** (UserPromptSubmit, UserPromptExpansion, PostToolUse*, Stop, SubagentStop, ConfigChange, PreCompact, TaskCreated, TaskCompleted, TeammateIdle):

```json
{
  "decision": "block",
  "reason": "Explanation shown",
  "hookSpecificOutput": {
    "hookEventName": "<event>",
    "additionalContext": "Info injected into Claude's context"
  }
}
```

**PreToolUse-specific:**

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow|deny|ask|defer",
    "permissionDecisionReason": "Why",
    "updatedInput": { "command": "modified command" },
    "additionalContext": "Info for Claude"
  }
}
```

**PermissionRequest-specific:**

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow|deny",
      "updatedInput": { "command": "..." },
      "permissionRule": "Bash(.*)"
    }
  }
}
```

**WorktreeCreate-specific:** command hook prints path to stdout (raw), or HTTP returns `worktreePath` in `hookSpecificOutput`. Non-zero exit fails creation.

**Elicitation-specific:**

```json
{
  "hookSpecificOutput": {
    "hookEventName": "Elicitation",
    "action": "accept|decline|cancel",
    "content": { "field_name": "field_value" }
  }
}
```

### G. Exit code semantics for command hooks

| Code | Meaning | Effect |
|---|---|---|
| 0 | Success | parse stdout as JSON (or use as `additionalContext` if plain text) |
| 2 | Blocking error | read stderr; block if event supports it (see table below) |
| Other | Non-blocking error | first line of stderr shown in transcript; execution continues |

**Exit code 2 — which events actually block:**

| Event | Blocks |
|---|---|
| PreToolUse, PermissionRequest, UserPromptSubmit, UserPromptExpansion, Stop, SubagentStop, TeammateIdle, TaskCreated, TaskCompleted, ConfigChange, PreCompact | YES |
| PostToolUse, PostToolUseFailure, PermissionDenied, Notification, all observability events | NO (stderr shown only) |

### H. HTTP hook response handling

| Response | Treated as |
|---|---|
| 2xx + empty body | exit 0 equivalent |
| 2xx + plain text | exit 0, text → additionalContext |
| 2xx + JSON | exit 0, parsed as full hook output |
| Non-2xx | non-blocking error |
| Connection failure / timeout | non-blocking error |

To block via HTTP: 2xx + JSON containing `decision: "block"` or `permissionDecision: "deny"`.

### I. Environment variables available to hook commands

```
CLAUDE_PROJECT_DIR    project root (constant)
CLAUDE_PLUGIN_ROOT    plugin install dir (only if hook from plugin)
CLAUDE_PLUGIN_DATA    plugin persistent data dir
CLAUDE_ENV_FILE       writable env-export file (SessionStart, Setup, CwdChanged, FileChanged only)
CLAUDE_CODE_REMOTE    "true" in remote envs
CLAUDE_EFFORT         current effort level (CC ≥ 2.1.136)
```

**Persisting env vars across the session** — write `export FOO=bar` lines (with `>>`) to `$CLAUDE_ENV_FILE` during SessionStart or Setup. They become available to every subsequent Bash tool call.

### J. Execution behavior

| Property | Value |
|---|---|
| Default timeout | 600s (command/http/mcp_tool), 30s (prompt and UserPromptSubmit), 60s (agent) |
| Parallel execution | all matching hooks for an event run in parallel |
| Deduplication | identical handlers (same command/URL/etc.) run once even if matched multiple times |
| Output truncation | string fields capped at 10,000 chars; overflow saved to file with preview |
| Cancellation | New event mid-run cancels in-flight script |
| Token cost | zero — local execution, no API |

### K. What your settings.json currently covers vs. doesn't

Your census (per `/Users/4jp/CLAUDE.md` hook reference):

```
PreToolUse:        16   ← covered
SessionStart:       5   ← covered
SessionEnd:         5   ← covered
UserPromptSubmit:   3   ← covered
PostToolUse:        4   ← covered
Stop:               1   ← covered
                  ───
                   34
```

Events with **zero coverage** but high signal-to-noise for your workflow:

| Event | Why it'd help |
|---|---|
| `PreCompact` | Auto-archive working state before compaction destroys turn-local diagnostic context. You already auto-archive `/insights` on SessionEnd — `PreCompact` is the parallel hook for mid-session compactions. |
| `FileChanged` (matcher `.env\|.envrc\|*.toml`) | Detect when secrets files are written (defensive). Pairs with your security-essentials-pack skill. |
| `StopFailure` (matcher `rate_limit`) | Persist a marker when you hit Pro/Max limits so you can correlate sessions to limit windows. |
| `SubagentStart` / `SubagentStop` | Track fleet dispatch volume; you have a Dispatch Protocol — these events are the audit trail. |
| `InstructionsLoaded` (matcher `compact`) | Observe CLAUDE.md re-loads after compaction; useful for diagnosing the memory-regression class of bugs you hit on 2026-05-20. |
| `Elicitation` (matcher specific MCP server) | Auto-approve or auto-fill MCP server prompts (Figma/Notion/etc.) that you always answer the same way. |
| `TaskCreated` / `TaskCompleted` | If you ever start using TaskCreate heavily; gives task-creation observability. |
| `PermissionDenied` | Log every classifier denial so you can see what `auto` mode is blocking. Sibling to your `feedback_unauthorized_commit_chezmoi` rule — empirical data on what gets blocked. |

### L. Common patterns

**Block dangerous Bash:**

```bash
#!/usr/bin/env bash
set -euo pipefail
INPUT=$(cat)
CMD=$(echo "$INPUT" | jq -r '.tool_input.command // empty')
if echo "$CMD" | grep -qE '^\s*(rm -rf /|brew zap)'; then
  echo "Blocked: destructive operation" >&2
  exit 2
fi
exit 0
```

**Inject SessionStart context:**

```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Branch: main | Uncommitted: 3 files"
  }
}
```

**Auto-approve a class of operations** (PreToolUse):

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "permissionDecisionReason": "Read-only operation in allowed directory"
  }
}
```

**Conditional firing via `if`:**

```json
{ "type": "command", "if": "Bash(git push *)", "command": "guard-no-force-push.sh" }
```

The `if` field is a permission-rule grammar — `Bash(<glob>)`, `Edit(<glob>)` etc. **Warning per your CLAUDE.md:** JSON formatters strip unknown `if` fields. Verify after any `jq` pass.

### M. Debugging cheatsheet

| Symptom | Cause |
|---|---|
| Hook silently doesn't fire | matcher regex mismatch · `disableAllHooks: true` · workspace trust not accepted |
| Exit 2 doesn't block | event doesn't support blocking (see table above) · exit code 1 was used instead |
| JSON output ignored | non-zero exit code (JSON only parsed on exit 0) · JSON not on stdout |
| Hook output truncated | over 10,000 chars — check the overflow file path printed in transcript |
| `$CLAUDE_TOOL_INPUT` empty | bug class you hit 2026-05-17; use stdin JSON not the env-var (verified working: `INPUT=$(cat)`) |

Run `claude --debug` to see hook stderr in the debug log. Use `/hooks` interactively to browse what's configured + where it's sourced from.

---
