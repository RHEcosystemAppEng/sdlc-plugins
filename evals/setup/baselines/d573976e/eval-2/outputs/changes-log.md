# Changes Log

## Summary

Incremental update to an existing Project Configuration. One new Serena instance discovered and added.

## Added

### Repository Registry
- Added row: `trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui`

## Preserved (no changes)

### Repository Registry
- Preserved existing row: `trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend`

### Jira Configuration
- Preserved: Project key: TC
- Preserved: Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Preserved: Feature issue type ID: 10142
- Preserved: Git Pull Request custom field: customfield_10875
- Preserved: GitHub Issue custom field: customfield_10747

### Code Intelligence
- Preserved: Tool naming convention documentation
- Preserved: `serena_backend` example
- Preserved: `serena_backend` limitation under `### Limitations`

### Bug Configuration
- Preserved: Bug issue type ID: 10001
- Preserved: Bug template: docs/bug-template.md
- Preserved: Bug-to-Task link type: Blocks

## Skipped

### Jira Field Defaults
- Not scaffolded: requires MCP tool calls (`getJiraIssueTypeMetaWithFields`) to discover available priorities and fixVersions. MCP invocation not available in this run.

### Hierarchy Configuration
- Not scaffolded: requires MCP tool calls (`getJiraProjectIssueTypesMetadata`) to discover issue type hierarchy levels. MCP invocation not available in this run.

### Security Configuration
- Not scaffolded: user declined when asked whether to enable security triage.

### Constraints Template (Step 7)
- Skipped: simulated environment, cannot check or write to target project filesystem.

### CONVENTIONS.md (Step 8)
- Skipped: simulated environment, cannot check or write to target project filesystem.
