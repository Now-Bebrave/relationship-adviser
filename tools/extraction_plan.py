from __future__ import annotations


MODES = {"notes_only", "notes_plus_images", "notes_plus_spotcheck", "full_video"}


def choose_extraction_mode(
    has_notes: bool,
    notes_complete: bool,
    has_images: bool,
    conflict: bool,
) -> str:
    if conflict:
        return "notes_plus_spotcheck"
    if has_notes and notes_complete:
        return "notes_plus_images" if has_images else "notes_only"
    if has_notes:
        return "notes_plus_spotcheck"
    return "full_video"
