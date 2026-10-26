# Changes Log

## Preserved (from existing CLAUDE.md)

- Project title: `# my-project`
- Documentation section: links to architecture.md and api.md
- Getting Started section: clone, npm install, npm start instructions

Note: The existing CLAUDE.md content is preserved as-is. The Project Configuration section is appended as a new section.

## Added

### `# Project Configuration` (new section)

The entire Project Configuration section was created from scratch since none existed.

### `## Repository Registry` (new)

Added table with two repositories:

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend |
| trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui |

### `## Jira Configuration` (new)

Added with all five fields:
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### `## Code Intelligence` (new)

Added with:
- Tool naming convention documentation (`mcp__<instance>__<tool>`)
- Concrete example using `serena_backend` instance
- `### Limitations` subsection: no known limitations

### `## Bug Configuration` (new)

Added with all three required fields:
- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

### `## Hierarchy Configuration` (new)

Added with:
- Default epic grouping strategy: by-sub-feature

## Not Added

### `### Jira Field Defaults`

Not created -- requires MCP or REST API auto-discovery of available priorities and fixVersions, which is not available in this simulation.

### `## Security Configuration`

Not created -- user declined to enable security triage for this project.

### `docs/constraints.md`

Not copied -- simulation mode, no file system operations outside outputs/.

### `CONVENTIONS.md` files

Not scaffolded -- simulation mode, no file system operations outside outputs/.
