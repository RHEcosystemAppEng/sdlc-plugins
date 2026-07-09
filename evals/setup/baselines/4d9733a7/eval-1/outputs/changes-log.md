# Changes Log

## Summary

The existing CLAUDE.md had no `# Project Configuration` section. All configuration sections were created new. No existing content was modified or removed.

## Preserved (unchanged)

- Original CLAUDE.md content: project title (`# my-project`), description, `## Documentation` section, `## Getting Started` section — all preserved as-is. The Project Configuration section would be appended after the existing content.

## Added

### `# Project Configuration` (new top-level section)

The entire section was created from scratch, containing the following subsections:

### `## Repository Registry` (new)

Added a table with 2 repositories:

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend |
| trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui |

### `## Jira Configuration` (new)

Added 5 configuration fields:
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

Note: `### Jira Field Defaults` subsection was not scaffolded (no priority/fixVersion values provided during simulation).

### `## Code Intelligence` (new)

Added:
- Tool naming convention explanation (`mcp__<instance>__<tool>`)
- Concrete example using `serena_backend` instance
- `### Limitations` subheading — no limitations reported

### `## Bug Configuration` (new)

Added 3 configuration fields:
- Bug issue type ID: 10001
- Bug template: docs/bug-template.md (linked)
- Bug-to-Task link type: Blocks

### `## Hierarchy Configuration` (new)

Added 1 configuration field:
- Default epic grouping strategy: by-sub-feature

## Not Added (skipped)

- `### Jira Field Defaults` — not scaffolded (no MCP tool calls in simulation; no values provided)
- `## Security Configuration` — user declined to enable security triage
- `docs/constraints.md` — skipped (simulation mode, no file writes to target project)
- `CONVENTIONS.md` files — skipped (simulation mode, no file writes to target repositories)
- Bug template file — skipped per task instructions (simulation)
