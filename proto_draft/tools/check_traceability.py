#!/usr/bin/env python3
"""check_traceability.py <scenarios.md> <traceability.md> [--head COMMIT] - warn-only check of requirement -> scenario traceability.
scenarios.md: records start with '# תרחיש sc-<n>: ...' and fields as '- **מצב:** בוצע | **חוסם שחרור?** כן', '- **הוכחה ...:** ...', '- **commit שנבדק:** ...'.
traceability.md: table '| דרישה / החלטה | עדיפות | תרחישים (sc-n) |'. Warns on: a 'חייב' row without a scenario; an unknown or duplicate sc id;
a defined scenario not in the table; state בוצע/חי without proof or without 'commit שנבדק'; bad state; with --head, a tested commit that is not the HEAD
(proof may be stale). Prints INFO with the number of blocking scenarios not yet done. Exit 1 on warnings, 0 clean, 2 usage. Never writes."""
import re, sys
STATES = ("פתוח", "בוצע", "חי")
def field(block, name):
    m = re.search(r"^- \*\*" + re.escape(name) + r"[^*]*\*\*:?[ \t]*(.*)$", block, re.M)
    return m.group(1).strip() if m else None
def parse_scenarios(text):
    out, dup = {}, []
    parts = re.split(r"^# תרחיש (sc-\d+)\b.*$", text, flags=re.M)
    for i in range(1, len(parts), 2):
        sid, block = parts[i], parts[i + 1]
        if sid in out: dup.append(sid)
        st = re.search(r"\*\*מצב:\*\*\s*([^\s|]+)", block)
        bl = re.search(r"\*\*חוסם שחרור\?\*\*\s*([^\s|]+)", block)
        proof = field(block, "הוכחה"); commit = field(block, "commit שנבדק")
        out[sid] = {"state": st.group(1) if st else None, "blocking": bl.group(1) == "כן" if bl else False,
                    "proof": proof or "", "commit": commit or ""}
    return out, dup
def empty(v): return (not v) or v.startswith("(")
def main():
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    head = None
    if "--head" in sys.argv:
        i = sys.argv.index("--head"); head = sys.argv[i + 1] if i + 1 < len(sys.argv) else None
        a = [x for x in a if x != head]
    if len(a) != 2: print(__doc__); return 2
    try: sc, dup = parse_scenarios(open(a[0], encoding="utf-8").read()); tr = open(a[1], encoding="utf-8").read()
    except OSError as e: print("ERROR:", e); return 2
    warn = 0
    def w(m):
        nonlocal warn; print("WARN", m); warn += 1
    for d in dup: w(f"duplicate scenario id {d}")
    referenced = set()
    for line in tr.splitlines():
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if not line.startswith("|") or len(c) < 3 or c[0] in ("דרישה / החלטה", "---") or set(c[0]) <= set("-: "): continue
        ids = re.findall(r"sc-\d+", c[2]); referenced.update(ids)
        if c[1] == "חייב" and not ids: w(f"must-have without scenario: {c[0]}")
        for i in ids:
            if i not in sc: w(f"unknown scenario {i} (row: {c[0]})")
    for sid, s in sc.items():
        if s["state"] not in STATES: w(f"{sid}: bad or missing state ({s['state']})"); continue
        if sid not in referenced: w(f"{sid}: defined but not in the traceability table")
        if s["state"] in ("בוצע", "חי"):
            if empty(s["proof"]): w(f"{sid}: state {s['state']} without proof")
            if empty(s["commit"]): w(f"{sid}: state {s['state']} without tested commit")
            elif head and not (head.startswith(s["commit"]) or s["commit"].startswith(head)):
                w(f"{sid}: tested commit {s['commit'][:12]} differs from HEAD {head[:12]} (proof may be stale)")
    open_block = [k for k, s in sc.items() if s["blocking"] and s["state"] == "פתוח"]
    print(f"INFO scenarios={len(sc)} blocking-open={len(open_block)}" + (f" ({', '.join(open_block)})" if open_block else ""))
    print("RESULT:", "WARN" if warn else "OK"); return 1 if warn else 0
sys.exit(main())
