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

    def test_ipv_screening_playbook_prioritizes_private_ongoing_support(self) -> None:
        note = (ROOT / "knowledge" / "notes" / "2018_uspstf_ipv_screening_review.md").read_text(encoding="utf-8")
        playbook = (ROOT / "knowledge" / "playbooks" / "ipv-screening-and-support.md").read_text(encoding="utf-8")
        self.assertIn("moderate net benefit", note)
        self.assertIn("abstract_reviewed", note)
        self.assertIn("私下", playbook)
        self.assertIn("持续支持", playbook)
        self.assertIn("Stop conditions", playbook)

    def test_jealousy_playbook_separates_facts_from_control(self) -> None:
        note = (ROOT / "knowledge" / "notes" / "2017-romantic-jealousy-systematic-review.md").read_text(encoding="utf-8")
        playbook = (ROOT / "knowledge" / "playbooks" / "jealousy-and-uncertainty.md").read_text(encoding="utf-8")
        self.assertIn("230 studies", note)
        self.assertIn("abstract_reviewed", note)
        self.assertIn("事实", playbook)
        self.assertIn("14 天", playbook)
        self.assertIn("Stop conditions", playbook)

    def test_long_distance_playbook_requires_reunion_validation(self) -> None:
        note = (ROOT / "knowledge" / "notes" / "2007-jimenez-morales-long-distance-relationships.md").read_text(encoding="utf-8")
        playbook = (ROOT / "knowledge" / "playbooks" / "long-distance-relationship.md").read_text(encoding="utf-8")
        self.assertIn("Two studies", note)
        self.assertIn("abstract_reviewed", note)
        self.assertIn("2—4 周", playbook)
        self.assertIn("重聚", playbook)
        self.assertIn("Stop conditions", playbook)

    def test_cnm_playbook_requires_ongoing_consent_and_exit(self) -> None:
        note = (ROOT / "knowledge" / "notes" / "2023-gupta-tarantino-sanner-cnm-review.md").read_text(encoding="utf-8")
        playbook = (ROOT / "knowledge" / "playbooks" / "consensual-nonmonogamy-boundaries.md").read_text(encoding="utf-8")
        self.assertIn("209 studies", note)
        self.assertIn("abstract_reviewed", note)
        self.assertIn("持续同意", playbook)
        self.assertIn("退出机制", playbook)
        self.assertIn("Stop conditions", playbook)

    def test_mental_health_support_playbook_is_bounded_and_actionable(self) -> None:
        note = (ROOT / "knowledge" / "notes" / "2016-gariepy-honkaniemi-social-support-depression-review.md").read_text(encoding="utf-8")
        playbook = (ROOT / "knowledge" / "playbooks" / "mental-health-support-in-relationships.md").read_text(encoding="utf-8")
        self.assertIn("100 项研究", note)
        self.assertIn("abstract_reviewed", note)
        for marker in ("倾听", "就医支持", "48 小时", "专业", "Stop conditions", "自伤"):
            self.assertIn(marker, playbook)
        self.assertIn("```mermaid", playbook)

    def test_emotion_regulation_playbook_is_concrete_and_safety_bounded(self) -> None:
        note = (ROOT / "knowledge" / "notes" / "2022-jardine-vannier-voyer-emotional-intelligence-meta-analysis.md").read_text(encoding="utf-8")
        playbook = (ROOT / "knowledge" / "playbooks" / "emotion-regulation-and-conflict-deescalation.md").read_text(encoding="utf-8")
        self.assertIn("78 个样本", note)
        self.assertIn("90 个效应量", note)
        self.assertIn("abstract_reviewed", note)
        for marker in ("暂停", "具体请求", "7 天", "Stop conditions", "威胁", "```mermaid"):
            self.assertIn(marker, playbook)

    def test_substance_use_playbook_prioritizes_safety_and_referral(self) -> None:
        note = (ROOT / "knowledge" / "notes" / "2008-powers-behavioral-couples-therapy-substance-use-meta-analysis.md").read_text(encoding="utf-8")
        playbook = (ROOT / "knowledge" / "playbooks" / "substance-use-boundaries-and-support.md").read_text(encoding="utf-8")
        self.assertIn("meta_analysis", note)
        self.assertIn("abstract_reviewed", note)
        for marker in ("72 小时", "专业", "停止兜底", "Stop conditions", "暴力", "```mermaid"):
            self.assertIn(marker, playbook)

    def test_chronic_illness_playbook_preserves_autonomy_and_caregiver_capacity(self) -> None:
        note = (ROOT / "knowledge" / "notes" / "2021-weitkamp-dyadic-coping-chronic-illness-review.md").read_text(encoding="utf-8")
        playbook = (ROOT / "knowledge" / "playbooks" / "chronic-illness-caregiving-and-couple-coordination.md").read_text(encoding="utf-8")
        self.assertIn("systematic_review", note)
        self.assertIn("abstract_reviewed", note)
        for marker in ("患者自主", "照护者恢复", "两周", "备用人", "Stop conditions", "```mermaid"):
            self.assertIn(marker, playbook)

    def test_sleep_playbook_uses_reversible_experiment_and_medical_triage(self) -> None:
        note = (ROOT / "knowledge" / "notes" / "2025-wang-couple-relationships-sleep-meta-analysis.md").read_text(encoding="utf-8")
        playbook = (ROOT / "knowledge" / "playbooks" / "sleep-and-relationship-coordination.md").read_text(encoding="utf-8")
        self.assertIn("62 项研究", note)
        self.assertIn("43,860", note)
        self.assertIn("abstract_reviewed", note)
        for marker in ("一周", "可逆", "分床", "睡眠门诊", "Stop conditions", "```mermaid"):
            self.assertIn(marker, playbook)

    def test_economic_strain_playbook_covers_real_world_marriage_feasibility(self) -> None:
        note = (ROOT / "knowledge" / "notes" / "2020-falconier-jackson-economic-strain-couple-functioning-meta-analysis.md").read_text(encoding="utf-8")
        playbook = (ROOT / "knowledge" / "playbooks" / "economic-strain-and-marriage-feasibility.md").read_text(encoding="utf-8")
        self.assertIn("meta_analysis", note)
        self.assertIn("abstract_reviewed", note)
        for marker in ("收入", "债务", "家庭责任", "两周", "连续三个月", "Stop conditions", "```mermaid"):
            self.assertIn(marker, playbook)

    def test_partner_matching_playbook_separates_attraction_from_feasibility(self) -> None:
        note = (ROOT / "knowledge" / "notes" / "2004-watson-assortative-mating-newlywed-couples.md").read_text(encoding="utf-8")
        playbook = (ROOT / "knowledge" / "playbooks" / "partner-matching-and-real-world-fit.md").read_text(encoding="utf-8")
        self.assertIn("abstract_reviewed", note)
        for marker in ("外貌", "收入", "家庭与社会", "三阶段", "Stop conditions", "```mermaid"):
            self.assertIn(marker, playbook)

    def test_migration_marriage_playbook_covers_housing_and_family_tradeoffs(self) -> None:
        note = (ROOT / "knowledge" / "notes" / "2023-xiong-internal-migration-marriage-prospects-china.md").read_text(encoding="utf-8")
        playbook = (ROOT / "knowledge" / "playbooks" / "migration-housing-and-marriage-choice.md").read_text(encoding="utf-8")
        self.assertIn("abstract_reviewed", note)
        for marker in ("住房", "户籍", "父母", "30 天", "Stop conditions", "```mermaid"):
            self.assertIn(marker, playbook)

    def test_gender_role_playbook_converts_attitudes_into_observable_responsibilities(self) -> None:
        note = (ROOT / "knowledge" / "notes" / "2025-park-gender-role-attitudes-relationship-satisfaction.md").read_text(encoding="utf-8")
        playbook = (ROOT / "knowledge" / "playbooks" / "gender-role-and-marital-labor-audit.md").read_text(encoding="utf-8")
        self.assertIn("abstract_reviewed", note)
        for marker in ("实际分工", "两周", "完整责任", "生育", "Stop conditions", "```mermaid"):
            self.assertIn(marker, playbook)

    def test_appearance_playbook_separates_attraction_from_body_control(self) -> None:
        note = (ROOT / "knowledge" / "notes" / "2023-stiles-body-dissatisfaction-relationship-quality-meta-analysis.md").read_text(encoding="utf-8")
        playbook = (ROOT / "knowledge" / "playbooks" / "appearance-attraction-and-body-respect.md").read_text(encoding="utf-8")
        self.assertIn("56 项研究", note)
        self.assertIn("abstract_reviewed", note)
        for marker in ("外貌吸引", "身体尊重", "14 天", "强迫", "Stop conditions", "```mermaid"):
            self.assertIn(marker, playbook)

    def test_marriage_timing_playbook_resists_age_pressure_and_requires_audit(self) -> None:
        note = (ROOT / "knowledge" / "notes" / "2015-yu-xie-marriage-entry-urban-china.md").read_text(encoding="utf-8")
        playbook = (ROOT / "knowledge" / "playbooks" / "marriage-timing-and-pressure-audit.md").read_text(encoding="utf-8")
        self.assertIn("abstract_reviewed", note)
        for marker in ("年龄", "六周", "生育", "催婚", "Stop conditions", "```mermaid"):
            self.assertIn(marker, playbook)

    def test_online_dating_playbook_prioritizes_verification_and_first_date_safety(self) -> None:
        note = (ROOT / "knowledge" / "notes" / "2019-sharabi-caughlin-online-dating-deception.md").read_text(encoding="utf-8")
        playbook = (ROOT / "knowledge" / "playbooks" / "online-dating-verification-and-first-date-safety.md").read_text(encoding="utf-8")
        self.assertIn("94", note)
        self.assertIn("abstract_reviewed", note)
        for marker in ("视频", "公共场所", "不转账", "Stop conditions", "验证码", "```mermaid"):
            self.assertIn(marker, playbook)

    def test_infidelity_playbook_separates_boundaries_from_prevalence_and_requires_safety(self) -> None:
        note = (ROOT / "knowledge" / "notes" / "2024-warach-infidelity-prevalence-meta-analysis.md").read_text(encoding="utf-8")
        playbook = (ROOT / "knowledge" / "playbooks" / "infidelity-boundaries-and-repair-decision.md").read_text(encoding="utf-8")
        self.assertIn("305 项研究", note)
        self.assertIn("abstract_reviewed", note)
        for marker in ("性边界", "72 小时", "30 天", "停止第三方关系", "Stop conditions", "```mermaid"):
            self.assertIn(marker, playbook)

    def test_commitment_playbook_rejects_sunk_cost_and_checks_hard_gates(self) -> None:
        note = (ROOT / "knowledge" / "notes" / "2003-le-agnew-investment-model-meta-analysis.md").read_text(encoding="utf-8")
        playbook = (ROOT / "knowledge" / "playbooks" / "commitment-investment-and-exit-audit.md").read_text(encoding="utf-8")
        self.assertIn("52 项研究", note)
        self.assertIn("11,582", note)
        self.assertIn("abstract_reviewed", note)
        for marker in ("沉没成本", "14 天", "硬门槛", "Stop conditions", "```mermaid"):
            self.assertIn(marker, playbook)

    def test_financial_infidelity_playbook_separates_privacy_from_shared_risk(self) -> None:
        note = (ROOT / "knowledge" / "notes" / "2020-garbinsky-financial-infidelity-romantic-relationships.md").read_text(encoding="utf-8")
        playbook = (ROOT / "knowledge" / "playbooks" / "financial-infidelity-and-money-transparency.md").read_text(encoding="utf-8")
        self.assertIn("abstract_reviewed", note)
        for marker in ("共同账户", "72 小时", "三个月", "重大债务", "Stop conditions", "```mermaid"):
            self.assertIn(marker, playbook)

    def test_power_playbook_distinguishes_negotiation_from_control(self) -> None:
        note = (ROOT / "knowledge" / "notes" / "2024-young-seedall-couple-power-dynamics-review.md").read_text(encoding="utf-8")
        playbook = (ROOT / "knowledge" / "playbooks" / "relationship-power-and-major-decision-audit.md").read_text(encoding="utf-8")
        self.assertIn("abstract_reviewed", note)
        for marker in ("五问审计", "七天", "安全说不", "重大决定", "Stop conditions", "```mermaid"):
            self.assertIn(marker, playbook)

    def test_relationship_stage_playbook_separates_normal_fluctuation_from_harm(self) -> None:
        note = (ROOT / "knowledge" / "notes" / "2021-buhler-relationship-satisfaction-life-span-meta-analysis.md").read_text(encoding="utf-8")
        playbook = (ROOT / "knowledge" / "playbooks" / "relationship-stage-review-and-marital-maintenance.md").read_text(encoding="utf-8")
        self.assertIn("abstract_reviewed", note)
        for marker in ("六个阶段", "30 天", "生育", "重复模式", "Stop conditions", "```mermaid"):
            self.assertIn(marker, playbook)

    def test_coparenting_playbook_protects_children_and_requires_complete_responsibility(self) -> None:
        note = (ROOT / "knowledge" / "notes" / "2024-ronaghan-coparenting-marital-satisfaction-meta-analysis.md").read_text(encoding="utf-8")
        playbook = (ROOT / "knowledge" / "playbooks" / "coparenting-and-marital-coordination.md").read_text(encoding="utf-8")
        self.assertIn("108 项研究", note)
        self.assertIn("abstract_reviewed", note)
        for marker in ("两周", "孩子", "完整责任", "停止条件", "```mermaid"):
            self.assertIn(marker, playbook)

    def test_work_family_playbook_uses_capacity_and_protects_careers(self) -> None:
        note = (ROOT / "knowledge" / "notes" / "2016-fellows-work-family-conflict-couple-quality-meta-analysis.md").read_text(encoding="utf-8")
        playbook = (ROOT / "knowledge" / "playbooks" / "work-family-conflict-and-couple-coordination.md").read_text(encoding="utf-8")
        self.assertIn("33 项研究", note)
        self.assertIn("49 个样本", note)
        self.assertIn("abstract_reviewed", note)
        for marker in ("容量预算", "两周", "职业让步", "个人应急金", "Stop conditions", "```mermaid"):
            self.assertIn(marker, playbook)

    def test_social_network_playbook_uses_evidence_not_popularity(self) -> None:
        note = (ROOT / "knowledge" / "notes" / "2000-sprecher-felmlee-social-network-relationship-transitions.md").read_text(encoding="utf-8")
        playbook = (ROOT / "knowledge" / "playbooks" / "social-network-approval-and-relationship-decisions.md").read_text(encoding="utf-8")
        self.assertIn("abstract_reviewed", note)
        for marker in ("四级", "14 天", "具体事件", "支持网络", "Stop conditions", "```mermaid"):
            self.assertIn(marker, playbook)

    def test_dating_criteria_playbook_separates_hard_gates_from_preferences(self) -> None:
        note = (ROOT / "knowledge" / "notes" / "2014-eastwick-ideal-partner-preferences-meta-analysis.md").read_text(encoding="utf-8")
        playbook = (ROOT / "knowledge" / "playbooks" / "dating-criteria-and-real-world-validation.md").read_text(encoding="utf-8")
        self.assertIn("abstract_reviewed", note)
        for marker in ("硬门槛", "重要偏好", "三次", "外貌", "Stop conditions", "```mermaid"):
            self.assertIn(marker, playbook)
