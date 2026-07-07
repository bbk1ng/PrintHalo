from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "esphome" / "packages" / "custom_bambu_dashboard.yaml"
COMPILE_SCRIPT = ROOT / "scripts" / "compile-esphome.sh"


class DashboardSpecTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = PACKAGE.read_text()
        cls.compile_script = COMPILE_SCRIPT.read_text()

    def test_device_name_passed_via_terminal(self):
        # master YAML keeps name/friendly_name as substitutions...
        yaml = (ROOT / "esphome" / "round-amoled-466.yaml").read_text()
        self.assertRegex(yaml, re.compile(r"^substitutions:\n  name: ", re.MULTILINE))
        self.assertIn("name: ${name}", yaml)
        self.assertIn("friendly_name: ${friendly_name}", yaml)
        # ...and the compile script forwards terminal args as overrides
        self.assertIn('device_name="${1:-}"', self.compile_script)
        self.assertIn('friendly_name="${2:-}"', self.compile_script)
        self.assertIn('name_args+=(-s name "${device_name}")', self.compile_script)
        self.assertIn(
            'name_args+=(-s friendly_name "${friendly_name}")', self.compile_script
        )
        self.assertIn('"${name_args[@]}"', self.compile_script)

    def test_compile_gate_builds_amoled_board(self):
        self.assertIn('-s display_width "${width}"', self.compile_script)
        self.assertIn('compile "${config}"', self.compile_script)
        self.assertIn("pipx run esphome", self.compile_script)
        self.assertRegex(self.compile_script, r"-s display_width \"?\$\{width\}\"?")
        self.assertIn("round-amoled-466.yaml:466", self.compile_script)
        self.assertNotIn("round-gc9a01a-240.yaml", self.compile_script)

    def test_tap_only_two_page_navigation(self):
        self.assertIn("page_wrap: true", self.package)
        self.assertEqual(len(re.findall(r"^\s+- id: page_", self.package, re.MULTILINE)), 2)
        self.assertIn("id: page_status", self.package)
        self.assertIn("id: page_ams", self.package)
        self.assertGreaterEqual(self.package.count("scroll_dir: NONE"), 4)
        self.assertEqual(self.package.count("width: 40%"), 4)
        self.assertEqual(self.package.count("lvgl.page.previous"), 2)
        self.assertEqual(self.package.count("lvgl.page.next"), 2)

    def test_status_and_ams_entities_are_wired(self):
        for entity in (
            "_print_status",
            "_current_stage",
            "_print_progress",
            "_remaining_time",
            "_nozzle_temperature",
            "_bed_temperature",
            "_current_layer",
            "_total_layer_count",
            "_ams_humidity",
            "_ams_temperature",
        ):
            self.assertIn(entity, self.package)

        for slot in range(1, 5):
            self.assertIn(f"sensor.${{bambulab_printer}}_ams_tray_{slot}", self.package)
            self.assertIn(f"id: ams_tray_{slot}_color", self.package)
            self.assertRegex(
                self.package,
                re.compile(
                    rf"id: ams_tray_{slot}_color\n"
                    rf"\s+entity_id: sensor\.\$\{{bambulab_printer\}}_ams_tray_{slot}\n"
                    r"\s+attribute: color"
                ),
            )
        self.assertIn("r * 299 + g * 587 + b * 114", self.package)

    def test_dimming_is_multiplier_on_configured_brightness(self):
        self.assertIn("id: configured_brightness", self.package)
        self.assertIn("id: brightness_control", self.package)
        self.assertIn("level *= 0.50f", self.package)
        self.assertIn("id(display_dimmed) = should_dim", self.package)
        self.assertIn("id(print_active)", self.package)

    @staticmethod
    def visible_failed(raw_failed, stage_idleish, print_active, failed_latched):
        return raw_failed and (failed_latched or print_active or not stage_idleish)

    def test_failed_status_requires_active_or_latched_failure(self):
        raw_failed = (
            'ps.find("fail") != std::string::npos || '
            'ps.find("error") != std::string::npos'
        )
        display_failed = (
            "bool failed = raw_failed && "
            "(id(failed_print_latched) || id(print_active) || !stage_idleish);"
        )

        self.assertIn("id: failed_print_latched", self.package)
        self.assertIn(f"bool raw_failed = {raw_failed};", self.package)
        self.assertEqual(self.package.count(display_failed), 3)
        self.assertIn("bool failed = raw_failed && id(failed_print_latched);", self.package)
        self.assertIn(
            "if (raw_failed && (id(failed_print_latched) || id(print_active) || "
            "!stage_idleish)) id(failed_print_latched) = true;",
            self.package,
        )
        self.assertIn(
            "id(print_active) = !done && !raw_failed && print_present;",
            self.package,
        )

        self.assertFalse(self.visible_failed(True, True, False, False))
        self.assertTrue(self.visible_failed(True, True, True, False))
        self.assertTrue(self.visible_failed(True, True, False, True))
        self.assertTrue(self.visible_failed(True, False, False, False))
        self.assertFalse(self.visible_failed(False, False, True, True))

    def test_discrete_qmi8658_rotation(self):
        for register in ("0x35", "0x36", "0x37", "0x38", "0x39", "0x3A"):
            self.assertIn(register, self.package)
        self.assertIn("dominant < 2000", self.package)
        self.assertIn("millis() - pending_since >= 800", self.package)
        for rotation in ("0", "90", "180", "270"):
            self.assertIn(f"lvgl.display.set_rotation: {rotation}", self.package)
        self.assertNotIn("lv_obj_set_style_transform_angle", self.package)

    def test_shared_package_avoids_board_pixel_sizes(self):
        self.assertNotIn('screen_size: "240"', self.package)
        self.assertNotIn('screen_size: "466"', self.package)
        self.assertIn("width: ${ring_size}", self.package)
        self.assertIn("height: ${ring_size}", self.package)
        self.assertIn("width: 18%", self.package)
        self.assertIn("height: 27%", self.package)


if __name__ == "__main__":
    unittest.main()
