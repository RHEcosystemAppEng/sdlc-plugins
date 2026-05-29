# Changes Log

## Preserved Content

- All existing content from claude-md-empty.md is preserved (project heading, documentation links, getting started section). The Project Configuration section is appended; nothing was removed or modified.

## Added Content

### `# Project Configuration` (new section -- appended to CLAUDE.md)

All subsections below are entirely new (greenfield -- no prior Project Configuration existed).

### `## Repository Registry` (new)

Added repository registry table with two entries:

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend |
| trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui |

### `## Jira Configuration` (new)

Added all five Jira configuration fields:

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### `## Code Intelligence` (new)

Added code intelligence section with:

- Tool naming convention explanation (`mcp__<instance>__<tool>`)
- Concrete example using `serena_backend` instance
- `### Limitations` subheading noting no known limitations
