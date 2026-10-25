#!/usr/bin/env bash
# check_resources.sh [DIR] - read-only resource check before launching a wave of agents.
# Prints numbers only. Exit 0 = OK to launch, 1 = stop (disk over limit), 2 = error.
# Limits (defaults mirror settings.md): DISK_STOP_PERCENT=80, MIN_FREE_MB=500. Concurrency suggestion is advisory.
set -u
DIR="${1:-.}"; LIM="${DISK_STOP_PERCENT:-80}"; MINMB="${MIN_FREE_MB:-500}"
[ -d "$DIR" ] || { echo "not a directory" >&2; exit 2; }
used="$(df -P "$DIR" | awk 'NR==2{gsub("%","",$5); print $5}')"; free_mb="$(df -Pm "$DIR" | awk 'NR==2{print $4}')"
load="$(cut -d' ' -f1 /proc/loadavg 2>/dev/null || echo n/a)"; cpus="$(nproc 2>/dev/null || echo 1)"
mem="$(awk '/MemAvailable/{printf "%d", $2/1024}' /proc/meminfo 2>/dev/null || echo n/a)"
for v in "$LIM" "$MINMB" "$used" "$free_mb"; do case "$v" in ''|*[!0-9]*) echo "ERROR: non-numeric value ($v); cannot decide" >&2; exit 2;; esac; done
echo "disk_used_percent=$used limit=$LIM free_mb=$free_mb load1=$load cpus=$cpus mem_available_mb=$mem"
if [ "$used" -ge "$LIM" ] || [ "$free_mb" -lt "$MINMB" ]; then echo "RESULT: STOP (disk)"; exit 1; fi
sug=$cpus; [ "$sug" -gt 5 ] && sug=5
echo "suggested_concurrency<=$sug (agents_concurrency_cap and session usage decide the final number)"; echo "RESULT: OK"; exit 0
