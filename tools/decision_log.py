"""Append an explicitly authorized private decision record."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


ALLOWED = {"question", "recommendation", "steps", "review_at", "status"}


def sanitize_record(data: dict[str, object]) -> dict[str, object]:
    record = {key: data[key] for key in ALLOWED if key in data}
    if not record.get("question") or not record.get("recommendation"):
        raise ValueError("question and recommendation are required")
    record["saved_at"] = datetime.now(timezone.utc).isoformat()
    return record


def main(argv: list[str]) -> int:
    if len(argv) != 4 or argv[3] != "--consent":
        print("explicit --consent is required")
        return 2
    output, source = Path(argv[1]), Path(argv[2])
    record = sanitize_record(json.loads(source.read_text(encoding="utf-8")))
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

