# Agent Channel — pointer

The Claude ↔ Codex agent communication channel for this paper lives
in a dedicated repository at the user's home, not in this project
repo. This file points to it.

## Channel location

```
C:\Users\rohit\agent-channel\
└── papers\csur-pe-eval-2026\
    ├── channel.md           ← the conversation log (append-only)
    ├── claude_status.md     ← Claude's status
    ├── codex_status.md      ← Codex's status
    └── PROJECT_CONTEXT.md   ← project facts, paths, latest commit
```

Shared infrastructure at the channel-repo root:

- `C:\Users\rohit\agent-channel\README.md`
- `C:\Users\rohit\agent-channel\CHANNEL_PROTOCOL.md`
- `C:\Users\rohit\agent-channel\HOW_CODEX_CONNECTS.md`
- `C:\Users\rohit\agent-channel\HOW_CLAUDE_CONNECTS.md`

## Why a separate repo

- Reusable across all future papers (each paper gets a subdirectory
  under `papers/`).
- Lives inside both agents' default writable roots — Codex flagged
  in msg-002 that the original location (inside this project repo)
  was outside its writable sandbox.
- Protocol evolves independently of any one paper's git history.
- This project repo stays clean.

## How the human invokes either side

**To send work to Claude:**
> Read `C:\Users\rohit\agent-channel\papers\csur-pe-eval-2026\channel.md`
> and respond to any messages addressed to me (msg-NNN onward).

**To send work to Codex (first time):**
Paste:
> Read `C:\Users\rohit\agent-channel\HOW_CODEX_CONNECTS.md` and
> `C:\Users\rohit\agent-channel\papers\csur-pe-eval-2026\channel.md`.
> Onboard and reply.

**To send work to Codex (subsequent invocations):**
> Read `C:\Users\rohit\agent-channel\papers\csur-pe-eval-2026\channel.md`
> and respond to any messages addressed to me (msg-NNN onward).

## Channel lifecycle (active vs paused vs closed)

The channel has a state file: `papers/csur-pe-eval-2026/CHANNEL_STATE.md`.
Three states:

- **active** — a thread is open; the agent named in
  `claude_status.md` or `codex_status.md` owes the next reply.
- **paused** — no open thread; both sides have posted `RESOLVED.`
  and there is no pending work. The channel files stay in place;
  either agent can re-activate.
- **closed** — project shipped; the subdirectory will be moved to
  `_archive/`.

### Default behaviour (you do not need to manage state manually)

- After every `RESOLVED.` exchange, the agent that posted the
  resolution auto-flips state to `paused`.
- When you give Claude a routine project task (edit, compile,
  commit), Claude does NOT touch the channel.
- When you give Claude a task that explicitly involves Codex
  ("send to Codex", "ask Codex", "get Codex's review"), Claude
  auto-activates and posts. No need to ask permission.
- When you give Claude an ambiguous task ("review this", "audit
  this", "second opinion") and the channel is paused, Claude will
  ask: *"The Codex channel is currently paused. Activate and bring
  Codex in, or handle solo?"*

### Manually overriding state

You can edit `CHANNEL_STATE.md` directly at any time:

```
state: paused    ← change this line
```

Both agents respect the file as authoritative on next read.

### Current state of this paper's channel

Check `C:\Users\rohit\agent-channel\papers\csur-pe-eval-2026\CHANNEL_STATE.md`.
At the time this pointer was last updated: **active** (msg-003
awaiting Codex acknowledgement of the migration).

## Historical pointer

The pre-migration channel directory at
`<this-repo>/agent_channel/` is preserved as a stale stub with a
`README_REDIRECT.md` pointing at the new location. msg-001 and msg-002
were originally posted there and have been migrated verbatim to the
new location. Don't write to the old directory.
