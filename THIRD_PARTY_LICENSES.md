# Third-party assets and prior art

This repo bundles a few binary assets, and adapts UI/code from two other
open-source dashboards, none of which are covered by this project's own
[LICENSE](LICENSE) (MIT). They keep their own upstream licenses/terms.

## Prior art — adapted screens

### Screen 1 (status/progress layout) — adapted from PrintSphere

- **Source**: [PrintSphere](https://github.com/cptkirki/PrintSphere) by Cpt_Kirk.
- **License**: [Federation Non-Commercial License (FNCL) v1.1](https://github.com/cptkirki/PrintSphere/blob/main/LICENSE)
  — non-commercial use only, share-alike attribution required.
- PrintSphere is a native ESP-IDF/LVGL C++ project; nothing here is a code
  copy (this repo is ESPHome YAML), but the screen 1 arc/status layout and
  visual arrangement is closely adapted from PrintSphere's UI. Per FNCL §3,
  this is disclosed as a modified adaptation. Changes from the original:
  - screen rotates on touch, not swipe
  - auto-rotate in 90° increments, text always stays upright/readable
  - screen dims 50% when no print is active
  - reworked ETA and elapsed-time presentation

### Screen 2 (AMS spool page) — adapted from bambu-esp32s3-ha-round-dash

- **Source**: [TurboTime29/bambu-esp32s3-ha-round-dash](https://github.com/TurboTime29/bambu-esp32s3-ha-round-dash).
- **License**: MIT, Copyright (c) 2026 TurboTime29.
- The AMS tray/spool page (entity ids, color-attribute lambda pattern) is
  adapted directly from this project's ESPHome YAML, scaled from its
  original 240×240 board to this repo's 466×466 display.

## `esphome/fonts/materialdesignicons-webfont.ttf`

- **Source**: [Material Design Icons](https://pictogrammers.com/library/mdi/)
  (Pictogrammers).
- **License**: [SIL Open Font License 1.1](https://openfontlicense.org/) —
  free to use, embed, and redistribute, including in this repo's compiled
  firmware.

## `esphome/images/bambuicon.png`

- Small icon referencing the Bambu Lab brand, used only to visually identify
  the Bambu Lab print-status screen in this personal, non-commercial project.
- "Bambu Lab" and its logos are trademarks of Shanghai Lunkuo Technology Co.,
  Ltd. This project is **not affiliated with or endorsed by Bambu Lab**. If
  you redistribute or fork this project commercially, replace this icon with
  your own artwork.
