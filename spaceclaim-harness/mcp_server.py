"""MCP server exposing the SpaceClaim 2020 R1 gear harness to any MCP
client (Claude Code, Claude Desktop, ...).

Run on the Windows box that has SpaceClaim v201 installed:
    pip install "mcp[cli]"
    python mcp_server.py            # stdio transport

On machines without SpaceClaim the server still starts; build_gear falls
back to the mock backend unless mock=False is forced.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "harness"))

import gear_math
import verify as verify_mod
import mock_backend

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("spaceclaim")


def _config():
    path = os.path.join(HERE, "config.json")
    if os.path.exists(path):
        with open(path) as fh:
            return json.load(fh)
    return {}


def _spaceclaim_available():
    import runner
    exe = _config().get("spaceclaim_exe", runner.DEFAULT_EXE)
    return os.path.exists(exe), exe


@mcp.tool()
def env_check() -> dict:
    """Report whether a real SpaceClaim v201 backend is reachable."""
    ok, exe = _spaceclaim_available()
    return {"spaceclaim_exe": exe, "available": ok,
            "platform": sys.platform,
            "mode": "real" if ok else "mock-only"}


@mcp.tool()
def build_gear(module: float, teeth: int, pressure_angle_deg: float = 20.0,
               face_width: float = 10.0, bore_d: float = 0.0,
               mock: bool = None) -> dict:
    """Build a spur gear (headless SpaceClaim or mock), measure it, and
    verify against analytic gear formulas. Returns params, expected
    values, measured values, and the pass/fail verification report."""
    params = {"module": module, "teeth": teeth,
              "pressure_angle_deg": pressure_angle_deg,
              "face_width": face_width, "bore_d": bore_d}
    exp = gear_math.expectations(module, teeth, pressure_angle_deg,
                                 face_width, bore_d)
    available, exe = _spaceclaim_available()
    use_mock = mock if mock is not None else not available
    if use_mock:
        result = mock_backend.run(params)
    else:
        import runner
        cfg = _config()
        job_dir = os.path.join(HERE, "jobs",
                               "gear_m%g_z%d" % (module, teeth))
        result = runner.run(
            script_path=os.path.join(HERE, "sc_scripts", "spur_gear.py"),
            params=params, job_dir=job_dir,
            exe=cfg.get("spaceclaim_exe", exe),
            timeout_s=cfg.get("timeout_s", 600))
    report = verify_mod.verify(result, exp)
    return {"params": params, "expected": exp, "measured": result,
            "verification": report}


@mcp.tool()
def run_sc_script(script_path: str, params: dict, job_dir: str,
                  timeout_s: int = 600) -> dict:
    """Run an arbitrary IronPython script in headless SpaceClaim v201.
    The script must follow the SC_JOB_DIR/params.json -> result.json
    contract. Real backend only."""
    available, exe = _spaceclaim_available()
    if not available:
        return {"status": "error",
                "error": "SpaceClaim not found at %s" % exe}
    import runner
    return runner.run(script_path, params, job_dir,
                      exe=_config().get("spaceclaim_exe", exe),
                      timeout_s=timeout_s)


if __name__ == "__main__":
    mcp.run()
