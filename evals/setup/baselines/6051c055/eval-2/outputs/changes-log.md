# Changes Log

## Summary

Incremental update to an existing Project Configuration. One new Serena instance (`serena_ui`) was discovered and added. All existing configuration was preserved unchanged.

## PRESERVED (unchanged)

### Repository Registry
- Row: `trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend` -- preserved exactly as-is

### Jira Configuration
- Project key: TC -- preserved
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432 -- preserved
- Feature issue type ID: 10142 -- preserved
- Git Pull Request custom field: customfield_10875 -- preserved
- GitHub Issue custom field: customfield_10747 -- preserved

### Code Intelligence
- Naming convention explanation (`mcp__<instance>__<tool>`) -- preserved
- Example using `serena_backend` -- preserved
- Limitation for `serena_backend` (rust-analyzer indexing) -- preserved

### Bug Configuration
- Bug issue type ID: 10001 -- preserved
- Bug template: docs/bug-template.md -- preserved
- Bug-to-Task link type: Blocks -- preserved

## ADDED (new content)

### Repository Registry
- New row: `trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui`

### Code Intelligence -- Limitations
- New entry: `serena_ui`: No known limitations

## NOT CONFIGURED (skipped)

### Jira Field Defaults
- Not present in existing configuration. Skipped -- requires MCP discovery of available priorities and fixVersions.

### Hierarchy Configuration
- Not present in existing configuration. Skipped -- requires MCP discovery of issue type hierarchy.

### Security Configuration
- Not present in existing configuration. User declined to enable security triage. Section was not created.
