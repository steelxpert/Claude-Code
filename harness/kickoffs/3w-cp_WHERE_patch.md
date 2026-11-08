# Proposed patch to the 3w-cp skill — the "Where" W names the venue (owner request, FLIN-002, 2026-11-08)

Apply in SKILL.md, section "The four W's", block **3. Where.** Replace the first paragraph
("Where the next work should happen — always an explicit **cloud or local** recommendation
with one sentence of reasoning per task …") with:

> **3. Where.** Where the next work should happen: always one explicit line per task (or
> one for a uniform batch) in the form `Where: <venue> on <machine>`, followed by one
> sentence of reasoning. Venue is one of:
> - **Claude Code cloud** — repo work, Drive via connector, no PC files; machine = `cloud`.
> - **Claude Code local** — repo work that needs PC files or tools; machine = hostname.
> - **Cowork desktop + device bridge** — PC folders, PrePoMax / AIM / SpaceClaim, Drive
>   folders staged through the bridge; machine = hostname.
> - **Claude Project chat** — reading and client-facing drafting only; a kickoff is never
>   run inside a Project (owner rule ORG-003b).
>
> The cp block repeats the same `Where:` line verbatim, so the owner opens the right product
> on the right PC before pasting. The existing cloud-vs-local criteria below decide between
> the first three venues.

Keep the three criteria bullets (Cloud / Local / mixed) unchanged below the new paragraph.
In the cp section, change the bullet "**Where + Which lines**" to read: "repeat the
`Where: <venue> on <machine>` line and the model recommendation from the W's so the prompt
is self-contained."

Rationale: the four venues differ in what a session can reach (Drive connector, PC
folders, GUI tools, memory store) and in whether a kickoff may run there at all; "cloud or
local" alone did not say which product to open. Harvest target: org thread (ORG-005).
