#!/usr/bin/env python3
"""check_tools.py <tools.md> [--tools-dir DIR] - warn-only comparison of the tools registry with the tools directory.
Registry rows: '| tool-<n> | type | `path` | ...'. Warns on: a registered local path (tools/...) that does not exist; an
executable-looking file in the tools dir (.py .sh) that is not registered; duplicate ids. Exit 1 on warnings, 0 clean, 2 usage."""
import os, re, sys
def main():
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if not a: print(__doc__); return 2
    reg = os.path.abspath(a[0]); base = os.path.dirname(reg); td = base + "/tools"
    for i, x in enumerate(sys.argv):
        if x == "--tools-dir" and i + 1 < len(sys.argv): td = os.path.abspath(sys.argv[i + 1])
    ids, paths, warn = set(), set(), 0
    for line in open(reg, encoding="utf-8"):
        m = re.match(r"\|\s*(tool-\d+)\s*\|[^|]*\|\s*`([^`]+)`", line)
        if not m: continue
        tid, path = m.group(1), m.group(2)
        if tid in ids: print("WARN duplicate id:", tid); warn += 1
        ids.add(tid)
        if path.startswith("tools/"):
            paths.add(os.path.basename(path))
            if not os.path.exists(os.path.join(base, path)) and not os.path.exists(os.path.join(td, os.path.basename(path))):
                print(f"WARN registered but missing: {tid} {path}"); warn += 1
    if os.path.isdir(td):
        for f in sorted(os.listdir(td)):
            if f.endswith((".py", ".sh")) and f not in paths:
                print("WARN not registered (treated as R2):", f); warn += 1
    print("RESULT:", "WARN" if warn else "OK"); return 1 if warn else 0
sys.exit(main())
