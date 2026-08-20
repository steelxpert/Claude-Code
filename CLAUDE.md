# CLAUDE.md

## Token economy — work frugally

Keep token consumption to the minimum the task actually requires:

- **Read only what is needed.** Open only files directly relevant to the task, and read targeted sections (offset/limit, Grep) rather than whole files. Do not explore the repo "just in case".
- **No subagents or workflows for simple tasks.** A straightforward edit or question needs no parallel research agents, no multi-agent orchestration.
- **No redundant verification.** Do not re-read files after editing them; do not re-run tests or builds that already passed unless the code changed.
- **Concise output.** Short status notes while working, one compact summary at the end. No long narration, no restating file contents back to the user.
- **Prefer the cheapest sufficient approach.** One targeted Grep beats a broad scan; one validated change beats several speculative ones.


## GitHub Actions rules

Learned the hard way on 2026-08-19: a hung `apt-get` ran for 6 hours — the default
job limit — on four separate runs and consumed the entire month's Actions allowance
in one afternoon.

- Every job MUST set `timeout-minutes`. Never rely on the 6-hour default.
- Every workflow MUST have a `concurrency` block with `cancel-in-progress: true`.
- Every `apt-get` call MUST be wrapped in `timeout` and use `-o Acquire::Retries=3`.
- Cache dependencies: `cache: pip` on `setup-python`, `actions/cache` for ccache.
