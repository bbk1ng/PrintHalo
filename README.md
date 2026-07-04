# dashboard-esp32

An [ESPHome](https://esphome.io) dashboard for **Bambu Lab 3D printers**, built
for a round 466 × 466 AMOLED display on an ESP32-S3 board. It pulls live print
data from Home Assistant and shows progress, temperatures, layer counts, AMS tray
colours, and remaining time on a compact touch screen.

## Hardware

| Component | Detail |
|-----------|--------|
| MCU | ESP32-S3 (octal PSRAM, 80 MHz) |
| Display | 466 × 466 MIPI-SPI AMOLED (CO5300), quad-SPI |
| Touch | FT63x6 capacitive touch controller (I²C) |
| IMU | QMI8658 (I²C, used for auto-rotation) |

## Layout

```
.
├── esphome/
│   ├── round-amoled-466.yaml          # top-level ESPHome config for the 466 mm board
│   ├── packages/
│   │   └── custom_bambu_dashboard.yaml  # LVGL UI, sensors, AMS colour logic
│   ├── fonts/
│   │   └── materialdesignicons-webfont.ttf
│   └── images/
│       └── bambuicon.png
├── scripts/
│   └── compile-esphome.sh             # build helper (supports multi-device overrides)
├── tasks/                             # active plan & captured lessons
└── docs/                              # design notes
```

## Prerequisites

- [ESPHome](https://esphome.io/guides/installing_esphome) ≥ 2025.9.0
- Home Assistant with the [Bambu Lab integration](https://github.com/greghesp/ha-bambulab)
  installed and your printer configured

## Quick start

1. **Set your printer entity prefix** — open `esphome/round-amoled-466.yaml` and
   replace `YOUR_PRINTER_ENTITY` in the `substitutions` block with your printer's
   entity prefix (e.g. `p1s_00m00a000000`).

2. **Compile and flash**

   ```bash
   # Uses esphome on PATH, or falls back to pipx run esphome
   scripts/compile-esphome.sh

   # Flash a specific device (overrides name/friendly_name substitutions):
   scripts/compile-esphome.sh bambu-kitchen "Kitchen Bambu Dashboard"
   ```

3. **Connect to Wi-Fi** — on first boot the device creates a captive-portal AP
   (`Bambu Round Dashboard 466`). Connect and enter your Wi-Fi credentials.

4. **Add to Home Assistant** — the ESPHome integration will auto-discover the device.

## Screens

The LVGL UI contains multiple swipe-able pages:

- **Status** — progress arc, nozzle/bed temperatures, current layer, remaining time
- **AMS** — four filament slots with material name and swatch colour from the printer

Swipe left/right (or tap the left/right halves of the screen) to switch pages.
Brightness is adjustable via a Home Assistant number entity exposed by the device.

## Conventions

- **Plan first** — non-trivial work starts in `tasks/todo.md`.
- **Verify before done** — never mark complete without a passing test.
- **Capture lessons** — after any correction, add a rule to `tasks/lessons.md`.

See [WORKFLOW-ORCHESTRATION.md](WORKFLOW-ORCHESTRATION.md) for the agent workflow.
