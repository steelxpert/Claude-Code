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
6. [MEASURED] Drive upload from the cloud without pasting content: `create_file` accepts
   `base64Content = sha256:<hex>:<absolute path>` as a file reference; the four ledger files
   landed with byte-exact sizes (SESSIONS.csv 34699, STATE_INDEX.md 12519). Old copies were
   trashed only after the new sizes matched. New ids: SESSIONS.csv 1kO-37hpJYTOPHHOlqK7qB2Z_TWI1EW7t,
   STATE_INDEX.md 1N41x0jUPXMI5bo-z81iQZ2XBwBa0TLhS, folder flins 1rYjuocNUuLtwQfnTEtxxV59fLBMU_Fa-.
7. [MEASURED] A shallow clone fetched by `FETCH_HEAD` has no remote-tracking ref, so the stop
   hook reports "no remote branch" although the push succeeded. Fix: set
   `remote.origin.fetch` to `+refs/heads/*:refs/remotes/origin/*`, fetch the branch, `git branch -u`.
