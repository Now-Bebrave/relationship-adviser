# Relationship Adviser

Relationship Adviser is a portable, text-first skill for practical relationship decisions. The platform-independent rules live in `core/`; schemas and sanitized examples are public package content. Personal profiles, private cases, decision history, and raw media indexes belong in `private-vault/` and remain local.

The original media files stay in the user's MediaCrawler directory. This repository stores derived notes, timestamps, claims, and source indexes by reference rather than copying media.

The initial package is documentation-first and has no model or network dependency. Platform adapters load the same core rules and provide capability fallbacks for Codex, Claude Code, and WorkBuddy.
