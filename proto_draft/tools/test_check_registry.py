#!/usr/bin/env python3
"""Self-test for check_registry.py (temp dir, no network)."""
import json, os, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); TOOL = os.path.join(HERE, "check_registry.py")
fails = 0
def run(d): return subprocess.run([sys.executable, TOOL, d], capture_output=True, text=True)
def check(name, cond):
    global fails
    print(("PASS " if cond else "FAIL ") + name); fails += (not cond)
def mk(d, spec, col="a, b", body="a b"):
    os.makedirs(os.path.join(d, "x"), exist_ok=True)
    open(os.path.join(d, "x", "f.md"), "w", encoding="utf-8").write(body)
    json.dump(spec, open(os.path.join(d, "required_fields.json"), "w", encoding="utf-8"))
    open(os.path.join(d, "templates_registry.md"), "w", encoding="utf-8").write(
        "| T-z | x/f.md | goal | out/z.md | %s | - |\n" % col)
with tempfile.TemporaryDirectory() as d:
    mk(d, {"_comment": "c", "T-z": ["a", "b"]}); r = run(d)
    check("consistent -> OK", r.returncode == 0 and "RESULT: OK" in r.stdout)
with tempfile.TemporaryDirectory() as d:
    mk(d, {"_comment": "c"}); r = run(d)
    check("registry id missing in JSON", r.returncode == 1 and "NOT-IN-JSON: T-z" in r.stdout)
with tempfile.TemporaryDirectory() as d:
    mk(d, {"_comment": "c", "T-z": ["a", "b"], "T-q": ["a"]}); r = run(d)
    check("JSON id missing in registry", "NOT-IN-REGISTRY: T-q" in r.stdout and r.returncode == 1)
with tempfile.TemporaryDirectory() as d:
    mk(d, {"_comment": "c", "T-z": ["a", "b"]}, col="a, c"); r = run(d)
    check("column differs", "COLUMN-DIFFERS: T-z" in r.stdout)
with tempfile.TemporaryDirectory() as d:
    mk(d, {"_comment": "c", "T-z": ["a", "b"]}, body="a only"); r = run(d)
    check("keyword absent from template", "KEYWORD-ABSENT: T-z b" in r.stdout)
print("FAILS:", fails); sys.exit(1 if fails else 0)
