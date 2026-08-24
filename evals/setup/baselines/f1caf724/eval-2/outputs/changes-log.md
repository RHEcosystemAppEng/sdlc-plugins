# Changes Log

Summary of what was added versus preserved in the Project Configuration.

## Preserved (no changes)

### Repository Registry -- trustify-backend row
- Existing entry preserved as-is: trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend

### Jira Configuration
- All fields preserved as-is:
  - Project key: TC
  - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
  - Feature issue type ID: 10142
  - Git Pull Request custom field: customfield_10875
  - GitHub Issue custom field: customfield_10747

### Code Intelligence -- main section
- Tool naming convention explanation preserved
- `serena_backend` example preserved
- Existing limitation for `serena_backend` preserved: "rust-analyzer may take 30-60 seconds to index on first use"

### Bug Configuration
- All fields preserved as-is:
  - Bug issue type ID: 10001
  - Bug template: docs/bug-template.md
  - Bug-to-Task link type: Blocks

## Added

### Repository Registry -- trustify-ui row (NEW)
- Added new row: trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui
- Source: Serena instance `serena_ui` discovered in MCP tool listing; user provided repository name, role, and path

### Code Intelligence -- Limitations -- serena_ui entry (NEW)
- Added limitation entry: `serena_ui`: No known limitations
- Source: User confirmed no known limitations for the new Serena instance

## Not configured (skipped)

### Jira Field Defaults
- Not present in existing configuration
- Skipped: requires MCP tool calls to discover available priorities and fixVersions (not available in simulated run)

### Hierarchy Configuration
- Not present in existing configuration
- Skipped: requires MCP tool calls to discover issue type hierarchy (not available in simulated run)

### Security Configuration
- Not present in existing configuration
- Skipped: user declined when asked whether to enable security triage

### Constraints Template (docs/constraints.md)
- Skipped: cannot check or write filesystem in simulated run

### CONVENTIONS.md Scaffolding
- Skipped: cannot check or write filesystem in simulated run
