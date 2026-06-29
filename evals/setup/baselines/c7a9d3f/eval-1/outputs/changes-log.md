# Changes Log

## Summary

All sections were newly created — the existing CLAUDE.md had no Project Configuration section.

## Added

### `# Project Configuration` (new)
- Created top-level heading for all project configuration subsections

### `## Repository Registry` (new)
- Added table with 2 repository entries:
  - trustify-backend (Rust backend service, Serena instance: serena_backend, path: /home/user/trustify-backend)
  - trustify-ui (TypeScript frontend, Serena instance: serena_ui, path: /home/user/trustify-ui)

### `## Jira Configuration` (new)
- Added all 5 configuration fields:
  - Project key: TC
  - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
  - Feature issue type ID: 10142
  - Git Pull Request custom field: customfield_10875
  - GitHub Issue custom field: customfield_10747

### `## Code Intelligence` (new)
- Added tool naming convention documentation with `mcp__<instance>__<tool>` pattern
- Added concrete example using `serena_backend` instance
- Added `### Limitations` subsection with note that no limitations are known

### `## Bug Configuration` (new)
- Added all 3 configuration fields:
  - Bug issue type ID: 10001
  - Bug template: docs/bug-template.md
  - Bug-to-Task link type: Blocks

### `## Hierarchy Configuration` (new)
- Added default epic grouping strategy: by-sub-feature

## Preserved

- All existing CLAUDE.md content (project title, documentation links, getting-started section) — not included in the output file since the task only requested the Project Configuration section

## Skipped

- `### Jira Field Defaults` — not created; no field default values were provided in the simulation inputs
- `## Security Configuration` — not created; user declined to enable security triage
- Bug template file copy — skipped per simulation instructions
- `docs/constraints.md` — not copied; simulation mode (no file system operations beyond outputs/)
- `CONVENTIONS.md` scaffolding — not performed; simulation mode (no file system operations beyond outputs/)
