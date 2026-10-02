from pathlib import Path
import unittest

from tools.visual_output import (
    build_illustration_request,
    render_text_fallback,
    should_render_visual,
)


class VisualOutputTests(unittest.TestCase):
    def test_visual_trigger_and_request_are_platform_independent(self) -> None:
        self.assertTrue(should_render_visual(branches=3, timepoints=1, options=1, abstract=False))
        request = build_illustration_request(
            purpose="解释婚前决策分流",
            alt_text="婚前决策从核验到推进或退出的流程图",
            source="knowledge/playbooks/premarital-30-day-integrated-audit.md",
            prompt="用中性、清晰的流程图表现婚前核验分支",
            fallback="先核验事实，再决定推进、延后、改方案或退出。",
        )
        self.assertEqual(request["purpose"], "解释婚前决策分流")
        self.assertIn("fallback", request)

    def test_text_fallback_preserves_all_branches(self) -> None:
        fallback = render_text_fallback(
            "婚前决策分流",
            [("事实已核验", "进入协议"), ("信息缺口", "延后决定"), ("安全风险", "进入安全路径")],
        )
        for marker in ("事实已核验", "信息缺口", "安全风险", "进入安全路径"):
            self.assertIn(marker, fallback)

    def test_visual_request_rejects_missing_accessibility_fields(self) -> None:
        with self.assertRaises(ValueError):
            build_illustration_request("", "", "", "", "")

