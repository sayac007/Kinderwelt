#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
OUTPUT=${1:?Pass a new performance output directory}
if [[ -e "$OUTPUT" ]]; then echo 'Refusing existing output' >&2; exit 1; fi
mkdir -p "$OUTPUT"
OUTPUT=$(realpath "$OUTPUT")
STATE=$(mktemp -d /tmp/kinderwelt-modern-perf.XXXXXX)
trap 'rm -rf "$STATE"' EXIT
export XDG_DATA_HOME="$STATE/data" XDG_CONFIG_HOME="$STATE/config" XDG_CACHE_HOME="$STATE/cache"
mkdir -p "$XDG_DATA_HOME" "$XDG_CONFIG_HOME" "$XDG_CACHE_HOME"
export KINDERWELT_PERF_OUTPUT="$OUTPUT/performance.json"
RESULT=0
timeout 120 "${GODOT:-godot}" --headless --path . -s tests/qa/benchmark_modern.gd >"$OUTPUT/performance.log" 2>&1 || RESULT=$?
cat "$OUTPUT/performance.log"
if (( RESULT != 0 )); then exit "$RESULT"; fi
if rg -q 'SCRIPT ERROR:|ERROR:|Parse Error' "$OUTPUT/performance.log"; then exit 1; fi
python3 - "$KINDERWELT_PERF_OUTPUT" <<'PY'
import json,sys
r=json.load(open(sys.argv[1]));assert r['max_music_stream_slots']<=2
assert r['samples'] and r['background_state_resumed'] and r['startup_to_two_frames_ms']>0
print('PASS: desktop measurements recorded; Android measurements remain open')
PY
