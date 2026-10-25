#!/usr/bin/env python3
"""Self-test for leak_check.py (temp dir, no network). Prints PASS/FAIL per check; exit 1 on any FAIL."""
import os, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); TOOL = os.path.join(HERE, "leak_check.py")
fails = 0
def run(*a):
    r = subprocess.run([sys.executable, "-I", TOOL, *a], capture_output=True, text=True); return r.returncode, r.stdout
def check(name, cond):
    global fails
    print(("PASS " if cond else "FAIL ") + name); fails += (not cond)
with tempfile.TemporaryDirectory() as d:
    sec = os.path.join(d, "s.env"); open(sec, "w").write("KEY=Zq8vLmN2xRt5\n")
    t = os.path.join(d, "t"); os.makedirs(t)
    open(os.path.join(t, "a.txt"), "w").write("nothing here\n")
    rc, out = run("--secrets", sec, "--targets", t)
    check("clean tree -> 0 CLEAN", rc == 0 and "RESULT: CLEAN" in out)
    open(os.path.join(t, "b.txt"), "w").write("x = Zq8vLmN2xRt5\n")
    rc, out = run("--secrets", sec, "--targets", t)
    check("match -> 1 LEAK, path:line only", rc == 1 and "MATCH" in out and "Zq8vLmN2xRt5" not in out)
    os.remove(os.path.join(t, "b.txt"))
    empty = os.path.join(d, "e.env"); open(empty, "w").write("")
    rc, out = run("--secrets", empty, "--targets", t)
    check("no secrets loaded -> 2 (fail closed)", rc == 2 and "CLEAN" not in out)
    json_sec = os.path.join(d, "j.json"); open(json_sec, "w").write('{"k": "Zq8vLmN2xRt5"}\n')
    rc, out = run("--secrets", json_sec, "--targets", t)
    check("unsupported secrets format -> 2", rc == 2)
    os.symlink(os.path.join(t, "a.txt"), os.path.join(t, "ln.txt"))
    rc, out = run("--secrets", sec, "--targets", t)
    check("skipped symlink -> 3 INCOMPLETE", rc == 3 and "INCOMPLETE" in out and "CLEAN" not in out)
    os.remove(os.path.join(t, "ln.txt"))
    open(os.path.join(t, "big.bin"), "wb").write(b"a" * (2 * 1024 * 1024 + 10))
    rc, out = run("--secrets", sec, "--targets", t)
    check("skipped large file -> 3", rc == 3 and "large=1" in out)
    rc, out = run()
    check("usage -> 2", rc == 2)
print("FAILS:", fails); sys.exit(1 if fails else 0)
