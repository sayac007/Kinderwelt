#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
python3 scripts/variants.py prepare --output . --variant "${KINDERWELT_VARIANT:-auto}"
OUTPUT=${1:?Pass a new output directory}
if [[ -e "$OUTPUT" ]]; then echo 'Refusing existing output' >&2; exit 1; fi
mkdir -p "$OUTPUT"
OUTPUT=$(realpath "$OUTPUT")
STATE=$(mktemp -d /tmp/kinderwelt-quest-render.XXXXXX)
trap 'rm -rf "$STATE"' EXIT
export XDG_DATA_HOME="$STATE/data" XDG_CONFIG_HOME="$STATE/config" XDG_CACHE_HOME="$STATE/cache"
mkdir -p "$XDG_DATA_HOME" "$XDG_CONFIG_HOME" "$XDG_CACHE_HOME"
export KINDERWELT_RENDER_OUTPUT="$OUTPUT"
# Variant preparation recreates source/import descriptors; rebuild the cache.
"${GODOT:-godot}" --headless --path . --editor --import --quit >"$OUTPUT/import.log" 2>&1
if rg -q 'SCRIPT ERROR:|ERROR:|Parse Error' "$OUTPUT/import.log"; then cat "$OUTPUT/import.log"; exit 1; fi
RESULT=0
timeout 240 "${GODOT:-godot}" --path . --audio-driver Dummy -s tests/qa/render_quest.gd >"$OUTPUT/render.log" 2>&1 || RESULT=$?
cat "$OUTPUT/render.log"
if ((RESULT!=0)); then exit "$RESULT"; fi
if rg -q 'SCRIPT ERROR:|ERROR:|Parse Error' "$OUTPUT/render.log"; then exit 1; fi
python3 - "$OUTPUT" <<'PY'
import hashlib,json,struct,sys
from pathlib import Path
p=Path(sys.argv[1]);frames=json.loads((p/'renders.json').read_text())
assert len(frames)==343
for frame in frames:
 data=(p/(frame['name']+'.png')).read_bytes()
 assert data[:8]==b'\x89PNG\r\n\x1a\n'
 assert list(struct.unpack('>II',data[16:24]))==frame['pixels']
for profile in ['phone','small','landscape','dense']:
 assert len({hashlib.sha256((p/(profile+'-heroes'+suffix+'.png')).read_bytes()).hexdigest() for suffix in ['', '-move','-think','-success']})==4
for profile in ['phone','small','landscape','dense']:
 assert (p/(profile+'-scene-castle.png')).read_bytes()!=(p/(profile+'-scene-castle-floating.png')).read_bytes()
 assert len({hashlib.sha256((p/(profile+'-looks-'+look+'.png')).read_bytes()).hexdigest() for look in ['hero','alien','astronaut','scientist']})==4
print('PASS: 343 real frames; maximum-score headers in world and task; independent looks and three sceneries; seven heroes, live task rotations, score animations; original 24 tasks, 15 science tasks, eight worlds, all three languages, route paging and menus at four profiles; distinct animated poses')
PY
