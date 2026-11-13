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

## — 2026-11-12 (FLIN-005)

20. [MEASURED, FLIN-005] Gotcha 14 held again: first Artifact publish of the session refused with
   the diff, the identical retry refused ("resent unchanged"), the third call went through; every
   later publish in the session went straight. Small changes go best as `edits` on the publish call.
21. [MEASURED, FLIN-005] Plan / vertical cuts of the whole house settle nesting order where
   oblique views fail: append a wrapper to the served three.min.js that stores the renderer in
   window.__R, then set window.__R.clippingPlanes = [new THREE.Plane(normal, c)] and look straight
   down (fov 1.4-2.2 from 20 m = near-orthographic). Close obliques at a frame grid are blocked by
   the frame columns; cut instead.
22. [PROCESS, FLIN-005] Regression proof for viewer edits: dump Box3 of every member before the
   edit (dumpall.js -> base.json) and compare after (cmp.js); 1000 members, only the intended ones
   may change. It caught nothing wrong this session but made the frame rebuild safe to publish
   without screenshots.
23. [PROCESS, FLIN-005] The stop hook asks to commit while a sub-agent is still editing the file:
   do not commit a half-edited file; answer "agent still running" and commit after verification.
   When the owner writes "wait", TaskStop the agent and `git checkout --` the file at once.
24. [MEASURED, FLIN-005] OrbitControls r128 has no zoom-to-cursor: disable enableZoom and handle
   the wheel yourself - raycast the cursor (fallback: plane through the target), then scale camera
   and target about that point by 1.0015^deltaY; the point under the cursor stays within 0.3 px.
25. [PROCESS, FLIN-005] Owner's framing grammar, now consistent across the house: posts for
   hold-downs = cap track + stud A + stud B open to the braced field; long-wall X-strap ends =
   wind post (end stud, gap, two C back to back on the gable inner face plane) or a doubled end
   stud; tops of openings / gables = boxed girt with king + jack posts. Apply the same rule to
   every analogous place without being asked to list them one by one, but show it as a draft.

## — 2026-11-12 (FLIN-006)

26. [MEASURED, FLIN-006] Owner sketch rules in practice: render with a separate THREE.OrthographicCamera
   substituted inside the wrapped renderer.render (window.__ORTHO), and outline with LineSegments2 /
   LineMaterial (examples/js/lines, linewidth 3 at deviceScaleFactor 2) - WebGL ignores linewidth
   on plain LineSegments. Sections = two clipping planes (a slab) seen in iso. In the house view the
   Playwright locator screenshot can time out; stop requestAnimationFrame and grab the canvas with
   toDataURL instead (scratchpad shot3.js pattern).
27. [MEASURED, FLIN-006] Gotcha 14/20 again: first publish refused with the diff, identical retry
   refused, the third call published v32.
28. [PROCESS, FLIN-006] Commit drafts between sub-agent runs and dump a fresh Box3 baseline after
   each owner-approved change; cmp.js compares label+box multisets, so SEQ renumbering after a
   removal shows up as paired remove/add lines with identical boxes - read them as renames.


## — 2026-11-13 (FLIN-008)

29. [MEASURED, FLIN-008] Cloud network policy: cdnjs, jsdelivr, unpkg, scribd, pdfcoffee, help.scia.net,
   eurocodes.jrc.ec.europa.eu all refused (403 / ENOTFOUND); registry.npmjs.org and PyPI work. For a
   self-contained viewer take the libraries from `npm pack three@0.128.0` (`docs/pilot_house/make_standalone.py`).
   External worked examples (Access Steel SX022a/SX023a) must be fetched by the owner locally.
30. [MEASURED, FLIN-008] pycufsm 0.1.x compiled solver breaks under numpy 2 (`int()` of a 1-element array);
   `assessment_member_checks/_cufsm_shim.py` loads the pure-Python solver with the one-line patch. `prop2_new`
   (CUTWP) has the same bug; section properties come from the prototype's Annex C routine instead.
31. [MEASURED, FLIN-008] EN 1993-1-3 Annex C sectorial formulas with the pole at the origin give the shear centre
   relative to the POLE, not to the gravity centre; and notional widths bp measured to the corner midpoints
   (Fig. 5.1) require the corner arcs to be added back into Aeff / Ieff (7.7 % of Aeff on a C150x1.5). Both
   were caught only by the independent FE section model (sectionproperties) in the QA loop.
32. [PROCESS, FLIN-008] Narrow-flange short-lip C sections (C150x45x10, C200x60x15) show NO distinct distortional
   minimum in the CUFSM signature curve in compression; 5.5.3.2 still gives chi_d = 0.60-0.75. Using 5.5.3.1(8)
   numerical sigma_cr,s needs cFSM modal decomposition. The FLINS lip is at c/b = 0.22 against the 0.2 limit of
   5.2(2) - confirm the real lip length.
33. [PROCESS, FLIN-008] docx-js: `language: {value:'hu-HU', eastAsia:'hu-HU', bidirectional:'hu-HU'}` on the
   default run and on every TextRun gives clean hu-HU tags; `creator` / `lastModifiedBy` set core.xml. Casual
   one-page offer letter = structural-proposal-letter template with price/deadline sections in place of the
   data checklist (owner override of the no-price default).
