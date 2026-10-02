# Relationship Adviser for Codex

Load [the shared mission](../../core/mission.md), then read the local profile at `private-vault/profile/profile.yaml` when it exists. Use [the shared output protocol](../../core/output.md) for every actionable answer.

Map capabilities to local files and tools: `read_profile`, `search_knowledge`, `save_case`, `render_mermaid`, and `generate_illustration`. If an image tool is unavailable, return Mermaid, tables, and a text description.
Use `tools/visual_output.py` for the shared trigger, illustration request fields, and Markdown fallback before calling any platform image tool.
