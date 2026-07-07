# Changes Log

## Preserved (from existing CLAUDE.md)

The following sections from the original CLAUDE.md were preserved unchanged:

- `# my-project` heading and project description
- `## Documentation` section with architecture and API links
- `## Getting Started` section with setup instructions

## Newly Added

The following sections were newly added as the `# Project Configuration` block:

### Repository Registry
- Added table with 2 entries: backend (serena_backend) and frontend-ui (serena_ui)

### Jira Configuration
- Added all 5 fields: Project key (TC), Cloud ID, Feature issue type ID (10142), Git Pull Request custom field (customfield_10875), GitHub Issue custom field (customfield_10747)

### Code Intelligence
- Added Serena naming convention documentation (`mcp__<instance>__<tool>`)
- Added example usage with serena_backend
- Added Limitations subsection (no limitations known)

### Bug Configuration
- Added Bug issue type ID: 10001
- Added Bug template: docs/bug-template.md
- Added Bug-to-Task link type: Blocks

### Security Configuration
- **Newly added** -- user opted in to security triage configuration
- Added Product Lifecycle subsection with all 5 fields:
  - Product pages URL: https://access.example.com/product-lifecycle
  - Jira version prefix: MYPRODUCT
  - Vulnerability issue type ID: 10200
  - Component label pattern: pscomponent:
  - VEX Justification custom field: customfield_12345
- Added Version Streams table with 1 stream (2.1.x)
- Added Source Repositories table with 2 repositories (backend, frontend-ui)
- Skipped supportability matrix population (user declined)
- Skipped security-matrix.md scaffolding (user declined)
