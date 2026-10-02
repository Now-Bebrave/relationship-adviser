from pathlib import Path
import unittest

from tools.index_media import index_media


class MediaIndexTests(unittest.TestCase):
    def test_index_contains_path_size_hash_and_type(self) -> None:
        root = Path(__file__).parent / "fixtures" / "media"

        records = index_media(root)

        self.assertEqual(len(records), 2)
        types = {record["media_type"] for record in records}
        self.assertEqual(types, {"video/mp4", "audio/wav"})
        self.assertTrue(all(len(record["sha256"]) == 64 for record in records))
