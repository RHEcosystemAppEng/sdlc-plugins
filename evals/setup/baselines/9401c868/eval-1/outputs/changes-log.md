# Changes Log

## Summary

All sections are **new additions** -- the existing CLAUDE.md (`claude-md-empty.md`) had no `# Project Configuration` section.

## Preserved Content

The following existing content in CLAUDE.md was preserved unchanged:

- `# my-project` heading and description
- `## Documentation` section with architecture and API links
- `## Getting Started` section with setup instructions

## Added Sections

### 1. `# Project Configuration` (new)

Top-level heading added to contain all configuration subsections.

### 2. `## Repository Registry` (new)

Added table with two rows:

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend |
| trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui |

### 3. `## Jira Configuration` (new)

Added with five fields:

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

Note: `### Jira Field Defaults` subsection was not added because MCP was unavailable to discover available priorities and fixVersions.

### 4. `## Code Intelligence` (new)

Added with:

- Tool naming convention explanation (`mcp__<instance>__<tool>`)
- Concrete example using `serena_backend` instance
- `### Limitations` subheading with note that no limitations are known

### 5. `## Bug Configuration` (new)

Added with three fields:

- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

Note: Bug template file was not copied (simulation mode).

### 6. `## Hierarchy Configuration` (new)

Added with one field:

- Default epic grouping strategy: by-sub-feature

## Skipped Sections

### `## Security Configuration`

Not added -- user declined to enable security triage for this project.

### `### Jira Field Defaults`

Not added -- MCP unavailable to discover priorities and fixVersions; no user input provided for simulation.

### `docs/constraints.md`

Not copied -- simulation mode (no file system modifications outside outputs/).

### `CONVENTIONS.md` scaffolding

Not scaffolded -- simulation mode (no file system modifications outside outputs/).
