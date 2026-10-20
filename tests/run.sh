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
  local result=0
  timeout 120 "${GODOT:-godot}" "$@" >"$log" 2>&1 || result=$?
  cat "$log"
  if (( result != 0 )); then return "$result"; fi
  if rg -q 'SCRIPT ERROR:|ERROR:|Parse Error' "$log"; then return 1; fi
}
run_checked --headless --path . --editor --import --quit
run_checked --headless --path . --script tests/smoke.gd
run_checked --headless --path . --script tests/learning.gd
run_checked --headless --path . --script tests/input.gd
run_checked --headless --path . --script tests/scenarios.gd
run_checked --headless --path . --script tests/adventure.gd
run_checked --headless --path . --script tests/modern.gd
run_checked --headless --path . --script tests/boot.gd
