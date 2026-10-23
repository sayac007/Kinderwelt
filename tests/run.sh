#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
PROJECT=$(pwd)
python3 scripts/variants.py prepare --output "$PROJECT" --variant "${KINDERWELT_VARIANT:-auto}"
STATE=$(mktemp -d /tmp/kinderwelt-tests.XXXXXX)
trap 'rm -rf "$STATE"' EXIT
export XDG_DATA_HOME="$STATE/data" XDG_CONFIG_HOME="$STATE/config" XDG_CACHE_HOME="$STATE/cache"
mkdir -p "$XDG_DATA_HOME" "$XDG_CONFIG_HOME" "$XDG_CACHE_HOME"
checked() {
  local result=0
  timeout 120 "${GODOT:-godot}" "$@" >"$STATE/run.log" 2>&1 || result=$?
  cat "$STATE/run.log"
  if ((result!=0)); then return "$result"; fi
  if rg -q 'SCRIPT ERROR:|ERROR:|Parse Error' "$STATE/run.log"; then return 1; fi
}
checked --headless --path . --editor --import --quit
checked --headless --path . -s tests/quest.gd
checked --headless --path . -s tests/worlds.gd
checked --headless --path . -s tests/boot.gd
KINDERWELT_SAVE_TEST=write checked --headless --path . -s tests/save_restart.gd
KINDERWELT_SAVE_TEST=read checked --headless --path . -s tests/save_restart.gd
checked --headless --path . -s tests/rewards.gd
mkdir -p qa-results
export KINDERWELT_SPEECH_REPORT=${KINDERWELT_SPEECH_REPORT:-"$PROJECT/qa-results/speech-playback.json"}
export KINDERWELT_SEQUENCE_REPORT=${KINDERWELT_SEQUENCE_REPORT:-"$PROJECT/qa-results/speech-sequences.json"}
checked --headless --audio-driver Dummy --path . -s tests/qa/speech_playback.gd
checked --headless --audio-driver Dummy --path . -s tests/qa/speech_sequences.gd
checked --headless --audio-driver Dummy --path . -s tests/qa/world_speech.gd
# Verify a shipping-files-only project with an entirely empty import cache.
mkdir "$STATE/fresh"
cp -R core games assets project.godot export_presets.cfg "$STATE/fresh/"
checked --headless --path "$STATE/fresh" --editor --import --quit
checked --headless --path "$STATE/fresh" -s "$PROJECT/tests/boot.gd"
python3 -m unittest discover -s tests/android -v
python3 scripts/qa/audit.py
python3 scripts/qa/character_origins.py --output qa-results/character-origins.json
python3 scripts/qa/distractors.py --check

python3 scripts/qa/localization.py --check

python3 scripts/qa/voice_models.py

python3 scripts/music/notices.py --check

python3 scripts/qa/documentation.py --check
