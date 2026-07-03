# Setup Changes Log

## Changes Applied

### 1. Project Configuration section — CREATED

Appended `# Project Configuration` section to CLAUDE.md (after existing content).

### 2. Repository Registry — CREATED

Added `## Repository Registry` table with 2 repositories:

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| backend | Rust backend service | serena_backend | /home/user/backend |
| frontend-ui | TypeScript frontend | serena_ui | /home/user/frontend-ui |

### 3. Jira Configuration — CREATED

Added `## Jira Configuration` with all required and optional fields:
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### 4. Jira Field Defaults — SKIPPED

MCP discovery not available in simulation mode. No user inputs provided for priority/fixVersion defaults.

### 5. Code Intelligence — CREATED

Added `## Code Intelligence` section with:
- Tool naming convention: `mcp__<instance>__<tool>`
- Example using serena_backend instance
- `### Limitations` subsection: no known limitations

### 6. Constraints document — SKIPPED (simulation)

Would create `docs/constraints.md` from `constraints.template.md` in the target project.

### 7. CONVENTIONS.md — SKIPPED (simulation)

Would offer to scaffold CONVENTIONS.md for backend and frontend-ui repositories.

### 8. Bug Configuration — CREATED

Added `## Bug Configuration` with:
- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

Bug template file copy skipped (simulation mode).

### 9. Security Configuration — CREATED

Added `## Security Configuration` with three subsections:

**Product Lifecycle:**
- Product pages URL: https://access.example.com/product-lifecycle
- Jira version prefix: MYPRODUCT
- Vulnerability issue type ID: 10200
- Component label pattern: pscomponent:
- VEX Justification custom field: customfield_12345
- Optional fields (Upstream Affected Component, PS Component, Stream, ProdSec contact email, ProdSec Jira account ID, Embargo policy URL): left empty (user skipped)

**Version Streams:**
- 1 stream configured: 2.1.x

**Source Repositories:**
- 2 repositories configured: backend, frontend-ui (both upstream deployment context)

Supportability matrix population declined by user.
security-matrix.md scaffolding skipped by user.

### 10. Hierarchy Configuration — CREATED

Added `## Hierarchy Configuration` with:
- Default epic grouping strategy: by-sub-feature

## Validation

- `# Project Configuration` heading: PRESENT
- `## Repository Registry` with correct table columns (Repository, Role, Serena Instance, Path): PRESENT
- `## Jira Configuration` with required fields (Project key, Cloud ID, Feature issue type ID): PRESENT
- `## Code Intelligence` with `mcp__<instance>__<tool>` naming convention: PRESENT
- `### Limitations` subheading under Code Intelligence: PRESENT
- `## Bug Configuration` with all three fields (Bug issue type ID, Bug template, Bug-to-Task link type): PRESENT
- `## Security Configuration` with `### Product Lifecycle` and required fields: PRESENT
- `### Version Streams` with at least one row: PRESENT
- `### Source Repositories` with at least one row: PRESENT
- `## Hierarchy Configuration` with Default epic grouping strategy: PRESENT
