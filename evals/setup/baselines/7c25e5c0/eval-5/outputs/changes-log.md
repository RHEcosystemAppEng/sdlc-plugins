# Changes Log

## Summary

All Project Configuration sections were **newly added** to the CLAUDE.md (greenfield setup — no prior Project Configuration existed).

## Sections Added

### Repository Registry (NEW)
- Added `backend` entry (Serena instance: serena_backend, Role: Rust backend service, Path: /home/user/backend)
- Added `frontend-ui` entry (Serena instance: serena_ui, Role: TypeScript frontend, Path: /home/user/frontend-ui)

### Jira Configuration (NEW)
- Added Project key: TC
- Added Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Added Feature issue type ID: 10142
- Added Git Pull Request custom field: customfield_10875
- Added GitHub Issue custom field: customfield_10747

### Code Intelligence (NEW)
- Added tool naming convention documentation (`mcp__<instance>__<tool>`)
- Added usage example using `serena_backend`
- Added Limitations subsection — no known limitations for either instance

### Bug Configuration (NEW)
- Added Bug issue type ID: 10001
- Added Bug template: docs/bug-template.md
- Added Bug-to-Task link type: Blocks

### Security Configuration (NEW)
- Added Product Lifecycle with 5 fields (Product pages URL, Jira version prefix, Vulnerability issue type ID, Component label pattern, VEX Justification custom field)
- Added Version Streams table with 1 stream (2.1.x)
- Added Source Repositories table with 2 repositories (backend, frontend-ui)

## Sections Preserved

- Pre-existing non-configuration content (project heading `# my-project`, Documentation section, Getting Started section) preserved from the original CLAUDE.md
