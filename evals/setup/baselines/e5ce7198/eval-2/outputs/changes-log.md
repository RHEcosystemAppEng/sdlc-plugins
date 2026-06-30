# Changes Log

## Summary

Incremental update to existing Project Configuration. Two changes were made; all existing configuration was preserved.

## Changes Made

### 1. Repository Registry — added trustify-ui

**Added** new row for the newly discovered `serena_ui` instance:

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui |

### 2. Code Intelligence / Limitations — added serena_ui entry

**Added** limitation entry for the new Serena instance:

```
- `serena_ui`: No known limitations
```

## Preserved (no changes)

### Repository Registry — trustify-backend row
Existing entry preserved as-is:
- Repository: trustify-backend
- Role: Rust backend service
- Serena Instance: serena_backend
- Path: /home/user/trustify-backend

### Jira Configuration
All fields preserved as-is:
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### Code Intelligence — main section
Tool naming convention and example preserved as-is (using serena_backend example).

### Code Intelligence / Limitations — serena_backend entry
Existing limitation preserved as-is:
- `serena_backend`: rust-analyzer may take 30-60 seconds to index on first use

### Bug Configuration
All fields preserved as-is:
- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

### Non-configuration content
All content outside `# Project Configuration` preserved as-is:
- `# trustify-backend` heading
- `## Documentation` section with links

## Not Scaffolded

| Section | Reason |
|---|---|
| Jira Field Defaults | MCP discovery not available (simulated mode); no user input provided |
| Hierarchy Configuration | MCP discovery not available (simulated mode); no user input provided |
| Security Configuration | User declined to enable security triage |
| CONVENTIONS.md | Not part of this simulated run |
| docs/constraints.md | Not part of this simulated run |
