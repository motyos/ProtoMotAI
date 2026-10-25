#!/usr/bin/env python3
"""check_registry.py [templates_dir] - consistency of templates_registry.md with required_fields.json.
Checks: every T-id in the registry exists in the JSON and vice versa; the registry 'required fields' column equals
the JSON keywords joined by ', ' (T-ids whose registry text is descriptive are listed in DESCRIPTIVE); every keyword
appears in the template file. Exit 0 = ok, 1 = problems, 2 = usage."""
import json, os, re, sys
# Registry text is a human summary (with quotes/extra detail); the JSON holds the machine keywords.
DESCRIPTIVE = {'T-run','T-run-short','T-close','T-decision','T-question','T-next','T-scope','T-instr','T-step'}
def main():
    here = os.path.dirname(os.path.abspath(__file__))
    tdir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "..", "templates")
    if len(sys.argv) > 2: print(__doc__); return 2
    spec = json.load(open(os.path.join(tdir, "required_fields.json"), encoding="utf-8"))
    reg = open(os.path.join(tdir, "templates_registry.md"), encoding="utf-8").read()
    rows = {}
    for m in re.finditer(r"^\| (T-[\w-]+) \| (\S+) \| .*? \| .*? \| (.*?) \| .*? \|$", reg, re.M):
        rows[m.group(1)] = (m.group(2), m.group(3))
    probs = []
    for t in rows:
        if t not in spec: probs.append("NOT-IN-JSON: " + t)
    for t in spec:
        if t.startswith("T-") and t not in rows: probs.append("NOT-IN-REGISTRY: " + t)
    for t, (f, col) in rows.items():
        if t not in spec: continue
        if t not in DESCRIPTIVE and col != ", ".join(spec[t]):
            probs.append("COLUMN-DIFFERS: " + t)
        path = os.path.join(tdir, f)
        if not os.path.exists(path): probs.append("NO-FILE: %s %s" % (t, f)); continue
        low = open(path, encoding="utf-8").read().lower()
        for k in spec[t]:
            if k.lower() not in low: probs.append("KEYWORD-ABSENT: %s %s" % (t, k))
    for p in probs: print(p)
    print("RESULT:", "FAIL" if probs else "OK", "(%d templates)" % len(rows))
    return 1 if probs else 0
sys.exit(main())
