from pathlib import Path
import unittest


ROOT = Path(__file__).parents[1]


class AdviceQualityFixtureTests(unittest.TestCase):
    def test_fixture_cases_have_routing_and_quality_requirements(self) -> None:
        text = (ROOT / "tests" / "fixtures" / "advice_cases.yaml").read_text(encoding="utf-8")
        self.assertGreaterEqual(text.count("- id:"), 5)
        for marker in ("topic:", "prompt:", "required:", "safety:"):
            self.assertIn(marker, text)

    def test_topic_router_has_safety_first_rule_and_core_topics(self) -> None:
        text = (ROOT / "core" / "topic-router.md").read_text(encoding="utf-8")
        for marker in ("彩礼与婚房", "父母介入", "迁移与照护", "性与健康", "经济控制", "安全指南优先"):
            self.assertIn(marker, text)

    def test_case_workflow_blocks_private_data_from_public_cases(self) -> None:
        text = (ROOT / "docs" / "case-ingestion-workflow.md").read_text(encoding="utf-8")
        for marker in ("去标识化", "private-vault/cases/", "不进入 Git 提交", "已有图文笔记"):
            self.assertIn(marker, text)

    def test_evaluation_rubric_has_ten_dimensions_and_safety_gate(self) -> None:
        text = (ROOT / "docs" / "evaluation-rubric.md").read_text(encoding="utf-8")
        for marker in ("结论", "事实边界", "步骤", "话术", "反应", "停止条件", "备选方案", "现实变量", "安全", "证据边界", "8/10"):
            self.assertIn(marker, text)


if __name__ == "__main__":
    unittest.main()
