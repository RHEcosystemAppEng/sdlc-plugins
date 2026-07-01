# Changes Log

## Summary

All sections were newly created since the existing CLAUDE.md had no Project Configuration section.

## Added

### Project Configuration (new)
- Created `# Project Configuration` heading

### Repository Registry (new)
- Added table with 2 repositories:
  - `trustify-backend` -- Rust backend service, Serena instance `serena_backend`, path `/home/user/trustify-backend`
  - `trustify-ui` -- TypeScript frontend, Serena instance `serena_ui`, path `/home/user/trustify-ui`

### Jira Configuration (new)
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### Code Intelligence (new)
- Documented `mcp__<instance>__<tool>` naming convention
- Added concrete example using `serena_backend` instance
- Added `### Limitations` subheading with note that no limitations are known

### Bug Configuration (new)
- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

### Hierarchy Configuration (new)
- Default epic grouping strategy: by-sub-feature

## Preserved

- All existing CLAUDE.md content was preserved:
  - `# my-project` heading and description
  - `## Documentation` section with architecture and API links
  - `## Getting Started` section with setup instructions

## Skipped

- Jira Field Defaults: Not configured (MCP discovery of priorities/fixVersions not performed in simulation)
- Security Configuration: User declined to enable security triage
- Bug template file copy: Skipped per simulation instructions
- Constraints template copy: Not performed (simulation mode)
- CONVENTIONS.md scaffolding: Not performed (simulation mode)
