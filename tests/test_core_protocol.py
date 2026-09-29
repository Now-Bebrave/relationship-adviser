from pathlib import Path
import re
import unittest


ROOT = Path(__file__).parents[1]


class CoreProtocolTests(unittest.TestCase):
    def test_mission_links_all_core_documents(self) -> None:
        mission = (ROOT / "core" / "mission.md").read_text(encoding="utf-8")
        for name in ("intake", "reasoning", "evidence", "communication", "domains", "output"):
            self.assertIn(f"({name}.md)", mission)
            self.assertTrue((ROOT / "core" / f"{name}.md").exists())

    def test_output_contains_required_sections(self) -> None:
        output = (ROOT / "core" / "output.md").read_text(encoding="utf-8")
        labels = (
            "结论", "判断依据", "详细执行步骤", "对方可能反应",
            "对应回答和下一步", "停止条件", "备选方案", "信心与信息缺口",
        )
        for label in labels:
            self.assertRegex(output, re.escape(label))
