#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
mkdir -p qa-results
touch qa-results/.gdignore
python3 scripts/variants.py prepare --output . --variant "${KINDERWELT_VARIANT:-auto}"
OUTPUT=${1:?Pass a new output directory}
if [[ -e "$OUTPUT" ]]; then echo 'Refusing existing output' >&2; exit 1; fi
mkdir -p "$OUTPUT"
touch "$OUTPUT/.gdignore"
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
timeout 300 "${GODOT:-godot}" --path . --audio-driver Dummy -s tests/qa/render_quest.gd >"$OUTPUT/render.log" 2>&1 || RESULT=$?
cat "$OUTPUT/render.log"
if ((RESULT!=0)); then exit "$RESULT"; fi
if rg -q 'SCRIPT ERROR:|ERROR:|Parse Error' "$OUTPUT/render.log"; then exit 1; fi
python3 scripts/qa/verify_renders.py "$OUTPUT"
export KINDERWELT_AVATAR_RENDER_OUTPUT="$OUTPUT/avatars"
timeout 120 "${GODOT:-godot}" --path . --audio-driver Dummy -s tests/qa/avatar_render.gd >"$OUTPUT/avatar-render.log" 2>&1
cat "$OUTPUT/avatar-render.log"
if rg -q 'SCRIPT ERROR:|ERROR:|Parse Error' "$OUTPUT/avatar-render.log"; then exit 1; fi
mkdir "$OUTPUT/music-credits"
export KINDERWELT_CREDITS_OUTPUT="$OUTPUT/music-credits"
timeout 120 "${GODOT:-godot}" --path . --audio-driver Dummy -s tests/music_credits.gd >"$OUTPUT/music-credits.log" 2>&1
cat "$OUTPUT/music-credits.log"
if rg -q 'SCRIPT ERROR:|ERROR:|Parse Error' "$OUTPUT/music-credits.log"; then exit 1; fi
mkdir "$OUTPUT/privacy"
export KINDERWELT_PRIVACY_RENDER_OUTPUT="$OUTPUT/privacy"
timeout 120 "${GODOT:-godot}" --path . --audio-driver Dummy -s tests/qa/privacy_render.gd >"$OUTPUT/privacy-render.log" 2>&1
cat "$OUTPUT/privacy-render.log"
if rg -q 'SCRIPT ERROR:|ERROR:|Parse Error' "$OUTPUT/privacy-render.log"; then exit 1; fi
