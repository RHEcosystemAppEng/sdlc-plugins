# Changes Log

Summary of what was added versus preserved in the Project Configuration.

## Added

### Repository Registry
- **New row**: trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui
  - Source: Discovered serena_ui Serena instance in MCP tool listing (10 tools with `mcp__serena_ui__` prefix). Repository details provided by user.

## Preserved (No Changes)

### Repository Registry
- **Existing row**: trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend
  - Reason: Already in Registry, matching discovered serena_backend instance.

### Jira Configuration
- Project key: TC — preserved
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432 — preserved
- Feature issue type ID: 10142 — preserved
- Git Pull Request custom field: customfield_10875 — preserved
- GitHub Issue custom field: customfield_10747 — preserved
- Reason: All required and optional fields already populated. No changes needed.

### Code Intelligence
- Naming convention explanation (`mcp__<instance>__<tool>`) — preserved
- serena_backend example code block — preserved
- Limitations subsection heading — preserved
- `serena_backend` limitation entry (rust-analyzer indexing delay) — preserved
- Reason: Generic naming convention already covers the newly added serena_ui instance. User reported no known limitations for serena_ui, so no new limitation entries were added.

### Bug Configuration
- Bug issue type ID: 10001 — preserved
- Bug template: docs/bug-template.md — preserved
- Bug-to-Task link type: Blocks — preserved
- Reason: All three required fields fully populated with no placeholder markers.

## Skipped (Not Configured)

### Jira Field Defaults
- Not present in existing configuration
- Skipped: Required MCP tool (`getJiraIssueTypeMetaWithFields`) not available in current tool listing. Can be configured in a future setup run.

### Hierarchy Configuration
- Not present in existing configuration
- Skipped: Required MCP tool (`getJiraProjectIssueTypesMetadata`) not available in current tool listing for issue type hierarchy discovery. Can be configured in a future setup run.

### Security Configuration
- Not present in existing configuration
- Skipped: User declined when asked whether to enable security triage for this project.

### Constraints Template (docs/constraints.md)
- Not checked or written (eval simulation mode — no filesystem modifications outside outputs/).

### CONVENTIONS.md Scaffolding
- Not checked or written for either repository (eval simulation mode — no filesystem modifications outside outputs/).
