# Relationship Adviser Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a platform-independent relationship-adviser package with a local private-vault boundary, executable output protocol, knowledge-card schemas, and one sanitized end-to-end case.

**Architecture:** Markdown is the human-readable source of truth; JSON schemas and small Python standard-library validators provide machine checks. Public core files live in the repository, while private-vault/ is ignored and contains personal data. The first deliverable does not require a model API or external service.

**Tech Stack:** Markdown, JSON, YAML templates, Python 3.11+ standard library, Git, PowerShell smoke checks.

**Spec:** docs/superpowers/specs/2026-09-29-relationship-adviser-design.md

## Global Constraints

- Keep one platform-independent core; adapters must not duplicate analysis rules.
- Default decision priority is personal_objective; ask for a priority when goals conflict, information is insufficient, or stakes are high.
- Every action recommendation must include a conclusion, steps, possible reactions, responses, stop conditions, one alternative, and confidence/unknowns.
- Label facts, inferences, recommendations, and unknowns separately.
- Keep personal profiles, sensitive cases, and raw media outside the public package.
- Treat research, professional material, creator content, and personal cases as separate evidence levels (L1–L4).
- Use no third-party Python dependency in the foundation package.
- Do not push to GitHub until local validation passes and the user is told that the backup step is ready.

---

### Task 1: Bootstrap the repository boundary

**Files:**
- Create: .gitignore
- Create: README.md
- Create: core/.gitkeep
- Create: knowledge-schema/.gitkeep
- Create: examples/.gitkeep
- Create: private-vault/README.md
- Test: tests/test_repository_boundary.py

**Interfaces:**
- Produces the public/private directory contract used by every later task.
- private-vault/ is ignored by Git except for its README; examples/ contains only sanitized data.

- [ ] Step 1: Initialize the local repository and create the directory skeleton

Run:

~~~powershell
git init
New-Item -ItemType Directory -Force core,knowledge-schema,examples,private-vault,tests | Out-Null
~~~

Expected: a local Git repository and the five directories exist.

- [ ] Step 2: Write the ignore boundary

Add these exact patterns to .gitignore:

~~~gitignore
private-vault/**
!private-vault/README.md
**/*.local.*
**/raw-media/
**/*.mp4
**/*.mov
**/*.mkv
~~~

- [ ] Step 3: Document the two data roots

README.md must state that core/, schemas, adapters, visuals, and sanitized examples are public package content; private-vault/ stores personal files; MediaCrawler remains at its existing path and is indexed by reference.

- [ ] Step 4: Add the boundary test

Create tests/test_repository_boundary.py:

~~~python
from pathlib import Path
import shutil
import subprocess
import unittest


class RepositoryBoundaryTests(unittest.TestCase):
    def tearDown(self) -> None:
        shutil.rmtree("private-vault/profile", ignore_errors=True)

    def test_private_vault_is_ignored(self) -> None:
        private_file = Path("private-vault/profile/profile.yaml")
        private_file.parent.mkdir(parents=True, exist_ok=True)
        private_file.write_text("relationship_status: private\n", encoding="utf-8")
        result = subprocess.run(
            ["git", "check-ignore", "--no-index", str(private_file)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0)

    def test_public_example_directory_is_not_ignored(self) -> None:
        result = subprocess.run(
            ["git", "check-ignore", "--no-index", "examples/example.md"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
~~~

- [ ] Step 5: Run the boundary test and commit

Run: python -m unittest discover -s tests -p "test_repository_boundary.py" -v

Expected: both tests pass. Commit with:

~~~powershell
git add .gitignore README.md private-vault/README.md core/.gitkeep knowledge-schema/.gitkeep examples/.gitkeep tests/test_repository_boundary.py
git commit -m "chore: bootstrap public and private package boundary"
~~~

### Task 2: Create the core analysis protocol

**Files:**
- Create: core/mission.md
- Create: core/domains.md
- Create: core/intake.md
- Create: core/reasoning.md
- Create: core/evidence.md
- Create: core/communication.md
- Create: core/output.md
- Test: tests/test_core_protocol.py

**Interfaces:**
- core/mission.md is the single entry point.
- core/output.md defines the required output headings consumed by all adapters.
- The other files are referenced by relative Markdown links from mission.md.

- [ ] Step 1: Write the failing protocol test

The test must assert that mission.md links to each core file and that output.md contains these exact labels: 结论, 判断依据, 详细执行步骤, 对方可能反应, 对应回答和下一步, 停止条件, 备选方案, 信心与信息缺口.

- [ ] Step 2: Run the test to verify the protocol is absent

Run: python -m unittest discover -s tests -p "test_core_protocol.py" -v

Expected: FAIL because the core files do not exist.

- [ ] Step 3: Write the minimal core documents

mission.md must instruct the agent to load intake.md, reasoning.md, evidence.md, communication.md, domains.md, and output.md in that order. reasoning.md must define the nine-step decision skeleton from the spec. evidence.md must define L1–L4 and the four output labels: fact, inference, recommendation, unknown. communication.md must require concrete scripts, reaction branches, boundaries, and stop conditions. domains.md must include all agreed domains, including PUA as identification/defense and MBTI limitations.

- [ ] Step 4: Run the protocol test

Run: python -m unittest discover -s tests -p "test_core_protocol.py" -v

Expected: PASS, with every relative link resolving to a file.

- [ ] Step 5: Commit the core protocol

Run: git add core tests/test_core_protocol.py && git commit -m "feat: add platform-independent analysis protocol".

### Task 3: Add schemas and sanitized knowledge-card templates

**Files:**
- Create: knowledge-schema/source.schema.json
- Create: knowledge-schema/video-card.schema.json
- Create: knowledge-schema/case.schema.json
- Create: knowledge-schema/decision.schema.json
- Create: knowledge/sources.yaml
- Create: examples/templates/source-card.yaml
- Create: examples/templates/video-card.yaml
- Create: examples/templates/decision-card.yaml
- Create: examples/knowledge-seed.md
- Test: tests/test_schema_contract.py

**Interfaces:**
- Every card has title, type, source, evidence_level, confidence, application, and limits where applicable.
- Video cards accept extraction_mode values notes_only, notes_plus_images, notes_plus_spotcheck, and full_video.
- knowledge/sources.yaml is the source register; each entry has title, topic, target evidence level, and verification status.
- The schemas are documentation contracts; the foundation validator checks required keys and enum values without installing a JSON-schema package.

- [ ] Step 1: Write failing schema-contract tests

Test that each schema parses as JSON, required keys are present, and video-card.schema.json contains all four extraction modes.

- [ ] Step 2: Run the schema tests and verify failure

Run: python -m unittest discover -s tests -p "test_schema_contract.py" -v

Expected: FAIL because the schemas do not exist.

- [ ] Step 3: Add the four schemas, source register, and human templates

Use the field names in the approved spec. Add the agreed P0/P1/P2 candidate topics and books to knowledge/sources.yaml with verification_status: candidate so the catalog does not imply that online links, editions, DOIs, or licenses have already been checked. Keep templates empty or filled only with neutral examples; never place personal data in examples/.

- [ ] Step 4: Add the human-readable seed list

examples/knowledge-seed.md must group candidates by relationship science, communication and negotiation, sexuality and intimacy, family and marriage, law and safety, social context, and field cases. It must state which entries are candidate sources awaiting online verification.

- [ ] Step 5: Run the schema tests

Run: python -m unittest discover -s tests -p "test_schema_contract.py" -v

Expected: PASS.

- [ ] Step 6: Commit the schemas and source register

Run: git add knowledge-schema knowledge/sources.yaml examples/templates examples/knowledge-seed.md tests/test_schema_contract.py && git commit -m "feat: add knowledge and decision card contracts".

### Task 4: Create the private-vault templates and profile rules

**Files:**
- Create: private-vault/profile/profile.yaml.example
- Create: private-vault/cases/.gitkeep
- Create: private-vault/decisions/.gitkeep
- Create: private-vault/knowledge-notes/.gitkeep
- Create: private-vault/video-notes/.gitkeep
- Create: private-vault/source-index/.gitkeep
- Create: core/profile-policy.md
- Test: tests/test_profile_policy.py

**Interfaces:**
- profile.yaml.example exposes the approved fields: identity, goals, preferences, constraints, patterns, and memory_rules.
- profile-policy.md defines explicit-save behavior and conflict handling.

- [ ] Step 1: Write tests for privacy defaults

Assert that the example sets default_priority: personal_objective, save_by_default: false, and require_explicit_save_for_sensitive_events: true.

- [ ] Step 2: Run the tests and verify failure

Run: python -m unittest discover -s tests -p "test_profile_policy.py" -v

Expected: FAIL because the profile template does not exist.

- [ ] Step 3: Add the profile template and policy

Use empty values and arrays. Document that personal experiences, sexual experiences, and family conflicts remain session-only until the user explicitly asks to save them.

- [ ] Step 4: Run the profile tests

Run: python -m unittest discover -s tests -p "test_profile_policy.py" -v

Expected: PASS.

- [ ] Step 5: Commit the private-vault contract

Run: git add private-vault core/profile-policy.md tests/test_profile_policy.py && git commit -m "feat: add local profile and memory policy".

### Task 5: Add the first sanitized case and package validator

**Files:**
- Create: examples/cases/bride-price-family-negotiation.md
- Create: tools/validate_package.py
- Create: tests/fixtures/minimal-question.md
- Test: tests/test_package_validator.py

**Interfaces:**
- tools/validate_package.py exposes validate(root: Path) -> list[str] and a CLI returning exit code 0 for a valid package and 1 with one error per line for invalid packages.
- The sample case contains claims, scripts, expected reactions, responses, limits, and a source note without local personal paths.

- [ ] Step 1: Write the failing validator test

The test calls validate(Path(".")) and asserts an empty error list only after all required core files, schemas, templates, and sample case exist.

- [ ] Step 2: Run the validator test to verify failure

Run: python -m unittest discover -s tests -p "test_package_validator.py" -v

Expected: FAIL with missing-file errors.

- [ ] Step 3: Implement the standard-library validator

Check required paths, relative links from core/mission.md, required output labels, extraction-mode values, and the absence of personal absolute paths under examples/.

- [ ] Step 4: Add the sanitized彩礼 case

Record the strategy as an L3 case: establish respect, delay an unprepared numeric commitment, ask for the other side's expectation, move to bilateral negotiation, and set concrete follow-up conditions. Keep the source reference generic and do not copy private filesystem paths.

- [ ] Step 5: Run the full foundation checks

Run:

~~~powershell
python -m unittest discover -s tests -v
python tools/validate_package.py
~~~

Expected: all tests pass and the validator exits 0.

- [ ] Step 6: Commit the foundation release

Run: git add examples tools tests && git commit -m "feat: add validated foundation package and sample case".

## Foundation handoff

After Task 5 passes, the package can be loaded as a text-only skill and the private-vault boundary is ready. The next plan adds note-first video indexing, optional extraction backends, platform adapters, visual rules, and cross-platform smoke tests.
