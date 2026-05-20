# Agent-to-Agent Channel Protocol

A file-based, append-only message log shared between two CLI agents
(Claude Code and OpenAI Codex / ChatGPT) collaborating on the CSUR
PE-evaluation taxonomy paper.

## Channel files

All channel files live in this directory:
`C:\Users\rohit\Documents\Research Papers\ResearchPaper1_PE_evaluation_for_LLM\agent_channel\`

| File | Purpose | Who writes |
|---|---|---|
| `channel.md` | The conversation log — append messages here | Both agents |
| `claude_status.md` | Claude's availability + last-seen message ID | Claude only |
| `codex_status.md` | Codex's availability + last-seen message ID | Codex only |
| `CHANNEL_PROTOCOL.md` | This file — read once, then follow it | Neither (read-only spec) |
| `HOW_CODEX_CONNECTS.md` | Paste this to Codex to onboard it | Read-only onboarding doc |

## Why file-based

Neither agent runs continuously, so there's no persistent socket to
connect to. Both agents run as CLI tools invoked by the human user.
The file system is the shared substrate. The human "ferries" turns by
invoking each agent in turn (or by running them concurrently in
separate terminals).

Polling cadence: each agent reads `channel.md` on every invocation
and processes any messages newer than its `*_status.md` last-seen
marker.

## Message format

The channel is a single markdown file (`channel.md`) of concatenated
message blocks. Each message block has this structure:

```
---
id: msg-NNN
from: claude | codex
to: codex | claude | both
timestamp: YYYY-MM-DDTHH:MM:SSZ
in_reply_to: msg-NNN | null
topic: short-noun-phrase
---

[Message body in markdown. Multiple paragraphs allowed. Code blocks
allowed. Reference files by absolute path or by `repo:` prefix for
project-relative paths.]

[optional trailing horizontal rule `---` to separate visually]
```

### Field rules

- `id`: incrementing integer prefixed `msg-`. Pick the next unused ID
  by reading the file. If two agents race on the same ID, the second
  to commit should bump and rewrite.
- `from`: `claude` or `codex` (exactly these strings; lowercase).
- `to`: target recipient or `both` for broadcast.
- `timestamp`: ISO 8601 UTC.
- `in_reply_to`: ID of the message being responded to, or `null` for
  a new thread.
- `topic`: short label so the human can scan the log (e.g.
  `verb-sweep`, `silhouette-circularity`, `compile-error`).

### Body conventions

- Be terse. This is agent-to-agent, not agent-to-human.
- Cite file paths and line numbers when proposing changes.
- If you want the other agent to take action, say so explicitly:
  `ACTION REQUESTED:` followed by a bullet list.
- If you want a yes/no confirmation, end with `CONFIRM?`.
- If you're closing a thread, end with `RESOLVED.`

## Writing a message

1. Open `channel.md` and read the most recent `id` value.
2. Append a new block at end of file with the next `id`.
3. Update your `*_status.md` file with the new last-seen ID and a
   timestamp.
4. The other agent will see it on next invocation.

## Reading messages

1. Read `channel.md` (use `Read` or `Get-Content` end-of-file).
2. Read your `*_status.md` to find the last ID you processed.
3. Process all messages with `id` > last-seen and `to` ∈ {your name,
   `both`}.
4. Update your `*_status.md` with the new highest ID processed.

## Conflict handling

- File-locking is not guaranteed across CLI tools. If two agents append
  simultaneously, the later writer should detect the collision (re-read
  before commit) and renumber.
- For long messages, write to a temp file first, then `cp` (atomic on
  most filesystems) to `channel.md` only after constructing the full
  appended content.

## Lifecycle

- Channel is alive as long as either agent is being invoked.
- Either agent can close their side by appending a final message with
  `topic: channel-close` and `RESOLVED.` body, then updating their
  `*_status.md` to `status: closed`.

## Git policy

The `agent_channel/` directory should be committed to the repo so the
conversation is preserved with the work. Each agent should commit
their own messages plus any code changes they make as a result.
