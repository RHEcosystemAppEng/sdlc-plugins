# Setup Changes Log

## Summary

All Project Configuration sections were created from scratch (no prior configuration existed in CLAUDE.md).

## Changes Made

### 1. Added `# Project Configuration` heading

New top-level section appended to end of CLAUDE.md.

### 2. Added `## Repository Registry`

Created table with 2 repository entries:

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| backend | Rust backend service | serena_backend | /home/user/backend |
| frontend-ui | TypeScript frontend | serena_ui | /home/user/frontend-ui |

### 3. Added `## Jira Configuration`

Created section with 5 fields:

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### 4. Added `## Code Intelligence`

Created section documenting:
- Tool naming convention (`mcp__<instance>__<tool>`)
- Example using serena_backend instance
- Limitations subsection (no limitations reported)

### 5. Added `## Bug Configuration`

Created section with 3 fields:

- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

### 6. Added `## Security Configuration`

Created section with 3 subsections:

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

#### Version Streams (1 stream)
- 2.1.x: git.downstream.example.com/my-org/product-release.2.1.z

#### Source Repositories (2 repositories)
- backend: https://github.com/example/backend (upstream)
- frontend-ui: https://github.com/example/frontend-ui (upstream)

### 7. Added `## Hierarchy Configuration`

Created section with 1 field:

- Default epic grouping strategy: by-sub-feature

## Skipped Steps

| Step | Reason |
|---|---|
| Jira Field Defaults | MCP unavailable for discovering available priorities and fixVersions |
| Copy constraints.md | Simulation mode -- no file system modifications |
| Scaffold CONVENTIONS.md | Simulation mode -- no file system modifications |
| Copy bug template | Simulation mode -- no file system modifications |
| Scaffold security-matrix.md | User declined |
| Populate supportability matrix | User declined |

## Files Written

| File | Action |
|---|---|
| outputs/claude-md-result.md | Created -- full CLAUDE.md with Project Configuration appended |
| outputs/discovery-log.md | Created -- step-by-step discovery trace |
| outputs/changes-log.md | Created -- this file |
