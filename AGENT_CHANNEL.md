# Agent Channel — pointer

Agent-to-agent communication between Claude Code and Codex lives in
the `agent_channel/` subdirectory.

| For | Read |
|---|---|
| Onboarding Codex (paste path to Codex) | `agent_channel/HOW_CODEX_CONNECTS.md` |
| Protocol spec (message format, lifecycle) | `agent_channel/CHANNEL_PROTOCOL.md` |
| Current conversation | `agent_channel/channel.md` |
| Claude's status | `agent_channel/claude_status.md` |
| Codex's status (created by Codex on join) | `agent_channel/codex_status.md` |

## How the human invokes either side

- **To send work to Claude:** open the Claude Code CLI in this repo
  and type `read agent_channel/channel.md and respond to any messages
  addressed to me (msg-NNN onward)`.
- **To send work to Codex:** open Codex / ChatGPT CLI with this repo
  mounted and paste the contents of `agent_channel/HOW_CODEX_CONNECTS.md`
  (first invocation only; subsequent invocations just need
  `read agent_channel/channel.md and respond`).

Both agents commit their own messages plus any code changes they make
as a result, so the channel and the work are in the same git history.
