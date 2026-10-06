# Changes Log

## Summary

Incremental update to existing Project Configuration. One new Serena instance (serena_ui) was discovered and added to the Registry and Code Intelligence sections. All existing configuration was preserved unchanged.

## Changes Made

### Repository Registry

- **ADDED** row: `trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui`
- **PRESERVED** row: `trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend`

### Code Intelligence — Limitations

- **ADDED** entry: `serena_ui: No known limitations`
- **PRESERVED** entry: `serena_backend: rust-analyzer may take 30-60 seconds to index on first use`

## Sections Preserved (No Changes)

### Jira Configuration

All fields preserved as-is:
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### Code Intelligence (body)

Preserved the existing tool naming convention explanation and serena_backend example. No modifications to the section body.

### Bug Configuration

All fields preserved as-is:
- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

## Sections Not Created

### Jira Field Defaults

Not created. Requires Atlassian MCP discovery (`getJiraIssueTypeMetaWithFields`) to fetch available priorities and fixVersions. MCP tool invocation was not available in this run.

### Hierarchy Configuration

Not created. Requires Atlassian MCP discovery (`getJiraProjectIssueTypesMetadata`) to determine the project's issue type hierarchy. MCP tool invocation was not available in this run.

### Security Configuration

Not created. User declined when asked whether to enable security triage for this project.
