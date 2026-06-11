# Changes Log

## Sections Added

### 1. Project Configuration (top-level heading)

- Added `# Project Configuration` as new top-level section.

### 2. Repository Registry

- Added `## Repository Registry` table with 2 repositories:
  - `backend` -- Rust backend service (serena_backend, /home/user/backend)
  - `frontend-ui` -- TypeScript frontend (serena_ui, /home/user/frontend-ui)

### 3. Jira Configuration

- Added `## Jira Configuration` with all fields:
  - Project key: TC
  - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
  - Feature issue type ID: 10142
  - Git Pull Request custom field: customfield_10875
  - GitHub Issue custom field: customfield_10747

### 4. Code Intelligence

- Added `## Code Intelligence` section with:
  - Tool naming convention: `mcp__<instance>__<tool>`
  - Example using `serena_backend` instance
  - `### Limitations` subsection (no limitations known)

### 5. Security Configuration

- Added `## Security Configuration` section with:
  - `### Product Lifecycle` subsection with all 5 fields:
    - Product pages URL: https://access.example.com/product-lifecycle
    - Jira version prefix: MYPRODUCT
    - Vulnerability issue type ID: 10200
    - Component label pattern: pscomponent:
    - VEX Justification custom field: customfield_12345
  - `### Version Streams` table with 1 row:
    - 2.1.x stream (git.downstream.example.com/my-org/product-release.2.1.z)
  - `### Source Repositories` table with 2 rows:
    - backend (https://github.com/example/backend)
    - frontend-ui (https://github.com/example/frontend-ui)

## Sections Skipped

- Constraints template copy (eval mode)
- CONVENTIONS.md scaffolding (eval mode)
- Supportability matrix population (user declined)
- security-matrix.md scaffolding (user skipped)
