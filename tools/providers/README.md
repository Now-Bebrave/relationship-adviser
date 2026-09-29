# Optional video providers

The foundation keeps ASR and OCR optional. A local provider must implement:

```python
class VideoExtractor:
    def extract(self, path: Path) -> dict:
        return {"transcript": [], "ocr": []}
```

Every segment must preserve a start time, end time, and text. Providers run against local media and must not upload source files.
