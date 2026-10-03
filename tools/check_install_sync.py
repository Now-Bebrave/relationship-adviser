"""Compare public package files across local skill installations."""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path


EXCLUDED_PARTS = {".git", ".test-tmp", "__pycache__"}


def public_hashes(root: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file() or any(part in EXCLUDED_PARTS for part in path.parts):
            continue
        relative = path.relative_to(root).as_posix()
        if relative.startswith("private-vault/") and relative != "private-vault/README.md":
            continue
        result[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def compare(canonical: Path, targets: list[Path]) -> list[str]:
    expected = public_hashes(canonical)
    errors: list[str] = []
    for target in targets:
        actual = public_hashes(target)
        missing = sorted(expected.keys() - actual.keys())
        extra = sorted(actual.keys() - expected.keys())
        changed = sorted(path for path in expected.keys() & actual.keys() if expected[path] != actual[path])
        if missing or extra or changed:
            errors.append(f"{target}: missing={len(missing)} extra={len(extra)} changed={len(changed)}")
    return errors


def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print("usage: python tools/check_install_sync.py CANONICAL TARGET [TARGET ...]")
        return 2
    errors = compare(Path(argv[1]), [Path(value) for value in argv[2:]])
    if errors:
        print("\n".join(errors))
        return 1
    print("all installations match canonical source")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

