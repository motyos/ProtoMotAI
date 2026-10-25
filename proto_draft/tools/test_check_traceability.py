#!/usr/bin/env python3
"""test_check_traceability.py - self-test for check_traceability.py (temp files only). Exit 0 = all PASS."""
import os, subprocess, sys, tempfile
TOOL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "check_traceability.py")
def mk(s):
    f = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8"); f.write(s); f.close(); return f.name
def sc(n, state="פתוח", block="כן", proof="", commit=""):
    return f"# תרחיש sc-{n}: שם\n- **מצב:** {state}  | **חוסם שחרור?** {block}\n- **הוכחה (פקודה / ריצה / מספר):** {proof}\n- **commit שנבדק:** {commit}\n\n"
def tr(*rows): return "| דרישה / החלטה | עדיפות | תרחישים (sc-n) |\n|---|---|---|\n" + "".join(f"| {r} |\n" for r in rows)
def run(s, t, *x):
    r = subprocess.run([sys.executable, "-I", TOOL, mk(s), mk(t), *x], capture_output=True, text=True); return r.returncode, r.stdout
fails = 0
def check(n, ok):
    global fails
    print(("PASS " if ok else "FAIL ") + n); fails += 0 if ok else 1
rc, o = run(sc(1, "בוצע", "כן", "ריצה 1 עברה", "abc1234"), tr("login | חייב | sc-1")); check("clean case OK", rc == 0 and "RESULT: OK" in o)
rc, o = run(sc(1), tr("login | חייב | ")); check("must-have without scenario warns", rc == 1 and "must-have without scenario" in o)
rc, o = run(sc(1), tr("login | חייב | sc-1", "pay | צריך | sc-9")); check("unknown scenario warns", rc == 1 and "unknown scenario sc-9" in o)
rc, o = run(sc(1) + sc(2), tr("login | חייב | sc-1")); check("scenario not in table warns", rc == 1 and "sc-2: defined but not" in o)
rc, o = run(sc(1, "בוצע", "כן", "", "abc"), tr("a | חייב | sc-1")); check("done without proof warns", rc == 1 and "without proof" in o)
rc, o = run(sc(1, "בוצע", "כן", "ok", ""), tr("a | חייב | sc-1")); check("done without commit warns", rc == 1 and "without tested commit" in o)
rc, o = run(sc(1, "בוצע", "כן", "ok", "abc1234"), tr("a | חייב | sc-1"), "--head", "ffff0000"); check("stale proof vs HEAD warns", rc == 1 and "may be stale" in o)
rc, o = run(sc(1, "בוצע", "כן", "ok", "abc1234"), tr("a | חייב | sc-1"), "--head", "abc1234def"); check("matching HEAD prefix OK", rc == 0)
rc, o = run(sc(1, "אולי"), tr("a | חייב | sc-1")); check("bad state warns", rc == 1 and "bad or missing state" in o)
rc, o = run(sc(1) + sc(1), tr("a | חייב | sc-1")); check("duplicate id warns", rc == 1 and "duplicate scenario id" in o)
rc, o = run(sc(1, "פתוח", "כן"), tr("a | חייב | sc-1")); check("blocking-open reported as INFO, exit 0", rc == 0 and "blocking-open=1" in o)
r = subprocess.run([sys.executable, "-I", TOOL], capture_output=True, text=True); check("usage exit 2", r.returncode == 2)
sys.exit(1 if fails else 0)
