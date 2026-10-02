# Relationship Adviser

Relationship Adviser is a portable, text-first skill for practical relationship decisions. The platform-independent rules live in `core/`; schemas and sanitized examples are public package content. Personal profiles, private cases, decision history, and raw media indexes belong in `private-vault/` and remain local.

The original media files stay in the user's MediaCrawler directory. This repository stores derived notes, timestamps, claims, and source indexes by reference rather than copying media.

The initial package is documentation-first and has no model or network dependency. Platform adapters load the same core rules and provide capability fallbacks for Codex, Claude Code, and WorkBuddy.

## Knowledge map

- `knowledge/README.md`: knowledge-base navigation and loading order.
- `knowledge/notes/`: verified research cards, with DOI, review status, usable claims, and limits.
- `knowledge/books/`: verified book metadata and rules for using L2 material.
- `knowledge/legal/`: official-law indexes and practical legal checklists.
- `knowledge/playbooks/`: action sequences, scripts, reaction branches, and stop conditions derived from named evidence.
- `knowledge/verified-sources.md`: public source register and verification depth.
- `knowledge/rejected-sources.md`: retracted or disqualified sources that must not be reused.
- `private-vault/`: local-only profile, personal cases, video notes, and media indexes; ignored by Git except for its README.
