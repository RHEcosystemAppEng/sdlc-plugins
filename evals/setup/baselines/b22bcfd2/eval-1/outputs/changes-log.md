# Changes Log

## Summary

The existing CLAUDE.md had no `# Project Configuration` section. All configuration sections were created new.

## Added

### `# Project Configuration` (new)
- Top-level heading added to structure all project-specific configuration.

### `## Repository Registry` (new)
- Added table with 2 rows:
  - trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend
  - trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui

### `## Jira Configuration` (new)
- Added 5 fields:
  - Project key: TC
  - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
  - Feature issue type ID: 10142
  - Git Pull Request custom field: customfield_10875
  - GitHub Issue custom field: customfield_10747

### `## Code Intelligence` (new)
- Added tool naming convention explanation with `mcp__<instance>__<tool>` pattern.
- Added concrete example using `serena_backend` instance.
- Added `### Limitations` subheading — no limitations reported for either instance.

### `## Bug Configuration` (new)
- Added 3 fields:
  - Bug issue type ID: 10001
  - Bug template: docs/bug-template.md
  - Bug-to-Task link type: Blocks

### `## Hierarchy Configuration` (new)
- Added 1 field:
  - Default epic grouping strategy: by-sub-feature

## Preserved

- All existing content in CLAUDE.md (project description, documentation links, getting started section) was preserved.
- No sections were removed or overwritten.

## Skipped

- `### Jira Field Defaults` — not scaffolded (MCP-based field discovery not available in simulation).
- `## Security Configuration` — user declined to enable security triage.
- `docs/constraints.md` copy — skipped (simulation, no file operations).
- `CONVENTIONS.md` scaffolding — skipped (simulation, no file operations).
- Bug template file copy — skipped (simulation).
