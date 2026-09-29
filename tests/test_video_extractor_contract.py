from pathlib import Path
import unittest

from tools.video_extractors import get_extractor


class FakeExtractor:
    def extract(self, path: Path) -> dict:
        return {"transcript": [], "ocr": []}


class VideoExtractorContractTests(unittest.TestCase):
    def test_fake_provider_shape(self) -> None:
        result = FakeExtractor().extract(Path("video.mp4"))
        self.assertEqual(set(result), {"transcript", "ocr"})

    def test_default_provider_fails_explicitly(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "No local ASR/OCR provider"):
            get_extractor().extract(Path("video.mp4"))
