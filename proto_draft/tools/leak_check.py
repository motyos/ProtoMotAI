#!/usr/bin/env python3
"""leak_check.py --secrets FILE [--secrets FILE2 ...] --targets DIR_OR_FILE [...]
Local leak check for uploads. The secrets files are read by THIS script only (the chat never sees them);
values (8+ chars, KEY=VALUE lines) are hashed (sha256), then every token of every target file is hashed and compared.
Output: path:line only. Never prints a value or a hash. Exit codes: 0 clean and complete; 1 a match; 2 usage error or no secret values
loaded (the check is meaningless, so it fails closed); 3 incomplete (files skipped: too large, unreadable, symlink) and no match found.
The secrets files are read by this script only, by the owner's explicit approval. Limits: only exact whole-token matches; use pattern checks as a complement."""
import hashlib, os, re, sys
def h(s): return hashlib.sha256(s.encode("utf-8", "ignore")).hexdigest()
def collect(argv, flag):
    return [argv[i + 1] for i, a in enumerate(argv) if a == flag and i + 1 < len(argv)]
SKIPPED = {"large": 0, "unreadable": 0, "symlink": 0}
def targets_iter(paths):
    for t in paths:
        if os.path.isfile(t): yield t; continue
        for dp, dn, fn in os.walk(t, followlinks=False):
            dn[:] = [d for d in dn if d not in (".git", "node_modules", "vendor")]
            for f in fn:
                p = os.path.join(dp, f)
                if os.path.islink(p): SKIPPED["symlink"] += 1; continue
                yield p
def main():
    secs, tg = collect(sys.argv, "--secrets"), collect(sys.argv, "--targets")
    if not secs or not tg: print(__doc__); return 2
    hashes = set()
    for sf in secs:
        try:
            for line in open(sf, encoding="utf-8", errors="ignore"):
                if "=" in line:
                    v = line.split("=", 1)[1].strip().strip("'\"")
                    if len(v) >= 8: hashes.add(h(v))
        except OSError: print("cannot read secrets file (path hidden)"); return 2
    print(f"secret values loaded: {len(hashes)} (not shown)")
    if not hashes:
        print("ERROR: no secret values loaded (empty file or no KEY=VALUE lines with 8+ chars); result would be meaningless")
        return 2
    hits = 0
    for p in targets_iter(tg):
        try:
            if os.path.getsize(p) > 2 * 1024 * 1024: SKIPPED["large"] += 1; continue
            for n, line in enumerate(open(p, encoding="utf-8", errors="ignore"), 1):
                if any(h(tok) in hashes for tok in re.findall(r"[^\s'\"=:,;<>()\[\]{}]{8,}", line)):
                    print(f"MATCH {p}:{n}"); hits += 1
        except OSError: SKIPPED["unreadable"] += 1
    skipped = sum(SKIPPED.values())
    print("skipped: large=%d unreadable=%d symlink=%d" % (SKIPPED["large"], SKIPPED["unreadable"], SKIPPED["symlink"]))
    if hits: print("RESULT: LEAK"); return 1
    if skipped: print("RESULT: INCOMPLETE (skipped files were not checked)"); return 3
    print("RESULT: CLEAN"); return 0
sys.exit(main())
