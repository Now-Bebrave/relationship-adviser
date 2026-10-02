import json
from pathlib import Path
import unittest


ROOT = Path(__file__).parents[1]


class AdapterTests(unittest.TestCase):
    def test_root_skill_entry_is_installable(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("name: relationship-adviser", skill)
        self.assertIn("core/mission.md", skill)
        self.assertIn("knowledge/playbooks/", skill)
        install = (ROOT / "docs" / "INSTALL.md").read_text(encoding="utf-8")
        self.assertIn("relationship-adviser", install)
        self.assertIn("git clone", install)

    def test_manifest_lists_all_targets(self) -> None:
        manifest = json.loads((ROOT / "adapters" / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(set(manifest["platforms"]), {"codex", "claude-code", "workbuddy"})

    def test_adapters_load_shared_core(self) -> None:
        for platform in ("codex", "claude-code", "workbuddy"):
            path = ROOT / "adapters" / platform / "SKILL.md"
            text = path.read_text(encoding="utf-8")
            self.assertIn("../../core/mission.md", text)
            self.assertIn("../../core/output.md", text)
            self.assertIn("read_profile", text)
            self.assertIn("search_knowledge", text)
            self.assertNotIn("1. 定义用户要达成的结果", text)
