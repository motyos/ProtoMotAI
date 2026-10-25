#!/usr/bin/env python3
"""Self-test for build_docs.py and check_links.py on a dummy protocol (no network)."""
import os, subprocess, sys, tempfile
here = os.path.dirname(os.path.abspath(__file__))
def run(script, *a): return subprocess.run([sys.executable, f"{here}/{script}", *a], capture_output=True, text=True)
with tempfile.TemporaryDirectory() as t:
    p = f"{t}/proto"; os.makedirs(f"{p}/templates"); os.makedirs(f"{p}/modules")
    open(f"{p}/settings.md", "w", encoding="utf-8").write("# s\n## בחירות\n| הגדרה | ערך |\n|---|---|\n| protocol_version | V9 |\n| x | a | b |\n<!-- toggles:begin -->\n| מפתח | קובץ | אב | מצב |\n|---|---|---|---|\n| m1 | modules/m1.md | - | כבוי |\n| m2 | modules/m1.md | m1 | דלוק |\n<!-- toggles:end -->\n")
    open(f"{p}/modules/m1.md", "w", encoding="utf-8").write("# m1\n\nמודול: m1 | גרסה: 0.3 | סטטוס: טיוטה | מצב: דלוק | תלוי ב: core | רמת סיכון: נמוכה\n")
    open(f"{p}/templates/templates_registry.md", "w", encoding="utf-8").write("## core\n| מזהה | קובץ | מטרה |\n|---|---|---|\n| T-x | a.md | b |\n")
    open(f"{p}/tools.md", "w", encoding="utf-8").write("| מזהה | סוג |\n|---|---|\n| tool-1 | protocol |\n")
    d = f"{t}/docs/reference"
    chk0 = run("build_docs.py", "--proto", p, "--docs", d, "--check"); gen = run("build_docs.py", "--proto", p, "--docs", d)
    chk1 = run("build_docs.py", "--proto", p, "--docs", d, "--check")
    mods = open(f"{d}/modules.md", encoding="utf-8").read(); sets = open(f"{d}/settings.md", encoding="utf-8").read()
    open(f"{p}/tools.md", "a", encoding="utf-8").write("| tool-2 | project |\n")
    chk2 = run("build_docs.py", "--proto", p, "--docs", d, "--check")
    os.makedirs(f"{t}/md"); open(f"{t}/md/ok.md", "w").write("x\n"); open(f"{t}/md/a.md", "w").write("[ok](ok.md) [bad](nope.md) [web](https://x.y) [anc](#a) `[code](zzz.md)`\n```\n[fence](q.md)\n```\n")
    lk = run("check_links.py", f"{t}/md")
checks = {"check before generate warns": chk0.returncode == 1, "generate ok": gen.returncode == 0, "check after generate clean": chk1.returncode == 0,
          "module row has header info": "0.3" in mods and "`m1`" in mods and "V9" in mods, "effective state of child under off parent is off": [l for l in mods.splitlines() if l.startswith("| `m2`")][0].split("|")[5].strip() == "כבוי", "settings row with extra pipe kept": "a | b" in sets,
          "stale detected after source change": chk2.returncode == 1 and "tools.md" in chk2.stdout,
          "broken link found only once": lk.stdout.count("broken link") == 1 and "nope.md" in lk.stdout and lk.returncode == 1}
for k, v in checks.items(): print(("PASS " if v else "FAIL ") + k)
sys.exit(0 if all(checks.values()) else 1)
