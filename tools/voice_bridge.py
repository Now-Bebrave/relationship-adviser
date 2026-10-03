"""Provider-neutral bridge for voice transcripts and spoken responses."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


SENSITIVE_TOKEN = re.compile(r"(?:\d+(?:\.\d+)?\s*(?:元|万|个月|年|天)|不|没有|拒绝|威胁|暴力|怀孕|债务)")


def build_voice_request(data: dict[str, object]) -> dict[str, object]:
    transcript = str(data.get("transcript", "")).strip()
    if not transcript:
        raise ValueError("transcript is required")
    confidence = data.get("confidence")
    review_tokens = sorted(set(SENSITIVE_TOKEN.findall(transcript)))
    low_confidence = isinstance(confidence, (int, float)) and float(confidence) < 0.85
    return {
        "source": "voice",
        "language": data.get("language", "zh-CN"),
        "transcript": transcript,
        "confidence": confidence,
        "needs_confirmation": low_confidence or bool(review_tokens),
        "review_tokens": review_tokens,
        "save_to_profile": False,
    }


def build_tts_request(data: dict[str, object]) -> dict[str, object]:
    text = str(data.get("spoken_text") or data.get("text") or "").strip()
    if not text:
        raise ValueError("spoken_text or text is required")
    return {"language": data.get("language", "zh-CN"), "spoken_text": text, "provider": "platform_or_local", "fallback": "display_text"}


def main(argv: list[str]) -> int:
    if len(argv) not in (3, 4):
        print("usage: python tools/voice_bridge.py INPUT.json OUTPUT.json [--response]")
        return 2
    data = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    result = build_tts_request(data) if len(argv) == 4 and argv[3] == "--response" else build_voice_request(data)
    Path(argv[2]).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

