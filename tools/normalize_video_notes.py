from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


SUPPORTED_MODES = {"notes_only", "notes_plus_images"}
TIMESTAMP = re.compile(r"\[(\d{2}:\d{2}:\d{2})-(\d{2}:\d{2}:\d{2})\]")
SECTION_MAP = {
    "观点": "claims",
    "主张": "claims",
    "话术": "scripts",
    "对方反应": "expected_reactions",
    "回应": "responses",
    "限制": "limits",
}


def normalize_notes(source: Path, metadata: dict) -> dict:
    mode = metadata.get("extraction_mode", "notes_only")
    if mode not in SUPPORTED_MODES:
        raise ValueError(f"unsupported mode {mode!r}; use notes_only or notes_plus_images")
    text = source.read_text(encoding="utf-8")
    sections: dict[str, list[str]] = {key: [] for key in SECTION_MAP.values()}
    transcript: list[dict] = []
    current = "transcript"
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        heading = re.sub(r"^#+\s*", "", line)
        if line.startswith("#"):
            current = SECTION_MAP.get(heading, "transcript")
            continue
        match = TIMESTAMP.search(line)
        if match:
            transcript.append({"start": match.group(1), "end": match.group(2), "text": TIMESTAMP.sub("", line).strip()})
        elif current == "transcript":
            transcript.append({"text": line})
        else:
            sections[current].append(line.lstrip("- "))
    return {
        "title": metadata.get("title", source.stem),
        "source": {key: metadata[key] for key in ("platform", "url", "local_path", "author") if key in metadata},
        "topic": metadata.get("topic", ""),
        "evidence_level": metadata.get("evidence_level", "L3"),
        "extraction_mode": mode,
        "transcript": transcript,
        "claims": [{"claim": item} for item in sections["claims"]],
        "playbook": {
            "goal": metadata.get("goal", ""),
            "steps": [],
            "scripts": sections["scripts"],
            "expected_reactions": sections["expected_reactions"],
            "responses": sections["responses"],
            "stop_conditions": [],
        },
        "limits": sections["limits"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--platform", default="")
    parser.add_argument("--author", default="")
    parser.add_argument("--mode", default="notes_only")
    args = parser.parse_args()
    card = normalize_notes(args.source, {"platform": args.platform, "author": args.author, "extraction_mode": args.mode})
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(card, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
