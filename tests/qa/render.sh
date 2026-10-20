#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
if [[ -z "${DISPLAY:-}" && -z "${WAYLAND_DISPLAY:-}" ]]; then
  echo 'NOT RUN: a real rendering backend/display is required; headless is not visual evidence.' >&2
  exit 2
fi
OUTPUT=${1:-"$PWD/qa-results/render-$(date -u +%Y%m%dT%H%M%SZ)-$$"}
if [[ -e "$OUTPUT" ]]; then echo 'Refusing an existing render output directory.' >&2; exit 1; fi
mkdir -p "$OUTPUT"
OUTPUT=$(realpath "$OUTPUT")
SESSION=$(mktemp -d /tmp/kinderwelt-render.XXXXXX)
trap 'rm -rf "$SESSION"' EXIT
export XDG_DATA_HOME="$SESSION/data" XDG_CONFIG_HOME="$SESSION/config" XDG_CACHE_HOME="$SESSION/cache"
mkdir -p "$XDG_DATA_HOME" "$XDG_CONFIG_HOME" "$XDG_CACHE_HOME"
export KINDERWELT_RENDER_OUTPUT="$OUTPUT"
RESULT=0
timeout 180 "${GODOT:-godot}" --path . --audio-driver Dummy --script tests/qa/render_review.gd >"$OUTPUT/render.log" 2>&1 || RESULT=$?
cat "$OUTPUT/render.log"
if (( RESULT != 0 )); then exit "$RESULT"; fi
if rg -q 'SCRIPT ERROR:|ERROR:|Parse Error' "$OUTPUT/render.log"; then exit 1; fi
python3 - "$OUTPUT" <<'PY'
import json,sys,struct
from pathlib import Path
root=Path(sys.argv[1]); report=json.loads((root/'render.json').read_text())
registrations=json.loads(Path('content/modules.json').read_text())
tasks={(e['id'], t['id']) for e in registrations for t in json.loads(Path(e['levels'].removeprefix('res://')).read_text())['levels']}
expected={(m,t,v) for m,t in tasks for v in [(320,568),(768,1024)]}
actual={(f['module'],f['task'],tuple(f['viewport'])) for f in report['frames']}
assert actual==expected and report['frames'], 'Missing render coverage'
assert all((root/f['file']).is_file() and (root/f['file']).stat().st_size>0 for f in report['frames']), 'Missing images'
assert all(struct.unpack('>II',(root/f['file']).read_bytes()[16:24])==tuple(f['viewport']) for f in report['frames']), 'Image dimensions differ from declared viewport'
print(f'Rendered {len(tasks)} tasks at two viewports; {len(report["frames"])} synthetic frames. Manual review is separate.')
PY
