import pathlib
import unittest

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent


class TestLicensing(unittest.TestCase):
    def test_license_file_present(self):
        license_path = REPO_ROOT / "LICENSE"
        self.assertTrue(license_path.is_file())
        self.assertIn("MIT License", license_path.read_text())

    def test_third_party_licenses_documented(self):
        notice_path = REPO_ROOT / "THIRD_PARTY_LICENSES.md"
        self.assertTrue(notice_path.is_file())
        text = notice_path.read_text()
        self.assertIn("materialdesignicons-webfont.ttf", text)
        self.assertIn("bambuicon.png", text)
        self.assertIn("PrintSphere", text)
        self.assertIn("TurboTime29", text)


if __name__ == "__main__":
    unittest.main()
