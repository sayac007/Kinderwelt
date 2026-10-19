#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
# Isolate tests from real local saves and permit use in sandboxed cloud tasks.
TEST_STATE=$(mktemp -d /tmp/kinderwelt-tests.XXXXXX)
trap 'rm -rf "$TEST_STATE"' EXIT
export XDG_DATA_HOME="$TEST_STATE/data" XDG_CONFIG_HOME="$TEST_STATE/config" XDG_CACHE_HOME="$TEST_STATE/cache"
mkdir -p "$XDG_DATA_HOME" "$XDG_CONFIG_HOME" "$XDG_CACHE_HOME"
run_checked() {
  local log="$TEST_STATE/run.log"
  "${GODOT:-godot}" "$@" >"$log" 2>&1 || { cat "$log"; return 1; }
  cat "$log"
  if rg -q 'SCRIPT ERROR:|ERROR:|Parse Error' "$log"; then return 1; fi
}
run_checked --headless --path . --editor --import --quit
run_checked --headless --path . --script tests/smoke.gd
run_checked --headless --path . --quit-after 60
