from __future__ import annotations

from collections.abc import Iterable


def should_render_visual(*, branches: int, timepoints: int, options: int, abstract: bool) -> bool:
    """Return whether a diagram or illustration materially improves comprehension."""
    return branches > 2 or timepoints > 1 or options >= 3 or abstract


def build_illustration_request(
    purpose: str,
    alt_text: str,
    source: str,
    prompt: str,
    fallback: str,
) -> dict[str, str]:
    fields = {
        "purpose": purpose,
        "alt_text": alt_text,
        "source": source,
        "prompt": prompt,
        "fallback": fallback,
    }
    if any(not value.strip() for value in fields.values()):
        raise ValueError("purpose, alt_text, source, prompt, and fallback are required")
    return fields


def render_text_fallback(title: str, branches: Iterable[tuple[str, str]]) -> str:
    rows = list(branches)
    if not title.strip() or not rows:
        raise ValueError("title and at least one branch are required")
    lines = [f"### {title}", "", "| 情况 | 下一步 |", "|---|---|"]
    lines.extend(f"| {condition} | {action} |" for condition, action in rows)
    return "\n".join(lines)

