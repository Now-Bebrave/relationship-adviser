from __future__ import annotations

from pathlib import Path
from typing import Protocol


class VideoExtractor(Protocol):
    def extract(self, path: Path) -> dict:
        """Return timestamped transcript and OCR segments."""


class MissingVideoExtractor:
    def extract(self, path: Path) -> dict:
        raise RuntimeError(
            "No local ASR/OCR provider is configured for full_video extraction; "
            "provide notes/subtitles or configure a local provider."
        )


def get_extractor() -> VideoExtractor:
    return MissingVideoExtractor()
