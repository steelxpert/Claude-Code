# SpaceClaim 2020 R1 agent harness

Closed-loop "Claude designs → SpaceClaim builds → math verifies"
pipeline for Ansys Discovery SpaceClaim **2020 R1 (v201, API V18)**,
driven headless via `/RunScript`. No PyAnsys (needs ≥24 R1 backends);
this uses only what a 2020 R1 perpetual license ships.

```
Claude / MCP client
      │  build_gear(m, z, ...)
      ▼
mcp_server.py ──► harness/runner.py ──► SpaceClaim.exe /RunScript=
      │                 │                 sc_scripts/spur_gear.py
      │                 │  SC_JOB_DIR       (IronPython, API V18)
      │                 ▼                        │
      │           jobs/<job>/params.json ◄───────┘ writes result.json,
      │                 │                          gear.stp, gear.png
      ▼                 ▼
harness/verify.py ◄── result.json      analytic truth: harness/gear_math.py
```

## Quickstart (any OS — mock backend, no license)

```bash
python3 harness/loop.py --mock --module 2 --teeth 24 --face-width 12
python3 harness/loop.py --mock --defect missing_tooth --module 2 --teeth 24   # exit 1
```

## Quickstart (Windows box with SpaceClaim v201)

1. `copy config.example.json config.json` and fix the exe path if needed.
2. First run only: repair the `VERIFY`-tagged API calls in
   `sc_scripts/spur_gear.py` against a recorded macro — procedure in
   `.claude/skills/spaceclaim-scripting/SKILL.md`.
3. `python harness/loop.py --real --config config.json --module 2 --teeth 24`

## MCP server

```bash
pip install "mcp[cli]"
python mcp_server.py
```

Registered for Claude Code by the repo's `.mcp.json`. Tools:
`env_check`, `build_gear` (build + measure + verify in one licensed
launch), `run_sc_script` (arbitrary script under the job contract).
If Claude Code runs on a different machine than SpaceClaim, run this
server on the Windows box and connect over an HTTP/SSE transport.

## The loop

Each iteration is one licensed launch (startup dominates, so build +
measure + export are batched). `loop.py` prints a JSON report; a failing
check names the defect (wrong tooth count, open profile, volume out of
the root/tip envelope...). The outer agent fixes the script or params
and reruns; non-obvious fixes get appended to the skill's gotcha list —
that is the "learning" mechanism, durable across sessions.

## Status

- Verified here (Linux, mock): gear math, verifier, defect detection,
  loop driver, all CPython syntax.
- Template, needs first-run repair on the Windows box: the
  `VERIFY`-tagged SpaceClaim API calls in `sc_scripts/spur_gear.py`.
