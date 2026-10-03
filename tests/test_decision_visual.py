import json
import unittest
from pathlib import Path

from tools.render_decision_visual import render_svg


ROOT = Path(__file__).parents[1]


class DecisionVisualTests(unittest.TestCase):
    def test_timeline_fixture_renders_accessible_mobile_svg(self) -> None:
        data = json.loads((ROOT / "examples" / "visuals" / "migration-90-day-card.json").read_text(encoding="utf-8"))
        svg = render_svg(data)
        self.assertIn('width="1080"', svg)
        self.assertIn("<title>", svg)
        self.assertIn("<desc>", svg)
        self.assertIn("76–90 天", svg)
        self.assertIn("下一步", svg)

    def test_all_five_visual_types_are_supported(self) -> None:
        base = {"title": "测试", "conclusion": "先核验", "items": [{"label": "条件", "value": "行动", "level": "high"}], "next_step": "复核", "alt_text": "测试图"}
        for kind in ("timeline", "risk", "responsibility", "cost", "decision"):
            svg = render_svg({**base, "type": kind})
            self.assertIn("<svg", svg, kind)
        self.assertIn("HIGH", render_svg({**base, "type": "risk"}))

    def test_svg_escapes_user_content(self) -> None:
        data = {"type": "decision", "title": "<script>", "conclusion": "a & b", "items": [{"label": "<x>", "value": "ok"}], "next_step": "复核", "alt_text": "alt"}
        svg = render_svg(data)
        self.assertNotIn("<script>", svg)
        self.assertIn("&lt;script&gt;", svg)
        self.assertIn("a &amp; b", svg)

    def test_missing_required_field_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            render_svg({"type": "timeline"})


if __name__ == "__main__":
    unittest.main()

