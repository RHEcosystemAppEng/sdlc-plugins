# Changes Log

## Summary

All sections were created from scratch since the existing CLAUDE.md had no Project Configuration.

## Sections Added

### 1. Project Configuration (top-level heading)

Added `# Project Configuration` heading — new section appended to CLAUDE.md.

### 2. Repository Registry

Added `## Repository Registry` table with 2 entries:

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| backend | Rust backend service | serena_backend | /home/user/backend |
| frontend-ui | TypeScript frontend | serena_ui | /home/user/frontend-ui |

### 3. Jira Configuration

Added `## Jira Configuration` with all 5 fields:
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### 4. Code Intelligence

Added `## Code Intelligence` section with:
- Naming convention documentation (`mcp__<instance>__<tool>`)
- Concrete example using `serena_backend`
- `### Limitations` subsection (no limitations known)

### 5. Bug Configuration

Added `## Bug Configuration` with all 3 fields:
- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

### 6. Security Configuration

Added `## Security Configuration` with all subsections:

#### Product Lifecycle
- Product pages URL: https://access.example.com/product-lifecycle
- Jira version prefix: MYPRODUCT
- Vulnerability issue type ID: 10200
- Component label pattern: pscomponent:
- VEX Justification custom field: customfield_12345

#### Version Streams
One stream configured:
- 2.1.x with Konflux release repo, local path, and security matrix path

#### Source Repositories
Two repositories configured:
- backend (https://github.com/example/backend) — upstream
- frontend-ui (https://github.com/example/frontend-ui) — upstream

## Sections Not Added

- **Jira Field Defaults**: Requires MCP or REST API discovery of available priorities and fixVersions (not available in simulation)
- **Hierarchy Configuration**: Requires MCP or REST API discovery of issue type hierarchy (not available in simulation)

## Files Written

- `outputs/claude-md-result.md` — Generated Project Configuration section
- `outputs/discovery-log.md` — Discovery log
- `outputs/changes-log.md` — This file
