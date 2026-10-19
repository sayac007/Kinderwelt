#!/usr/bin/env bash
set -euo pipefail
DEST=${GODOT_INSTALL_DIR:-/workspace/tools/godot-4.7.2}
ARCHIVE=Godot_v4.7.2-stable_linux.x86_64.zip
BASE=https://github.com/godotengine/godot/releases/download/4.7.2-stable
TEMP_DIR=$(mktemp -d)
trap 'rm -rf "$TEMP_DIR"' EXIT
curl -fsSL "$BASE/$ARCHIVE" -o "$TEMP_DIR/$ARCHIVE"
curl -fsSL "$BASE/SHA512-SUMS.txt" -o "$TEMP_DIR/SHA512-SUMS.txt"
(cd "$TEMP_DIR"; awk -v name="$ARCHIVE" '$2 == name || $2 == "*" name' SHA512-SUMS.txt > selected.sha512; test -s selected.sha512; sha512sum -c selected.sha512)
mkdir -p "$DEST"
unzip -o "$TEMP_DIR/$ARCHIVE" -d "$DEST"
