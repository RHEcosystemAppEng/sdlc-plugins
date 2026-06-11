# Changes Log

## Summary

This is a greenfield setup. The existing CLAUDE.md (`claude-md-empty.md`) had no `# Project Configuration` section. All configuration sections were created new.

## Added

### `# Project Configuration` (new section)

The entire section was created from scratch, including all subsections below.

### `## Repository Registry` (new)

Added table with 2 repositories:

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend |
| trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui |

### `## Jira Configuration` (new)

Added all 5 fields:

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### `## Code Intelligence` (new)

Added:
- Tool naming convention explanation (`mcp__<instance>__<tool>`)
- Concrete example using `serena_backend` instance
- `### Limitations` subheading with note that no limitations are known

## Preserved

- All existing content in `claude-md-empty.md` was preserved (project heading, Documentation section, Getting Started section).
- No existing entries were removed or overwritten.

## Skipped

- `## Security Configuration` — user declined security triage setup.
