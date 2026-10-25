#!/usr/bin/env python3
"""run_metrics.py - per-run statistics from the run log (UTC timestamps) and optional git; appends one row to runs/metrics.md.
Usage:
  run_metrics.py row   <run.log> [--progress run.md] [--repo DIR] [--idle-gap-min N]   print the markdown row
  run_metrics.py add   <run.log> --metrics runs/metrics.md [same options]               append the row (creates the page header if missing)
  run_metrics.py check <run.log> --metrics runs/metrics.md                              warn (exit 1) if the run has no row
  run_metrics.py calibrate --metrics runs/metrics.md [--min-runs N]                     median actual/estimate ratio, only with enough runs
Sources: log lines '<yyyy-mm-dd HH:MM:SS> UTC <TYPE>: text' (TYPE = ACTION|FINDING|DECISION|LESSON|BACKFILL|NOTE); lines without a
timestamp are ignored. Estimate = '**הערכה (שעות):** <number>' in the progress file. Wall time includes waiting; active time sums gaps
shorter than --idle-gap-min (default 30). Tokens and session usage are NOT computed here (agent-reported / owner-reported only).
Never reads secrets; prints counts only."""
import datetime as dt, os, re, statistics, subprocess, sys
HDR = "| ריצה | התחלה UTC | סיום UTC | משך כולל | זמן פעיל | הערכה (שעות) | יחס פעיל/הערכה | פעולות | ממצאים | החלטות | לקחים | commits | הערות |\n|---|---|---|---|---|---|---|---|---|---|---|---|---|\n"
MARK = "<!-- metrics-runs:end -->"
PAGE = "# metrics - סטטיסטיקות ריצות\n\n> שורה אוטומטית לכל ריצה (`tools/run_metrics.py add`). טוקנים וניצול סשן: רק מדווחים (ראה מקטעים למטה). משך כולל כולל המתנות.\n\n## 1. ריצות\n" + HDR + MARK + "\n\n## 2. ניצול סשן (דיווח הבעלים בלבד)\n| זמן UTC | ניצול | הערה |\n|---|---|---|\n\n## 3. סוכנים (רק כשמודול agents דלוק; \"כפי שדווח\", ייתכן מצטבר בסוכן שהופעל מחדש)\n| ריצה | סוכן | מנוע | סבב | טוקנים (כפי שדווח) | משך | הערה |\n|---|---|---|---|---|---|---|\n\n## 4. כיול\n(`run_metrics.py calibrate`; לא לפני `calibration_min_runs` ריצות)\n"
def opt(n, d=None):
    for i, a in enumerate(sys.argv):
        if a == n and i + 1 < len(sys.argv): return sys.argv[i + 1]
    return d
def parse(log):
    pat = re.compile(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) UTC (\w+):")
    ts, cnt = [], {}
    for line in open(log, encoding="utf-8", errors="ignore"):
        m = pat.match(line)
        if m:
            ts.append(dt.datetime.strptime(m.group(1), "%Y-%m-%d %H:%M:%S")); cnt[m.group(2)] = cnt.get(m.group(2), 0) + 1
    return ts, cnt
def hm(td): s = int(td.total_seconds()); return f"{s // 3600}:{(s % 3600) // 60:02d}"
def estimate(progress):
    if not progress or not os.path.exists(progress): return None
    m = re.search(r"הערכה \(שעות\):\*{0,2}\s*([0-9]+(?:\.[0-9]+)?)", open(progress, encoding="utf-8").read())
    return float(m.group(1)) if m else None
def commits(repo, a, b):
    if not repo: return "-"
    try:
        out = subprocess.run(["git", "-C", repo, "log", "--oneline", f"--since={a:%Y-%m-%d %H:%M:%S} +0000", f"--until={b:%Y-%m-%d %H:%M:%S} +0000"], capture_output=True, text=True, timeout=20).stdout
        return str(len([l for l in out.splitlines() if l.strip()]))
    except Exception: return "-"
def row(log):
    ts, cnt = parse(log)
    if not ts: print("no timestamped log lines in", log, file=sys.stderr); sys.exit(2)
    gap = dt.timedelta(minutes=int(opt("--idle-gap-min", "30"))); ts.sort()
    active = sum((b - a for a, b in zip(ts, ts[1:]) if b - a <= gap), dt.timedelta(0)); wall = ts[-1] - ts[0]
    est = estimate(opt("--progress")); ratio = f"{active.total_seconds() / 3600 / est:.2f}" if est else "-"
    rid = os.path.basename(log)[:-4] if log.endswith(".log") else os.path.basename(log)
    return rid, f"| {rid} | {ts[0]:%Y-%m-%d %H:%M} | {ts[-1]:%Y-%m-%d %H:%M} | {hm(wall)} | {hm(active)} | {est if est else '-'} | {ratio} | {cnt.get('ACTION', 0)} | {cnt.get('FINDING', 0)} | {cnt.get('DECISION', 0)} | {cnt.get('LESSON', 0)} | {commits(opt('--repo'), ts[0], ts[-1])} | |"
def has_row(metrics, rid):
    return os.path.exists(metrics) and any(l.startswith(f"| {rid} |") for l in open(metrics, encoding="utf-8"))
def main():
    if len(sys.argv) < 2: print(__doc__); return 2
    cmd = sys.argv[1]
    if cmd == "calibrate":
        m = opt("--metrics"); need = int(opt("--min-runs", "3")); vals = []
        for l in open(m, encoding="utf-8"):
            c = [x.strip() for x in l.strip().strip("|").split("|")]
            if len(c) >= 13 and re.fullmatch(r"\d+(\.\d+)?", c[6] or ""): vals.append(float(c[6]))
        if len(vals) < need: print(f"not enough data: {len(vals)} runs with estimate and ratio, need {need}"); return 1
        print(f"n={len(vals)} median ratio={statistics.median(vals):.2f} min={min(vals):.2f} max={max(vals):.2f} (actual active time / estimate)"); return 0
    if len(sys.argv) < 3: print(__doc__); return 2
    log = sys.argv[2]
    if not os.path.exists(log): print("log not found"); return 2
    rid, r = row(log)
    if cmd == "row": print(r); return 0
    metrics = opt("--metrics")
    if not metrics: print("--metrics required"); return 2
    if cmd == "check":
        if has_row(metrics, rid): print("OK: row exists for", rid); return 0
        print("WARN: no metrics row for", rid, "- run: run_metrics.py add"); return 1
    if cmd == "add":
        if has_row(metrics, rid): print("row already exists:", rid); return 1
        if not os.path.exists(metrics):
            os.makedirs(os.path.dirname(os.path.abspath(metrics)), exist_ok=True); open(metrics, "w", encoding="utf-8").write(PAGE)
        s = open(metrics, encoding="utf-8").read()
        if MARK not in s: print("marker missing in metrics page"); return 2
        open(metrics, "w", encoding="utf-8").write(s.replace(MARK, r + "\n" + MARK, 1)); print("added:", rid); return 0
    print(__doc__); return 2
sys.exit(main())
