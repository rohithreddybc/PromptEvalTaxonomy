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

## Historical pointer

The pre-migration channel directory at
`<this-repo>/agent_channel/` is preserved as a stale stub with a
`README_REDIRECT.md` pointing at the new location. msg-001 and msg-002
were originally posted there and have been migrated verbatim to the
new location. Don't write to the old directory.
