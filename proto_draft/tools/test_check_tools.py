#!/usr/bin/env python3
"""Self-test for check_tools.py using a temp dummy project."""
import os, subprocess, sys, tempfile
here = os.path.dirname(os.path.abspath(__file__))
def run(reg):
    return subprocess.run([sys.executable, f"{here}/check_tools.py", reg], capture_output=True, text=True)
with tempfile.TemporaryDirectory() as t:
    os.makedirs(f"{t}/tools"); open(f"{t}/tools/a.sh", "w").write("x"); open(f"{t}/tools/b.py", "w").write("x")
    row = "| tool-{n} | project | `tools/{f}` | x | x | x | R0 | warn | כן | פעיל |\n"
    open(f"{t}/tools.md", "w", encoding="utf-8").write(row.format(n=1, f="a.sh") + row.format(n=2, f="b.py"))
    clean = run(f"{t}/tools.md")
    open(f"{t}/tools.md", "w", encoding="utf-8").write(row.format(n=1, f="a.sh") + row.format(n=1, f="ghost.sh"))
    bad = run(f"{t}/tools.md")
checks = {"clean registry -> 0": clean.returncode == 0 and "OK" in clean.stdout,
          "unregistered file warned": "not registered" in bad.stdout and "b.py" in bad.stdout,
          "missing path warned": "missing" in bad.stdout and "ghost.sh" in bad.stdout,
          "duplicate id warned": "duplicate id" in bad.stdout, "warnings exit 1": bad.returncode == 1}
for k, v in checks.items(): print(("PASS " if v else "FAIL ") + k)
sys.exit(0 if all(checks.values()) else 1)
