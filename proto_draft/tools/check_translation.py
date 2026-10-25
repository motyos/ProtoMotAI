#!/usr/bin/env python3
"""check_translation.py [ROOT] - warn-only check that every Hebrew entry/doc page has an English twin and that the pair has not drifted.
Pairs: README.md <-> README.en.md, SECURITY.md <-> SECURITY.en.md, NOTICE.md <-> NOTICE.en.md, docs/he/<f>.md <-> docs/en/<f>.md.
Checks per pair: both exist; same number of '## ' headings; same number of fenced code blocks; same date in 'עודכן: yyyy-mm-dd' and 'Updated: yyyy-mm-dd'
(when either file has one). Also warns about an English page with no Hebrew twin. Exit 1 on warnings, 0 clean, 2 usage error."""
import os, re, sys, glob
def pairs(root):
    out = [(f"{n}.md", f"{n}.en.md") for n in ("README", "SECURITY", "NOTICE")]
    he = sorted(os.path.basename(p) for p in glob.glob(os.path.join(root, "docs", "he", "*.md")))
    en = sorted(os.path.basename(p) for p in glob.glob(os.path.join(root, "docs", "en", "*.md")))
    for f in sorted(set(he) | set(en)): out.append((f"docs/he/{f}", f"docs/en/{f}"))
    return out
def facts(path):
    t = open(path, encoding="utf-8").read()
    h = len(re.findall(r"^## ", t, re.M)); c = t.count("```")
    m = re.search(r"(?:עודכן|Updated): (\d{4}-\d{2}-\d{2})", t)
    return h, c, (m.group(1) if m else None)
def main():
    a = [x for x in sys.argv[1:]]
    if len(a) > 1 or any(x.startswith("-") for x in a): print(__doc__); return 2
    root = a[0] if a else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
    if not os.path.isdir(root): print("not a directory:", root); return 2
    warns = 0; n = 0
    for he, en in pairs(root):
        ph, pe = os.path.join(root, he), os.path.join(root, en); n += 1
        if not os.path.isfile(ph): print(f"WARN no Hebrew twin for {en}"); warns += 1; continue
        if not os.path.isfile(pe): print(f"WARN missing English twin: {en} (for {he})"); warns += 1; continue
        (h1, c1, d1), (h2, c2, d2) = facts(ph), facts(pe)
        if h1 != h2: print(f"WARN headings differ {he}={h1} {en}={h2}"); warns += 1
        if c1 != c2: print(f"WARN code fences differ {he}={c1} {en}={c2}"); warns += 1
        if d1 != d2: print(f"WARN update date differs {he}={d1} {en}={d2}"); warns += 1
    print(f"checked {n} pairs"); print("RESULT:", "WARN" if warns else "OK"); return 1 if warns else 0
if __name__ == "__main__": sys.exit(main())
