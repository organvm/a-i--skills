---
title: Claude Code Subagents — Complete Options Reference
date: 2026-05-20
scope: home (~/.claude/agents/, ~/.claude/settings.json)
status: reference
extracted_from: /Users/4jp/.claude/projects/-Users-4jp/9cb55c4d-3191-4b61-a8e8-192e4710affb.jsonl
extraction_date: 2026-05-22
related:
  - ~/.claude/agents/ (~30+ agents incl. plugin-dev, feature-dev, pr-review-toolkit, vercel)
  - https://code.claude.com/docs/en/sub-agents.md
  - 2026-05-20-statusline-options-reference.md (LOG #1 sibling)
  - 2026-05-20-hooks-options-reference.md (LOG #2 sibling)
---

# Claude Code Subagents — Complete Options Reference

## Why this file exists

Delivered inline as "LOG #3" in session `9cb55c4d` (2026-05-20). Promoted to a plan file 2026-05-22 alongside LOG #2 (Hooks) under "gravitational logical center" authorization — same precedent as LOG #1 (statusLine).

The closing three-engine-stack Insight block is preserved inside this file because it's the *cross-reference* between LOG #1, #2, and #3 — it has no other natural home.

---

## LOG #3 — Subagents: Complete Reference

Sources: https://code.claude.com/docs/en/sub-agents.md

### A. Agent file frontmatter — every field (14 total)

```yaml
---
# Required
name: code-reviewer                     # lowercase + hyphens; uniqueness key
description: Reviews code for...        # Claude reads this to decide when to delegate

# Optional — tooling
tools: Read, Glob, Grep                 # allowlist (omit = inherit all from parent)
disallowedTools: Write, Edit            # denylist (applied first, then `tools`)
skills:                                  # preload skill content into context
  - api-conventions

# Optional — model & effort
model: sonnet                           # sonnet|opus|haiku|<full-id>|inherit (default inherit)
effort: high                            # low|medium|high|xhigh|max (depends on model)

# Optional — permissions & isolation
permissionMode: acceptEdits             # default|acceptEdits|auto|dontAsk|bypassPermissions|plan
isolation: worktree                     # spawn into a temp git worktree
maxTurns: 20                            # hard ceiling on agentic loops

# Optional — composition
mcpServers:                             # scope MCP servers to this agent only
  - playwright:                         # inline definition
      type: stdio
      command: npx
      args: ["-y", "@playwright/mcp@latest"]
  - github                              # name-reference shares parent connection

hooks:                                  # lifecycle hooks scoped to this agent
  PreToolUse:
    - matcher: "Bash"
      hooks: [{ type: command, command: "./validate.sh" }]

memory: project                         # user|project|local — persistent learning dir

# Optional — UX
color: cyan                             # red|blue|green|yellow|purple|orange|pink|cyan
background: true                        # always spawn as background (default false)
initialPrompt: "Start by..."            # auto-submitted when run as --agent main session
---

System prompt body goes here. The body becomes the subagent's full system prompt
(plus environment details Claude appends).
```

### B. Discovery / scope precedence (highest wins)

```
Priority   Location                              Use for
1          Managed settings .claude/agents/      org-wide enforced agents
2          --agents CLI flag (JSON)              ephemeral testing
3          <project>/.claude/agents/             team-shared, version-controlled
4          ~/.claude/agents/                     personal cross-project
5          plugin's agents/ directory            distributed via plugin
```

**Discovery rules:**
- Both `.claude/agents/` and `~/.claude/agents/` are scanned **recursively** → use subfolders for organization
- Subfolder paths **do not** affect agent identity — only the `name:` frontmatter does
- Within one scope, duplicate `name:` → one wins silently (no warning)
- Plugin agents scoped: `agents/review/security.md` in plugin `my-plugin` → `my-plugin:review:security`
- Project agents discovered by walking up from cwd; `--add-dir` directories are NOT scanned for agents (only for file access)

**Reload semantics:** Agent files loaded at session start. Edit on disk → restart session. Edits via `/agents` UI → effective immediately.

### C. Agent tool — the invocation API

```
Agent({
  description: string,           // 3-5 word task description
  prompt: string,                 // task brief (self-contained — agent has no prior context)
  subagent_type?: string,         // which agent to use (defaults to general-purpose)
  model?: "sonnet"|"opus"|"haiku", // per-invocation override
  isolation?: "worktree",         // override frontmatter
  run_in_background?: boolean     // run concurrently
})
```

**Model resolution order** (highest authority first):
1. `CLAUDE_CODE_SUBAGENT_MODEL` env var
2. Per-invocation `model` parameter on the Agent call
3. Agent definition's `model:` frontmatter
4. Main conversation's model

### D. What loads in a subagent at startup (NOT the parent's context)

```
Always loaded:
  System prompt              (the agent's own markdown body + env details)
  Task message               (the prompt Claude writes when handing off)

Loaded for custom + general-purpose agents:
  CLAUDE.md hierarchy        (~/.claude/CLAUDE.md, project rules, CLAUDE.local.md, managed)
  Git status snapshot        (taken at parent session start)
  Preloaded skills           (full content of skills: field)

NOT loaded for Explore + Plan:
  CLAUDE.md, git status      (deliberately skipped for speed)
  Preloaded skills           (built-in agents have no skills field)

Never loaded:
  Parent conversation history (the entire point of the isolation)
  Files the parent has read
  Skills the parent has invoked
```

**Exception:** a **fork** (with `CLAUDE_CODE_FORK_SUBAGENT=1`) inherits the entire conversation, system prompt, tools, and model. Fork's tool calls stay isolated; only the result returns.

### E. Foreground vs background

| Mode | Behavior | Permission prompts |
|---|---|---|
| Foreground | Blocks main conversation until done | Surface to you |
| Background | Concurrent | Auto-denied (the call fails, agent continues) |

**How background gets chosen:**
- Frontmatter `background: true` → always background
- `run_in_background: true` on the Agent call → background for this invocation
- Claude chooses based on task type otherwise
- Press `Ctrl+B` to background a running foreground task
- `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1` disables all backgrounding

If a background agent fails on a denied permission, retry as foreground.

### F. Permission inheritance (subtle — read carefully)

Subagent's `permissionMode` is honored **unless** the parent uses one of these:

| Parent mode | Subagent override |
|---|---|
| `bypassPermissions` | ignored — bypass propagates |
| `acceptEdits` | ignored — acceptEdits propagates |
| `auto` | ignored — auto propagates; classifier evaluates subagent calls with parent's rules |
| `default`, `dontAsk`, `plan` | subagent's `permissionMode:` is honored |

**Implication for your setup:** if you launch with `--permission-mode auto`, every subagent inherits auto-classifier rules — meaning the unauthorized-commit-chezmoi rule that bit you 2026-05-17 applies to all subagents too.

### G. Memory field — persistent agent learning

```yaml
memory: project   # → .claude/agent-memory/<name>/
memory: user      # → ~/.claude/agent-memory/<name>/
memory: local     # → .claude/agent-memory-local/<name>/   (gitignored)
```

When memory is enabled:
- Agent's system prompt gets memory R/W instructions
- First 200 lines or 25KB of `MEMORY.md` in the dir auto-prepended to system prompt
- Read, Write, Edit tools auto-enabled (even if not in `tools:`)
- Agent maintains its own `MEMORY.md` curation — instruct it to read before tasks and write after

This is **separate from** the auto-memory at `~/.claude/projects/-Users-4jp/memory/` (which is per-scope, not per-agent). Agent-memory is per-agent, can span scopes.

### H. Hooks scoped to a subagent — three places

| Where | When it fires |
|---|---|
| Agent frontmatter `hooks:` | While that agent is active. `Stop` automatically rewritten to `SubagentStop`. |
| Project `settings.json` `SubagentStart` / `SubagentStop` | When any agent (matched by name) starts/stops in main session |
| Plugin agent hooks | **Ignored** — plugin subagents can't carry `hooks:`, `mcpServers:`, or `permissionMode:` (security restriction) |

### I. Invocation patterns — escalating from suggestion to default

```
Natural language       "Use the test-runner subagent to fix failing tests"
                        ↳ Claude decides whether to delegate (description-driven)

@-mention              "@\"code-reviewer (agent)\" look at the auth changes"
                        ↳ guarantees that specific agent runs once

Per-session default    claude --agent code-reviewer
                        ↳ main thread itself takes on the agent's prompt/tools/model
                        ↳ subagent's prompt replaces default Claude Code system prompt entirely
                        ↳ choice persists across resume

Project-wide default   .claude/settings.json: { "agent": "code-reviewer" }
                        ↳ every session in this project, unless --agent overrides
```

`--agent` resolution: bare name searched across all scopes; ambiguous → use scoped form `my-plugin:agent-name` or `my-plugin:subfolder:agent-name`.

### J. Disable a subagent

```json
{ "permissions": { "deny": ["Agent(Explore)", "Agent(my-custom-agent)"] } }
```

Or CLI: `claude --disallowedTools "Agent(Explore)"`

Inside a `--agent` main thread, restrict which subagents IT can spawn:

```yaml
tools: Agent(worker, researcher), Read, Bash   # only those two; everything else fails
tools: Agent, Read, Bash                       # any subagent
# Agent omitted entirely → cannot spawn any
```

Note: subagents cannot spawn subagents — `Agent(...)` in a subagent definition has no effect.

### K. Resume + transcript paths

- Each invocation = new instance, fresh context (except forks)
- To continue: ask Claude to resume that agent — it uses `SendMessage` tool with agent ID
- `SendMessage` only available when `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`
- Transcripts at `~/.claude/projects/{project}/{sessionId}/subagents/agent-{agentId}.jsonl`
- Cleaned up per `cleanupPeriodDays` setting (default 30)
- Auto-compaction at ~95% capacity; override via `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=50`

### L. What you currently use vs. unused fields

You have ~30+ agents available (built-ins + plugin-dev + feature-dev + coderabbit + pr-review-toolkit + vercel + statusline-setup + claude-code-guide + agent-sdk-dev + hookify + code-simplifier + Explore + Plan + general-purpose).

Frontmatter fields that would give the biggest leverage if you started using them:

| Field | Why for your workflow |
|---|---|
| `memory: project` | Your reviewer/auditor agents accumulate codebase insights. Right now every invocation starts fresh — a 100-codebase reviewer with memory becomes meaningfully better over time. |
| `mcpServers:` (scoped) | You have 30+ MCP servers loaded globally. Scoping Neon/Notion/Figma/Sentry to specific agents removes ~thousands of tokens of tool-description tax from your main context. |
| `skills:` (preload) | You have 162 skills. Preloading `voice-enforcement` into a writing agent or `security-essentials-pack` into a reviewer eliminates the discover-and-load round-trip. |
| `isolation: worktree` | Pairs with your IRF-OPS workflow — risky refactors get their own worktree, don't touch your main checkout. |
| `effort: low` on Explore-class agents | Save tokens on fast lookups while keeping `xhigh` for synthesis. |
| `initialPrompt:` | For `claude --agent <reviewer>` workflows you'd run frequently, eliminate the "what do you want me to do?" first turn. |
| `color:` | UI cue when many agents fan out — pairs with your "fan out agents" pattern. |
| `background: true` | For any agent that produces verbose output you don't want to watch synchronously (test-runner, log-scanner). |

### M. Picking foreground vs background vs main-conversation

| Use main conversation when | Use foreground subagent when | Use background subagent when |
|---|---|---|
| iterative refinement needed | task produces verbose output you don't want in context | task is independent & not gating next steps |
| multi-phase, shared context | want tool restrictions enforced | want concurrent execution |
| quick targeted change | self-contained, returns summary | named, retryable |
| latency matters | one-shot | observability via transcript |

For a quick question about something already in context, use `/btw` instead — it sees your full context, has no tools, answer is discarded.

### N. Forks — when neither subagent nor main fits

Fork mode (`CLAUDE_CODE_FORK_SUBAGENT=1`, requires CC ≥ 2.1.117):
- Inherits ENTIRE conversation including system prompt, tools, model, message history
- Replaces general-purpose subagent (named subagents still spawn fresh)
- Every spawn becomes background (use `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1` to invert)
- `/fork <directive>` spawns one explicitly; fork's name auto-derived from directive
- Cannot spawn nested forks

When to fork rather than subagent: you need to try multiple approaches from the *current* state in parallel, or the agent would need too much background to be useful.

### O. Plugin agent restrictions (security)

When an agent comes from a plugin, three frontmatter fields are **silently ignored**:
- `hooks:`
- `mcpServers:`
- `permissionMode:`

Workaround: copy the agent file into `.claude/agents/` or `~/.claude/agents/`. Or add `permissions.allow` rules in settings (but those apply session-wide, not just to that agent).

### P. Troubleshooting cheatsheet

| Symptom | Likely cause |
|---|---|
| Agent doesn't appear in `@`-typeahead | file in wrong dir · missing required frontmatter (`name`, `description`) · duplicate name in same scope (silent drop) · added since last session start (needs restart) |
| Agent ignores `permissionMode` | parent in `auto`/`acceptEdits`/`bypassPermissions` mode · agent loaded from plugin (field stripped) |
| Agent has no MCP tools | `mcpServers:` references unconfigured name · `tools:` allowlist doesn't include MCP tools |
| Agent's memory not persisting | `memory:` field missing · checked into git but agent-memory-local was meant · MEMORY.md exceeded 200 lines / 25 KB (curate it) |
| Background agent fails silently | permission prompt auto-denied · retry as foreground to see what triggered |
| Agent runs but with wrong model | check resolution order (env var > per-invocation > frontmatter > parent) |
| Forks not spawning | `CLAUDE_CODE_FORK_SUBAGENT=1` not set · CC version below 2.1.117 · named subagent invoked (forks replace general-purpose only) |

---

`★ Insight ─────────────────────────────────────`
**Three engine outputs now form a stack** — statusLine (read-only UX surface), hooks (event-driven enforcement surface), subagents (context-isolation surface). They compose: a SubagentStart hook can change the statusLine (write to a cache file the statusLine reads); a subagent's frontmatter hooks fire during its lifecycle and can themselves modify session state.

**Where your existing setup is conspicuously asymmetric:** 34 hooks but ~all of them on the parent-session lifecycle (PreToolUse, SessionStart, etc.). Zero hooks on subagent lifecycle (SubagentStart/SubagentStop) despite explicitly dispatching to subagents via your Dispatch Protocol. That's an observability gap — fleet activity goes unrecorded by your enforcement layer.

**Single highest-leverage move from these two logs:** add `memory: project` to one frequently-used reviewer agent and let it accumulate codebase patterns. The cost is one frontmatter field; the payoff compounds across every future invocation.
`─────────────────────────────────────────────────`
