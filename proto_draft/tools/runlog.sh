#!/usr/bin/env bash
# runlog.sh - append one timestamped line to a run log (English, UTC). Usage:
#   runlog.sh <logfile> <TYPE> <text...>
# TYPE: ACTION | FINDING | DECISION | LESSON | BACKFILL | NOTE
# The timestamp always comes from `date -u`, never from memory. Never put secrets in <text>.
set -u
[ $# -ge 3 ] || { echo "usage: runlog.sh <logfile> <TYPE> <text...>" >&2; exit 2; }
log="$1"; type="$2"; shift 2
case "$type" in ACTION|FINDING|DECISION|LESSON|BACKFILL|NOTE) ;; *) echo "bad TYPE: $type" >&2; exit 2;; esac
case "$log" in *..*) echo "log path must not contain '..'" >&2; exit 2;; esac
text="$*"; text="${text//$'\n'/ }"; text="${text//$'\r'/ }"   # single line: no forged log lines
mkdir -p "$(dirname "$log")" || { echo "cannot create log directory" >&2; exit 1; }
printf '%s UTC %s: %s\n' "$(date -u '+%Y-%m-%d %H:%M:%S')" "$type" "$text" >> "$log" \
  || { echo "ERROR: could not write log" >&2; exit 1; }
