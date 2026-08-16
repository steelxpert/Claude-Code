# CLAUDE.md

## Token economy — work frugally

Keep token consumption to the minimum the task actually requires:

- **Read only what is needed.** Open only files directly relevant to the task, and read targeted sections (offset/limit, Grep) rather than whole files. Do not explore the repo "just in case".
- **No subagents or workflows for simple tasks.** A straightforward edit or question needs no parallel research agents, no multi-agent orchestration.
- **No redundant verification.** Do not re-read files after editing them; do not re-run tests or builds that already passed unless the code changed.
- **Concise output.** Short status notes while working, one compact summary at the end. No long narration, no restating file contents back to the user.
- **Prefer the cheapest sufficient approach.** One targeted Grep beats a broad scan; one validated change beats several speculative ones.
