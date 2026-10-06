# Setup Changes Log

## Changes Applied

### 1. Added `# Project Configuration` section to CLAUDE.md

The entire Project Configuration section was created from scratch since no existing configuration was found.

### 2. Added `## Repository Registry`

Created the Repository Registry table with 2 entries:

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| backend | Rust backend service | serena_backend | /home/user/backend |
| frontend-ui | TypeScript frontend | serena_ui | /home/user/frontend-ui |

### 3. Added `## Jira Configuration`

Created the Jira Configuration section with all fields:

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### 4. Added `## Code Intelligence`

Created the Code Intelligence section documenting the Serena tool naming convention (`mcp__<instance>__<tool>`) with a concrete example using `serena_backend`. Added `### Limitations` subsection noting no known limitations.

### 5. Added `## Bug Configuration`

Created the Bug Configuration section with:

- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

### 6. Added `## Hierarchy Configuration`

Created the Hierarchy Configuration section with:

- Default epic grouping strategy: by-sub-feature

### 7. Added `## Security Configuration`

Created the Security Configuration section with three subsections:

#### Product Lifecycle
- Product pages URL: https://access.example.com/product-lifecycle
- Jira version prefix: MYPRODUCT
- Vulnerability issue type ID: 10200
- Component label pattern: pscomponent:
- VEX Justification custom field: customfield_12345
- Optional fields (Upstream Affected Component, PS Component, Stream, ProdSec contact, ProdSec Jira account ID, Embargo policy URL) left empty as not provided

#### Version Streams
- 1 stream configured: 2.1.x

#### Source Repositories
- 2 repositories configured: backend, frontend-ui (both with upstream deployment context)

## Skipped Actions (Simulation Mode)

- **Constraints template copy**: Would copy `constraints.template.md` to `docs/constraints.md`
- **CONVENTIONS.md scaffolding**: Would offer to scaffold for backend and frontend-ui repositories
- **Bug template copy**: Would copy bug template to `docs/bug-template.md`
- **security-matrix.md scaffolding**: Skipped per user request
- **Supportability matrix population**: Declined by user
- **Jira Field Defaults**: Skipped (requires MCP or REST API discovery of available priorities and fixVersions)
