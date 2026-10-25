#!/usr/bin/env python3
"""Self-test for run_lock.sh, runlog.sh and check_resources.sh (temp dirs only, no network). PASS/FAIL per check; exit 1 on any FAIL."""
import os, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); fails = 0
def sh(script, *a, env=None, cwd=None):
    e = dict(os.environ); e.pop("RUN_ID", None); e.pop("OWNER_OK", None)
    if env: e.update(env)
    r = subprocess.run(["bash", os.path.join(HERE, script), *a], capture_output=True, text=True, env=e, cwd=cwd, timeout=60)
    return r.returncode, r.stdout + r.stderr
def check(name, cond):
    global fails
    print(("PASS " if cond else "FAIL ") + name); fails += (not cond)
with tempfile.TemporaryDirectory() as d:
    rc, out = sh("run_lock.sh", "-d", d, "status"); check("status without lock -> free", rc == 0 and "free" in out)
    rc, out = sh("run_lock.sh", "-d", d, "acquire", "r1", "purpose", "docs", "runs/r1.md"); check("acquire -> 0", rc == 0)
    rc, out = sh("run_lock.sh", "-d", d, "acquire", "r2", "p", "docs", "runs/r2.md"); check("second run blocked -> 1", rc == 1 and "BLOCKED" in out)
    rc, out = sh("run_lock.sh", "-d", d, "check"); check("check without RUN_ID blocked -> 1", rc == 1)
    rc, out = sh("run_lock.sh", "-d", d, "check", env={"RUN_ID": "r1"}); check("check as owner -> 0", rc == 0)
    rc, out = sh("run_lock.sh", "-d", d, "heartbeat"); check("heartbeat without RUN_ID refused -> 1", rc == 1 and "RUN_ID" in out)
    rc, out = sh("run_lock.sh", "-d", d, "release", env={"RUN_ID": "other"}); check("release by non-owner refused -> 1", rc == 1)
    rc, out = sh("run_lock.sh", "-d", d, "heartbeat", env={"RUN_ID": "r1"}); check("heartbeat as owner -> 0", rc == 0)
    rc, out = sh("run_lock.sh", "-d", d, "acquire", "r3", "p", "docs", "/etc/x.md"); check("absolute progress path -> 2", rc == 2)
    rc, out = sh("run_lock.sh", "-d", d, "acquire", "r3", "p", "docs", "../x.md"); check("'..' progress path -> 2", rc == 2)
    rc, out = sh("run_lock.sh", "-d", d, "acquire", "r3", "line1\nline2", "docs", "runs/x.md"); check("newline in field -> 2", rc == 2)
    rc, out = sh("run_lock.sh", "-d", d, "takeover", "r9", "p", "docs", "runs/r9.md", env={"OWNER_OK": "1"}); check("takeover of fresh lock refused -> 1", rc == 1)
    lock = os.path.join(d, "run_lock.md"); s = open(lock).read()
    import re; s = re.sub(r"last_update_utc: .*", "last_update_utc: 2000-01-01T00:00:00Z", s); open(lock, "w").write(s)
    rc, out = sh("run_lock.sh", "-d", d, "takeover", "r9", "p", "docs", "runs/r9.md"); check("stale takeover without OWNER_OK refused -> 1", rc == 1 and "approval" in out)
    rc, out = sh("run_lock.sh", "-d", d, "takeover", "r9", "p", "docs", "runs/r9.md", env={"OWNER_OK": "1"}); check("stale takeover with OWNER_OK -> 0", rc == 0)
    s = open(lock).read(); s = re.sub(r"last_update_utc: .*", "last_update_utc: garbage", s); open(lock, "w").write(s)
    rc, out = sh("run_lock.sh", "-d", d, "takeover", "r10", "p", "docs", "runs/r10.md", env={"OWNER_OK": "1"}); check("unparseable time never stale -> takeover refused", rc == 1)
    rc, out = sh("run_lock.sh", "-d", d, "release", env={"RUN_ID": "r9"}); check("release by owner -> 0", rc == 0)
    rc, out = sh("run_lock.sh", "-d", d, "status"); check("after release free", "status: free" in out)
    rc, out = sh("run_lock.sh", "-d", os.path.join(d, "nodir"), "status"); check("missing dir -> 2", rc == 2)
    log = os.path.join(d, "runs", "x.log")
    rc, out = sh("runlog.sh", log, "ACTION", "hello\nFAKE 2000 ACTION: forged"); txt = open(log).read()
    check("runlog single line (no forged line)", rc == 0 and len(txt.splitlines()) == 1)
    rc, out = sh("runlog.sh", log, "BAD", "x"); check("runlog bad type -> 2", rc == 2)
    rc, out = sh("runlog.sh", os.path.join(d, "a", "..", "b.log"), "NOTE", "x"); check("runlog '..' path -> 2", rc == 2)
    ro = os.path.join(d, "ro"); os.makedirs(ro); os.chmod(ro, 0o500)
    if os.geteuid() != 0:
        rc, out = sh("runlog.sh", os.path.join(ro, "x.log"), "NOTE", "x"); check("runlog write failure -> 1", rc == 1)
    os.chmod(ro, 0o700)
    rc, out = sh("check_resources.sh", d); check("check_resources numeric -> 0 or 1", rc in (0, 1) and "disk_used_percent=" in out)
    rc, out = sh("check_resources.sh", d, env={"DISK_STOP_PERCENT": "0"}); check("limit 0 -> STOP (1)", rc == 1 and "STOP" in out)
    rc, out = sh("check_resources.sh", d, env={"DISK_STOP_PERCENT": "abc"}); check("non-numeric limit -> 2 (fail closed)", rc == 2)
    rc, out = sh("check_resources.sh", os.path.join(d, "nodir")); check("not a directory -> 2", rc == 2)
print("FAILS:", fails); sys.exit(1 if fails else 0)
