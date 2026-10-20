#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
# Read the immutable version from the same policy used by CI and the QA report.
GUT_COMMIT=$(python3 -c 'import json; print(json.load(open("tests/qa/policy.json"))["gut_commit"])')
GUT_SOURCE="$PWD/.godot/qa-tools/gut"
if [[ ! -d "$GUT_SOURCE/.git" ]]; then
  if [[ -e "$GUT_SOURCE" ]]; then
    echo 'Refusing to replace an unknown QA tools directory.' >&2
    exit 1
  fi
  mkdir -p "$GUT_SOURCE"
  git -C "$GUT_SOURCE" init -q
  git -C "$GUT_SOURCE" remote add origin https://github.com/bitwes/Gut.git
fi
if ! git -C "$GUT_SOURCE" cat-file -e "$GUT_COMMIT^{commit}" 2>/dev/null; then
  git -C "$GUT_SOURCE" fetch --depth 1 origin "$GUT_COMMIT"
fi
if [[ -n "$(git -C "$GUT_SOURCE" status --porcelain --untracked-files=no)" ]]; then
  echo 'Pinned GUT source has local modifications; refusing to overwrite.' >&2
  exit 1
fi
git -C "$GUT_SOURCE" -c advice.detachedHead=false checkout -q "$GUT_COMMIT"
test "$(git -C "$GUT_SOURCE" rev-parse HEAD)" = "$GUT_COMMIT"
mkdir -p addons
if [[ -e addons/gut || -L addons/gut ]]; then
  test "$(realpath addons/gut)" = "$GUT_SOURCE/addons/gut" || {
    echo 'Existing addons/gut differs from the pinned development dependency.' >&2
    exit 1
  }
else
  ln -s ../.godot/qa-tools/gut/addons/gut addons/gut
fi
printf 'GUT source verified at %s\n' "$GUT_COMMIT"
