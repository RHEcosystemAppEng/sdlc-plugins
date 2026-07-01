# Changes Log

## Summary

The existing CLAUDE.md had no `# Project Configuration` section. All configuration sections were created from scratch. No existing content was modified or removed.

## Added

### `# Project Configuration` (new top-level section)

Added as a new section. The existing CLAUDE.md content (project title, Documentation, Getting Started) is preserved unchanged.

### `## Repository Registry` (new)

Added table with 2 rows:
- `trustify-backend` | Rust backend service | serena_backend | /home/user/trustify-backend
- `trustify-ui` | TypeScript frontend | serena_ui | /home/user/trustify-ui

### `## Jira Configuration` (new)

Added with 5 fields:
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### `## Code Intelligence` (new)

Added with:
- Tool naming convention explanation (`mcp__<instance>__<tool>`)
- Concrete example using `serena_backend` instance
- `### Limitations` subheading with note that no limitations are known

### `## Bug Configuration` (new)

Added with 3 fields:
- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

### `## Hierarchy Configuration` (new)

Added with 1 field:
- Default epic grouping strategy: by-sub-feature

## Preserved

- All existing CLAUDE.md content (project title, Documentation section, Getting Started section) -- unchanged
- No existing configuration entries were removed or overwritten

## Skipped

- `### Jira Field Defaults`: Not configured (MCP discovery of priorities/fixVersions not performed in simulation)
- `## Security Configuration`: User declined to enable security triage
- Bug template file copy: Skipped per simulation instructions
- `docs/constraints.md` copy: Not written (simulation mode -- only outputs/ files created)
- `CONVENTIONS.md` scaffolding: Not performed (simulation mode)
