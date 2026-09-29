# Relationship Adviser Ingestion and Adapters Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add resource-efficient video-to-text ingestion, local media indexing, Codex/Claude Code/WorkBuddy adapters, and visual-output rules on top of the foundation package.

**Architecture:** Text notes and subtitles are the first ingestion source. Existing notes use notes_only or notes_plus_images; incomplete notes use targeted spot checks; full audio/OCR extraction is selected only when no useful text is available. Adapters point to the same core files and expose capability fallbacks instead of duplicating reasoning rules.

**Tech Stack:** Markdown, JSON/YAML, Python 3.11+ standard library, optional locally installed media tools discovered during implementation, Mermaid.

**Spec:** docs/superpowers/specs/2026-09-29-relationship-adviser-design.md

## Global Constraints

- Preserve the extraction modes notes_only, notes_plus_images, notes_plus_spotcheck, and full_video.
- Do not parse a full video when complete usable notes or subtitles exist.
- Keep original media in the user's MediaCrawler directory; store paths, hashes, timestamps, and derived text in the private vault.
- Every extracted claim must retain source location and time range where available.
- An adapter may map tools but may not redefine the core decision protocol.
- Mermaid and image output must have Markdown/table fallbacks.
- Do not upload source media or private notes to external services.

---

### Task 1: Build the note-first video-card normalizer

**Files:**
- Create: tools/normalize_video_notes.py
- Create: tests/fixtures/video-notes/sample-notes.md
- Test: tests/test_normalize_video_notes.py

**Interfaces:**
- normalize_notes(source: Path, metadata: dict) -> dict returns a video-card dictionary with extraction_mode, transcript, claims, playbook, and limits.
- The CLI accepts --source, --output, --platform, --author, and --mode; it supports notes_only and notes_plus_images in this task.

- [ ] Step 1: Write the failing normalizer tests

Test that a note with headings 观点, 话术, 对方反应, and 限制 produces structured fields and preserves a timestamp such as [00:01:12-00:01:35].

- [ ] Step 2: Run the tests to verify failure

Run: python -m unittest discover -s tests -p "test_normalize_video_notes.py" -v

Expected: FAIL because normalize_video_notes.py does not exist.

- [ ] Step 3: Implement the parser with no third-party dependencies

Parse Markdown headings and timestamp ranges with re. Preserve unrecognized paragraphs under transcript instead of discarding them. Reject unsupported modes with a clear ValueError naming the accepted modes.

- [ ] Step 4: Run the normalizer tests

Run: python -m unittest discover -s tests -p "test_normalize_video_notes.py" -v

Expected: PASS and the output matches video-card.schema.json field names.

- [ ] Step 5: Commit the note-first ingestion

Run: git add tools/normalize_video_notes.py tests/fixtures/video-notes tests/test_normalize_video_notes.py && git commit -m "feat: normalize text-first video notes".

### Task 2: Add MediaCrawler indexing and targeted extraction planning

**Files:**
- Create: tools/index_media.py
- Create: tools/extraction_plan.py
- Create: tests/fixtures/media-index/clip.mp4
- Test: tests/test_media_index.py
- Test: tests/test_extraction_plan.py

**Interfaces:**
- index_media(root: Path) -> list[dict] returns path, size_bytes, modified_at, sha256, and media_type without copying media.
- choose_extraction_mode(has_notes: bool, notes_complete: bool, has_images: bool, conflict: bool) -> str returns one of the four approved modes.

- [ ] Step 1: Write tests for indexing and mode selection

Cover these cases: complete notes → notes_only; notes plus screenshots → notes_plus_images; incomplete notes → notes_plus_spotcheck; no notes → full_video; conflicting notes and media → notes_plus_spotcheck.

- [ ] Step 2: Run the tests to verify failure

Run: python -m unittest discover -s tests -p "test_media_index.py" -v
Run: python -m unittest discover -s tests -p "test_extraction_plan.py" -v

Expected: FAIL because both modules are absent.

- [ ] Step 3: Implement path-only indexing

Walk only the configured MediaCrawler directory, hash files in chunks, and write a JSON index to private-vault/source-index/media-index.json. Do not copy, delete, or upload media.

- [ ] Step 4: Implement deterministic extraction-mode selection

Encode the decision table in choose_extraction_mode; keep it independent from any ASR or OCR provider.

- [ ] Step 5: Run the indexing and mode tests

Run: python -m unittest discover -s tests -p "test_media_index.py" -v
Run: python -m unittest discover -s tests -p "test_extraction_plan.py" -v

Expected: PASS.

- [ ] Step 6: Commit the indexer

Run: git add tools/index_media.py tools/extraction_plan.py tests && git commit -m "feat: index local media and choose minimal extraction mode".

### Task 3: Add optional full-video provider contracts

**Files:**
- Create: tools/video_extractors.py
- Create: tools/providers/README.md
- Create: tests/test_video_extractor_contract.py

**Interfaces:**
- VideoExtractor.extract(path: Path) -> dict returns timestamped transcript segments and OCR segments.
- get_extractor() -> VideoExtractor either returns a configured local provider or raises RuntimeError that names the missing local capability and points to the notes-first path.

- [ ] Step 1: Write the provider contract test

Assert that a fake provider can return {transcript: [], ocr: []} and that the default provider failure is explicit and does not silently claim extraction succeeded.

- [ ] Step 2: Run the test to verify failure

Run: python -m unittest discover -s tests -p "test_video_extractor_contract.py" -v

Expected: FAIL because the provider contract is absent.

- [ ] Step 3: Implement the provider protocol and fake-provider test double

Keep the core package dependency-free. Provider discovery may use an executable configured by the adapter, but it must return the same timestamped structure.

- [ ] Step 4: Run the contract test

Run: python -m unittest discover -s tests -p "test_video_extractor_contract.py" -v

Expected: PASS.

- [ ] Step 5: Commit the provider contract

Run: git add tools/video_extractors.py tools/providers tests/test_video_extractor_contract.py && git commit -m "feat: define optional video extraction provider contract".

### Task 4: Add platform adapters

**Files:**
- Create: adapters/README.md
- Create: adapters/manifest.json
- Create: adapters/codex/SKILL.md
- Create: adapters/claude-code/SKILL.md
- Create: adapters/workbuddy/SKILL.md
- Test: tests/test_adapters.py

**Interfaces:**
- adapters/manifest.json maps each platform to core/mission.md, core/output.md, profile_path, and capability fallback names.
- Each adapter entry loads the same core files and states the same output headings.

- [ ] Step 1: Verify each platform's current skill-discovery convention

Record the verified entry filename and installation path in adapters/README.md. If a platform cannot be verified offline, document the tested portable Markdown entry and mark the platform-specific installation as a manual integration check; do not invent a tool API.

- [ ] Step 2: Write adapter consistency tests

Test that all three adapter files reference core/mission.md and core/output.md, contain read_profile and search_knowledge, and do not contain a second copy of the decision skeleton.

- [ ] Step 3: Add the shared manifest and adapter entries

Keep platform-specific content limited to loading instructions, local path configuration, capability mapping, and fallback behavior.

- [ ] Step 4: Run adapter tests

Run: python -m unittest discover -s tests -p "test_adapters.py" -v

Expected: PASS.

- [ ] Step 5: Commit the adapters

Run: git add adapters tests/test_adapters.py && git commit -m "feat: add portable platform adapters".

### Task 5: Add visual-output rules and fallback fixtures

**Files:**
- Create: visuals/diagram-rules.md
- Create: visuals/illustration-rules.md
- Create: examples/visuals/reaction-branch.mmd
- Create: examples/visuals/reaction-branch.md
- Test: tests/test_visual_rules.py

**Interfaces:**
- Mermaid diagrams are fenced with mermaid and include a text summary.
- Image requests include purpose, alt text, source, and a Markdown/table fallback.

- [ ] Step 1: Write visual-rule tests

Assert that the Mermaid fixture contains a reaction branch and that the Markdown fixture states the same branch in text.

- [ ] Step 2: Run the tests to verify failure

Run: python -m unittest discover -s tests -p "test_visual_rules.py" -v

Expected: FAIL because the visual rules and fixtures are absent.

- [ ] Step 3: Add the rules and fixtures

Document triggers for visual output: more than two reaction branches, multiple time points, three or more options, or an abstract concept that benefits from a diagram. State that visual output never replaces the conclusion.

- [ ] Step 4: Run the visual tests

Run: python -m unittest discover -s tests -p "test_visual_rules.py" -v

Expected: PASS.

- [ ] Step 5: Commit the visual rules

Run: git add visuals examples/visuals tests/test_visual_rules.py && git commit -m "feat: add visual output and text fallback rules".

### Task 6: Run the cross-platform integration check

**Files:**
- Create: tests/fixtures/scenarios/bride-price.md
- Create: tools/check_integration.py
- Test: tests/test_integration.py

**Interfaces:**
- check_integration(root: Path) -> list[str] verifies core links, schema contracts, adapter references, extraction-mode handling, visual fallback, and the sanitized case.

- [ ] Step 1: Add the fixed scenario fixture

Use the sanitized bride-price scenario with no private names, local paths, or copied source screenshots.

- [ ] Step 2: Write the integration test

Assert that the validator reports no errors and that every adapter references the same core/output.md.

- [ ] Step 3: Implement the integration checker

Compose the existing validators and return one error per failed contract; do not call an external model or network service.

- [ ] Step 4: Run all tests

Run: python -m unittest discover -s tests -v

Expected: PASS.

- [ ] Step 5: Commit the cross-platform check

Run: git add tools/check_integration.py tests && git commit -m "test: add cross-platform package integration checks".

### Task 7: Prepare the GitHub backup

**Files:**
- Modify: .git/config through Git commands only
- Modify: README.md

- [ ] Step 1: Configure the supplied remote locally

Run: git remote add origin https://github.com/Now-Bebrave/adviser.git

If origin already exists, run: git remote set-url origin https://github.com/Now-Bebrave/adviser.git

- [ ] Step 2: Verify the branch and local history

Run:

~~~powershell
git branch --show-current
git log --oneline -5
git status --short
~~~

Expected: the implementation branch is named main, all planned commits are present, and the working tree is clean.

- [ ] Step 3: Show the exact backup command before pushing

Run: git push -u origin main only after the user has been told the local validation passed and the push is ready. Do not include private-vault files in the push.

## Ingestion and adapters handoff

Completion of Task 6 gives a locally validated package with note-first video handling, media indexing, optional extraction contracts, portable adapters, and visual fallbacks. Task 7 is the final backup step for the supplied GitHub repository.
