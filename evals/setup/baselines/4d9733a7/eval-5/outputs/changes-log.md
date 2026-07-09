# Setup Changes Log

## Summary

All sections were created from scratch — the existing CLAUDE.md had no Project Configuration section.

## Changes Made

### 1. Added `# Project Configuration` heading
- Location: appended after existing content in CLAUDE.md

### 2. Added `## Repository Registry`
- Created table with 2 repositories:
  - `backend` | Rust backend service | serena_backend | /home/user/backend
  - `frontend-ui` | TypeScript frontend | serena_ui | /home/user/frontend-ui

### 3. Added `## Jira Configuration`
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### 4. Added `## Code Intelligence`
- Documented `mcp__<instance>__<tool>` naming convention
- Added example using `serena_backend` instance
- Added `### Limitations` subheading with no known limitations

### 5. Added `## Bug Configuration`
- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks
- Bug template file copy skipped (simulation mode)

### 6. Added `## Security Configuration`
- Added `### Product Lifecycle` with:
  - Product pages URL: https://access.example.com/product-lifecycle
  - Jira version prefix: MYPRODUCT
  - Vulnerability issue type ID: 10200
  - Component label pattern: pscomponent:
  - VEX Justification custom field: customfield_12345
  - Optional fields left empty (user skipped)
- Added `### Version Streams` with 1 stream:
  - 2.1.x | git.downstream.example.com/my-org/product-release.2.1.z | /home/user/product-release.2.1.z | security-matrix.md
- Added `### Source Repositories` with 2 repos:
  - backend | https://github.com/example/backend | upstream
  - frontend-ui | https://github.com/example/frontend-ui | upstream

### 7. Added `## Hierarchy Configuration`
- Default epic grouping strategy: by-sub-feature

## Sections Not Configured

- `### Jira Field Defaults` — skipped because MCP discovery of available priorities and fixVersions was not available in simulation mode
- `docs/constraints.md` — file copy skipped (simulation mode)
- `CONVENTIONS.md` scaffolding — skipped (simulation mode)
- `security-matrix.md` scaffolding — skipped (user declined)
- Supportability matrix population — skipped (user declined)
