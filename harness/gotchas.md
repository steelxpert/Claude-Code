# FLINS gotchas — append-only, one dated section per session

Tags: [MEASURED] seen and reproduced in the session · [DOC] from documentation ·
[INFERENCE] deduced, not reproduced. Never edit an old section; add a pointer line.

## — 2026-11-08 (FLIN-002)

1. [MEASURED] A fresh cloud container has no `pytest`; `pip install pytest` then
   `python -m pytest` = 12 passed in 1.4 s. The package itself installs with `pip install -e .`.
2. [MEASURED] The cloud session's worker process restarted twice mid-session; the clone at
   `/home/user/claude-code` and the checked-out branch survived both restarts, the shell
   state (cwd, variables) did not. Re-run `git status` after a restart before trusting
   anything.
3. [MEASURED] The Google Drive connector in the cloud has no "update file content" call
   (only metadata update, create, trash). Writing the ledger from a cloud session therefore
   means: download, edit locally, create the new file in the ledger folder, verify size and
   line count, trash the old one. The file id changes; the owner's offline folder keeps
   working because offline availability is per folder.
4. [MEASURED] Drive holds three copies of the FLiBess harness (`Nonlinear Mechanical`
   twice plus a dated `2026.06.15` folder); the sizes are identical. Read the one under the
   folder created 2026-10-26 and treat the others as frozen backups.
5. [DOC] The client deck (artifact AJLrG5BTfyRMYuw5RyQYs8) numbers the test, demo and
   next-steps slides 15, 16, 17 in its footer; the deck file ids are `vizsgalatok`, `demo`,
   `kovetkezo`. Slide 17 carries the six client decisions used in the Tuesday agenda.
