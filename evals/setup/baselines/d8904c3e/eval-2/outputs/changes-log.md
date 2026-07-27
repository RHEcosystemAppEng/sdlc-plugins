# Changes Log

Summary of what was added versus preserved in the Project Configuration.

## Added

### Repository Registry
- **Added row**: `trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui`
  - Discovered serena_ui as a new Serena instance from MCP tool listing
  - User provided repository name, role, and path

### Code Intelligence -- Limitations
- **Added entry**: `serena_ui: No known limitations`
  - User confirmed no known limitations for the new Serena instance

## Preserved (No Changes)

### Repository Registry
- **Preserved row**: `trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend`
  - Already present in existing configuration; not modified

### Jira Configuration
- **Preserved all fields** (already fully populated):
  - Project key: TC
  - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
  - Feature issue type ID: 10142
  - Git Pull Request custom field: customfield_10875
  - GitHub Issue custom field: customfield_10747

### Code Intelligence
- **Preserved section body**: naming convention explanation and serena_backend example
- **Preserved limitation**: `serena_backend: rust-analyzer may take 30-60 seconds to index on first use`

### Bug Configuration
- **Preserved all fields** (already fully populated):
  - Bug issue type ID: 10001
  - Bug template: docs/bug-template.md
  - Bug-to-Task link type: Blocks

### Non-Configuration Content
- **Preserved**: `# trustify-backend` heading and `## Documentation` section (above Project Configuration)

## Skipped (Not Created)

| Section | Reason |
|---|---|
| Jira Field Defaults | MCP tools not available for auto-discovery of priorities and fixVersions |
| Hierarchy Configuration | MCP tools not available for issue type hierarchy discovery |
| Security Configuration | User declined when asked whether to enable security triage |
| docs/constraints.md | Eval constraint: no filesystem writes outside outputs/ |
| CONVENTIONS.md | Eval constraint: no filesystem writes outside outputs/ |
