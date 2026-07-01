# Changes Log

## Summary

2 changes applied, all other existing configuration preserved.

## Added

### Repository Registry — new row

Added `trustify-ui` to the Repository Registry table:

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui |

Source: Discovered `serena_ui` Serena instance from MCP tool listing. Instance was not present in the existing Registry. User provided repository name, role, and path.

### Code Intelligence — Limitations — new entry

Added limitation entry for `serena_ui`:

```
- `serena_ui`: No known limitations
```

Source: User confirmed no known limitations for the `serena_ui` Serena instance.

## Preserved (no changes)

### Repository Registry — existing row

Preserved `trustify-backend` row exactly as-is:

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend |

### Jira Configuration

Preserved all fields exactly as-is:
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### Code Intelligence — body text

Preserved the tool naming convention explanation and `serena_backend` example exactly as-is.

### Code Intelligence — Limitations — existing entry

Preserved `serena_backend` limitation exactly as-is:
- `serena_backend`: rust-analyzer may take 30-60 seconds to index on first use

### Bug Configuration

Preserved all fields exactly as-is:
- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

### Non-configuration content

Preserved all content above `# Project Configuration`:
- `# trustify-backend` heading
- `## Documentation` section with links

## Not scaffolded

### Jira Field Defaults

Not created. Requires MCP or REST API access to discover available priorities and fixVersions. MCP tools were not called per eval constraints.

### Hierarchy Configuration

Not created. Requires MCP or REST API access to discover Jira issue type hierarchy. MCP tools were not called per eval constraints.

### Security Configuration

Not created. User declined when asked whether to enable security triage.
