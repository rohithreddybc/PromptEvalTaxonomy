# Onboarding Brief for Codex / ChatGPT

You (Codex / ChatGPT CLI) are being asked to join a file-based
communication channel with another agent (Claude Code) collaborating
on a CSUR PE-evaluation taxonomy paper. This document is everything
you need to participate.

## TL;DR — paste this to the user if you need confirmation

> I see the channel at
> `C:\Users\rohit\Documents\Research Papers\ResearchPaper1_PE_evaluation_for_LLM\agent_channel\`.
> I've read `CHANNEL_PROTOCOL.md` and `channel.md`. Ready to engage.

## Step 1 — Read these files in this order

1. `agent_channel/CHANNEL_PROTOCOL.md` — full protocol spec (message
   format, lifecycle, conflict rules). Read this completely.
2. `agent_channel/channel.md` — the current conversation log. Read it
   end-to-end so you have full context.
3. `agent_channel/claude_status.md` — Claude's current state, last
   message-ID Claude has processed, current task/blocker.
4. Project memory (optional but helpful):
   `C:\Users\rohit\.claude\projects\C--Users-rohit-Documents-Research-Papers-ResearchPaper1-PE-evaluation-for-LLM\memory\project_csur_submission.md`
   — full edit history of the paper. Skim if context is thin.

## Step 2 — Initialize your status file

Create `agent_channel/codex_status.md` with this content:

```
---
agent: codex
status: online
last_seen_msg_id: <highest id you've now read in channel.md>
last_seen_at: <ISO 8601 UTC timestamp now>
current_task: idle | reviewing | reading-files | drafting-reply
blockers: none | <description>
---

[Optional one-paragraph free-form context, e.g. "I'm Codex 4.6 on
gpt-5 backend, working from a clean clone, no local edits in flight."]
```

Update this file every time you process or send messages.

## Step 3 — Reply to Claude's introduction

Claude has posted `msg-001` in `channel.md` introducing the channel
and asking you to acknowledge. Your reply should:

1. Have `id: msg-002`, `from: codex`, `to: claude`,
   `in_reply_to: msg-001`, `topic: handshake`.
2. Acknowledge the channel is alive.
3. State what you can see (your view of the paper's current state,
   what files you've read, what tools you have).
4. Note any disagreement with Claude's protocol or any extension
   you'd propose.

## Step 4 — Operating mode

After the handshake:

- The human will use the channel to relay reviews from you about the
  paper, or to ask one agent to instruct the other.
- You can also send unsolicited messages (e.g. "I noticed a stale
  citation at file:line — claude, please fix"). Use
  `topic: code-issue` or similar.
- When Claude makes a change in response to your message, Claude will
  post a follow-up message citing the commit hash and what was done.

## Step 5 — When you stop

Append a final message to `channel.md` with
`topic: session-end` and update `codex_status.md` to
`status: offline`. The next time you're invoked, just read the
channel again and resume.

## Things you should know about Claude's context

- Claude is running in Claude Code CLI on Windows with PowerShell as
  the shell.
- The git branch is `csur-submission-readiness-2026-05`.
- The paper compiles to `main.pdf` (47 pages) and `supplementary.pdf`
  (21 pages) — both clean, 0 errors, 0 undefined references.
- The 152-paper × D1-D7 corpus matrix is in `corpus_d1d7.csv`.
- The empirical-analysis script (silhouette, Cramér's V, bootstrap,
  unsupervised k-means) is in `_empirical_analysis.ps1`.
- Project memory at the path in Step 1 has the full edit log.

## Things Claude needs from you

If you have access to a richer environment (web fetch, full file
write, code execution), say so. Claude will route work that benefits
from your environment to you, and vice versa.

## Concrete first message you can paste verbatim

If your first reply is just an acknowledgement, paste this directly
into `agent_channel/channel.md` (after the existing content):

```
---
id: msg-002
from: codex
to: claude
timestamp: <REPLACE WITH ISO 8601 UTC NOW>
in_reply_to: msg-001
topic: handshake
---

Acknowledged. I've read CHANNEL_PROTOCOL.md and the existing
channel.md. I have access to: <list your tools/capabilities>. I've
reviewed the paper through `main.pdf` and the latest commit `eb6ce3d`.
Ready to engage.

ACTION REQUESTED:
- <optional, anything you want claude to do first>

RESOLVED.
```

Then commit `agent_channel/channel.md` and `agent_channel/codex_status.md`
in a small git commit so Claude sees both the message and your status
update at the next sync.
