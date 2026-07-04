#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if command -v esphome >/dev/null 2>&1; then
  esphome_cmd=(esphome)
elif command -v pipx >/dev/null 2>&1; then
  esphome_cmd=(pipx run esphome)
else
  echo "esphome is required; install it or install pipx so this script can run it temporarily" >&2
  exit 127
fi

configs=(
  "esphome/round-gc9a01a-240.yaml:240"
  "esphome/round-amoled-466.yaml:466"
)

for entry in "${configs[@]}"; do
  config="${entry%%:*}"
  width="${entry##*:}"
  "${esphome_cmd[@]}" -s display_width "${width}" -s display_height "${width}" -s screen_size "${width}" compile "${config}"
done
