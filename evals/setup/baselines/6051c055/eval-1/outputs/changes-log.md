# Changes Log

## Summary

The existing CLAUDE.md had no `# Project Configuration` section. All configuration sections were newly created.

## Added

### `# Project Configuration` (new)
- Created top-level heading for project configuration.

### `## Repository Registry` (new)
- Added table with columns: Repository, Role, Serena Instance, Path.
- Added row for trustify-backend (serena_backend, Rust backend service, /home/user/trustify-backend).
- Added row for trustify-ui (serena_ui, TypeScript frontend, /home/user/trustify-ui).

### `## Jira Configuration` (new)
- Added Project key: TC
- Added Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Added Feature issue type ID: 10142
- Added Git Pull Request custom field: customfield_10875
- Added GitHub Issue custom field: customfield_10747

### `## Code Intelligence` (new)
- Added tool naming convention documentation (`mcp__<instance>__<tool>`).
- Added concrete example using serena_backend instance.
- Added `### Limitations` subheading with note that no limitations are known.

### `## Bug Configuration` (new)
- Added Bug issue type ID: 10001
- Added Bug template: docs/bug-template.md
- Added Bug-to-Task link type: Blocks

## Preserved

- All existing content in the original CLAUDE.md (project title, Documentation section, Getting Started section) is preserved. The Project Configuration section would be appended at the end.

## Skipped

- **Hierarchy Configuration**: Skipped (requires MCP discovery which was not performed).
- **Jira Field Defaults**: Skipped (requires MCP discovery which was not performed).
- **Security Configuration**: Skipped (user declined to enable security triage).
- **Bug template file copy**: Skipped (simulation mode).
- **Constraints template copy**: Skipped (simulation mode).
- **CONVENTIONS.md scaffolding**: Skipped (simulation mode).
