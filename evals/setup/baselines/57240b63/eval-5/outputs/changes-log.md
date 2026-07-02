# Setup Changes Log

## Summary

All Project Configuration sections were newly added to CLAUDE.md. The file previously had no `# Project Configuration` section.

## Pre-existing Content Preserved

The following non-configuration content from the original CLAUDE.md was preserved without modification:
- `# my-project` heading and project description
- `## Documentation` section (architecture.md and api.md links)
- `## Getting Started` section (clone, npm install, npm start instructions)

## Sections Added

### 1. Project Configuration (top-level heading)
- **Status**: Newly added
- Appended after all pre-existing content

### 2. Repository Registry
- **Status**: Newly added
- Added 2 repository entries:
  - `backend` (Rust backend service, serena_backend, /home/user/backend)
  - `frontend-ui` (TypeScript frontend, serena_ui, /home/user/frontend-ui)

### 3. Jira Configuration
- **Status**: Newly added
- All 5 fields populated:
  - Project key: TC
  - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
  - Feature issue type ID: 10142
  - Git Pull Request custom field: customfield_10875
  - GitHub Issue custom field: customfield_10747

### 4. Code Intelligence
- **Status**: Newly added
- Documented `mcp__<instance>__<tool>` naming convention
- Included concrete example using `serena_backend`
- Added `### Limitations` subsection (no limitations reported)

### 5. Bug Configuration
- **Status**: Newly added
- All 3 fields populated:
  - Bug issue type ID: 10001
  - Bug template: docs/bug-template.md
  - Bug-to-Task link type: Blocks

### 6. Security Configuration
- **Status**: Newly added
- Added `### Product Lifecycle` subsection with all required fields:
  - Product pages URL: https://access.example.com/product-lifecycle
  - Jira version prefix: MYPRODUCT
  - Vulnerability issue type ID: 10200
  - Component label pattern: pscomponent:
  - VEX Justification custom field: customfield_12345
  - Optional fields left blank (Upstream Affected Component, PS Component, Stream, ProdSec contact email, ProdSec Jira account ID, Embargo policy URL)
- Added `### Version Streams` subsection with 1 stream row:
  - 2.1.x stream with Konflux release repo, local path, and security matrix path
- Added `### Source Repositories` subsection with 2 repository rows:
  - backend (https://github.com/example/backend, upstream)
  - frontend-ui (https://github.com/example/frontend-ui, upstream)
