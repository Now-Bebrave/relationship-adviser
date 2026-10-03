import unittest
from pathlib import Path

from tools.decision_calculator import calculate


ROOT = Path(__file__).parents[1]


class DecisionTemplateTests(unittest.TestCase):
    def test_index_declares_seven_templates(self) -> None:
        text = (ROOT / "knowledge" / "templates" / "index.yaml").read_text(encoding="utf-8")
        self.assertEqual(text.count("- id:"), 7)
        self.assertIn("exit_safety", text)

    def test_templates_have_actionable_fields(self) -> None:
        paths = list((ROOT / "knowledge" / "templates").glob("*.md"))
        self.assertEqual(len(paths), 8)
        for path in paths:
            text = path.read_text(encoding="utf-8")
            self.assertTrue("复核" in text or "Stop conditions" in text, path.name)

    def test_calculator_returns_commitment_ratio_and_stress(self) -> None:
        result = calculate({"monthly_income": 10000, "essential_expenses": 4000, "debt_payments": 1000, "new_debt_payment": 1000, "emergency_fund": 36000, "parent_support": 500})
        self.assertEqual(result["monthly_commitments"], 6000)
        self.assertEqual(result["remaining_after_commitments"], 4000)
        self.assertEqual(result["commitment_ratio"], 0.6)
        self.assertIn("income_minus_30_percent", result["stress"])

    def test_calculator_handles_zero_income(self) -> None:
        result = calculate({"monthly_income": 0})
        self.assertIsNone(result["commitment_ratio"])


if __name__ == "__main__":
    unittest.main()
