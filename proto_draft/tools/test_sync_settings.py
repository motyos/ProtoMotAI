#!/usr/bin/env python3
"""test_sync_settings.py - self-test for sync_settings.py --project-settings. Read-only on the protocol (uses temp files). Exit 0 = all PASS."""
import hashlib, os, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); TOOL = os.path.join(HERE, "sync_settings.py"); ROOT = os.path.join(HERE, "..")
def run(*a):
    r = subprocess.run([sys.executable, "-I", TOOL, *a], capture_output=True, text=True); return r.returncode, r.stdout
def ps(toggles="", values=""):
    f = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8")
    f.write("# x\n<!-- toggles:begin -->\n| מפתח | מצב |\n|---|---|\n" + toggles + "<!-- toggles:end -->\n\n## דריסות ערכים\n| הגדרה | ערך | הערה |\n|---|---|---|\n" + values + "\n## מקום אחסון\n- storage_mode: local\n")
    f.close(); return f.name
def h(p): return hashlib.sha256(open(os.path.join(ROOT, p), "rb").read()).hexdigest()
fails = 0
def check(name, ok):
    global fails
    print(("PASS " if ok else "FAIL ") + name); fails += 0 if ok else 1
f = ps("| migration | דלוק |\n")
rc, out = run("--summary", "--project-settings", f); check("overlay turns migration on", "migration: דלוק" in out and rc == 0)
f = ps("| agents.auto_decisions | דלוק |\n")
rc, out = run("--summary", "--project-settings", f); check("child under OFF parent stays off", "agents.auto_decisions: כבוי" in out)
f = ps("| agents | דלוק |\n")
rc, out = run("--summary", "--project-settings", f); check("parent on makes ON child effective", "agents.run_lock: דלוק" in out)
f = ps("| no_such_module | דלוק |\n")
rc, out = run("--project-settings", f); check("unknown key warns, exit 1", rc == 1 and "unknown module key" in out)
f = ps("| migration | אולי |\n")
rc, out = run("--project-settings", f); check("bad state warns", rc == 1 and "bad state" in out)
f = ps("", "| approval_style | חופשי | |\n")
rc, out = run("--project-settings", f); check("core rule override ignored with warning", rc == 1 and "IGNORED core rule override" in out)
before = (h("settings.md"), h("modules/general/migration/module.md"))
f = ps("| migration | דלוק |\n")
rc, out = run("--apply", "--project-settings", f)
check("--apply refused (exit 2)", rc == 2 and "REFUSED" in out)
check("protocol files unchanged", before == (h("settings.md"), h("modules/general/migration/module.md")))
rc, out = run("--project-settings", "/nonexistent/x.md"); check("missing file exit 2", rc == 2)
f = ps(); rc, out = run("--project-settings", f); check("empty overlay is OK", rc == 0 and "RESULT: OK" in out)
f = ps("| secure_dev | דלוק |\n", "| profiles_active_warn | 0 | |\n")
rc, out = run("--summary", "--project-settings", f); check("too many profiles warns (limit overridden to 0)", rc == 1 and "specialization profiles active" in out)
rc, out = run("--summary", "--project-settings", ps()); check("profiles within default limit: no warning", rc == 0 and "specialization profiles active" not in out)
sys.exit(1 if fails else 0)
