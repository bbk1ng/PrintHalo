#!/usr/bin/env bash
set -euo pipefail

# Usage: compile-esphome.sh [device-name] [friendly-name]
# The YAML is a master config; pass a device name (hostname) and friendly
# name here to build for a specific device without editing the file:
#   scripts/compile-esphome.sh bambu-kitchen "Kitchen Bambu Dashboard"
# Omit both to use the defaults in the YAML's substitutions block.

cd "$(dirname "$0")/.."

device_name="${1:-}"
friendly_name="${2:-}"

if command -v esphome >/dev/null 2>&1; then
  esphome_cmd=(esphome)
elif command -v pipx >/dev/null 2>&1; then
  esphome_cmd=(pipx run esphome)
else
  echo "esphome is required; install it or install pipx so this script can run it temporarily" >&2
  exit 127
fi

name_args=()
if [[ -n "${device_name}" ]]; then
  name_args+=(-s name "${device_name}")
fi
if [[ -n "${friendly_name}" ]]; then
  name_args+=(-s friendly_name "${friendly_name}")
fi

configs=(
  "esphome/round-amoled-466.yaml:466"
)

for entry in "${configs[@]}"; do
  config="${entry%%:*}"
  width="${entry##*:}"
  "${esphome_cmd[@]}" "${name_args[@]}" -s display_width "${width}" -s display_height "${width}" -s screen_size "${width}" compile "${config}"
done
