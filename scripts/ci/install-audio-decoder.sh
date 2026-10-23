#!/usr/bin/env bash
# Hosted runners usually provide FFmpeg. Avoid an unnecessary network update;
# package mirrors must not consume the entire quality-job time budget.
set -euo pipefail
mkdir -p qa-results
setup_log=qa-results/audio-decoder-setup.log
if ! ffmpeg -version >"$setup_log" 2>&1; then
  timeout 120 sudo apt-get -o Acquire::Retries=2 \
    -o Acquire::http::Timeout=20 -o Acquire::https::Timeout=20 update 2>&1 | tee -a "$setup_log"
  timeout 120 sudo apt-get -o Acquire::Retries=2 \
    -o Acquire::http::Timeout=20 -o Acquire::https::Timeout=20 \
    -o DPkg::Lock::Timeout=30 install -y --no-install-recommends ffmpeg 2>&1 | tee -a "$setup_log"
  ffmpeg -version >>"$setup_log" 2>&1
fi
sed -n '1p' "$setup_log"
