#!/usr/bin/env python3
"""check_manifest.py [--proto DIR] - warn-only check of professional profiles (specialization modules).
For each toggle in settings.md whose file is under modules/specialization/: the module has a '## מניפסט' section with all required fields
(key, שם, סוג, תחומים, גרסה, בשלות, תפקיד, מחברים, רישיון, מקורות, מה זה לא); key equals the toggle key; version equals the module header version;
maturity in draft/reviewed/approved and, when not draft, 'אומת ב' filled; the disclaimer mentions 'הסמכה'; a declared scenarios file exists;
profiles.md lists it with the same maturity and version. Also warns on a profile folder that is not in the toggles table, and a registry row without a toggle.
Exit 1 on warnings, 0 clean, 2 usage/IO error. Never writes."""
import os, re, sys
REQ = ["key", "שם", "סוג", "תחומים", "גרסה", "בשלות", "תפקיד", "מחברים", "רישיון", "מקורות", "מה זה לא"]
def main():
    proto = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    if "--proto" in sys.argv:
        i = sys.argv.index("--proto")
        if i + 1 >= len(sys.argv): print(__doc__); return 2
        proto = os.path.abspath(sys.argv[i + 1])
    try:
        st = open(os.path.join(proto, "settings.md"), encoding="utf-8").read()
        reg = open(os.path.join(proto, "profiles.md"), encoding="utf-8").read()
    except OSError as e: print("ERROR:", e); return 2
    m = re.search(r"<!-- toggles:begin -->(.*?)<!-- toggles:end -->", st, re.S)
    toggles = {}
    for line in (m.group(1).splitlines() if m else []):
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(c) == 4 and "modules/specialization/" in c[1]: toggles[c[0]] = c[1]
    rows = {}
    for line in reg.splitlines():
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if line.startswith("|") and len(c) >= 7 and c[0] not in ("key", "---") and not set(c[0]) <= set("-: "): rows[c[0]] = c
    warn = 0
    def w(msg):
        nonlocal warn; print("WARN", msg); warn += 1
    for key, rel in toggles.items():
        p = os.path.join(proto, rel)
        if not os.path.exists(p): w(f"{key}: module file missing ({rel})"); continue
        txt = open(p, encoding="utf-8").read()
        mm = re.search(r"^## מניפסט\s*$(.*?)(?=^## |\Z)", txt, re.S | re.M)
        if not mm: w(f"{key}: no '## מניפסט' section"); continue
        f = {}
        for line in mm.group(1).splitlines():
            x = re.match(r"^- ([^:]+):\s*(.*)$", line)
            if x: f[x.group(1).strip()] = x.group(2).strip()
        for r in REQ:
            if not f.get(r): w(f"{key}: manifest field missing or empty: {r}")
        if f.get("key") and f["key"] != key: w(f"{key}: manifest key '{f['key']}' differs from toggle key")
        hv = re.search(r"גרסה: ([^|\s]+)", txt)
        if hv and f.get("גרסה") and hv.group(1) != f["גרסה"]: w(f"{key}: manifest version {f['גרסה']} differs from header version {hv.group(1)}")
        mat = f.get("בשלות", "")
        if mat and mat not in ("draft", "reviewed", "approved"): w(f"{key}: bad maturity '{mat}'")
        if mat in ("reviewed", "approved") and f.get("אומת ב", "-") in ("", "-"): w(f"{key}: maturity {mat} without 'אומת ב'")
        if f.get("מה זה לא") and "הסמכה" not in f["מה זה לא"]: w(f"{key}: disclaimer must mention 'הסמכה'")
        sc = f.get("תרחישים", "")
        mf = re.search(r"`([^`]+)`", sc)
        if mf and not os.path.exists(os.path.join(os.path.dirname(p), mf.group(1))): w(f"{key}: declared scenarios file missing: {mf.group(1)}")
        if key not in rows: w(f"{key}: not listed in profiles.md")
        else:
            if f.get("בשלות") and rows[key][4] != f["בשלות"]: w(f"{key}: profiles.md maturity {rows[key][4]} differs from manifest {f['בשלות']}")
            if f.get("גרסה") and rows[key][5] != f["גרסה"]: w(f"{key}: profiles.md version {rows[key][5]} differs from manifest {f['גרסה']}")
    for key in rows:
        if key not in toggles: w(f"{key}: listed in profiles.md without a toggle in settings.md")
    sd = os.path.join(proto, "modules", "specialization")
    known = {os.path.basename(os.path.dirname(os.path.join(proto, r))) for r in toggles.values()} | {os.path.splitext(os.path.basename(r))[0] for r in toggles.values()}
    if os.path.isdir(sd):
        for n in sorted(os.listdir(sd)):
            if os.path.isdir(os.path.join(sd, n)) and n not in known: w(f"{n}: profile folder not in the toggles table")
    print("RESULT:", "WARN" if warn else "OK"); return 1 if warn else 0
sys.exit(main())
