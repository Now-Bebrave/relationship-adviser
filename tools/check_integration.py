from pathlib import Path
import json
import sys

PROJECT_ROOT = Path(__file__).parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tools.validate_package import validate


def check_integration(root: Path) -> list[str]:
    errors = validate(root)
    manifest_path = root / "adapters" / "manifest.json"
    if not manifest_path.exists():
        return errors + ["missing adapters/manifest.json"]
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("output_protocol") != "core/output.md":
        errors.append("adapter manifest does not use core/output.md")
    for platform, config in manifest.get("platforms", {}).items():
        entry = root / config["entry"]
        if not entry.exists():
            errors.append(f"missing adapter entry: {platform}")
        elif "../../core/output.md" not in entry.read_text(encoding="utf-8"):
            errors.append(f"adapter does not reference shared output: {platform}")
    for relative in ("visuals/diagram-rules.md", "visuals/illustration-rules.md", "examples/visuals/reaction-branch.md"):
        if not (root / relative).exists():
            errors.append(f"missing visual fallback path: {relative}")
    return errors


def main() -> int:
    errors = check_integration(PROJECT_ROOT)
    if errors:
        print("\n".join(errors))
        return 1
    print("integration validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
