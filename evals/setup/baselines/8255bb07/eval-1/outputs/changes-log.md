# Changes Log

## Preserved (unchanged)

- Project title: `# my-project`
- `## Documentation` section — preserved as-is
- `## Getting Started` section — preserved as-is

## Added

### `# Project Configuration` (new top-level section)

The entire Project Configuration section was added since none existed in the original CLAUDE.md.

### `## Repository Registry` (new)

Added repository registry table with 2 entries:

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend |
| trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui |

### `## Jira Configuration` (new)

Added Jira configuration with 5 fields:
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### `## Code Intelligence` (new)

Added Code Intelligence section with:
- Tool naming convention explanation (`mcp__<instance>__<tool>`)
- Concrete example using `serena_backend` instance
- `### Limitations` subsection noting no known limitations

### `## Bug Configuration` (new)

Added Bug Configuration section with 3 fields:
- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

### `## Hierarchy Configuration` (new)

Added Hierarchy Configuration section with:
- Default epic grouping strategy: by-sub-feature

## Not Added

### `### Jira Field Defaults`

Not added — MCP tools were not called (simulation mode), so available priorities and fixVersions could not be discovered.

### `## Security Configuration`

Not added — user declined to enable security triage for this project.

### `docs/constraints.md`

Not created — simulation mode, no file writes to project directories.

### `CONVENTIONS.md` files

Not created — simulation mode, no file writes to project directories.

### Bug template file (`docs/bug-template.md`)

Not created — simulation mode, bug template file copy was skipped per task instructions.
