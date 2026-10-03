from pathlib import Path
import re
import unittest


ROOT = Path(__file__).parents[1]


class PublicCaseTests(unittest.TestCase):
    def test_v14_case_index_has_ten_deidentified_training_cases(self) -> None:
        index = (ROOT / "knowledge" / "cases" / "index.yaml").read_text(encoding="utf-8")
        self.assertEqual(index.count("- id: case-"), 10)
        self.assertEqual(index.count("kind: synthetic_training_template"), 10)
        self.assertIn("privacy_rule:", index)

    def test_case_cards_have_required_sections_and_no_absolute_paths(self) -> None:
        cards = sorted((ROOT / "knowledge" / "cases").glob("case-*.md"))
        self.assertEqual(len(cards), 10)
        absolute = re.compile(r"(?:[A-Za-z]:[\\/]|/Users/|/home/)")
        for path in cards:
            text = path.read_text(encoding="utf-8")
            for marker in ("case_id", "source", "evidence_level", "privacy", "## Context", "## Facts and unknowns", "## Decision rule and actions", "## Likely reactions and responses", "## Result and limits", "## Stop conditions"):
                self.assertIn(marker, text, path.name)
            self.assertNotRegex(text, absolute)
            self.assertIn("synthetic_training_template", text)

    def test_public_case_readme_explains_l3_limits(self) -> None:
        text = (ROOT / "knowledge" / "cases" / "README.md").read_text(encoding="utf-8")
        for marker in ("去标识化", "训练模板", "不能替代研究证据", "private-vault"):
            self.assertIn(marker, text)


if __name__ == "__main__":
    unittest.main()
