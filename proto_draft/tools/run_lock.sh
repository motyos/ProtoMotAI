#!/usr/bin/env bash
# run_lock.sh - portable run lock for multi-chat work (module agents/run_lock).
# Usage: run_lock.sh [-d DIR] status|check|acquire RUN_ID PURPOSE SCOPE PROGRESS_FILE|heartbeat|log TEXT|release [NOTE]|takeover RUN_ID PURPOSE SCOPE PROGRESS_FILE
#   DIR = project write dir (default: current dir). Lock file: DIR/run_lock.md (key: value lines, written atomically).
# Exit codes: 0 ok / allowed to write; 1 not allowed (lock held by another run) ; 2 usage/error.
# status is always free to run. takeover only when the lock is stale (STALE_LOCK_HOURS, default 3) AND env OWNER_OK=1 is set
# (the chat sets it only after an explicit owner approval). No git hook here (enforcement = instruction only).
# Requires Linux (GNU date, flock). Calls are serialized with flock on DIR/.run_lock.flock (kept; add it to .gitignore).
# heartbeat/log/release require env RUN_ID equal to the lock owner. Fields must be single-line; PROGRESS_FILE must be relative with no '..'.
set -u
DIR="."; if [ "${1:-}" = "-d" ]; then DIR="$2"; shift 2; fi
LOCK="$DIR/run_lock.md"; STALE_H="${STALE_LOCK_HOURS:-3}"
case "$STALE_H" in ''|*[!0-9]*) echo "STALE_LOCK_HOURS must be an integer" >&2; exit 2;; esac
[ -d "$DIR" ] || { echo "not a directory: $DIR" >&2; exit 2; }
exec 9>"$DIR/.run_lock.flock" || { echo "cannot open lock guard" >&2; exit 2; }
flock -w 10 9 || { echo "lock guard busy, retry" >&2; exit 1; }
badfield() { case "$1" in *$'\n'*|*$'\r'*) return 0;; esac; return 1; }
badpath() { case "$1" in /*|*..*) return 0;; esac; return 1; }
owner_only() { [ -n "${RUN_ID:-}" ] && [ "$RUN_ID" = "$(get run_id)" ] || { echo "RUN_ID does not match the lock owner" >&2; exit 1; }; }
now() { date -u '+%Y-%m-%dT%H:%M:%SZ'; }
get() { [ -f "$LOCK" ] && sed -n "s/^$1: //p" "$LOCK" | head -1; }
epoch() { date -u -d "$1" +%s 2>/dev/null || echo 0; }
hist() { [ -f "$LOCK" ] && sed -n '/^## history/,$p' "$LOCK" | tail -n +2 | head -20; }
write() { # status run_id purpose scope progress started last note [history-line]
  local tmp; tmp="$(mktemp "$DIR/.run_lock.XXXXXX")" || { echo "cannot create temp file" >&2; exit 2; }
  { echo "# run_lock"; echo "status: $1"; echo "run_id: $2"; echo "purpose: $3"; echo "scope: $4"; echo "progress_file: $5"
    echo "started_utc: $6"; echo "last_update_utc: $7"; echo "note: $8"; echo "## history"
    [ -n "${9:-}" ] && echo "- ${9}"; hist | grep -v '^$' | head -9; } > "$tmp" && mv "$tmp" "$LOCK"
}
logline() { local pf; pf="$(get progress_file)"; [ -n "$pf" ] || return 0
  local lf="${pf%.md}.log"; [ "${lf:0:1}" = "/" ] || lf="$DIR/$lf"
  printf '%s %s: %s\n' "$(date -u '+%F %T UTC')" "$1" "$2" >> "$lf" 2>/dev/null || echo "WARN: could not write run log" >&2; }
is_stale() { local l e; l="$(get last_update_utc)"; [ -n "$l" ] || return 1
  e="$(epoch "$l")"; [ "$e" -gt 0 ] || return 1   # unparseable time: never stale (fail closed)
  [ $(( $(date -u +%s) - e )) -gt $(( STALE_H * 3600 )) ]; }
cmd="${1:-}"; shift || true
case "$cmd" in
  status)
    if [ ! -f "$LOCK" ]; then echo "status: free (no lock file)"; else
      echo "status: $(get status)"; echo "run_id: $(get run_id)"; echo "purpose: $(get purpose)"; echo "last_update_utc: $(get last_update_utc)"
      [ "$(get status)" = active ] && is_stale && echo "STALE: no update for over ${STALE_H}h - ask the owner before takeover"; fi; exit 0 ;;
  check)
    st="$( [ -f "$LOCK" ] && get status || echo free )"; [ "$st" = free ] && exit 0
    [ -n "${RUN_ID:-}" ] && [ "$RUN_ID" = "$(get run_id)" ] && exit 0
    echo "BLOCKED: lock held by $(get run_id)" >&2; exit 1 ;;
  acquire)
    [ $# -ge 4 ] || { echo "usage: acquire RUN_ID PURPOSE SCOPE PROGRESS_FILE" >&2; exit 2; }
    for f in "$1" "$2" "$3" "$4"; do badfield "$f" && { echo "fields must be single-line" >&2; exit 2; }; done
    badpath "$4" && { echo "PROGRESS_FILE must be relative without '..'" >&2; exit 2; }
    if [ -f "$LOCK" ] && [ "$(get status)" = active ] && [ "$(get run_id)" != "$1" ]; then
      echo "BLOCKED: active run $(get run_id); read-only mode, tell the owner" >&2; is_stale && echo "STALE: ask the owner before takeover" >&2; exit 1; fi
    t="$(now)"; write active "$1" "$2" "$3" "$4" "$t" "$t" "" "$t acquire $1"; logline ACTION "lock acquired $1"; exit 0 ;;
  heartbeat)
    [ "$(get status)" = active ] || { echo "no active lock" >&2; exit 1; }
    owner_only
    write active "$(get run_id)" "$(get purpose)" "$(get scope)" "$(get progress_file)" "$(get started_utc)" "$(now)" "$(get note)"; logline NOTE heartbeat; exit 0 ;;
  log)
    [ $# -ge 1 ] || { echo "usage: log TEXT" >&2; exit 2; }
    badfield "$*" && { echo "TEXT must be single-line" >&2; exit 2; }
    [ "$(get status)" = active ] || { echo "no active lock" >&2; exit 1; }
    owner_only
    logline ACTION "$*"; write active "$(get run_id)" "$(get purpose)" "$(get scope)" "$(get progress_file)" "$(get started_utc)" "$(now)" "$(get note)"; exit 0 ;;
  release)
    badfield "${*:-}" && { echo "NOTE must be single-line" >&2; exit 2; }
    [ "$(get status)" = active ] || { echo "no active lock" >&2; exit 1; }
    owner_only
    id="$(get run_id)"; logline ACTION "lock released $id"; t="$(now)"
    write free "" "" "" "" "" "$t" "${*:-}" "$t release $id"; exit 0 ;;
  takeover)
    [ $# -ge 4 ] || { echo "usage: takeover RUN_ID PURPOSE SCOPE PROGRESS_FILE" >&2; exit 2; }
    for f in "$1" "$2" "$3" "$4"; do badfield "$f" && { echo "fields must be single-line" >&2; exit 2; }; done
    badpath "$4" && { echo "PROGRESS_FILE must be relative without '..'" >&2; exit 2; }
    [ "$(get status)" = active ] || { echo "no active lock; use acquire" >&2; exit 1; }
    is_stale || { echo "lock is not stale (limit ${STALE_H}h); takeover refused" >&2; exit 1; }
    [ "${OWNER_OK:-0}" = 1 ] || { echo "takeover needs explicit owner approval (set OWNER_OK=1 only after it)" >&2; exit 1; }
    old="$(get run_id)"; t="$(now)"; write active "$1" "$2" "$3" "$4" "$t" "$t" "took over from $old" "$t takeover from $old by $1"
    logline DECISION "takeover from $old (owner approved)"; exit 0 ;;
  *) sed -n '2,9p' "$0" | sed 's/^# \{0,1\}//'; exit 2 ;;
esac
