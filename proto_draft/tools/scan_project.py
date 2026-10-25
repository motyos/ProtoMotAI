#!/usr/bin/env python3
"""scan_project.py <dir> [--max-files N] [--max-bytes N] [--max-depth N] - read-only inventory of a project.
- Never executes anything from the scanned tree; never follows symlinks; never writes.
- Never prints secret VALUES: findings are reported as path:line:type only.
- Files whose NAME matches the deny patterns (see sensitive_paths.md) are listed but never opened.
- Output: markdown to stdout (the T-inventory content). Everything not scanned is listed under 'NOT SCANNED'."""
import os, re, stat, sys, fnmatch
DENY = ["*secret*", ".env*", "*.pem", "*.key", "*.p12", "*.pfx", "id_rsa*", "*credential*", "*password*",
        "*token*", ".npmrc", ".pypirc", "*.kdbx", "*.keystore", "*.jks",
        "id_ed25519*", "id_ecdsa*", ".netrc", ".pgpass", "*.tfstate", "*.tfstate.*", "*.ovpn"]
SKIP_DIRS = {".git", "node_modules", "vendor", "storage", ".venv", "venv", "__pycache__", "dist", "build", ".idea",
             ".ssh", ".aws", ".gnupg", ".kube"}
TEXT_EXT = {".md", ".txt", ".py", ".js", ".ts", ".tsx", ".jsx", ".php", ".java", ".go", ".rb", ".rs", ".c", ".h", ".cpp",
            ".cs", ".sh", ".sql", ".json", ".yml", ".yaml", ".toml", ".ini", ".cfg", ".conf", ".xml", ".html", ".css", ".env.example"}
LANG = {".py": "Python", ".js": "JavaScript", ".ts": "TypeScript", ".tsx": "TypeScript", ".jsx": "JavaScript", ".php": "PHP",
        ".java": "Java", ".go": "Go", ".rb": "Ruby", ".rs": "Rust", ".c": "C", ".cpp": "C++", ".cs": "C#", ".sh": "Shell", ".sql": "SQL"}
MARKERS = {"package.json": "Node", "composer.json": "PHP/Composer", "requirements.txt": "Python", "pyproject.toml": "Python",
           "pom.xml": "Java/Maven", "go.mod": "Go", "Cargo.toml": "Rust", "Gemfile": "Ruby", "Dockerfile": "Docker",
           "docker-compose.yml": "Docker Compose", "docker-compose.yaml": "Docker Compose", "Makefile": "Make"}
DOC_NAMES = ["README", "CLAUDE", "INSTRUCTIONS", "DECISIONS", "ADR", "TODO", "CHANGELOG", "LOG", "OPEN_QUESTIONS", "SECURITY",
             "CONTRIBUTING", "LICENSE", "ROADMAP", "ARCHITECTURE"]
SECRET_PATTERNS = [
    ("private-key-block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("aws-access-key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("github-token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b")),
    ("url-with-password", re.compile(r"[a-z][a-z0-9+.-]*://[^/\s:@]+:[^/\s@]{3,}@")),
    ("key-assignment", re.compile(r"(?i)\b(pass(word)?|pwd|secret|token|api[_-]?key|client[_-]?secret|access[_-]?key)\b\s*[:=]\s*['\"][^'\"\s]{8,}['\"]")),
    ("long-random-string", re.compile(r"[A-Za-z0-9+/=_-]{48,}")),
]
def is_denied(name):
    return any(fnmatch.fnmatch(name.lower(), p.lower()) for p in DENY)
def main():
    OPTS = ("--max-files", "--max-bytes", "--max-depth")
    args, skip = [], False
    for a in sys.argv[1:]:
        if skip: skip = False; continue
        if a in OPTS: skip = True; continue
        if a.startswith("--"): print("unknown option:", a); return 2
        args.append(a)
    def opt(n, d):
        for i, a in enumerate(sys.argv):
            if a == n and i + 1 < len(sys.argv):
                try: return int(sys.argv[i + 1])
                except ValueError: print("not an integer:", sys.argv[i + 1]); sys.exit(2)
        return d
    if not args: print(__doc__); return 2
    root = os.path.abspath(args[0])
    if not os.path.isdir(root): print("NOT A DIRECTORY:", root); return 2
    max_files, max_bytes, max_depth = opt("--max-files", 5000), opt("--max-bytes", 512 * 1024), opt("--max-depth", 8)
    langs, markers, docs, denied, tests, ci, findings, notscanned = {}, [], [], [], [], [], [], []
    tools_found = []
    total = scanned = 0; has_git = os.path.isdir(os.path.join(root, ".git")); license_file = None
    top = []
    for dp, dn, fn in os.walk(root, followlinks=False):
        rel = os.path.relpath(dp, root); depth = 0 if rel == "." else rel.count(os.sep) + 1
        if depth == 1 or rel == ".": top.append(rel)
        keep = []
        for d in sorted(dn):
            if d in SKIP_DIRS: notscanned.append(f"{os.path.join(rel, d) if rel != '.' else d}/ (skipped dir)")
            elif depth >= max_depth: notscanned.append(f"{os.path.join(rel, d)}/ (max depth)")
            elif os.path.islink(os.path.join(dp, d)): notscanned.append(f"{os.path.join(rel, d)} (symlink)")
            else: keep.append(d)
        dn[:] = keep
        for f in sorted(fn):
            p = os.path.join(dp, f); r = os.path.relpath(p, root)
            if os.path.islink(p): notscanned.append(f"{r} (symlink)"); continue
            total += 1
            ext = os.path.splitext(f)[1].lower()
            if ext in LANG: langs[LANG[ext]] = langs.get(LANG[ext], 0) + 1
            if re.match(r"(tools|scripts|bin)(/|$)", r) or f in ("Makefile", "Jenkinsfile"): tools_found.append(r)
            if f in MARKERS: markers.append(f"{r} ({MARKERS[f]})")
            base = os.path.splitext(f)[0].upper()
            if any(base == n or base.startswith(n) for n in DOC_NAMES): docs.append(r)
            if base.startswith("LICENSE") or base.startswith("COPYING"): license_file = r
            if re.search(r"(^|/)(tests?|spec|__tests__)(/|$)", r) or re.search(r"(test_|_test\.|\.test\.|\.spec\.)", f): tests.append(r)
            if r.startswith(".github/workflows") or f in (".gitlab-ci.yml", "Jenkinsfile", ".travis.yml"): ci.append(r)
            if is_denied(f):
                denied.append(r); continue
            if scanned >= max_files: notscanned.append(f"{r} (max files)"); continue
            if ext not in TEXT_EXT and f not in MARKERS and ext != "": continue
            try:
                if not stat.S_ISREG(os.lstat(p).st_mode): notscanned.append(f"{r} (not a regular file)"); continue
                if os.path.getsize(p) > max_bytes: notscanned.append(f"{r} (larger than {max_bytes} bytes)"); continue
                with open(p, "r", encoding="utf-8", errors="ignore") as fh:
                    scanned += 1
                    for n, line in enumerate(fh, 1):
                        for typ, rx in SECRET_PATTERNS:
                            if rx.search(line): findings.append((r, n, typ)); break
            except OSError as e:
                notscanned.append(f"{r} (unreadable: {e.strerror})")
    gi = os.path.join(root, ".gitignore"); gi_text = ""
    if os.path.isfile(gi):
        try: gi_text = open(gi, encoding="utf-8", errors="ignore").read()
        except OSError: pass
    env_ignored = bool(re.search(r"^\.env", gi_text, re.M))
    print(f"# T-inventory - {os.path.basename(root)}\n")
    print(f"- **נסרק:** {scanned} קבצי טקסט מתוך {total} קבצים (מכסות: קבצים {max_files}, גודל {max_bytes}, עומק {max_depth})")
    print(f"- **git:** {'יש תיקיית .git (לא הורצה שום פקודת git)' if has_git else 'אין'}")
    print(f"- **רישיון:** {license_file or 'לא נמצא קובץ רישיון'}")
    print(f"- **.gitignore:** {'קיים' if gi_text else 'חסר'}; מכסה .env: {'כן' if env_ignored else 'לא'}")
    print("\n## שפות (לפי סיומת)"); [print(f"- {k}: {v}") for k, v in sorted(langs.items(), key=lambda x: -x[1])] or print("- אין")
    print("\n## קבצי סימון טכנולוגיה"); [print(f"- {m}") for m in markers] or print("- אין")
    print("\n## מסמכים קיימים"); [print(f"- {d}") for d in docs[:60]] or print("- אין")
    print("\n## בדיקות ו-CI"); print(f"- קבצי בדיקות: {len(tests)}"); print(f"- CI: {', '.join(ci) if ci else 'לא נמצא'}")
    print("\n## קבצים עם שם רגיש (לא נפתחו)"); [print(f"- {d}") for d in denied] or print("- אין")
    print("\n## חשד לסודות בקבצים (נתיב:שורה:סוג בלבד, בלי ערכים)"); [print(f"- {a}:{b}:{c}") for a, b, c in findings[:200]] or print("- לא נמצא")
    if len(findings) > 200: print(f"- ... ועוד {len(findings) - 200}")
    print("\n## כלים וסקריפטים שנמצאו (לא הורצו)")
    cand = [x for x in tools_found][:60]
    [print(f"- {x}") for x in cand] or print("- אין")
    print("\n## NOT SCANNED"); [print(f"- {x}") for x in notscanned[:100]] or print("- אין")
    if len(notscanned) > 100: print(f"- ... ועוד {len(notscanned) - 100}")
    print("\n## תיקיות ברמה העליונה"); [print(f"- {t}") for t in sorted(set(x for x in top if x != '.'))[:80]]
    return 0
if __name__ == "__main__": sys.exit(main())
