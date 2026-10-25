#!/usr/bin/env python3
"""build_docs.py [--proto DIR] [--docs DIR] [--check] - generate docs/reference/*.md from the protocol sources (single source of truth).
Sources (under --proto, default: the protocol folder that holds this script): settings.md (toggles + settings tables), each module file header,
templates/templates_registry.md, tools.md. Output (under --docs, default <proto>/../docs/reference): modules.md, settings.md, templates.md, tools.md, ids.md (ids.md only when filename_templates.md has the ids block).
Deterministic (no dates). --check writes nothing: warns (exit 1) when an output file is missing or differs. Generated files say 'do not edit'."""
import os, re, sys
def opt(n, d=None):
    for i, a in enumerate(sys.argv):
        if a == n and i + 1 < len(sys.argv): return sys.argv[i + 1]
    return d
PROTO = os.path.abspath(opt("--proto", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))
DOCS = os.path.abspath(opt("--docs", os.path.join(PROTO, "..", "docs", "reference")))
def read(p): return open(os.path.join(PROTO, p), encoding="utf-8").read()
def cells(line):
    c = [x.strip() for x in line.strip().strip("|").split("|")]
    return c
def tables(text):
    """yield (heading, header_cells, rows) for each markdown table"""
    out, head, lines, i = [], "", text.splitlines(), 0
    while i < len(lines):
        l = lines[i]
        if l.startswith("## "): head = l[3:].strip()
        if l.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[\s:|-]+\|?$", lines[i + 1]):
            hdr = cells(l); rows = []; i += 2
            while i < len(lines) and lines[i].startswith("|"): rows.append(cells(lines[i])); i += 1
            out.append((head, hdr, rows)); continue
        i += 1
    return out
def header_info(path):
    try: first = [l for l in open(os.path.join(PROTO, path), encoding="utf-8") if l.startswith("מודול:")][0]
    except Exception: return {}
    d = {}
    for part in first.strip().split(" | "):
        if ":" in part: k, v = part.split(":", 1); d[k.strip()] = v.strip()
    return d
def esc(s): return s.replace("\n", " ")
def banner(title, sources, ver):
    return f"# {title}\n\n> **נוצר אוטומטית. לא לערוך ידנית.** מקורות: {sources}. הפקה מחדש: `python3 tools/build_docs.py`; בדיקה: `--check`. גרסת פרוטוקול: {ver}.\n\n"
def table(hdr, rows):
    s = "| " + " | ".join(hdr) + " |\n|" + "---|" * len(hdr) + "\n"
    return s + "".join("| " + " | ".join(esc(x) for x in r) + " |\n" for r in rows)
def build():
    st = read("settings.md"); ver = "-"
    for h, hdr, rows in tables(st):
        for r in rows:
            if r and r[0] == "protocol_version": ver = r[1] if len(r) > 1 else "-"
    out = {}
    # modules
    toggles = re.search(r"<!-- toggles:begin -->(.*?)<!-- toggles:end -->", st, re.S)
    rows = []; state = {}
    if toggles:
        for h, hdr, rs in tables(toggles.group(1)):
            for r in rs:
                if len(r) == 4: state[r[0]] = (r[2], r[3])
    def eff(k):
        par, st_ = state[k]
        return st_ == "דלוק" and (par == "-" or par not in state or eff(par))
    if toggles:
        for h, hdr, rs in tables(toggles.group(1)):
            for r in rs:
                if len(r) == 4:
                    info = header_info(r[1])
                    rows.append([f"`{r[0]}`", f"`{r[1]}`", r[2] if r[2] != "-" else "", r[3], ("דלוק" if eff(r[0]) else "כבוי"), info.get("גרסה", ""), info.get("סטטוס", ""), info.get("רמת סיכון", ""), info.get("תלוי ב", "")])
    out["modules.md"] = banner("מודולים", "`settings.md` (טבלת המתגים), כותרת כל קובץ מודול", ver) + "הליבה תמיד פעילה. מודול בן פעיל רק אם האב דלוק. המצב כאן הוא ברירת המחדל לפרויקט חדש.\n\n" + table(["מפתח", "קובץ", "אב", "מצב בהגדרות", "מצב אפקטיבי", "גרסה", "סטטוס", "סיכון", "תלוי ב"], rows)
    # settings
    parts = []
    for h, hdr, rs in tables(re.sub(r"<!-- toggles:begin -->.*?<!-- toggles:end -->", "", st, flags=re.S)):
        if len(hdr) >= 2 and hdr[0] in ("הגדרה", "מפתח") and hdr[0] == "הגדרה":
            parts.append(f"## {h}\n\n" + table(["הגדרה", "ערך"], [[r[0], " | ".join(r[1:])] for r in rs if r]))
    out["settings.md"] = banner("הגדרות", "`settings.md`", ver) + "\n".join(parts)
    # templates
    rg = read("templates/templates_registry.md"); parts = []
    for h, hdr, rs in tables(rg):
        if hdr and hdr[0] == "מזהה": parts.append(f"## {h}\n\n" + table(hdr, rs))
    out["templates.md"] = banner("תבניות", "`templates/templates_registry.md`", ver) + "\n".join(parts)
    # tools
    tl = read("tools.md"); parts = []
    for h, hdr, rs in tables(tl):
        if hdr and hdr[0] == "מזהה": parts.append(table(hdr, rs))
    out["tools.md"] = banner("כלים", "`tools.md`", ver) + "\n".join(parts)
    try: ft = read("filename_templates.md")
    except OSError: ft = ""
    m = re.search(r"<!-- ids:begin -->(.*?)<!-- ids:end -->", ft, re.S)
    if m:
        parts = [table(hdr, rs) for h, hdr, rs in tables(m.group(1)) if hdr and hdr[0] == "מזהה"]
        out["ids.md"] = banner("מזהים ופירושם", "`filename_templates.md` (סעיף מזהים ופירושם)", ver) + "\n".join(parts)
    return out
def main():
    out = build(); warn = 0
    if "--check" in sys.argv:
        for name, txt in out.items():
            p = os.path.join(DOCS, name)
            if not os.path.exists(p): print("WARN missing:", name); warn += 1
            elif open(p, encoding="utf-8").read() != txt: print("WARN stale (differs from sources):", name); warn += 1
        print("RESULT:", "WARN" if warn else "OK"); return 1 if warn else 0
    os.makedirs(DOCS, exist_ok=True)
    for name in out:
        p = os.path.join(DOCS, name)
        if os.path.exists(p) and "נוצר אוטומטית" not in open(p, encoding="utf-8").read(400):
            print("REFUSED: existing file is not a generated doc, not overwriting:", p); return 2
    for name, txt in out.items(): open(os.path.join(DOCS, name), "w", encoding="utf-8").write(txt); print("wrote", name)
    return 0
sys.exit(main())
