#!/usr/bin/env python3
"""Self-test for check_translation.py (temp dir). Prints PASS/FAIL per check; exit 1 on any FAIL."""
import os, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); TOOL = os.path.join(HERE, "check_translation.py")
fails = 0
def run(*a):
    r = subprocess.run([sys.executable, "-I", TOOL, *a], capture_output=True, text=True); return r.returncode, r.stdout
def check(name, cond):
    global fails
    print(("PASS " if cond else "FAIL ") + name); fails += (not cond)
def w(p, t):
    os.makedirs(os.path.dirname(p), exist_ok=True); open(p, "w", encoding="utf-8").write(t)
HE = "# x\n\nעודכן: 2026-10-25\n\n## a\n\n## b\n\n```\ncode\n```\n"
EN = "# x\n\nUpdated: 2026-10-25\n\n## a\n\n## b\n\n```\ncode\n```\n"
with tempfile.TemporaryDirectory() as d:
    for n in ("README", "SECURITY", "NOTICE"): w(f"{d}/{n}.md", HE); w(f"{d}/{n}.en.md", EN)
    w(f"{d}/docs/he/faq.md", HE); w(f"{d}/docs/en/faq.md", EN)
    rc, out = run(d); check("complete pairs -> OK", rc == 0 and "RESULT: OK" in out)
    w(f"{d}/docs/en/faq.md", EN + "## extra\n"); rc, out = run(d); check("heading mismatch warns", rc == 1 and "headings differ" in out)
    w(f"{d}/docs/en/faq.md", EN.replace("2026-10-25", "2026-10-20")); rc, out = run(d); check("date mismatch warns", rc == 1 and "date differs" in out)
    w(f"{d}/docs/en/faq.md", EN); os.remove(f"{d}/docs/en/faq.md"); rc, out = run(d); check("missing English twin warns", rc == 1 and "missing English twin" in out)
    w(f"{d}/docs/en/faq.md", EN); w(f"{d}/docs/en/only.md", EN); rc, out = run(d); check("English page without Hebrew twin warns", rc == 1 and "no Hebrew twin" in out)
    rc, out = run("--bad"); check("bad option -> 2", rc == 2)
    rc, out = run("/nonexistent/x"); check("missing dir -> 2", rc == 2)
sys.exit(1 if fails else 0)
