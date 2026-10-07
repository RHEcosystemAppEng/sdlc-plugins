# Changes Log

## Summary

2 changes applied to the Project Configuration. All existing entries preserved intact.

## Added

### Repository Registry

- **Added row**: `trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui`
  - Source: Serena instance `serena_ui` discovered in MCP tool listing, user provided repository details

### Code Intelligence — Limitations

- **Added entry**: `serena_ui`: No known limitations
  - Source: User confirmed no known limitations for the new Serena instance

## Preserved (Unchanged)

### Repository Registry

- **Preserved row**: `trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend`

### Jira Configuration

- **Preserved**: Project key: TC
- **Preserved**: Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Preserved**: Feature issue type ID: 10142
- **Preserved**: Git Pull Request custom field: customfield_10875
- **Preserved**: GitHub Issue custom field: customfield_10747

### Code Intelligence

- **Preserved**: Tool naming convention documentation (`mcp__<instance>__<tool>`)
- **Preserved**: `serena_backend` usage example (find_symbol call)
- **Preserved**: `serena_backend` limitation entry (rust-analyzer may take 30-60 seconds to index on first use)

### Bug Configuration

- **Preserved**: Bug issue type ID: 10001
- **Preserved**: Bug template: docs/bug-template.md
- **Preserved**: Bug-to-Task link type: Blocks

## Not Configured (Skipped)

### Jira Field Defaults

- **Reason**: Auto-discovery requires Atlassian MCP calls (`getJiraIssueTypeMetaWithFields`) which are unavailable in simulation mode. No user input was specified for manual fallback.

### Hierarchy Configuration

- **Reason**: Auto-discovery requires Atlassian MCP calls (`getJiraProjectIssueTypesMetadata`) which are unavailable in simulation mode. No user input was specified for manual hierarchy entry.

### Security Configuration

- **Reason**: User declined when asked whether to enable security triage for this project.

### Constraints Template (docs/constraints.md)

- **Reason**: Simulation mode — cannot verify or write files outside the outputs directory.

### CONVENTIONS.md Scaffolding

- **Reason**: Simulation mode — cannot check filesystem at repository paths. No user input specified for scaffolding preference.
