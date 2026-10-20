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
PERF_FLAGS=(--headless)
if [[ ${2:-} == --graphical ]]; then
  if [[ -z ${DISPLAY:-}${WAYLAND_DISPLAY:-} ]]; then echo "Graphical backend required" >&2; exit 2; fi
  PERF_FLAGS=()
fi
RESULT=0
python3 scripts/qa/measure_process.py --metrics "$OUTPUT/process.json" --log "$OUTPUT/performance.log" -- "${GODOT:-godot}" "${PERF_FLAGS[@]}" --audio-driver Dummy --path . -s tests/qa/benchmark_modern.gd || RESULT=$?
cat "$OUTPUT/performance.log"
if (( RESULT != 0 )); then exit "$RESULT"; fi
if rg -q 'SCRIPT ERROR:|ERROR:|Parse Error' "$OUTPUT/performance.log"; then exit 1; fi
python3 - "$KINDERWELT_PERF_OUTPUT" <<'PY'
import json,sys
r=json.load(open(sys.argv[1]));assert r['max_music_stream_slots']<=2
assert r['samples'] and r['background_state_resumed'] and r['startup_to_two_frames_ms']>0
p=json.load(open(sys.argv[1].replace('performance.json','process.json')));assert p['startup_to_ready_wall_seconds']>0 and p['startup_to_ready_wall_seconds']<p['elapsed_seconds']
print('PASS: desktop measurements recorded; Android measurements remain open')
PY
