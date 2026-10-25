#!/usr/bin/env python3
"""sync_settings.py [--apply] - keep module header lines in sync with the toggles table in settings.md.
Default is --check (no writes): prints every file whose header "מצב:" differs from the toggle. Exit 1 if drift.
(also warns, without failing, on literal threshold numbers in modules/ and templates/ that should be setting names)
--summary prints the effective state of every module (no writes).
--apply rewrites only the state word (דלוק/כבוי) in the header line, preserving any parenthetical note.
--project-settings FILE overlays the project's toggles (project_settings.md; table '| מפתח | מצב |' between the toggles markers) on the
protocol defaults: --summary and the default check then report the EFFECTIVE state, never write protocol files, and --apply is refused
(exit 2). Warns (exit 1) on unknown keys, bad states, and attempts to override core rules (approval_style, write_scope).
Effective state = own toggle AND parent toggles (a child under an OFF parent is reported as 'effective: off')."""
import os, re, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
def load():
    s = open(os.path.join(ROOT, "settings.md"), encoding="utf-8").read()
    m = re.search(r"<!-- toggles:begin -->(.*?)<!-- toggles:end -->", s, re.S)
    rows = {}
    for line in m.group(1).splitlines():
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(c) == 4 and c[0] not in ("מפתח", "---") and not c[0].startswith("-"):
            rows[c[0]] = {"file": c[1], "parent": c[2], "state": c[3]}
    return rows
def effective(rows, k):
    r = rows[k]
    if r["state"] != "דלוק": return "כבוי"
    return "דלוק" if r["parent"] == "-" else effective(rows, r["parent"])
NON_OVERRIDABLE = ("approval_style", "write_scope")
def overlay(rows, path):
    """Return (effective_rows, warnings). Overlay states from the project settings file; protocol rows are not modified on disk."""
    txt = open(path, encoding="utf-8").read(); warns = []
    eff = {k: dict(v) for k, v in rows.items()}
    m = re.search(r"<!-- toggles:begin -->(.*?)<!-- toggles:end -->", txt, re.S)
    for line in (m.group(1).splitlines() if m else []):
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(c) < 2 or c[0] in ("מפתח", "---") or c[0].startswith("-"): continue
        if c[0] not in eff: warns.append(f"WARN unknown module key in project settings: {c[0]}"); continue
        if c[1] not in ("דלוק", "כבוי"): warns.append(f"WARN bad state for {c[0]}: {c[1]}"); continue
        eff[c[0]]["state"] = c[1]
    vm = re.search(r"## דריסות ערכים(.*?)(?:\n## |\Z)", txt, re.S)
    for line in (vm.group(1).splitlines() if vm else []):
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(c) >= 2 and c[0] in NON_OVERRIDABLE:
            warns.append(f"WARN IGNORED core rule override: {c[0]} (core rules cannot be overridden)")
    return eff, warns
UNITS = {"stale_lock_hours": "שעות", "heartbeat_minutes": "דקות", "disk_stop_percent": "%", "session_usage_cap_percent": "%"}
def profiles_warn(eff_rows, limit_override=None):
    """warn-only: too many effective specialization profiles (each one adds reading to the context)."""
    txt = open(os.path.join(ROOT, "settings.md"), encoding="utf-8").read()
    m = re.search(r"\|\s*profiles_active_warn\s*\|\s*(\d+)", txt)
    limit = limit_override if limit_override is not None else (int(m.group(1)) if m else 3)
    active = [k for k, r in eff_rows.items() if "modules/specialization/" in r["file"] and effective(eff_rows, k) == "דלוק"]
    if len(active) > limit:
        print(f"WARN {len(active)} specialization profiles active (limit profiles_active_warn={limit}): {', '.join(active)}"); return 1
    return 0
def hardcoded():
    # warn-only: a threshold value from settings.md written as a literal number next to its unit in a module file
    txt = open(os.path.join(ROOT, "settings.md"), encoding="utf-8").read(); n = 0
    for k, unit in UNITS.items():
        m = re.search(r"\|\s*" + k + r"\s*\|\s*(\d+)", txt)
        if not m: continue
        rx = re.compile(r"(?<![\d.])" + m.group(1) + r"\s*" + re.escape(unit))
        for dp, dn, fn in [x for d in ("modules", "templates") for x in os.walk(os.path.join(ROOT, d))]:
            for f in fn:
                if not f.endswith(".md"): continue
                for i, line in enumerate(open(os.path.join(dp, f), encoding="utf-8"), 1):
                    if rx.search(line): print(f"WARN hardcoded {k}={m.group(1)} in {os.path.relpath(os.path.join(dp, f), ROOT)}:{i} - use the setting name"); n += 1
    return n
def main():
    apply = "--apply" in sys.argv
    rows = load(); drift = 0
    if "--project-settings" in sys.argv:
        i = sys.argv.index("--project-settings")
        if i + 1 >= len(sys.argv) or not os.path.exists(sys.argv[i + 1]):
            print("ERROR: --project-settings needs an existing file"); return 2
        if apply:
            print("REFUSED: --apply does not write protocol files when --project-settings is used (the protocol is read-only; record changes in project_settings.md)"); return 2
        eff, warns = overlay(rows, sys.argv[i + 1])
        for w in warns: print(w)
        lim = None
        vm = re.search(r"\|\s*profiles_active_warn\s*\|\s*(\d+)", open(sys.argv[i + 1], encoding="utf-8").read())
        if vm: lim = int(vm.group(1))
        pw = profiles_warn(eff, lim)
        if "--summary" in sys.argv:
            for k in eff: print(f"{k}: {effective(eff, k)}")
            return 1 if (warns or pw) else 0
        for k in eff:
            if eff[k]["state"] != rows[k]["state"]:
                print(f"INFO {k}: project={eff[k]['state']} protocol-default={rows[k]['state']} (effective: {effective(eff, k)})")
        print("RESULT:", "WARN" if (warns or pw) else "OK"); return 1 if (warns or pw) else 0
    if "--summary" in sys.argv:
        for k in rows: print(f"{k}: {effective(rows, k)}")
        profiles_warn(rows)
        return 0
    for k, r in rows.items():
        if r["state"] not in ("דלוק", "כבוי"):
            print("BAD STATE:", k, r["state"]); drift += 1; continue
        p = os.path.join(ROOT, r["file"])
        if not os.path.exists(p):
            print("MISSING FILE:", r["file"]); drift += 1; continue
        txt = open(p, encoding="utf-8").read()
        m = re.search(r"(מצב: )(דלוק|כבוי)([^|]*)", txt)
        if not m:
            print("NO HEADER מצב:", r["file"]); drift += 1; continue
        eff = effective(rows, k)
        note = "" if eff == r["state"] else f" (effective: {eff})"
        if m.group(2) != r["state"]:
            drift += 1
            print(f"DRIFT {k}: header={m.group(2)} toggle={r['state']}{note}")
            if apply:
                if not os.path.realpath(p).startswith(os.path.realpath(ROOT) + os.sep):
                    print("REFUSED: module path escapes protocol root:", r["file"]); drift += 1; continue
                new = txt[:m.start(2)] + r["state"] + txt[m.end(2):]
                open(p, "w", encoding="utf-8").write(new)
        elif note:
            print(f"INFO {k}: toggle={r['state']}{note}")
    hc = hardcoded()
    print("RESULT:", "OK" if drift == 0 else ("APPLIED" if apply else "DRIFT"))
    return 0 if (drift == 0 or apply) else 1
sys.exit(main())
