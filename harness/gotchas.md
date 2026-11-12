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
8. [MEASURED, FLIN-003] A cloud session whose repo is not in its sources can clone and read
   through the git proxy but every push returns 403. Attach the repo with push access at
   Step 0 (`add_repo`, access push) before any work; a later attach works but costs a turn.
9. [MEASURED, FLIN-003] The Drive connector creates and trashes files but cannot change the
   content of an existing file. Ledger rows from a cloud session go into a
   `PENDING_ROW_<id>.txt` in the ledger root for the next PC session to append.
10. [MEASURED, FLIN-003] Opening `SESSIONS.csv` in Excel (Hungarian locale) and saving wraps
   every row in quotes and pads `;;;`. Repair = Drive web > Manage versions > delete the
   damaged current version (Download of an older version can be greyed out). Text editor only.
11. [MEASURED, FLIN-003] The container cannot fetch three.js from cdnjs / jsDelivr (proxy 403).
   Test artifact pages with `npm i three@0.128.0` in the scratchpad and Playwright
   `page.route` fulfilling the two script URLs from `node_modules`; wrap the file in a
   doctype / body shell for the test only.
12. [PROCESS, FLIN-003] The owner steers the design himself: one item at a time, pictures
   over text, assembly + exploded view for every sketch, draft before publishing. Running
   ahead with own details (first roof draft, rafter proposal) cost rework.
13. [PROCESS, FLIN-003] Sub-agent hand-backs list what they did NOT look at; open the key
   screenshot yourself before showing it. A geometry brief with coordinates gets a right
   first draft; a vague one does not.


## — 2026-11-12 (FLIN-004)

14. [MEASURED, FLIN-004] Artifact-tool publish to a URL this session has not read: refused
   with a line diff of the live page (the diff counts as the read); the identical retry is
   refused once more ("resent unchanged"); the third identical call goes through. Budget
   three calls, or read the page first (the read costs the whole 90 KB file).
15. [MEASURED, FLIN-004] Sonnet screenshot briefs with named camera positions missed the
   target twice in the whole-house scene (a frame rafter in the way, the detail too small).
   A numeric check settles it in one run: page.evaluate over window.__members with
   THREE.Box3().expandByObject(mesh) gives world extents per member name (nesting order,
   clearance to a track web). The exploded view cannot show the real order, because the
   explode offsets set it.
16. [MEASURED, FLIN-004] The harness gave the session a branch created from main, without
   harness/ and docs/pilot_house. `git checkout -B <session branch> origin/<previous FLIN
   branch>` and push fixed it in one step. The kickoff must name the branch to base on.
17. [MEASURED, FLIN-004] pytest and ezdxf are not in the fresh container: `pip install -e
   ".[dev]"` first (about 30 s), then 12 passed.
18. [PROCESS, FLIN-004] Owner loop refined: "show screenshot" at the comment stage means a
   draft rendering before approval; commit the draft to the branch ("draft, owner check
   pending") when the stop hook asks; republish the artifact only after the yes. A brief
   that gives per-member offsets (stack of three nested sections) got a right first draft;
   the only rework was the owner's own refinement (members run individually to the track).
19. [PROCESS, FLIN-004] Terminology: the line where two wall panels meet is a horizontal
   "panel joint" (track-to-track connection), not a "splice" (EN 1993-1-8 6.2.7 keeps that
   word for one member). Tier: Fable is not needed for this item-by-item work (D-019).
