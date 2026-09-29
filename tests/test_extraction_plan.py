import unittest

from tools.extraction_plan import choose_extraction_mode


class ExtractionPlanTests(unittest.TestCase):
    def test_complete_notes_use_notes_only(self) -> None:
        self.assertEqual(choose_extraction_mode(True, True, False, False), "notes_only")

    def test_notes_and_images_use_notes_plus_images(self) -> None:
        self.assertEqual(choose_extraction_mode(True, True, True, False), "notes_plus_images")

    def test_incomplete_or_conflicting_notes_use_spot_check(self) -> None:
        self.assertEqual(choose_extraction_mode(True, False, False, False), "notes_plus_spotcheck")
        self.assertEqual(choose_extraction_mode(True, True, False, True), "notes_plus_spotcheck")

    def test_no_notes_uses_full_video(self) -> None:
        self.assertEqual(choose_extraction_mode(False, False, False, False), "full_video")
