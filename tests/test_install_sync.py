import unittest
from pathlib import Path

from tools.check_install_sync import compare, public_hashes


ROOT = Path(__file__).parents[1]


class InstallSyncTests(unittest.TestCase):
    def test_public_hashes_exclude_private_and_runtime_files(self) -> None:
        hashes = public_hashes(ROOT)
        self.assertIn("SKILL.md", hashes)
        self.assertIn("private-vault/README.md", hashes)
        self.assertFalse(any(path.startswith("private-vault/") and path != "private-vault/README.md" for path in hashes))
        self.assertFalse(any("__pycache__" in path or path.startswith(".test-tmp/") for path in hashes))

    def test_repository_matches_itself(self) -> None:
        self.assertEqual(compare(ROOT, [ROOT]), [])


if __name__ == "__main__":
    unittest.main()

