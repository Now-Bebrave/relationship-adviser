"""Render dependency-free, accessible SVG decision cards for mobile viewing."""
from __future__ import annotations

import html
import json
import sys
from pathlib import Path


KINDS = {"timeline", "risk", "responsibility", "cost", "decision"}
COLORS = {"low": "#2f855a", "medium": "#b7791f", "high": "#c53030"}


def _escape(value: object) -> str:
    return html.escape(str(value), quote=True)


def _wrap(text: object, limit: int = 26) -> list[str]:
    value = str(text).strip()
    return [value[i:i + limit] for i in range(0, len(value), limit)] or [""]


def render_svg(data: dict[str, object]) -> str:
    kind = str(data.get("type", ""))
    if kind not in KINDS:
        raise ValueError(f"type must be one of {sorted(KINDS)}")
    for field in ("title", "conclusion", "items", "next_step", "alt_text"):
        if not data.get(field):
            raise ValueError(f"missing required field: {field}")
    items = data["items"]
    if not isinstance(items, list) or not items:
        raise ValueError("items must be a non-empty list")

    row_height = 150
    height = max(1200, 530 + len(items) * row_height)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="{height}" viewBox="0 0 1080 {height}">',
        f'<title>{_escape(data["title"])}</title>',
        f'<desc>{_escape(data["alt_text"])}</desc>',
        '<rect width="1080" height="100%" fill="#f7fafc"/>',
        '<rect x="60" y="60" width="960" height="210" rx="28" fill="#1a365d"/>',
        f'<text x="100" y="130" fill="white" font-size="42" font-weight="700">{_escape(data["title"])}</text>',
    ]
    y = 185
    for line in _wrap(data["conclusion"], 34):
        parts.append(f'<text x="100" y="{y}" fill="#e2e8f0" font-size="28">{_escape(line)}</text>')
        y += 38

    y = 330
    for index, item in enumerate(items, 1):
        if not isinstance(item, dict):
            raise ValueError("each item must be an object")
        label = item.get("label", f"{index}")
        value = item.get("value", "")
        level = str(item.get("level", "low"))
        accent = COLORS.get(level, "#2b6cb0") if kind == "risk" else "#2b6cb0"
        parts.extend([
            f'<rect x="60" y="{y}" width="960" height="120" rx="22" fill="white" stroke="#cbd5e0" stroke-width="2"/>',
            f'<circle cx="125" cy="{y + 60}" r="34" fill="{accent}"/>',
            f'<text x="125" y="{y + 70}" text-anchor="middle" fill="white" font-size="24" font-weight="700">{_escape(index)}</text>',
            f'<text x="180" y="{y + 43}" fill="#2d3748" font-size="26" font-weight="700">{_escape(label)}</text>',
        ])
        line_y = y + 82
        for line in _wrap(value, 39)[:2]:
            parts.append(f'<text x="180" y="{line_y}" fill="#4a5568" font-size="24">{_escape(line)}</text>')
            line_y += 30
        if kind == "risk":
            parts.append(f'<text x="930" y="{y + 43}" text-anchor="end" fill="{accent}" font-size="22" font-weight="700">{_escape(level.upper())}</text>')
        y += row_height

    parts.extend([
        f'<rect x="60" y="{y + 10}" width="960" height="170" rx="24" fill="#edf2f7"/>',
        f'<text x="100" y="{y + 65}" fill="#1a365d" font-size="27" font-weight="700">下一步</text>',
    ])
    line_y = y + 108
    for line in _wrap(data["next_step"], 38)[:2]:
        parts.append(f'<text x="100" y="{line_y}" fill="#2d3748" font-size="25">{_escape(line)}</text>')
        line_y += 32
    parts.append('</svg>')
    return "\n".join(parts)


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: python tools/render_decision_visual.py INPUT.json OUTPUT.svg")
        return 2
    data = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    output = Path(argv[2])
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_svg(data), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

