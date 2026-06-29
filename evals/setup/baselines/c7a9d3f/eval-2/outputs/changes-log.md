# Changes Log

## Summary

Incremental update to existing Project Configuration. One new Serena instance (`serena_ui`) was discovered and added. All existing configuration was preserved without modification.

## Changes by Section

### Repository Registry

**Modified** — added 1 new row

| Action | Repository | Role | Serena Instance | Path |
|---|---|---|---|---|
| Preserved | trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend |
| **Added** | trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui |

### Jira Configuration

**Preserved** — no changes

All fields retained as-is:
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### Jira Field Defaults

**Not added** — requires MCP tool interaction to discover available priorities and fixVersions, which was not available in this simulation.

### Code Intelligence

**Modified** — updated Limitations subsection

- Preserved: Tool naming convention explanation and `serena_backend` example
- Preserved: `serena_backend` limitation (rust-analyzer indexing)
- **Added**: `serena_ui` limitation entry (no known limitations)

### Bug Configuration

**Preserved** — no changes

All fields retained as-is:
- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

### Hierarchy Configuration

**Not added** — requires MCP tool interaction to discover issue type hierarchy, which was not available in this simulation.

### Security Configuration

**Not added** — user declined when asked whether to enable security triage.
