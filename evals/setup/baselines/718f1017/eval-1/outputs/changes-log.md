# Changes Log

## Summary

The existing CLAUDE.md had no `# Project Configuration` section. All configuration sections were created from scratch. No existing content was modified or removed.

## Preserved Content

- Project title and description (`# my-project`, project overview)
- `## Documentation` section (architecture and API links)
- `## Getting Started` section (clone, install, start instructions)

## Added Sections

### 1. `# Project Configuration` (new)

Top-level heading added to contain all configuration subsections.

### 2. `## Repository Registry` (new)

Added a table with two repository entries:

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend |
| trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui |

### 3. `## Jira Configuration` (new)

Added five configuration fields:
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### 4. `## Code Intelligence` (new)

Added Serena tool naming convention documentation with:
- Tool prefix explanation (`mcp__<instance>__<tool>`)
- Concrete example using `serena_backend` instance
- `### Limitations` subheading noting no known limitations

### 5. `## Bug Configuration` (new)

Added three configuration fields:
- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

### 6. `## Hierarchy Configuration` (new)

Added one configuration field:
- Default epic grouping strategy: by-sub-feature

## Skipped Sections

- `### Jira Field Defaults` — not created (requires MCP discovery of available priorities and fixVersions, which could not be simulated)
- `## Security Configuration` — not created (user declined to enable security triage)
- `docs/constraints.md` — not copied (simulation mode, no file operations)
- `CONVENTIONS.md` scaffolding — not performed (simulation mode, no file operations)
- Bug template file copy — not performed (simulation mode)
