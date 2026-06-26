# Setup Changes Log

## Changes Made

### Added: `# Project Configuration`

Top-level Project Configuration section added to CLAUDE.md.

### Added: `## Repository Registry`

Added Repository Registry table with 2 entries:

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| backend | Rust backend service | serena_backend | /home/user/backend |
| frontend-ui | TypeScript frontend | serena_ui | /home/user/frontend-ui |

### Added: `## Jira Configuration`

Added Jira Configuration with 5 fields:

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### Added: `## Code Intelligence`

Added Code Intelligence section with:
- Tool naming convention: `mcp__<instance>__<tool>`
- Example using serena_backend instance
- Limitations subsection (no limitations known)

### Added: `## Bug Configuration`

Added Bug Configuration with 3 fields:

- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

### Added: `## Security Configuration`

Added Security Configuration with three subsections:

**Product Lifecycle:**
- Product pages URL: https://access.example.com/product-lifecycle
- Jira version prefix: MYPRODUCT
- Vulnerability issue type ID: 10200
- Component label pattern: pscomponent:
- VEX Justification custom field: customfield_12345

**Version Streams (1 entry):**
- 2.1.x: git.downstream.example.com/my-org/product-release.2.1.z

**Source Repositories (2 entries):**
- backend: https://github.com/example/backend
- frontend-ui: https://github.com/example/frontend-ui
