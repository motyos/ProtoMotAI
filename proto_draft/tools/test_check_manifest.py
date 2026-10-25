#!/usr/bin/env python3
"""test_check_manifest.py - self-test for check_manifest.py using temporary protocol folders. Exit 0 = all PASS."""
import os, subprocess, sys, tempfile
TOOL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "check_manifest.py")
GOOD = {"key": "demo", "שם": "דמו", "סוג": "טכנולוגיה", "תחומים": "web", "גרסה": "0.1", "בשלות": "draft", "אומת ב": "-", "תפקיד": "x",
        "מחברים": "me", "רישיון": "CC BY 4.0", "מקורות": "אין, נימוק", "תרחישים": "אין", "מה זה לא": "זה לא הסמכה רשמית"}
def mk(over=None, drop=None, reg_mat="draft", reg_ver="0.1", toggle=True, extra_dir=False, scen=None):
    d = tempfile.mkdtemp(); f = dict(GOOD); f.update(over or {})
    for k in (drop or []): f.pop(k, None)
    os.makedirs(os.path.join(d, "modules/specialization/demo"))
    if scen: f["תרחישים"] = scen
    man = "## מניפסט\n" + "".join(f"- {k}: {v}\n" for k, v in f.items())
    open(os.path.join(d, "modules/specialization/demo/module.md"), "w", encoding="utf-8").write("# demo\n\nמודול: demo | גרסה: 0.1 | סטטוס: טיוטה\n\n" + man)
    tg = "| demo | modules/specialization/demo/module.md | - | דלוק |\n" if toggle else ""
    open(os.path.join(d, "settings.md"), "w", encoding="utf-8").write("<!-- toggles:begin -->\n| מפתח | קובץ | אב | מצב |\n|---|---|---|---|\n" + tg + "<!-- toggles:end -->\n")
    open(os.path.join(d, "profiles.md"), "w", encoding="utf-8").write(f"| key | שם | סוג | תחומים | בשלות | גרסה | תיקייה |\n|---|---|---|---|---|---|---|\n| demo | דמו | t | web | {reg_mat} | {reg_ver} | x |\n")
    if extra_dir: os.makedirs(os.path.join(d, "modules/specialization/orphan"))
    return d
def run(d):
    r = subprocess.run([sys.executable, "-I", TOOL, "--proto", d], capture_output=True, text=True); return r.returncode, r.stdout
fails = 0
def check(n, ok):
    global fails
    print(("PASS " if ok else "FAIL ") + n); fails += 0 if ok else 1
rc, o = run(mk()); check("clean profile OK", rc == 0 and "RESULT: OK" in o)
rc, o = run(mk(drop=["מחברים"])); check("missing field warns", rc == 1 and "field missing or empty: מחברים" in o)
rc, o = run(mk(over={"key": "other"})); check("manifest key differs from toggle", rc == 1 and "differs from toggle key" in o)
rc, o = run(mk(over={"גרסה": "0.2"}, reg_ver="0.2")); check("manifest version differs from header", rc == 1 and "differs from header version" in o)
rc, o = run(mk(over={"בשלות": "reviewed"}, reg_mat="reviewed")); check("reviewed without 'אומת ב' warns", rc == 1 and "without 'אומת ב'" in o)
rc, o = run(mk(over={"בשלות": "reviewed", "אומת ב": "round 5"}, reg_mat="reviewed")); check("reviewed with verification OK", rc == 0)
rc, o = run(mk(over={"בשלות": "beta"}, reg_mat="beta")); check("bad maturity warns", rc == 1 and "bad maturity" in o)
rc, o = run(mk(reg_mat="approved")); check("registry maturity mismatch warns", rc == 1 and "profiles.md maturity" in o)
rc, o = run(mk(over={"מה זה לא": "בלי הצהרה"})); check("disclaimer must mention הסמכה", rc == 1 and "disclaimer" in o)
rc, o = run(mk(scen="`scenarios.md`")); check("declared scenarios file missing warns", rc == 1 and "scenarios file missing" in o)
rc, o = run(mk(toggle=False)); check("registry row without toggle warns", rc == 1 and "without a toggle" in o)
rc, o = run(mk(extra_dir=True)); check("unregistered profile folder warns", rc == 1 and "orphan" in o)
r = subprocess.run([sys.executable, "-I", TOOL, "--proto", "/nonexistent"], capture_output=True, text=True); check("missing protocol exit 2", r.returncode == 2)
sys.exit(1 if fails else 0)
