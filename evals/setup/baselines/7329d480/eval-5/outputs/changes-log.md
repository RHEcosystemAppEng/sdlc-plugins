# Setup Changes Log

All sections below were **newly added** to CLAUDE.md (no prior Project Configuration existed).

## Sections Added

### 1. `# Project Configuration`
- Top-level heading created

### 2. `## Repository Registry`
- Added table with 2 repositories:
  - `backend` (Rust backend service, serena_backend, /home/user/backend)
  - `frontend-ui` (TypeScript frontend, serena_ui, /home/user/frontend-ui)

### 3. `## Jira Configuration`
- Added 5 fields:
  - Project key: TC
  - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
  - Feature issue type ID: 10142
  - Git Pull Request custom field: customfield_10875
  - GitHub Issue custom field: customfield_10747

### 4. `## Code Intelligence`
- Added naming convention documentation (`mcp__<instance>__<tool>`)
- Added example using `serena_backend` instance
- Added `### Limitations` subsection (no known limitations)

### 5. `## Bug Configuration`
- Added 3 fields:
  - Bug issue type ID: 10001
  - Bug template: docs/bug-template.md
  - Bug-to-Task link type: Blocks

### 6. `## Security Configuration`
- Added `### Product Lifecycle` subsection with 5 fields:
  - Product pages URL: https://access.example.com/product-lifecycle
  - Jira version prefix: MYPRODUCT
  - Vulnerability issue type ID: 10200
  - Component label pattern: pscomponent:
  - VEX Justification custom field: customfield_12345
- Added `### Version Streams` subsection with 1 stream:
  - 2.1.x (git.downstream.example.com/my-org/product-release.2.1.z)
- Added `### Source Repositories` subsection with 2 repositories:
  - backend (https://github.com/example/backend, upstream)
  - frontend-ui (https://github.com/example/frontend-ui, upstream)
