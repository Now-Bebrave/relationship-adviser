from pathlib import Path
import unittest


ROOT = Path(__file__).parents[1]


class ProfilePolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profile = (ROOT / "private-vault" / "profile" / "profile.yaml.example").read_text(encoding="utf-8")
        cls.policy = (ROOT / "core" / "profile-policy.md").read_text(encoding="utf-8")

    def test_personal_objective_is_default(self) -> None:
        self.assertIn("default_priority: personal_objective", self.profile)

    def test_sensitive_memory_requires_explicit_save(self) -> None:
        self.assertIn("save_by_default: false", self.profile)
        self.assertIn("require_explicit_save_for_sensitive_events: true", self.profile)
        self.assertIn("明确要求", self.policy)

    def test_profile_sections_exist(self) -> None:
        for section in ("identity:", "goals:", "preferences:", "constraints:", "patterns:", "memory_rules:"):
            self.assertIn(section, self.profile)
