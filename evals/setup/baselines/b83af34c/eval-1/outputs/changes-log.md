# Changes Log

## Summary

All sections were added new — the existing CLAUDE.md had no Project Configuration section.

## Preserved (from existing CLAUDE.md)

- `# my-project` heading and project description
- `## Documentation` section with architecture and API links
- `## Getting Started` section with setup instructions

No existing configuration was modified or removed.

## Added

### `# Project Configuration` (new section)

Added top-level Project Configuration heading.

### `## Repository Registry` (new section)

Added repository registry table with two entries:

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend |
| trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui |

### `## Jira Configuration` (new section)

Added Jira configuration with all five fields:

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### `## Code Intelligence` (new section)

Added Code Intelligence section with:
- Tool naming convention documentation (`mcp__<instance>__<tool>`)
- Concrete example using `serena_backend` instance
- `### Limitations` subsection (no known limitations)

### `## Bug Configuration` (new section)

Added Bug Configuration section with:
- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

### `## Hierarchy Configuration` (new section)

Added Hierarchy Configuration section with:
- Default epic grouping strategy: by-sub-feature

## Skipped

- **Jira Field Defaults**: Not configured (MCP tools not available in simulation to discover priorities and fixVersions)
- **Security Configuration**: User declined to enable security triage
- **Constraints template**: Not copied (simulation mode — no file system modifications outside outputs/)
- **CONVENTIONS.md scaffolding**: Not performed (simulation mode)
- **Bug template copy**: Not performed (simulation mode)
