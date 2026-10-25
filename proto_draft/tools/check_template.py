#!/usr/bin/env python3
"""check_template.py <template-id> <file> - verify a file created from a template has its required fields.
Reads ../templates/required_fields.json. Exit 0 = ok, 1 = missing fields, 2 = usage error.
Also flags unreplaced placeholders like <subject> left in the first 12 lines."""
import json, os, re, sys
def main():
    if len(sys.argv) != 3:
        print(__doc__); return 2
    tid, path = sys.argv[1], sys.argv[2]
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "..", "templates", "required_fields.json"), encoding="utf-8") as f:
        spec = json.load(f)
    if tid not in spec:
        print("unknown template id:", tid); return 2
    text = open(path, encoding="utf-8").read()
    low = text.lower()
    missing = [k for k in spec[tid] if k.lower() not in low]
    head = "\n".join(text.splitlines()[:12])
    left = sorted(set(re.findall(r"<[a-z_]+>", head)))
    for k in missing: print("MISSING:", k)
    for p in left: print("PLACEHOLDER-LEFT:", p)
    print("RESULT:", "FAIL" if (missing or left) else "OK")
    return 1 if (missing or left) else 0
sys.exit(main())
