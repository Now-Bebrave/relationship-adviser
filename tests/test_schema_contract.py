import json
from pathlib import Path
import unittest


ROOT = Path(__file__).parents[1]


class SchemaContractTests(unittest.TestCase):
    def test_all_json_schemas_parse(self) -> None:
        for path in (ROOT / "knowledge-schema").glob("*.json"):
            with self.subTest(path=path):
                json.loads(path.read_text(encoding="utf-8"))

    def test_required_schema_keys_exist(self) -> None:
        expected = {
            "source.schema.json": {"title", "type", "source", "evidence_level", "confidence", "application", "limits"},
            "video-card.schema.json": {"title", "source", "topic", "evidence_level", "extraction_mode", "transcript", "claims", "playbook", "limits"},
            "case.schema.json": {"title", "context", "goal", "actions", "reactions", "result", "limits"},
            "decision.schema.json": {"question", "priority", "recommendation", "steps", "stop_conditions", "review"},
        }
        for filename, keys in expected.items():
            schema = json.loads((ROOT / "knowledge-schema" / filename).read_text(encoding="utf-8"))
            self.assertTrue(keys.issubset(set(schema["required"])))

    def test_video_extraction_modes_are_complete(self) -> None:
        schema = json.loads((ROOT / "knowledge-schema" / "video-card.schema.json").read_text(encoding="utf-8"))
        modes = set(schema["properties"]["extraction_mode"]["enum"])
        self.assertEqual(modes, {"notes_only", "notes_plus_images", "notes_plus_spotcheck", "full_video"})

    def test_source_register_declares_candidate_status(self) -> None:
        register = (ROOT / "knowledge" / "sources.yaml").read_text(encoding="utf-8")
        self.assertIn('verification_status: "candidate"', register)
        self.assertIn("relationship science", register)
