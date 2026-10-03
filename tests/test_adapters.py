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
        self.assertIn("/relationship-adviser", install)

    def test_manifest_lists_all_targets(self) -> None:
        manifest = json.loads((ROOT / "adapters" / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(set(manifest["platforms"]), {"codex", "claude-code", "workbuddy"})
        self.assertEqual(manifest["version"], "2.0.0")
        for capability in ("voice_input", "voice_output", "private_decision_log"):
            self.assertIn(capability, manifest["capabilities"])

    def test_adapters_load_shared_core(self) -> None:
        for platform in ("codex", "claude-code", "workbuddy"):
            path = ROOT / "adapters" / platform / "SKILL.md"
            text = path.read_text(encoding="utf-8")
            self.assertIn("../../core/mission.md", text)
            self.assertIn("../../core/output.md", text)
            self.assertIn("read_profile", text)
            self.assertIn("search_knowledge", text)
            self.assertNotIn("1. 定义用户要达成的结果", text)

    def test_workbuddy_registers_explicit_relationship_adviser_command(self) -> None:
        root_skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        mobile = (ROOT / "adapters" / "workbuddy" / "MOBILE_PROMPT.md").read_text(encoding="utf-8")
        self.assertIn("name: relationship-adviser", root_skill)
        self.assertIn("/relationship-adviser", mobile)
