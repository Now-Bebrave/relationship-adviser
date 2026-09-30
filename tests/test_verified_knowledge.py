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

    def test_attachment_and_dissolution_queues_are_promoted(self) -> None:
        attachment = (ROOT / "knowledge" / "notes" / "2019-candel-turliuc-insecure-attachment-meta-analysis.md").read_text(encoding="utf-8")
        dissolution = (ROOT / "knowledge" / "notes" / "2010-le-et-al-relationship-dissolution-meta-analysis.md").read_text(encoding="utf-8")
        self.assertIn("verification_status: abstract_reviewed", attachment)
        self.assertIn("Actor effects", attachment)
        self.assertIn("37,761", dissolution)
        self.assertIn("commitment", dissolution.lower())

    def test_shared_finance_guidance_preserves_scope_and_safety(self) -> None:
        note = (ROOT / "knowledge" / "notes" / "2023-olson-bank-account-structure-experiment.md").read_text(encoding="utf-8")
        playbook = (ROOT / "knowledge" / "playbooks" / "shared-finance-structure.md").read_text(encoding="utf-8")
        self.assertIn("engaged or newlywed", note)
        self.assertIn("random", note.lower())
        self.assertIn("financial control", playbook.lower())

    def test_dyadic_coping_playbook_distinguishes_stressor_types(self) -> None:
        note = (ROOT / "knowledge" / "notes" / "2019-falconier-kuhn-dyadic-coping-review.md").read_text(encoding="utf-8")
        playbook = (ROOT / "knowledge" / "playbooks" / "dyadic-coping.md").read_text(encoding="utf-8")
        self.assertIn("139 studies", note)
        self.assertIn("within-relationship", note)
        self.assertIn("stress communication", playbook.lower())
        self.assertIn("停止", playbook)

    def test_reproductive_coercion_guidance_is_safety_first(self) -> None:
        note = (ROOT / "knowledge" / "notes" / "2018-grace-anderson-reproductive-coercion-review.md").read_text(encoding="utf-8")
        playbook = (ROOT / "knowledge" / "playbooks" / "reproductive-autonomy.md").read_text(encoding="utf-8")
        self.assertIn("27", note)
        self.assertIn("birth control sabotage", note.lower())
        self.assertIn("不要单独对质", playbook)
        self.assertIn("停止条件", playbook)

    def test_repair_playbook_requires_behavioral_change(self) -> None:
        note = (ROOT / "knowledge" / "notes" / "2014-mccullough-conciliatory-gestures-forgiveness.md").read_text(encoding="utf-8")
        playbook = (ROOT / "knowledge" / "playbooks" / "repair-after-harm.md").read_text(encoding="utf-8")
        self.assertIn("337", note)
        self.assertIn("abstract_reviewed", note)
        self.assertIn("7天", playbook)
        self.assertIn("停止条件", playbook)
        self.assertIn("胁迫", playbook)

    def test_desire_discrepancy_playbook_preserves_consent(self) -> None:
        note = (ROOT / "knowledge" / "notes" / "2020-vowels-mark-sexual-desire-discrepancy.md").read_text(encoding="utf-8")
        playbook = (ROOT / "knowledge" / "playbooks" / "sexual-desire-discrepancy.md").read_text(encoding="utf-8")
        self.assertIn("229", note)
        self.assertIn("full_text_reviewed", note)
        self.assertIn("自由拒绝", playbook)
        self.assertIn("停止条件", playbook)
        self.assertIn("不以恢复性行为为目标", playbook)

    def test_premarital_audit_has_hard_gates_and_staged_decision(self) -> None:
        playbook = (ROOT / "knowledge" / "playbooks" / "premarital-cohabitation-audit.md").read_text(encoding="utf-8")
        self.assertIn("DOI 10.1037/a0012584", playbook)
        self.assertIn("四周", playbook)
        self.assertIn("暂停升级", playbook)
        self.assertIn("停止条件", playbook)
        self.assertIn("生育", playbook)

    def test_exit_playbook_covers_safety_logistics_and_recovery(self) -> None:
        note = (ROOT / "knowledge" / "notes" / "2019-verhallen-breakup-stress.md").read_text(encoding="utf-8")
        playbook = (ROOT / "knowledge" / "playbooks" / "relationship-exit-execution.md").read_text(encoding="utf-8")
        self.assertIn("26.8%", note)
        self.assertIn("full_text_reviewed", note)
        self.assertIn("72小时", playbook)
        self.assertIn("住房", playbook)
        self.assertIn("Stop conditions", playbook)
        self.assertIn("自伤", playbook)

    def test_digital_boundaries_playbook_rejects_surveillance_as_trust(self) -> None:
        note = (ROOT / "knowledge" / "notes" / "2021-tandon-social-media-jealousy-review.md").read_text(encoding="utf-8")
        playbook = (ROOT / "knowledge" / "playbooks" / "digital-boundaries-and-jealousy.md").read_text(encoding="utf-8")
        self.assertIn("45 empirical studies", note)
        self.assertIn("abstract_reviewed", note)
        self.assertIn("不以强制检查作为信任证明", playbook)
        self.assertIn("Stop conditions", playbook)
        self.assertIn("网络跟踪", playbook)

    def test_family_boundary_playbook_requires_partner_enforcement(self) -> None:
        note = (ROOT / "knowledge" / "notes" / "2001-bryant-conger-inalaw-conflict.md").read_text(encoding="utf-8")
        playbook = (ROOT / "knowledge" / "playbooks" / "family-boundaries-and-inlaws.md").read_text(encoding="utf-8")
        self.assertIn("abstract_reviewed", note)
        self.assertIn("共同执行", playbook)
        self.assertIn("Stop conditions", playbook)
        self.assertIn("未经同意上门", playbook)

    def test_mental_load_playbook_requires_full_responsibility(self) -> None:
        note = (ROOT / "knowledge" / "notes" / "2023-reich-stiebert-gendered-mental-labor-review.md").read_text(encoding="utf-8")
        playbook = (ROOT / "knowledge" / "playbooks" / "emotional-labor-and-mental-load.md").read_text(encoding="utf-8")
        self.assertIn("31 full-text articles", note)
        self.assertIn("abstract_reviewed", note)
        self.assertIn("发现", playbook)
        self.assertIn("跟进", playbook)
        self.assertIn("两周", playbook)
        self.assertIn("Stop conditions", playbook)

    def test_trust_repair_playbook_is_bounded_and_optional(self) -> None:
        note = (ROOT / "knowledge" / "notes" / "2025-giacobbi-lalot-trust-repair-review.md").read_text(encoding="utf-8")
        playbook = (ROOT / "knowledge" / "playbooks" / "trust-repair-after-betrayal.md").read_text(encoding="utf-8")
        self.assertIn("13 empirical articles", note)
        self.assertIn("abstract_reviewed", note)
        self.assertIn("30 天", playbook)
        self.assertIn("可撤回", playbook)
        self.assertIn("Stop conditions", playbook)
        self.assertIn("强制密码", playbook)

    def test_parenthood_transition_playbook_prioritizes_health_and_workload(self) -> None:
        note = (ROOT / "knowledge" / "notes" / "2022-bogdan-turliuc-candel-parenthood-meta-analysis.md").read_text(encoding="utf-8")
        playbook = (ROOT / "knowledge" / "playbooks" / "transition-to-parenthood.md").read_text(encoding="utf-8")
        self.assertIn("49 studies", note)
        self.assertIn("abstract_reviewed", note)
        self.assertIn("产后12周", playbook)
        self.assertIn("3、6、12个月", playbook)
        self.assertIn("睡眠", playbook)
        self.assertIn("Stop conditions", playbook)

    def test_sti_notification_playbook_is_medical_and_safety_first(self) -> None:
        note = (ROOT / "knowledge" / "notes" / "2012_cochrane_partner_notification_sti.md").read_text(encoding="utf-8")
        playbook = (ROOT / "knowledge" / "playbooks" / "sti-partner-notification.md").read_text(encoding="utf-8")
        self.assertIn("26 trials", note)
        self.assertIn("abstract_reviewed", note)
        self.assertIn("检测机构", playbook)
        self.assertIn("第三方通知", playbook)
        self.assertIn("Stop conditions", playbook)
