# Changes Log

Summary of what was added versus preserved during setup.

## Added

### Repository Registry
- **Added row**: `trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui`
  - Source: Newly discovered `serena_ui` Serena instance from MCP tool listing, with user-provided metadata.

### Code Intelligence > Limitations
- **Added entry**: `` `serena_ui`: No known limitations ``
  - Source: User confirmed no known limitations for the new Serena instance.

## Preserved (unchanged)

### Repository Registry
- **Preserved row**: `trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend`
  - Existing entry retained as-is.

### Jira Configuration
- **Preserved**: Project key: TC
- **Preserved**: Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Preserved**: Feature issue type ID: 10142
- **Preserved**: Git Pull Request custom field: customfield_10875
- **Preserved**: GitHub Issue custom field: customfield_10747
  - All fields already populated; no changes needed.

### Code Intelligence
- **Preserved**: Tool naming convention explanation and `serena_backend` example
- **Preserved**: `serena_backend` limitation entry (rust-analyzer indexing note)
  - Existing content retained; only the new `serena_ui` limitation was appended.

### Bug Configuration
- **Preserved**: Bug issue type ID: 10001
- **Preserved**: Bug template: docs/bug-template.md
- **Preserved**: Bug-to-Task link type: Blocks
  - All fields already populated; no changes needed.

### Non-configuration content
- **Preserved**: `# trustify-backend` heading and `## Documentation` section
  - Content above `# Project Configuration` was retained verbatim.

## Skipped (not created)

### Jira Field Defaults
- **Not created**: Requires MCP discovery (`getJiraIssueTypeMetaWithFields`) to fetch available priorities and fixVersions. Simulated run cannot call MCP tools.

### Hierarchy Configuration
- **Not created**: Requires MCP discovery (`getJiraProjectIssueTypesMetadata`) to list issue type hierarchy. Simulated run cannot call MCP tools.

### Security Configuration
- **Not created**: User declined when asked whether to enable security triage.

### Constraints Template (docs/constraints.md)
- **Not written**: Simulation does not modify target project files. Would be scaffolded from `constraints.template.md` in a live run.

### CONVENTIONS.md
- **Not written**: Simulation does not modify target project files. Would be offered for scaffolding in each repository in a live run.
