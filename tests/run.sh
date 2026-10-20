#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
STATE=$(mktemp -d /tmp/kinderwelt-tests.XXXXXX)
trap 'rm -rf "$STATE"' EXIT
export XDG_DATA_HOME="$STATE/data" XDG_CONFIG_HOME="$STATE/config" XDG_CACHE_HOME="$STATE/cache"
mkdir -p "$XDG_DATA_HOME" "$XDG_CONFIG_HOME" "$XDG_CACHE_HOME"
for SCRIPT in import quest boot; do
  RESULT=0
  if [[ "$SCRIPT" == import ]]; then
    timeout 120 "${GODOT:-godot}" --headless --path . --editor --import --quit >"$STATE/run.log" 2>&1 || RESULT=$?
  else
    timeout 120 "${GODOT:-godot}" --headless --path . -s "tests/$SCRIPT.gd" >"$STATE/run.log" 2>&1 || RESULT=$?
  fi
  cat "$STATE/run.log"
  if ((RESULT!=0)); then exit "$RESULT"; fi
  if rg -q 'SCRIPT ERROR:|ERROR:|Parse Error' "$STATE/run.log"; then exit 1; fi
done
python3 -m unittest discover -s tests/android -v
python3 scripts/qa/audit.py
