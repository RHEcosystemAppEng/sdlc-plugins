# Setup Changes Log

## Summary

All Project Configuration sections were newly added to CLAUDE.md. The file previously had no `# Project Configuration` section.

## Sections Added

### 1. Repository Registry (NEW)

Added table with two repository entries:
- `backend` (Rust backend service) -- Serena instance `serena_backend`, path `/home/user/backend`
- `frontend-ui` (TypeScript frontend) -- Serena instance `serena_ui`, path `/home/user/frontend-ui`

### 2. Jira Configuration (NEW)

Added all five fields:
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### 3. Code Intelligence (NEW)

Added section with:
- Tool naming convention explanation (`mcp__<instance>__<tool>`)
- Example using `serena_backend` instance
- Limitations subsection (no known limitations)

### 4. Bug Configuration (NEW)

Added section with all three fields:
- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

Note: Bug template file copy was skipped (simulation mode).

### 5. Security Configuration (NEW)

Added section with three subsections:

**Product Lifecycle:**
- Product pages URL: https://access.example.com/product-lifecycle
- Jira version prefix: MYPRODUCT
- Vulnerability issue type ID: 10200
- Component label pattern: pscomponent:
- VEX Justification custom field: customfield_12345

**Version Streams:**
- 2.1.x stream with Konflux release repo, local path, and security matrix path

**Source Repositories:**
- backend (https://github.com/example/backend)
- frontend-ui (https://github.com/example/frontend-ui)

## Files Not Modified

- No actual CLAUDE.md was modified (eval simulation)
- Bug template file copy was skipped (simulation)
- Security matrix scaffolding was skipped (user declined)
- Supportability matrix population was skipped (user declined)
