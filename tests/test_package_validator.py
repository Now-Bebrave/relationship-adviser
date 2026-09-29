from pathlib import Path
import unittest

from tools.validate_package import REQUIRED_PATHS, validate


ROOT = Path(__file__).parents[1]


class PackageValidatorTests(unittest.TestCase):
    def test_verified_knowledge_indexes_are_required(self) -> None:
        expected = {
            "knowledge/verified-sources.md",
            "knowledge/books/verified-catalog.md",
            "knowledge/legal/2024-bride-price-judicial-interpretation.md",
            "knowledge/legal/bride-price-negotiation-and-evidence-checklist.md",
            "knowledge/legal/civil-code-marriage-family.md",
            "knowledge/legal/anti-domestic-violence-law.md",
        }
        self.assertTrue(expected.issubset(REQUIRED_PATHS))

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
