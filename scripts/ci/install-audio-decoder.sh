#!/usr/bin/env bash
# Hosted runners usually provide FFmpeg. The fallback uses a pinned static
# development decoder; unrelated apt repositories cannot block game tests.
set -euo pipefail
mkdir -p qa-results
setup_log=qa-results/audio-decoder-setup.log
if ! ffmpeg -version >"$setup_log" 2>&1; then
  cat "$setup_log"
  decoder_root="${RUNNER_TEMP:-$PWD/build/ci-tools}/kinderwelt-ffmpeg"
  timeout 120 python3 "$(dirname "$0")/audio_decoder.py" --destination "$decoder_root" 2>&1 | tee -a "$setup_log"
  export PATH="$decoder_root:$PATH"
  ffmpeg -version >>"$setup_log" 2>&1
fi
ffmpeg -version 2>&1 | sed -n '1p'
