#!/usr/bin/env python3
"""Self-test for run_metrics.py on a dummy log (no git, no network)."""
import os, subprocess, sys, tempfile
here = os.path.dirname(os.path.abspath(__file__))
def run(*a): return subprocess.run([sys.executable, f"{here}/run_metrics.py", *a], capture_output=True, text=True)
with tempfile.TemporaryDirectory() as t:
    log = f"{t}/run_20260101_x.log"; prog = f"{t}/run_20260101_x.md"; met = f"{t}/runs/metrics.md"
    open(log, "w").write("2026-01-01 10:00:00 UTC ACTION: a\nbackfill: ignored\n2026-01-01 10:10:00 UTC FINDING: f\n2026-01-01 10:20:00 UTC DECISION: d\n2026-01-01 12:00:00 UTC LESSON: l\n2026-01-01 12:30:00 UTC ACTION: b\n")
    open(prog, "w", encoding="utf-8").write("- **הערכה (שעות):** 1\n")
    r = run("row", log, "--progress", prog)
    chk0 = run("check", log, "--metrics", met); add = run("add", log, "--metrics", met, "--progress", prog); dup = run("add", log, "--metrics", met)
    chk1 = run("check", log, "--metrics", met); cal = run("calibrate", "--metrics", met, "--min-runs", "3")
    page = open(met, encoding="utf-8").read()
checks = {"wall 2:30": "| 2:30 |" in r.stdout, "active 0:50 (gap over 30min excluded)": "| 0:50 |" in r.stdout,
          "ratio 0.83": "| 0.83 |" in r.stdout, "counts 2/1/1/1": "| 2 | 1 | 1 | 1 |" in r.stdout,
          "check before add warns (exit 1)": chk0.returncode == 1, "add creates page": add.returncode == 0 and "metrics-runs:end" in page,
          "duplicate add refused": dup.returncode == 1, "check after add OK": chk1.returncode == 0,
          "calibrate refuses small sample": cal.returncode == 1 and "not enough data" in cal.stdout}
for k, v in checks.items(): print(("PASS " if v else "FAIL ") + k)
sys.exit(0 if all(checks.values()) else 1)
