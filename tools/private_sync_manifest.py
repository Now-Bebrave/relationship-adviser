"""Create a local-only integrity manifest for private-vault files."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


def build_manifest(root: Path, output: Path) -> dict[str, object]:
    files: list[dict[str, object]] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.resolve() == output.resolve():
            continue
        content = path.read_bytes()
        files.append({"path": path.relative_to(root).as_posix(), "size": len(content), "sha256": hashlib.sha256(content).hexdigest()})
    return {"version": 1, "content_included": False, "files": files}


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: python tools/private_sync_manifest.py PRIVATE_ROOT OUTPUT.json")
        return 2
    root, output = Path(argv[1]), Path(argv[2])
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(build_manifest(root, output), ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

