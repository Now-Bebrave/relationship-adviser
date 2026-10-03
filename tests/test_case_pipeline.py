import unittest
from pathlib import Path

from tools.case_pipeline import build_draft, classify_line, fingerprint, privacy_flags


class CasePipelineTests(unittest.TestCase):
    def test_classifies_explicit_fact_claim_inference_and_unknown(self) -> None:
        self.assertEqual(classify_line("[事实] 已支付定金")["kind"], "fact")
        self.assertEqual(classify_line("观点：应该立即结婚")["kind"], "claim")
        self.assertEqual(classify_line("推测：对方可能会反悔")["kind"], "inference")
        self.assertEqual(classify_line("未知：付款用途")["kind"], "unknown")

    def test_privacy_flags_detect_path_phone_and_email(self) -> None:
        flags = privacy_flags(r"D:\private\video.mp4 13800138000 test@example.com")
        self.assertEqual(set(flags), {"absolute_path", "phone_number", "email"})

    def test_build_draft_routes_sensitive_content_to_private_review(self) -> None:
        source = Path(__file__).parents[1] / ".test-tmp" / "case-pipeline-note.txt"
        source.parent.mkdir(exist_ok=True)
        source.write_text("[事实] D:\\private\\clip.mp4\n[观点] 先沟通", encoding="utf-8")
        try:
            draft = build_draft(source, {"platform": "douyin", "topic": "婚姻"})
        finally:
            source.unlink(missing_ok=True)
        self.assertEqual(draft["routing"], "private_review")
        self.assertTrue(draft["review_required"])
        self.assertEqual(draft["content"][0]["kind"], "fact")

    def test_fingerprint_is_stable_for_whitespace(self) -> None:
        self.assertEqual(fingerprint("a  b"), fingerprint("a\nb"))


if __name__ == "__main__":
    unittest.main()
