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

    def test_relationship_pacing_playbook_requires_explicit_transition_decisions(self) -> None:
        note = (ROOT / "knowledge" / "notes" / "2006-stanley-rhoades-markman-sliding-deciding-cohabitation.md").read_text(encoding="utf-8")
        playbook = (ROOT / "knowledge" / "playbooks" / "relationship-pacing-and-transition-decisions.md").read_text(encoding="utf-8")
        self.assertIn("abstract_reviewed", note)
        for marker in ("七个", "六问", "30 天", "退出成本", "Stop conditions", "```mermaid"):
            self.assertIn(marker, playbook)

    def test_relationship_definition_playbook_turns_uncertainty_into_explicit_boundaries(self) -> None:
        note_path = ROOT / "knowledge" / "notes" / "1999-knobloch-solomon-relational-uncertainty.md"
        playbook_path = ROOT / "knowledge" / "playbooks" / "relationship-definition-and-exclusivity-boundaries.md"
        self.assertTrue(note_path.exists())
        self.assertTrue(playbook_path.exists())
        note = note_path.read_text(encoding="utf-8")
        playbook = playbook_path.read_text(encoding="utf-8")
        self.assertIn("abstract_reviewed", note)
        for marker in ("自我不确定性", "伴侣不确定性", "关系不确定性", "排他", "14 天", "Stop conditions", "```mermaid"):
            self.assertIn(marker, playbook)

    def test_dating_progression_playbook_requires_concrete_reciprocal_action(self) -> None:
        note_path = ROOT / "knowledge" / "notes" / "2024-coduto-fox-mobile-dating-initiation-escalation.md"
        playbook_path = ROOT / "knowledge" / "playbooks" / "dating-chat-to-real-world-progression.md"
        self.assertTrue(note_path.exists())
        self.assertTrue(playbook_path.exists())
        note = note_path.read_text(encoding="utf-8")
        playbook = playbook_path.read_text(encoding="utf-8")
        self.assertIn("37", note)
        self.assertIn("abstract_reviewed", note)
        for marker in ("渠道编织", "两次明确邀约", "14 天", "互惠", "公开场所", "Stop conditions", "```mermaid"):
            self.assertIn(marker, playbook)

    def test_premarital_disclosure_playbook_separates_risk_from_privacy(self) -> None:
        note = (ROOT / "knowledge" / "notes" / "2024-slepian-psychology-of-secrecy.md").read_text(encoding="utf-8")
        playbook = (ROOT / "knowledge" / "playbooks" / "premarital-major-facts-disclosure-and-verification.md").read_text(encoding="utf-8")
        self.assertIn("abstract_reviewed", note)
        for marker in ("共同风险", "知情同意", "个人隐私", "四周", "婚史", "债务", "Stop conditions", "```mermaid"):
            self.assertIn(marker, playbook)

    def test_housing_ownership_playbook_separates_affordability_from_title(self) -> None:
        affordability = (ROOT / "knowledge" / "notes" / "2019-krapf-wagner-housing-affordability-union-dissolution.md").read_text(encoding="utf-8")
        assets = (ROOT / "knowledge" / "notes" / "2019-deng-hoekstra-elsinga-women-housing-assets-china.md").read_text(encoding="utf-8")
        playbook = (ROOT / "knowledge" / "playbooks" / "housing-ownership-and-joint-purchase-audit.md").read_text(encoding="utf-8")
        self.assertIn("abstract_reviewed", affordability)
        self.assertIn("abstract_reviewed", assets)
        for marker in ("产权", "首付", "父母出资", "还贷", "退出", "30 天", "Stop conditions", "```mermaid"):
            self.assertIn(marker, playbook)

    def test_parent_care_playbook_requires_budget_time_and_backup_responsibility(self) -> None:
        note = (ROOT / "knowledge" / "notes" / "2012-fingerman-intergenerational-relationships.md").read_text(encoding="utf-8")
        ambivalence = (ROOT / "knowledge" / "notes" / "2003-willson-shuey-elder-parent-inlaw-ambivalence.md").read_text(encoding="utf-8")
        playbook = (ROOT / "knowledge" / "playbooks" / "parent-care-and-inlaw-responsibility-audit.md").read_text(encoding="utf-8")
        self.assertIn("abstract_reviewed", note)
        self.assertIn("abstract_reviewed", ambivalence)
        for marker in ("金额上限", "时间", "兄弟姐妹", "备用人", "六周", "Stop conditions", "```mermaid"):
            self.assertIn(marker, playbook)

    def test_wedding_budget_playbook_separates_bride_price_from_total_cost(self) -> None:
        playbook = (ROOT / "knowledge" / "playbooks" / "bride-price-and-wedding-budget-negotiation.md").read_text(encoding="utf-8")
        for marker in ("DOI 10.1037/str0000157", "总成本", "彩礼", "婚礼", "三种预算", "书面", "反应", "Stop conditions", "```mermaid"):
            self.assertIn(marker, playbook)

    def test_reconstituted_family_playbook_stages_children_and_ex_partner_boundaries(self) -> None:
        playbook = (ROOT / "knowledge" / "playbooks" / "reconstituted-family-and-stepfamily-audit.md").read_text(encoding="utf-8")
        for marker in ("DOI 10.1037/fam0001149", "继亲", "前任", "孩子", "六周", "抚养", "反应", "Stop conditions", "```mermaid"):
            self.assertIn(marker, playbook)

    def test_marital_intimacy_maintenance_playbook_uses_reversible_experiment(self) -> None:
        playbook = (ROOT / "knowledge" / "playbooks" / "marital-intimacy-maintenance-and-repair.md").read_text(encoding="utf-8")
        for marker in ("DOI 10.1037/bul0000342", "亲密", "性", "睡眠", "30 天", "反应", "停止条件", "Stop conditions", "```mermaid"):
            self.assertIn(marker, playbook)

    def test_separation_playbook_separates_financial_exit_from_coparenting(self) -> None:
        playbook = (ROOT / "knowledge" / "playbooks" / "separation-financial-disentanglement-and-coparenting.md").read_text(encoding="utf-8")
        for marker in ("DOI 10.1037/fam0001149", "72 小时", "30 天", "共同账户", "债务", "孩子", "交接", "反应", "Stop conditions", "```mermaid"):
            self.assertIn(marker, playbook)

    def test_childbearing_decision_playbook_requires_consent_and_capacity_audit(self) -> None:
        note = (ROOT / "knowledge" / "notes" / "2024-ranjbar-childbearing-decision-scoping-review.md").read_text(encoding="utf-8")
        playbook = (ROOT / "knowledge" / "playbooks" / "childbearing-intention-timing-and-capacity-audit.md").read_text(encoding="utf-8")
        self.assertIn("46 studies", note)
        self.assertIn("full_text_reviewed", note)
        for marker in ("知情同意", "不生育", "六周", "职业", "住房", "育儿", "反应", "Stop conditions", "```mermaid"):
            self.assertIn(marker, playbook)

    def test_ex_partner_boundary_playbook_uses_behavior_not_gender_bans(self) -> None:
        note = (ROOT / "knowledge" / "notes" / "2024-salavati-boon-extradyadic-behavior-judgments.md").read_text(encoding="utf-8")
        playbook = (ROOT / "knowledge" / "playbooks" / "ex-partner-and-potential-attraction-boundaries.md").read_text(encoding="utf-8")
        self.assertIn("135 participants", note)
        self.assertIn("30 vignettes", note)
        self.assertIn("abstract_reviewed", note)
        for marker in ("隐瞒", "频率", "前任", "两周", "不按性别", "监控", "反应", "Stop conditions", "```mermaid"):
            self.assertIn(marker, playbook)

    def test_dating_money_playbook_separates_gifts_loans_and_shared_costs(self) -> None:
        note = (ROOT / "knowledge" / "notes" / "2023-lazarus-online-romance-fraud-review.md").read_text(encoding="utf-8")
        playbook = (ROOT / "knowledge" / "playbooks" / "dating-loans-transfers-and-gift-boundaries.md").read_text(encoding="utf-8")
        self.assertIn("26 empirical studies", note)
        self.assertIn("abstract_reviewed", note)
        for marker in ("赠与", "借款", "共同消费", "24 小时", "不追加", "凭证", "反应", "Stop conditions", "```mermaid"):
            self.assertIn(marker, playbook)

    def test_age_resource_gap_playbook_audits_power_not_age_alone(self) -> None:
        note = (ROOT / "knowledge" / "notes" / "2018-lee-mckinnish-age-gap-marital-satisfaction.md").read_text(encoding="utf-8")
        playbook = (ROOT / "knowledge" / "playbooks" / "age-income-and-resource-gap-power-audit.md").read_text(encoding="utf-8")
        self.assertIn("3,374 couples", note)
        self.assertIn("18,987 couple-years", note)
        self.assertIn("full_text_reviewed", note)
        for marker in ("年龄差本身", "收入", "决定权", "职业", "退出能力", "30 天", "反应", "Stop conditions", "```mermaid"):
            self.assertIn(marker, playbook)

    def test_gambling_spending_playbook_stops_debt_escalation_and_prioritizes_safety(self) -> None:
        review = (ROOT / "knowledge" / "notes" / "2022-hing-gambling-family-violence-review.md").read_text(encoding="utf-8")
        loot_boxes = (ROOT / "knowledge" / "notes" / "2021-garea-loot-box-meta-analysis.md").read_text(encoding="utf-8")
        playbook = (ROOT / "knowledge" / "playbooks" / "gambling-speculation-and-game-spending-boundaries.md").read_text(encoding="utf-8")
        self.assertIn("46 journal articles", review)
        self.assertIn("full_text_reviewed", review)
        self.assertIn("abstract_reviewed", loot_boxes)
        for marker in ("追损", "72 小时", "游戏氪金", "债务", "账户", "专业", "暴力", "反应", "Stop conditions", "```mermaid"):
            self.assertIn(marker, playbook)

    def test_pornography_boundary_playbook_distinguishes_use_from_harm(self) -> None:
        meta = (ROOT / "knowledge" / "notes" / "2017-wright-pornography-satisfaction-meta-analysis.md").read_text(encoding="utf-8")
        couples = (ROOT / "knowledge" / "notes" / "2021-kohut-couple-pornography-context.md").read_text(encoding="utf-8")
        playbook = (ROOT / "knowledge" / "playbooks" / "pornography-live-content-and-sexual-boundaries.md").read_text(encoding="utf-8")
        self.assertIn("50 studies", meta)
        self.assertIn("50,000", meta)
        self.assertIn("full_text_reviewed", couples)
        for marker in ("自愿", "隐瞒", "直播打赏", "两周", "不等于成瘾", "监控", "私密内容", "反应", "Stop conditions", "```mermaid"):
            self.assertIn(marker, playbook)

    def test_past_relationship_playbook_separates_current_risk_from_private_detail(self) -> None:
        jealousy = (ROOT / "knowledge" / "notes" / "2018-frampton-social-media-retroactive-jealousy.md").read_text(encoding="utf-8")
        disclosure = (ROOT / "knowledge" / "notes" / "2021-ritter-sex-secret-disclosure.md").read_text(encoding="utf-8")
        playbook = (ROOT / "knowledge" / "playbooks" / "past-relationship-disclosure-and-retroactive-jealousy.md").read_text(encoding="utf-8")
        self.assertIn("36 participants", jealousy)
        self.assertIn("abstract_reviewed", jealousy)
        self.assertIn("full_text_reviewed", disclosure)
        for marker in ("当前共同风险", "私人细节", "婚史", "性健康", "14 天", "停止追问", "社交媒体", "反应", "Stop conditions", "```mermaid"):
            self.assertIn(marker, playbook)

    def test_relationship_cycling_playbook_requires_change_before_reconciliation(self) -> None:
        couples = (ROOT / "knowledge" / "notes" / "2014-vennum-relationship-cycling-cohabitation-marriage.md").read_text(encoding="utf-8")
        distress = (ROOT / "knowledge" / "notes" / "2018-monk-relationship-cycling-distress.md").read_text(encoding="utf-8")
        playbook = (ROOT / "knowledge" / "playbooks" / "breakup-reconciliation-cycle-and-reentry-gates.md").read_text(encoding="utf-8")
        self.assertIn("323 cohabiting", couples)
        self.assertIn("752 married", couples)
        self.assertIn("545 individuals", distress)
        self.assertIn("abstract_reviewed", distress)
        for marker in ("复合门槛", "结构性变化", "30 天", "不恢复", "沉没成本", "反应", "Stop conditions", "```mermaid"):
            self.assertIn(marker, playbook)

    def test_fear_of_singlehood_playbook_separates_pressure_from_partner_fit(self) -> None:
        fear = (ROOT / "knowledge" / "notes" / "2013-spielmann-fear-of-being-single.md").read_text(encoding="utf-8")
        pressure = (ROOT / "knowledge" / "notes" / "2021-sprecher-felmlee-social-pressure-singlehood.md").read_text(encoding="utf-8")
        playbook = (ROOT / "knowledge" / "playbooks" / "fear-of-singlehood-and-partner-choice-audit.md").read_text(encoding="utf-8")
        self.assertIn("longitudinal", fear)
        self.assertIn("616 single", pressure)
        self.assertIn("abstract_reviewed", fear)
        for marker in ("害怕单身", "伴侣匹配", "家庭压力", "14 天", "不因催婚", "反应", "Stop conditions", "```mermaid"):
            self.assertIn(marker, playbook)

    def test_phone_boundaries_playbook_separates_phubbing_from_surveillance(self) -> None:
        partner = (ROOT / "knowledge" / "notes" / "2016-roberts-david-partner-phubbing.md").read_text(encoding="utf-8")
        chinese = (ROOT / "knowledge" / "notes" / "2022-zhan-phubbing-chinese-adults.md").read_text(encoding="utf-8")
        playbook = (ROOT / "knowledge" / "playbooks" / "phone-use-and-couple-attention-boundaries.md").read_text(encoding="utf-8")
        self.assertIn("relationship satisfaction", partner)
        self.assertIn("504 Chinese adults", chinese)
        self.assertIn("abstract_reviewed", partner)
        for marker in ("手机干扰", "回复边界", "14 天", "不等于监控", "共同时间", "反应", "Stop conditions", "```mermaid"):
            self.assertIn(marker, playbook)

    def test_job_loss_playbook_separates_temporary_shock_from_control(self) -> None:
        note = (ROOT / "knowledge" / "notes" / "2022-gedikli-unemployment-wellbeing-meta-analysis.md").read_text(encoding="utf-8")
        playbook = (ROOT / "knowledge" / "playbooks" / "unemployment-income-shock-and-couple-decision-audit.md").read_text(encoding="utf-8")
        self.assertIn("46 samples", note)
        self.assertIn("abstract_reviewed", note)
        for marker in ("收入冲击", "90 天", "应急金", "责任转移", "不等于控制", "反应", "Stop conditions", "```mermaid"):
            self.assertIn(marker, playbook)

    def test_parenting_conflict_playbook_protects_children_from_triangular_conflict(self) -> None:
        conflict = (ROOT / "knowledge" / "notes" / "2020-van_eldik-interparental-conflict-meta-analysis.md").read_text(encoding="utf-8")
        grandparent = (ROOT / "knowledge" / "notes" / "2021-liang-grandmother-coparenting-china.md").read_text(encoding="utf-8")
        playbook = (ROOT / "knowledge" / "playbooks" / "parenting-values-and-grandparent-boundaries.md").read_text(encoding="utf-8")
        self.assertIn("169 studies", conflict)
        self.assertIn("60 children", grandparent)
        self.assertIn("abstract_reviewed", conflict)
        for marker in ("孩子面前", "祖辈", "两周", "不让孩子传话", "共同规则", "反应", "Stop conditions", "```mermaid"):
            self.assertIn(marker, playbook)

    def test_personal_space_playbook_separates_autonomy_from_withdrawal(self) -> None:
        needs = (ROOT / "knowledge" / "notes" / "2000-laguardia-autonomy-relatedness-attachment.md").read_text(encoding="utf-8")
        solitude = (ROOT / "knowledge" / "notes" / "2023-weinstein-solitude-wellbeing.md").read_text(encoding="utf-8")
        playbook = (ROOT / "knowledge" / "playbooks" / "personal-space-and-relationship-boundaries.md").read_text(encoding="utf-8")
        self.assertIn("autonomy", needs)
        self.assertIn("178", solitude)
        self.assertIn("abstract_reviewed", needs)
        for marker in ("独处", "个人空间", "7 天", "回归时间", "不等于冷暴力", "反应", "Stop conditions", "```mermaid"):
            self.assertIn(marker, playbook)

    def test_premarital_integrated_audit_covers_real_world_decision_factors(self) -> None:
        playbook = (ROOT / "knowledge" / "playbooks" / "premarital-30-day-integrated-audit.md").read_text(encoding="utf-8")
        for marker in ("30 天", "外貌", "收入", "家庭", "城市", "性", "生育", "谁负责", "反应", "Stop conditions", "```mermaid"):
            self.assertIn(marker, playbook)

    def test_secrecy_and_disclosure_playbook_separates_privacy_from_shared_risk(self) -> None:
        note = (ROOT / "knowledge" / "notes" / "2024-slepian-psychology-of-secrecy.md").read_text(encoding="utf-8")
        playbook = (ROOT / "knowledge" / "playbooks" / "privacy-secrecy-and-major-disclosure.md").read_text(encoding="utf-8")
        self.assertIn("10.1177/09637214241226676", note)
        for marker in ("共同风险", "个人隐私", "知情同意", "四周", "披露", "反应", "Stop conditions", "```mermaid"):
            self.assertIn(marker, playbook)

    def test_sexual_consent_playbook_covers_withdrawal_and_pressure(self) -> None:
        playbook = (ROOT / "knowledge" / "playbooks" / "sexual-consent-and-refusal-boundaries.md").read_text(encoding="utf-8")
        for marker in ("同意", "撤回", "拒绝", "压力", "疼痛", "反应", "Stop conditions", "```mermaid"):
            self.assertIn(marker, playbook)

    def test_case_evidence_triage_separates_facts_from_interpretations(self) -> None:
        playbook = (ROOT / "knowledge" / "playbooks" / "case-evidence-triage-and-decision-log.md").read_text(encoding="utf-8")
        for marker in ("事实", "解释", "证据", "视频", "隐私", "反应", "Stop conditions", "```mermaid"):
            self.assertIn(marker, playbook)

    def test_marriage_expense_source_is_metadata_verified_and_limited(self) -> None:
        note = (ROOT / "knowledge" / "notes" / "2023-duan-jin-sun-teng-marriage-expenses-rural-migrants.md").read_text(encoding="utf-8")
        sources = (ROOT / "knowledge" / "sources.yaml").read_text(encoding="utf-8")
        verified = (ROOT / "knowledge" / "verified-sources.md").read_text(encoding="utf-8")
        self.assertIn("10.1111/fare.12909", note)
        self.assertIn("1,391", note)
        self.assertIn("abstract_reviewed", note)
        self.assertIn("10.1111/fare.12909", sources)
        self.assertIn("10.1111/fare.12909", verified)
