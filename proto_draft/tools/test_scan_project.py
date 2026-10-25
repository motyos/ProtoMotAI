#!/usr/bin/env python3
"""Self-test for scan_project.py: builds a dummy tree in a temp dir, scans it, asserts that
secrets are reported by path:line:type only, deny-named files are not opened, symlinks/skip dirs are not followed."""
import os, subprocess, sys, tempfile
here = os.path.dirname(os.path.abspath(__file__))
with tempfile.TemporaryDirectory() as t:
    os.makedirs(f"{t}/app/tests"); os.makedirs(f"{t}/node_modules/x")
    open(f"{t}/app/conf.py", "w").write('password = "Abcdefgh12345"\nurl = "http://u:pw12345@host/x"\n')
    open(f"{t}/.env", "w").write("KEY=zzzzzzzzzzzzzzzz\n")
    open(f"{t}/app/tests/test_a.py", "w").write("x\n")
    open(f"{t}/node_modules/x/a.js", "w").write("password = 'Neverscanned99'\n")
    os.symlink("/etc", f"{t}/app/link")
    open(f"{t}/id_ed25519", "w").write("KEYMATERIAL1234567890\n"); open(f"{t}/main.tfstate", "w").write("STATEVALUE1234567890\n")
    os.makedirs(f"{t}/.ssh"); open(f"{t}/.ssh/cfg", "w").write("password = 'SshHidden12345'\n")
    os.mkfifo(f"{t}/pipe.md")
    out = subprocess.run([sys.executable, "-I", f"{here}/scan_project.py", t], capture_output=True, text=True, timeout=30).stdout
    out_opt = subprocess.run([sys.executable, "-I", f"{here}/scan_project.py", "--max-files", "100", t], capture_output=True, text=True, timeout=30).stdout
bad = [v for v in ("Abcdefgh12345", "pw12345", "zzzzzzzz", "Neverscanned99", "KEYMATERIAL", "STATEVALUE", "SshHidden") if v in out]
checks = {"no secret values in output": not bad, "finding reported": "app/conf.py:1:key-assignment" in out,
          ".env listed not opened": "\n- .env\n" in out and "- .env:" not in out, "symlink not followed": "app/link (symlink)" in out,
          "node_modules skipped": "node_modules/ (skipped dir)" in out,
          "id_ed25519 and tfstate denied, not opened": "- id_ed25519" in out and "- main.tfstate" in out,
          ".ssh skipped": ".ssh/ (skipped dir)" in out, "FIFO not opened (no hang)": "pipe.md (not a regular file)" in out,
          "option before dir parsed": "app/conf.py:1:key-assignment" in out_opt}
for k, v in checks.items(): print(("PASS " if v else "FAIL ") + k)
sys.exit(0 if all(checks.values()) else 1)
