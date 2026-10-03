from pathlib import Path
import json
import re
import sys


REQUIRED_PATHS = (
    "core/mission.md",
    "core/intake.md",
    "core/reasoning.md",
    "core/evidence.md",
    "core/communication.md",
    "core/domains.md",
    "core/output.md",
    "core/voice.md",
    "core/profile-policy.md",
    "knowledge-schema/source.schema.json",
    "knowledge-schema/video-card.schema.json",
    "knowledge-schema/case.schema.json",
    "knowledge-schema/decision.schema.json",
    "knowledge/sources.yaml",
    "knowledge/verified-sources.md",
    "knowledge/rejected-sources.md",
    "knowledge/books/verified-catalog.md",
    "knowledge/legal/2024-bride-price-judicial-interpretation.md",
    "knowledge/legal/bride-price-negotiation-and-evidence-checklist.md",
    "knowledge/legal/civil-code-marriage-family.md",
    "knowledge/legal/anti-domestic-violence-law.md",
    "examples/knowledge-seed.md",
    "examples/cases/bride-price-family-negotiation.md",
    "adapters/workbuddy/MOBILE_PROMPT.md",
    "docs/mobile-and-voice.md",
)

OUTPUT_LABELS = (
    "结论", "判断依据", "详细执行步骤", "对方可能反应",
    "对应回答和下一步", "停止条件", "备选方案", "信心与信息缺口",
)


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    for relative in REQUIRED_PATHS:
        if not (root / relative).exists():
            errors.append(f"missing required path: {relative}")

    mission_path = root / "core" / "mission.md"
    if mission_path.exists():
        mission = mission_path.read_text(encoding="utf-8")
        for name in ("intake", "reasoning", "evidence", "communication", "domains", "output"):
            if f"({name}.md)" not in mission:
                errors.append(f"core/mission.md does not link {name}.md")

    output_path = root / "core" / "output.md"
    if output_path.exists():
        output = output_path.read_text(encoding="utf-8")
        for label in OUTPUT_LABELS:
            if label not in output:
                errors.append(f"core/output.md is missing label: {label}")

    video_schema_path = root / "knowledge-schema" / "video-card.schema.json"
    if video_schema_path.exists():
        try:
            schema = json.loads(video_schema_path.read_text(encoding="utf-8"))
            modes = set(schema["properties"]["extraction_mode"]["enum"])
            expected = {"notes_only", "notes_plus_images", "notes_plus_spotcheck", "full_video"}
            if modes != expected:
                errors.append("video-card extraction modes do not match the approved contract")
        except (json.JSONDecodeError, KeyError, TypeError) as exc:
            errors.append(f"invalid video-card schema: {exc}")

    examples_root = root / "examples"
    if examples_root.exists():
        absolute_path = re.compile(r"(?:[A-Za-z]:[\\/]|/Users/|/home/)")
        for path in examples_root.rglob("*"):
            if path.is_file() and absolute_path.search(path.read_text(encoding="utf-8")):
                errors.append(f"example contains an absolute local path: {path}")
    return errors


def main() -> int:
    errors = validate(Path(__file__).parents[1])
    if errors:
        print("\n".join(errors))
        return 1
    print("package validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
