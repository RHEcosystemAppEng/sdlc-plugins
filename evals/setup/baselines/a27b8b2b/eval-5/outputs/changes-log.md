# Setup Changes Log

## Summary

All sections created from scratch -- no existing Project Configuration was present in the target CLAUDE.md.

## Changes Made

### 1. Repository Registry (NEW)

Added `## Repository Registry` table with 2 repositories:

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| backend | Rust backend service | serena_backend | /home/user/backend |
| frontend-ui | TypeScript frontend | serena_ui | /home/user/frontend-ui |

### 2. Jira Configuration (NEW)

Added `## Jira Configuration` with 5 fields:

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### 3. Code Intelligence (NEW)

Added `## Code Intelligence` section with:
- Tool naming convention documentation (`mcp__<instance>__<tool>`)
- Usage example using `serena_backend`
- `### Limitations` subsection (no limitations reported)

### 4. Bug Configuration (NEW)

Added `## Bug Configuration` with 3 fields:

- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

### 5. Hierarchy Configuration (NEW)

Added `## Hierarchy Configuration` with:
- Default epic grouping strategy: by-sub-feature

### 6. Security Configuration (NEW)

Added `## Security Configuration` with 3 subsections:

**Product Lifecycle:**
- Product pages URL: https://access.example.com/product-lifecycle
- Jira version prefix: MYPRODUCT
- Vulnerability issue type ID: 10200
- Component label pattern: pscomponent:
- VEX Justification custom field: customfield_12345

**Version Streams:** 1 stream
- 2.1.x (git.downstream.example.com/my-org/product-release.2.1.z)

**Source Repositories:** 2 repositories
- backend (https://github.com/example/backend) -- upstream
- frontend-ui (https://github.com/example/frontend-ui) -- upstream

## Skipped Actions

| Action | Reason |
|---|---|
| Jira Field Defaults | MCP unavailable for priority/fixVersion discovery; no manual values provided |
| Copy constraints.template.md to docs/constraints.md | Simulation mode -- no actual file operations |
| Scaffold CONVENTIONS.md in repositories | Simulation mode -- no actual file operations |
| Copy bug template to docs/bug-template.md | Simulation mode -- skipped per eval instructions |
| Scaffold security-matrix.md | User skipped scaffolding |
| Populate supportability matrix | User declined |
