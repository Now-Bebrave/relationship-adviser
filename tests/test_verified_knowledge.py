from pathlib import Path
import re
import unittest


ROOT = Path(__file__).parents[1]


class VerifiedKnowledgeTests(unittest.TestCase):
    def test_verified_notes_have_unique_doi_and_status(self) -> None:
        dois: list[str] = []
        for path in (ROOT / "knowledge" / "notes").glob("*.md"):
            text = path.read_text(encoding="utf-8")
            match = re.search(r'^doi: "([^"]+)"', text, re.MULTILINE)
            self.assertIsNotNone(match, path.name)
            dois.append(match.group(1).lower())
            self.assertRegex(text, r"verification_status: (?:metadata_verified|abstract_reviewed|full_text_reviewed)")
            self.assertIn("retrieved_at:", text)
        self.assertEqual(len(dois), len(set(dois)))

    def test_playbooks_name_evidence_and_stop_conditions(self) -> None:
        for path in (ROOT / "knowledge" / "playbooks").glob("*.md"):
            text = path.read_text(encoding="utf-8")
            self.assertIn("DOI", text)
            self.assertRegex(text.lower(), r"stop")

    def test_bride_price_checklist_is_actionable(self) -> None:
        path = ROOT / "knowledge" / "legal" / "bride-price-negotiation-and-evidence-checklist.md"
        text = path.read_text(encoding="utf-8")
        for section in ("## 谈判前硬参数", "## 反应分支", "## 证据清单", "## 停止条件"):
            self.assertIn(section, text)
        self.assertIn("```mermaid", text)
        self.assertIn("法释〔2024〕1号", text)

    def test_domestic_violence_note_uses_official_text(self) -> None:
        path = ROOT / "knowledge" / "legal" / "anti-domestic-violence-law.md"
        text = path.read_text(encoding="utf-8")
        self.assertIn("https://www.gov.cn/zhengce/2015-12/28/content_5029898.htm", text)
        for article in ("第二条", "第十五条", "第二十条", "第二十三条", "第二十九条", "第三十七条"):
            self.assertIn(article, text)

    def test_retracted_sources_are_explicitly_excluded(self) -> None:
        path = ROOT / "knowledge" / "rejected-sources.md"
        text = path.read_text(encoding="utf-8")
        self.assertIn("10.1037/fam0000907", text)
        self.assertIn("retracted", text.lower())
        self.assertIn("不得用于", text)
