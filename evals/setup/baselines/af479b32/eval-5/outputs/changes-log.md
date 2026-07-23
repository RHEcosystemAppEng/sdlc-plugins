# Setup Changes Log

## Summary

All changes are new additions. The original CLAUDE.md had no Project Configuration section.

## Changes Applied

### 1. Added `# Project Configuration` section

Appended the entire Project Configuration section to the end of the existing CLAUDE.md content.

### 2. Added `## Repository Registry`

Created table with 2 repository entries:

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| backend | Rust backend service | serena_backend | /home/user/backend |
| frontend-ui | TypeScript frontend | serena_ui | /home/user/frontend-ui |

### 3. Added `## Jira Configuration`

Created with all 5 fields:

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### 4. Added `## Code Intelligence`

Created with:
- Tool naming convention: `mcp__<instance>__<tool>`
- Example using `serena_backend` instance
- `### Limitations` subheading with no known limitations noted

### 5. Added `## Bug Configuration`

Created with 3 fields:
- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

### 6. Added `## Security Configuration`

Created with 3 subsections:

#### `### Product Lifecycle`
- Product pages URL: https://access.example.com/product-lifecycle
- Jira version prefix: MYPRODUCT
- Vulnerability issue type ID: 10200
- Component label pattern: pscomponent:
- VEX Justification custom field: customfield_12345
- Optional fields left blank: Upstream Affected Component, PS Component, Stream, ProdSec contact email, ProdSec Jira account ID, Embargo policy URL

#### `### Version Streams`
1 stream: 2.1.x

#### `### Source Repositories`
2 repositories: backend, frontend-ui (both upstream deployment context)

## Sections Not Created

- **Hierarchy Configuration**: Skipped — MCP not available for issue type hierarchy discovery, no hierarchy data provided in simulation
- **Jira Field Defaults**: Skipped — MCP not available for priority/fixVersion discovery, no field default data provided in simulation
- **docs/constraints.md**: Skipped — simulation mode, no file system writes outside outputs/
- **CONVENTIONS.md**: Skipped — simulation mode, no file system writes outside outputs/
- **docs/bug-template.md**: Skipped — simulation mode, no file system writes outside outputs/
- **security-matrix.md**: Skipped — user declined scaffolding
- **Supportability matrix**: Skipped — user declined population
