from pathlib import Path
import unittest

from tools.check_integration import check_integration


ROOT = Path(__file__).parents[1]


class IntegrationTests(unittest.TestCase):
    def test_package_integration(self) -> None:
        self.assertEqual(check_integration(ROOT), [])
