# Changes Log

## Preserved (existing content)

- `# my-project` heading and description
- `## Documentation` section with architecture and API links
- `## Getting Started` section with setup instructions
- All existing content preserved verbatim; no modifications or removals

## Added

### `# Project Configuration` (new top-level section)

Appended at the end of the existing CLAUDE.md content.

### `## Repository Registry` (new)

Added table with 2 rows:
- trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend
- trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui

### `## Jira Configuration` (new)

Added 5 fields:
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

Note: `### Jira Field Defaults` subsection not added (MCP discovery unavailable in simulation mode).

### `## Code Intelligence` (new)

Added:
- Tool naming convention explanation (`mcp__<instance>__<tool>`)
- Concrete example using `serena_backend` instance
- `### Limitations` subsection noting no known limitations

### `## Bug Configuration` (new)

Added 3 fields:
- Bug issue type ID: 10001
- Bug template: docs/bug-template.md (linked)
- Bug-to-Task link type: Blocks

### `## Hierarchy Configuration` (new)

Added 1 field:
- Default epic grouping strategy: by-sub-feature

## Not Added

- `### Jira Field Defaults` — skipped (requires MCP discovery of available priorities and fixVersions)
- `## Security Configuration` — user declined enablement
- `docs/constraints.md` — skipped (simulation mode, no file writes outside outputs/)
- `CONVENTIONS.md` in target repositories — skipped (simulation mode)
- Bug template file (`docs/bug-template.md`) — skipped (simulation mode)
