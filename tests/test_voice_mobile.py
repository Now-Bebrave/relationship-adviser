import json
import unittest
from pathlib import Path

from tools.decision_log import sanitize_record
from tools.private_sync_manifest import build_manifest
from tools.voice_bridge import build_tts_request, build_voice_request


ROOT = Path(__file__).parents[1]


class VoiceMobileTests(unittest.TestCase):
    def test_voice_request_flags_amount_negation_and_low_confidence(self) -> None:
        result = build_voice_request({"transcript": "我没有同意借 20 万，而且对方威胁我", "language": "zh-CN", "confidence": 0.8})
        self.assertTrue(result["needs_confirmation"])
        self.assertIn("20 万", result["review_tokens"])
        self.assertIn("没有", result["review_tokens"])
        self.assertFalse(result["save_to_profile"])

    def test_tts_request_has_text_fallback(self) -> None:
        result = build_tts_request({"spoken_text": "先核对事实，再决定。"})
        self.assertEqual(result["provider"], "platform_or_local")
        self.assertEqual(result["fallback"], "display_text")

    def test_private_decision_record_uses_allowlist(self) -> None:
        result = sanitize_record({"question": "是否迁移", "recommendation": "先试住", "steps": ["核验工作"], "private_chat": "不得保存"})
        self.assertNotIn("private_chat", result)
        self.assertIn("saved_at", result)

    def test_sync_manifest_contains_hashes_not_content(self) -> None:
        test_root = ROOT / ".test-tmp" / "private-sync"
        test_root.mkdir(parents=True, exist_ok=True)
        sample = test_root / "record.txt"
        sample.write_text("private value", encoding="utf-8")
        try:
            manifest = build_manifest(test_root, test_root / "manifest.json")
        finally:
            sample.unlink(missing_ok=True)
            (test_root / "manifest.json").unlink(missing_ok=True)
        encoded = json.dumps(manifest)
        self.assertFalse(manifest["content_included"])
        self.assertNotIn("private value", encoded)
        self.assertEqual(len(manifest["files"][0]["sha256"]), 64)

    def test_workbuddy_mobile_prompt_preserves_safety_and_save_consent(self) -> None:
        text = (ROOT / "adapters" / "workbuddy" / "MOBILE_PROMPT.md").read_text(encoding="utf-8")
        for marker in ("金额", "停止条件", "语音回答", "保存这次决策"):
            self.assertIn(marker, text)


if __name__ == "__main__":
    unittest.main()

