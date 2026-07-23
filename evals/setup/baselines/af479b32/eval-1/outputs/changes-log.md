# Changes Log

## Preserved (existing content)

The following content from the original CLAUDE.md was preserved without modification:

- `# my-project` heading and project description
- `## Documentation` section with architecture and API links
- `## Getting Started` section with setup instructions

## Added (new content)

The following sections were added as new content (none existed previously):

### `# Project Configuration` (new)

Top-level heading added to contain all configuration subsections.

### `## Repository Registry` (new)

Added table with 2 repositories:

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

### `## Code Intelligence` (new)

Added section with:
- Tool naming convention explanation (`mcp__<instance>__<tool>`)
- Concrete example using `serena_backend` instance
- `### Limitations` subheading noting no known limitations

### `## Bug Configuration` (new)

Added 3 configuration fields:

- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

### `## Hierarchy Configuration` (new)

Added 1 configuration field:

- Default epic grouping strategy: by-sub-feature

## Skipped (not created)

- `### Jira Field Defaults` — skipped (MCP calls not available in simulation to discover priorities/fixVersions)
- `## Security Configuration` — skipped (user declined to enable security triage)
- `docs/constraints.md` — skipped (simulation, no file modifications outside outputs/)
- `CONVENTIONS.md` files — skipped (simulation, no file modifications outside outputs/)
- Bug template file copy — skipped (simulation)
