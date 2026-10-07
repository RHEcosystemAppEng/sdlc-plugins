# Changes Log

## Summary

The CLAUDE.md file (`claude-md-empty.md`) had no existing `# Project Configuration` section. All configuration sections were created new. No existing content was modified or removed.

## Added

### `# Project Configuration` (new top-level section)

Appended at the end of the existing CLAUDE.md content.

### `## Repository Registry` (new)

Added table with two repository entries:

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend |
| trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui |

### `## Jira Configuration` (new)

Added all five fields:

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### `## Code Intelligence` (new)

Added:
- Tool naming convention explanation with `mcp__<instance>__<tool>` pattern
- Concrete example using `serena_backend` instance
- `### Limitations` subheading with note that no limitations are known

### `## Bug Configuration` (new)

Added all three fields:

- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

### `## Hierarchy Configuration` (new)

Added:
- Default epic grouping strategy: by-sub-feature

## Preserved

- `# my-project` heading and description
- `## Documentation` section (architecture.md, api.md links)
- `## Getting Started` section (clone, npm install, npm start instructions)

## Skipped

- **Jira Field Defaults**: Not created -- priorities and fixVersions could not be auto-discovered without live MCP calls. Can be added in a subsequent setup run.
- **Security Configuration**: User declined to enable security triage.
- **Constraints template**: Skipped (simulation mode -- no file copy to target project).
- **CONVENTIONS.md scaffolding**: Skipped (simulation mode -- no file operations on target repositories).
- **Bug template file copy**: Skipped (simulation mode -- as specified by task).
