# Changes Log

## Summary

Incremental update to an existing Project Configuration. One new Serena instance (serena_ui) was discovered and integrated. All existing configuration was preserved.

## Preserved (no changes)

### Repository Registry -- existing row
- `trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend` -- preserved as-is

### Jira Configuration -- all fields
- Project key: TC -- preserved
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432 -- preserved
- Feature issue type ID: 10142 -- preserved
- Git Pull Request custom field: customfield_10875 -- preserved
- GitHub Issue custom field: customfield_10747 -- preserved

### Code Intelligence -- existing content
- Tool naming convention explanation (`mcp__<instance>__<tool>`) -- preserved
- Code example using serena_backend -- preserved
- Limitations entry for serena_backend (rust-analyzer indexing) -- preserved

### Bug Configuration -- all fields
- Bug issue type ID: 10001 -- preserved
- Bug template: docs/bug-template.md -- preserved
- Bug-to-Task link type: Blocks -- preserved

## Added

### Repository Registry -- new row
- `trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui` -- added for newly discovered serena_ui instance

### Code Intelligence -- Limitations
- `serena_ui`: No known limitations -- added for newly discovered instance

## Not scaffolded

### Jira Field Defaults
- Not present in existing configuration
- Requires Atlassian MCP calls to discover available priorities and fixVersions
- Not scaffolded in this simulation (MCP tools not invoked)

### Hierarchy Configuration
- Not present in existing configuration
- Requires Atlassian MCP calls to discover issue type hierarchy
- Not scaffolded in this simulation (MCP tools not invoked)

### Security Configuration
- Not present in existing configuration
- User declined when asked whether to enable security triage
- Not scaffolded per user choice
