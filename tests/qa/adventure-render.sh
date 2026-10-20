#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
if [[ -z ${DISPLAY:-}${WAYLAND_DISPLAY:-} ]]; then
  echo 'NOT RUN: graphical backend required' >&2
  exit 2
fi
OUTPUT=${1:?Pass a new screenshot output directory}
if [[ -e "$OUTPUT" ]]; then echo "Refusing existing screenshot output" >&2; exit 1; fi
mkdir -p "$OUTPUT"
OUTPUT=$(realpath "$OUTPUT")
STATE=$(mktemp -d /tmp/kinderwelt-adventure-render.XXXXXX)
trap 'rm -rf "$STATE"' EXIT
export XDG_DATA_HOME="$STATE/data" XDG_CONFIG_HOME="$STATE/config" XDG_CACHE_HOME="$STATE/cache"
mkdir -p "$XDG_DATA_HOME" "$XDG_CONFIG_HOME" "$XDG_CACHE_HOME"
export KINDERWELT_RENDER_OUTPUT="$OUTPUT"
RESULT=0
timeout 180 "${GODOT:-godot}" --path . --audio-driver Dummy -s tests/qa/render_adventure.gd >"$OUTPUT/render.log" 2>&1 || RESULT=$?
cat "$OUTPUT/render.log"
if (( RESULT != 0 )); then exit "$RESULT"; fi
if rg -q 'SCRIPT ERROR:|ERROR:|Parse Error' "$OUTPUT/render.log"; then exit 1; fi
python3 - "$OUTPUT" <<'PY'
import json,struct,sys
from pathlib import Path
root=Path(sys.argv[1]);frames=json.loads((root/'adventure-render.json').read_text())['frames']
assert len(frames)==45
for frame in frames:
 data=(root/frame['file']).read_bytes()
 assert data[:8]==b'\x89PNG\r\n\x1a\n'
 assert list(struct.unpack('>II',data[16:24]))==frame['pixels']
print('PASS: 45 adventure renders, five profiles (including large text)')
PY
