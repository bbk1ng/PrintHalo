# PrintHalo

![PrintHalo — a round Home Assistant dashboard for Bambu Lab printers](docs/assets/printhalo-banner.png)

A round-display **Home Assistant dashboard for Bambu Lab 3D printers**, built for a
466 × 466 AMOLED on an ESP32-S3. The full-bleed progress ring — the *halo* — tells you
the state of a print from across the room: green while printing, blue when it's done,
grey when idle. It pulls live data over Home Assistant and shows progress, temperatures,
layer counts, remaining time, and AMS filament colours on a desk-sized dial.

> Formerly `dashboard-esp32`. Community project — not affiliated with or endorsed by Bambu Lab.

> Built with [agent-orch](https://github.com/bbk1ng/agent-orch) — multi-agent author/audit/test-gate pipeline.

## Screens

| Status | AMS |
|:------:|:---:|
| ![Status screen](docs/assets/screen-status.png) | ![AMS screen](docs/assets/screen-ams.png) |
| Progress ring, nozzle / bed temps, current layer, elapsed / ETA | Four filament slots with material name and swatch colour from the printer |

Swipe left/right — or tap the left/right half of the glass — to switch pages. The screen
auto-rotates in 90° steps and keeps text upright, and dims to 50% five minutes after a
print finishes.

## The ring at a glance

One colour tells you the state of a print from across the room:

| ![Idle](docs/assets/state-idle.png) | ![Preheat](docs/assets/state-preheat.png) | ![Levelling](docs/assets/state-leveling.png) | ![Printing](docs/assets/state-printing.png) |
|:---:|:---:|:---:|:---:|
| **Idle** — ready, grey | **Preheat** — warming up, orange | **Levelling** — bed mesh, purple | **Printing** — live progress, green |

| ![Paused](docs/assets/state-paused.png) | ![Finished](docs/assets/state-finished.png) | ![Error](docs/assets/state-error.gif) | |
|:---:|:---:|:---:|:---:|
| **Paused** — on hold, amber | **Finished** — complete, blue | **Error** — needs attention | |

*(Full overview: [state-tiles.png](docs/assets/state-tiles.png))*

## Hardware

| Component | Detail |
|-----------|--------|
| MCU | ESP32-S3 (octal PSRAM, 80 MHz) |
| Display | 466 × 466 MIPI-SPI AMOLED (CO5300), quad-SPI |
| Touch | FT63x6 capacitive touch controller (I²C) |
| IMU | QMI8658 (I²C, used for auto-rotation) |

## Prerequisites

- [ESPHome](https://esphome.io/guides/installing_esphome) ≥ 2025.9.0
- Home Assistant with the [Bambu Lab integration](https://github.com/greghesp/ha-bambulab)
  installed and your printer configured

## Quick start — Home Assistant ESPHome add-on (recommended)

No clone needed. The device config is pulled straight from this repo as an
[ESPHome remote package](https://esphome.io/components/packages.html#remote-git-packages);
only a small per-device YAML lives in your Home Assistant config.

1. **Add your secrets** — in the ESPHome dashboard open `secrets.yaml` (or edit
   `/config/esphome/secrets.yaml`) and make sure it contains:

   ```yaml
   wifi_ssid: "YourWifi"
   wifi_password: "YourPassword"
   # Your printer's entity prefix from the Bambu Lab integration,
   # e.g. p1s_00m00a000000 (Settings > Devices & Services > Bambu Lab)
   bambulab_printer: YOUR_PRINTER_ENTITY
   ```

   The repo's own `esphome/secrets.yaml` is gitignored, so `!secret` references in the
   remote package resolve against your local file.

2. **Create a device file** — e.g. `/config/esphome/printhalo.yaml`:

   ```yaml
   substitutions:
     name: printhalo
     friendly_name: PrintHalo
     # per-device overrides go here, e.g. brightness_default: "70"

   packages:
     printhalo:
       url: https://github.com/bbk1ng/PrintHalo
       ref: main
       files: [esphome/round-amoled-466.yaml]
       refresh: 1d

   wifi:
     ssid: !secret wifi_ssid
     password: !secret wifi_password
   ```

   `refresh: 1d` re-pulls this repo daily; use *Clean Build Files* in the ESPHome
   dashboard to force an update.

3. **Multiple devices** — one file per device from the same package. Give each a unique
   `name`/`friendly_name` substitution, and optionally pin its IP for OTA:

   ```yaml
   substitutions:
     name: printhalo-kitchen
     friendly_name: PrintHalo Kitchen

   wifi:
     ssid: !secret wifi_ssid
     password: !secret wifi_password
     use_address: 192.168.1.155
   ```

4. **Install** — first time over USB from the ESPHome dashboard, OTA afterwards. The
   ESPHome integration auto-discovers the device in Home Assistant.

Brightness is adjustable via a Home Assistant number entity exposed by the device.

## Quick start — standalone CLI

1. **Set your printer entity prefix** — copy `esphome/secrets.yaml.example` to
   `esphome/secrets.yaml` (gitignored, so it survives `git pull` and isn't published) and
   replace `YOUR_PRINTER_ENTITY` with your printer's entity prefix (e.g. `p1s_00m00a000000`).

   ```bash
   cp esphome/secrets.yaml.example esphome/secrets.yaml
   ```

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

## Credits / prior art

PrintHalo's two screens are adapted from other open-source projects, not built from scratch:

- **Status screen** — layout adapted from [PrintSphere](https://github.com/cptkirki/PrintSphere)
  (Cpt_Kirk, FNCL non-commercial license).
- **AMS screen** — adapted from [TurboTime29/bambu-esp32s3-ha-round-dash](https://github.com/TurboTime29/bambu-esp32s3-ha-round-dash)
  (MIT), scaled from its original 240 × 240 board to 466 × 466.

See [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md) for full license terms.

## License

MIT — see [LICENSE](LICENSE). Bundled third-party assets (MDI font, Bambu icon) and adapted
UI/code from other projects keep their own terms — see [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md).
