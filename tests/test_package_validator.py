from pathlib import Path
import unittest

from tools.validate_package import validate


ROOT = Path(__file__).parents[1]


class PackageValidatorTests(unittest.TestCase):
    def test_current_package_is_valid(self) -> None:
        self.assertEqual(validate(ROOT), [])

    def test_validator_detects_missing_core_file(self) -> None:
        missing = ROOT / "core" / "output.md"
        content = missing.read_text(encoding="utf-8")
        missing.unlink()
        try:
            errors = validate(ROOT)
            self.assertIn("missing required path: core/output.md", errors)
        finally:
            missing.write_text(content, encoding="utf-8")
