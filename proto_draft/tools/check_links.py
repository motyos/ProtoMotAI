#!/usr/bin/env python3
"""check_links.py <path>... [--skip DIRNAME ...] - warn-only check of relative markdown links ([text](target)) in .md files.
Ignores http(s)/mailto/#anchors and code fences. Reports file:line and the missing target. Exit 1 on warnings, 0 clean, 2 usage."""
import os, re, sys
SKIP = {".git", "_to_delete", "node_modules"}
def main():
    args, skip, i = [], set(SKIP), 1
    while i < len(sys.argv):
        if sys.argv[i] == "--skip" and i + 1 < len(sys.argv): skip.add(sys.argv[i + 1]); i += 2
        else: args.append(sys.argv[i]); i += 1
    if not args: print(__doc__); return 2
    files = []
    for a in args:
        if os.path.isfile(a): files.append(a)
        else:
            for dp, dn, fn in os.walk(a):
                dn[:] = [d for d in dn if d not in skip]
                files += [os.path.join(dp, f) for f in fn if f.endswith(".md")]
    warn = checked = 0
    for f in sorted(files):
        fence = False
        for n, line in enumerate(open(f, encoding="utf-8", errors="ignore"), 1):
            if line.lstrip().startswith("```"): fence = not fence; continue
            if fence: continue
            for m in re.finditer(r"\[[^\]]*\]\(([^)\s]+)\)", re.sub(r"`[^`]*`", "", line)):
                t = m.group(1)
                if re.match(r"^(https?:|mailto:|#)", t): continue
                t = t.split("#", 1)[0]
                if not t: continue
                checked += 1
                if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(f), t))):
                    print(f"WARN broken link: {f}:{n} -> {t}"); warn += 1
    print(f"checked {checked} links in {len(files)} files"); print("RESULT:", "WARN" if warn else "OK"); return 1 if warn else 0
sys.exit(main())
