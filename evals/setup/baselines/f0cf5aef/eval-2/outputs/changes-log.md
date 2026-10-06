# Setup Changes Log

## Summary

Incremental update to existing Project Configuration. One new Serena instance (serena_ui / trustify-ui) was discovered and added. All existing configuration was preserved.

## Changes Made

### Repository Registry

- **Added**: `trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui`
- **Preserved**: `trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend`

### Code Intelligence — Limitations

- **Added**: `serena_ui`: No limitations known
- **Preserved**: `serena_backend`: rust-analyzer may take 30-60 seconds to index on first use

## Sections Preserved (No Changes)

### Jira Configuration

All fields preserved as-is:
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### Code Intelligence (body)

Naming convention explanation and example preserved as-is. Only the Limitations subsection was updated.

### Bug Configuration

All fields preserved as-is:
- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

## Sections Not Created

### Jira Field Defaults

Not created — requires Atlassian MCP auto-discovery (getJiraIssueTypeMetaWithFields) which was not available in this run. Can be configured in a future setup run.

### Hierarchy Configuration

Not created — requires Atlassian MCP auto-discovery (getJiraProjectIssueTypesMetadata) which was not available in this run. Can be configured in a future setup run.

### Security Configuration

Not created — user declined to enable security triage when prompted.
