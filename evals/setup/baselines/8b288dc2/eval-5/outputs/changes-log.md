# Changes Log

## Summary

All Project Configuration sections were created from scratch since the existing CLAUDE.md had no `# Project Configuration` section.

## Changes Made

### 1. Repository Registry (NEW)

Added `## Repository Registry` table with 2 repositories:

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| backend | Rust backend service | serena_backend | /home/user/backend |
| frontend-ui | TypeScript frontend | serena_ui | /home/user/frontend-ui |

### 2. Jira Configuration (NEW)

Added `## Jira Configuration` with:
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### 3. Code Intelligence (NEW)

Added `## Code Intelligence` section with:
- Tool naming convention: `mcp__<instance>__<tool>`
- Example using `serena_backend` instance
- `### Limitations` subsection noting no known limitations

### 4. Bug Configuration (NEW)

Added `## Bug Configuration` section with:
- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

### 5. Security Configuration (NEW)

Added `## Security Configuration` section with:

#### Product Lifecycle
- Product pages URL: https://access.example.com/product-lifecycle
- Jira version prefix: MYPRODUCT
- Vulnerability issue type ID: 10200
- Component label pattern: pscomponent:
- VEX Justification custom field: customfield_12345
- Upstream Affected Component custom field: (not configured)
- PS Component custom field: (not configured)
- Stream custom field: (not configured)
- ProdSec contact email: (not configured)
- ProdSec Jira account ID: (not configured)
- Embargo policy URL: (not configured)

#### Version Streams
- 2.1.x: git.downstream.example.com/my-org/product-release.2.1.z (local: /home/user/product-release.2.1.z, matrix: security-matrix.md)

#### Source Repositories
- backend: https://github.com/example/backend (upstream)
- frontend-ui: https://github.com/example/frontend-ui (upstream)

### 6. Hierarchy Configuration (NEW)

Added `## Hierarchy Configuration` section with:
- Default epic grouping strategy: by-sub-feature

## Files Not Modified

- No actual CLAUDE.md was modified (output written to `outputs/claude-md-result.md`).
- `docs/constraints.md` copy skipped (simulation mode).
- `CONVENTIONS.md` scaffolding skipped (simulation mode).
- `docs/bug-template.md` copy skipped (simulation mode).
- `security-matrix.md` scaffolding skipped (user declined).
- Supportability matrix population skipped (user declined).
