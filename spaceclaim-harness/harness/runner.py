"""Launch headless Ansys SpaceClaim 2020 R1 (v201) and run one job.

Windows only. Contract with the in-app IronPython script:
  - runner writes  <job_dir>/params.json
  - runner sets    SC_JOB_DIR=<job_dir> in the child environment
  - script writes  <job_dir>/result.json (+ gear.stp, gear.png, log.txt)

Arguments are passed via the environment variable, NOT /ScriptArgs,
because SC_JOB_DIR works identically across SpaceClaim versions.
Each launch checks out the license seat and costs 20-60 s: batch all
work for one iteration into one script run.
"""
import json
import os
import subprocess
import time


DEFAULT_EXE = r"C:\Program Files\ANSYS Inc\v201\scdm\SpaceClaim.exe"


def load_config(path):
    with open(path) as fh:
        return json.load(fh)


def run(script_path, params, job_dir, exe=DEFAULT_EXE, timeout_s=600):
    os.makedirs(job_dir, exist_ok=True)
    with open(os.path.join(job_dir, "params.json"), "w") as fh:
        json.dump(params, fh, indent=2)

    cmd = [
        exe,
        "/RunScript=%s" % os.path.abspath(script_path),
        "/Headless=True",
        "/Splash=False",
        "/Welcome=False",
        "/ExitAfterScript=True",
    ]
    env = dict(os.environ, SC_JOB_DIR=os.path.abspath(job_dir))

    t0 = time.time()
    proc = subprocess.run(cmd, env=env, capture_output=True, text=True,
                          timeout=timeout_s)
    elapsed = time.time() - t0

    result_path = os.path.join(job_dir, "result.json")
    if os.path.exists(result_path):
        with open(result_path) as fh:
            result = json.load(fh)
    else:
        result = {
            "status": "error",
            "error": "SpaceClaim exited (rc=%d, %.0fs) without writing "
                     "result.json" % (proc.returncode, elapsed),
            "stdout": proc.stdout[-2000:],
            "stderr": proc.stderr[-2000:],
        }
    result.setdefault("backend", "spaceclaim-v201")
    result["elapsed_s"] = round(elapsed, 1)
    return result
