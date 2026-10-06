# Changes Log

## Summary

All changes are appended to the existing CLAUDE.md content. No existing content was modified or removed.

## Sections Added

### 1. `# Project Configuration` (new)

Top-level heading added after the existing `## Getting Started` section.

### 2. `## Repository Registry` (new)

Added repository registry table with 2 entries:

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| backend | Rust backend service | serena_backend | /home/user/backend |
| frontend-ui | TypeScript frontend | serena_ui | /home/user/frontend-ui |

### 3. `## Jira Configuration` (new)

Added Jira configuration with 5 fields:
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### 4. `## Code Intelligence` (new)

Added Code Intelligence section with:
- Tool naming convention explanation
- Example using `serena_backend` instance
- `### Limitations` subsection (no limitations reported)

### 5. `## Bug Configuration` (new)

Added Bug Configuration section with 3 fields:
- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

Note: Bug template file copy was skipped (simulation mode).

### 6. `## Security Configuration` (new)

Added Security Configuration section with 3 subsections:

#### `### Product Lifecycle`
- Product pages URL: https://access.example.com/product-lifecycle
- Jira version prefix: MYPRODUCT
- Vulnerability issue type ID: 10200
- Component label pattern: pscomponent:
- VEX Justification custom field: customfield_12345

#### `### Version Streams`
- 1 stream: 2.1.x

#### `### Source Repositories`
- 2 repositories: backend, frontend-ui (both upstream deployment context)

### 7. `## Hierarchy Configuration` (new)

Added Hierarchy Configuration section:
- Default epic grouping strategy: by-sub-feature

## Sections Not Changed

- `### Jira Field Defaults` — not added (MCP calls required for priority/fixVersion discovery not available in simulation)

## Files Not Written (Simulation Mode)

- `docs/constraints.md` — would be copied from constraints template
- `docs/bug-template.md` — would be copied from bug template
- `CONVENTIONS.md` in backend — would be scaffolded from template
- `CONVENTIONS.md` in frontend-ui — would be scaffolded from template
- `security-matrix.md` — scaffolding skipped per user instruction
