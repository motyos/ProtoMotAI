#!/usr/bin/env python3
"""check_overview.py <overview.md> [--runs DIR] [--max-lag-days N] - warn-only drift check for the project overview page.
1) the 7 chapters of T-overview exist and keep their fixed order; 2) 'עודכן: yyyy-mm-dd' is not older than the newest
runs/run_<yyyymmdd>_*.md by more than N days (default overview_stale_days = 3). Exit 1 on warnings, 0 if clean, 2 on usage error."""
import os, re, sys, glob, datetime
CH = ["מצב והצעד הבא", "מה זה ולמי", "סביבה וטכנולוגיה", "מפת מסמכים", "כללי עבודה קריטיים", "כלים", "מגבלות ידועות"]
def main():
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    def opt(n, d):
        for i, x in enumerate(sys.argv):
            if x == n and i + 1 < len(sys.argv): return sys.argv[i + 1]
        return d
    if not a: print(__doc__); return 2
    p = a[0]; runs = opt("--runs", os.path.join(os.path.dirname(os.path.abspath(p)), "..", "runs")); lag = int(opt("--max-lag-days", "3"))
    txt = open(p, encoding="utf-8").read(); warn = 0
    pos = []
    for c in CH:
        m = re.search(r"^## \d+\. " + re.escape(c), txt, re.M)
        if not m: print("WARN missing chapter:", c); warn += 1
        else: pos.append(m.start())
    if pos != sorted(pos): print("WARN chapters out of order"); warn += 1
    m = re.search(r"עודכן:\s*(\d{4}-\d{2}-\d{2})", txt)
    if not m: print("WARN no 'עודכן: yyyy-mm-dd' line"); warn += 1
    else:
        upd = datetime.date.fromisoformat(m.group(1)); newest = None
        for f in glob.glob(os.path.join(runs, "run_*.md")):
            d = re.match(r"run_(\d{8})_", os.path.basename(f))
            if d:
                x = datetime.datetime.strptime(d.group(1), "%Y%m%d").date()
                newest = x if newest is None or x > newest else newest
        if newest and (newest - upd).days > lag:
            print(f"WARN overview updated {upd} but newest run is {newest} (lag {(newest - upd).days}d > {lag}d)"); warn += 1
    print("RESULT:", "WARN" if warn else "OK"); return 1 if warn else 0
sys.exit(main())
