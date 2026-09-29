from pathlib import Path
import unittest

from tools.normalize_video_notes import normalize_notes


ROOT = Path(__file__).parents[1]


class NormalizeVideoNotesTests(unittest.TestCase):
    def test_markdown_sections_become_video_card_fields(self) -> None:
        card = normalize_notes(ROOT / "tests/fixtures/video-notes/sample-notes.md", {"extraction_mode": "notes_only"})
        self.assertEqual(card["extraction_mode"], "notes_only")
        self.assertEqual(card["claims"][0]["claim"], "先确认双方目标，再讨论金额。")
        self.assertEqual(card["transcript"][0]["start"], "00:01:12")
        self.assertEqual(card["playbook"]["expected_reactions"], ["对方可能要求当场报数。"])

    def test_unsupported_mode_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            normalize_notes(ROOT / "tests/fixtures/video-notes/sample-notes.md", {"extraction_mode": "full_video"})
