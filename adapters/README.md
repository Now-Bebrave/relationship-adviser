# Platform adapters

All adapters load the same files: ../../core/mission.md and ../../core/output.md. They expose local profile and knowledge paths, then fall back to Markdown, tables, and Mermaid when a platform tool is unavailable.

The entry filenames are portable Markdown wrappers. Platform-specific installation paths should be verified in each target environment before publishing a release.
