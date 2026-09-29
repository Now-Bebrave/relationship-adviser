from pathlib import Path
import subprocess
import unittest


class RepositoryBoundaryTests(unittest.TestCase):
    def test_private_vault_is_ignored(self) -> None:
        private_file = Path("private-vault/.ignore-probe")
        result = subprocess.run(
            ["git", "check-ignore", "--no-index", str(private_file)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0)

    def test_public_example_directory_is_not_ignored(self) -> None:
        result = subprocess.run(
            ["git", "check-ignore", "--no-index", "examples/example.md"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
