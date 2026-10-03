import json
import unittest
from pathlib import Path

from tools.evaluate_advice import score_answer


ROOT = Path(__file__).parents[1]


class AdviceEvaluatorTests(unittest.TestCase):
    def test_reference_answers_pass_their_declared_gate(self) -> None:
        cases = json.loads((ROOT / "tests" / "fixtures" / "reference_answers.json").read_text(encoding="utf-8"))
        self.assertEqual(len(cases), 2)
        for case in cases:
            result = score_answer(case["answer"], safety=case["safety"])
            self.assertTrue(result["passed"], case["id"])

    def test_missing_safety_fails_even_with_high_general_score(self) -> None:
        text = "结论 建议。事实 推断 未知。步骤 第一方 时间。话术 可以说。反应 对方可能。停止条件 暂停。备选方案 替代。现实变量 收入住房家庭债务健康。证据 群体不能据此。"
        result = score_answer(text, safety=True)
        self.assertFalse(result["passed"])
        self.assertFalse(result["dimensions"]["安全"])

    def test_short_vague_answer_does_not_pass(self) -> None:
        result = score_answer("看情况，建议沟通。")
        self.assertFalse(result["passed"])


if __name__ == "__main__":
    unittest.main()
