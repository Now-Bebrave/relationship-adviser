from pathlib import Path
import unittest

from tools.index_media import index_media


class MediaIndexTests(unittest.TestCase):
    def test_index_contains_path_size_hash_and_type(self) -> None:
        root = Path(r"D:\WorkFiles\mediaCrawler\MediaCrawler\data\dy\media\7690246010651675913")
        records = index_media(root)
        self.assertGreaterEqual(len(records), 2)
        types = {record["media_type"] for record in records}
        self.assertIn("video/mp4", types)
        self.assertIn("audio/wav", types)
        self.assertTrue(all(len(record["sha256"]) == 64 for record in records))
