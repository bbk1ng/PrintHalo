# Project Instructions

Instructions for Claude Code (and other agents) working in this repo. Keep this
file current — it is loaded into context every session.

## What this is

PrintHalo (formerly `dashboard-esp32`) — a round Home Assistant dashboard for Bambu Lab
3D printers. Targets a 466×466 MIPI-SPI AMOLED (CO5300, quad-SPI) on an ESP32-S3 (octal
PSRAM, 80 MHz), with FT63x6 capacitive touch and a QMI8658 IMU for auto-rotation. Pulls
live print state over Home Assistant (via the
[Bambu Lab integration](https://github.com/greghesp/ha-bambulab)) and renders a
full-bleed progress ring plus temps, layer count, ETA, and AMS filament colours. Shipped
as an ESPHome remote package — device entry point is `esphome/round-amoled-466.yaml`;
consumers add a small per-device YAML in their own HA config (see README.md).

### ESPHome builds

- Compile: `scripts/compile-esphome.sh [device-name] [friendly-name]` — wraps
  `esphome ... compile esphome/round-amoled-466.yaml` (falls back to `pipx run esphome`
  if `esphome` isn't installed). Omit args to use the YAML's default substitutions.
- **Run builds on tmpfs, never on this NFS share** — NFS builds intermittently drop
  `lvgl.h` and fail partway through. Work from local/tmpfs storage (or a git worktree
  on local disk) when compiling.
- Hardware notes: production pucks are 1.43" CO5300 AMOLED units at `.155` / `.165`; no
  onboard audio; P2S print-control is blocked by Bambu's signed-MQTT requirement.

## Workflow

This repo follows [WORKFLOW-ORCHESTRATION.md](WORKFLOW-ORCHESTRATION.md):

1. **Plan first** — for any non-trivial task (3+ steps), write the plan to
   `tasks/todo.md` with checkable items before touching code.
2. **One concern per change** — small, reviewable diffs.
3. **Verify before done** — run `python3 -m unittest discover -s tests`; never mark a
   task complete without a passing test.
4. **Capture lessons** — after any correction, add a rule to `tasks/lessons.md`.

## Conventions

- Tests are stdlib `unittest` — no test framework dependency. Run:
  `python3 -m unittest discover -s tests`.
- Source lives in `src/`, tests mirror it in `tests/`.
- Orchestrated changes go through `orch task "<change>"`; config in `.orch/orch.yml`.

## Guardrails

- Make the smallest change that solves the problem. Find root causes, no
  temporary patches.
- Don't add a dependency for what a few lines of stdlib can do.
- Confirm before destructive or irreversible actions.

<!-- orch:begin (managed by `orch init --link`; edits here are overwritten) -->
## orch
This repo uses agent-orch. See `.orch/ORCH.md` for usage; config in `.orch/orch.yml`.
@.orch/ORCH.md
<!-- orch:end -->
