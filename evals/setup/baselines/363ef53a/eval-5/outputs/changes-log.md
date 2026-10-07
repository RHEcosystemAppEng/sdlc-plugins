# Changes Log

## Summary

Appended a complete `# Project Configuration` section to the existing CLAUDE.md content. The original file had no Project Configuration section, so all subsections were created from scratch.

## Changes Made

### 1. Added `# Project Configuration` heading

- Location: appended after existing content (after `## Getting Started` section)

### 2. Added `## Repository Registry`

- Created table with 2 repository entries:
  - `backend` | Rust backend service | serena_backend | /home/user/backend
  - `frontend-ui` | TypeScript frontend | serena_ui | /home/user/frontend-ui

### 3. Added `## Jira Configuration`

- Created field list with 5 entries:
  - Project key: TC
  - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
  - Feature issue type ID: 10142
  - Git Pull Request custom field: customfield_10875
  - GitHub Issue custom field: customfield_10747

### 4. Added `## Code Intelligence`

- Documented `mcp__<instance>__<tool>` naming convention
- Added concrete example using `serena_backend` instance
- Added `### Limitations` subsection noting no known limitations

### 5. Added `## Bug Configuration`

- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

### 6. Added `## Hierarchy Configuration`

- Default epic grouping strategy: by-sub-feature

### 7. Added `## Security Configuration`

- Added `### Product Lifecycle` with 5 fields:
  - Product pages URL: https://access.example.com/product-lifecycle
  - Jira version prefix: MYPRODUCT
  - Vulnerability issue type ID: 10200
  - Component label pattern: pscomponent:
  - VEX Justification custom field: customfield_12345
- Added `### Version Streams` table with 1 stream:
  - 2.1.x | git.downstream.example.com/my-org/product-release.2.1.z | /home/user/product-release.2.1.z | security-matrix.md
- Added `### Source Repositories` table with 2 repositories:
  - backend | https://github.com/example/backend | upstream
  - frontend-ui | https://github.com/example/frontend-ui | upstream

## Files Not Modified

- No actual project files were modified (simulation mode).
- Bug template file copy skipped (simulation).
- Constraints template copy skipped (simulation).
- CONVENTIONS.md scaffolding skipped (simulation).
- security-matrix.md scaffolding skipped (user declined).
- Supportability matrix population skipped (user declined).
