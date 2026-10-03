"""Turn a note/transcript into a reviewable, privacy-aware case draft."""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path


ABSOLUTE_PATH = re.compile(r"(?:[A-Za-z]:[\\/]|/Users/|/home/)")
PHONE = re.compile(r"(?<!\d)(?:\+?86[- ]?)?1[3-9]\d{9}(?!\d)")
EMAIL = re.compile(r"\b[^\s@]+@[^\s@]+\.[^\s@]+\b")
PREFIXES = {"事实": "fact", "观点": "claim", "推测": "inference", "未知": "unknown"}


def classify_line(line: str) -> dict[str, str]:
    clean = line.strip().lstrip("- ")
    match = re.match(r"^\[?(事实|观点|推测|未知)\]?(?:[:：]\s*|\s+)(.*)$", clean)
    if match:
        return {"kind": PREFIXES[match.group(1)], "text": match.group(2).strip()}
    return {"kind": "unclassified", "text": clean}


def privacy_flags(text: str) -> list[str]:
    flags: list[str] = []
    if ABSOLUTE_PATH.search(text):
        flags.append("absolute_path")
    if PHONE.search(text):
        flags.append("phone_number")
    if EMAIL.search(text):
        flags.append("email")
    return flags


def fingerprint(text: str) -> str:
    normalized = re.sub(r"\s+", " ", text.strip().lower())
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:16]


def build_draft(source: Path, metadata: dict[str, object]) -> dict[str, object]:
    text = source.read_text(encoding="utf-8")
    lines = [classify_line(line) for line in text.splitlines() if line.strip() and not line.lstrip().startswith("#")]
    flags = privacy_flags(text)
    return {
        "case_id": metadata.get("case_id", f"draft-{fingerprint(text)}"),
        "source": {key: metadata[key] for key in ("platform", "url", "author", "published_at") if key in metadata},
        "topic": metadata.get("topic", ""),
        "extraction_mode": metadata.get("extraction_mode", "notes_only"),
        "content": lines,
        "fingerprint": fingerprint(text),
        "privacy_flags": flags,
        "routing": "private_review" if flags else "public_review",
        "review_required": True,
    }


def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print("usage: python tools/case_pipeline.py SOURCE.txt OUTPUT.json [--platform douyin]")
        return 2
    source, output = Path(argv[1]), Path(argv[2])
    metadata: dict[str, object] = {}
    if len(argv) >= 5 and argv[3] == "--platform":
        metadata["platform"] = argv[4]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(build_draft(source, metadata), ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
