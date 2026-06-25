# Changes Log

## Summary

All sections were **added** (none preserved) since the existing CLAUDE.md had no `# Project Configuration` section.

## Added

### `# Project Configuration`

Top-level heading created.

### `## Repository Registry`

New table with two rows:

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend |
| trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui |

### `## Jira Configuration`

New section with all required and optional fields:

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### `## Code Intelligence`

New section with:

- Tool naming convention (`mcp__<instance>__<tool>`)
- Example using `serena_backend` instance
- `### Limitations` subsection — no limitations reported

### `## Bug Configuration`

New section with:

- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

### `## Hierarchy Configuration`

New section with:

- Default epic grouping strategy: by-sub-feature

## Preserved

- All existing content from `claude-md-empty.md` (`# my-project`, `## Documentation`, `## Getting Started`) is preserved. The `# Project Configuration` section would be appended after the existing content.

## Skipped

- **Jira Field Defaults** (`### Jira Field Defaults`): Not configured — auto-discovery of priorities and fixVersions was not performed in simulation mode.
- **Security Configuration** (`## Security Configuration`): User declined to enable security triage.
- **Constraints document** (`docs/constraints.md`): Not written — output restricted to `outputs/` directory.
- **CONVENTIONS.md**: Not scaffolded — output restricted to `outputs/` directory.
- **Bug template file** (`docs/bug-template.md`): Not written — output restricted to `outputs/` directory.
