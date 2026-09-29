from pathlib import Path
import unittest


ROOT = Path(__file__).parents[1]


class VisualRuleTests(unittest.TestCase):
    def test_mermaid_and_text_fallback_match_branches(self) -> None:
        diagram = (ROOT / "examples/visuals/reaction-branch.mmd").read_text(encoding="utf-8")
        fallback = (ROOT / "examples/visuals/reaction-branch.md").read_text(encoding="utf-8")
        for branch in ("接受", "模糊或拖延", "拒绝或施压"):
            self.assertIn(branch, diagram)
            self.assertIn(branch, fallback)

    def test_rules_require_text_fallback(self) -> None:
        rules = (ROOT / "visuals/diagram-rules.md").read_text(encoding="utf-8")
        self.assertIn("text summary", rules)
