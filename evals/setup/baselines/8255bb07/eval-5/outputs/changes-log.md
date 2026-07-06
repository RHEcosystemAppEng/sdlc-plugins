# Changes Log

## Summary

All sections were added new -- the existing CLAUDE.md had no Project Configuration section.

## Preserved Content

- Original CLAUDE.md content preserved in full:
  - `# my-project` heading and description
  - `## Documentation` section with architecture and API doc links
  - `## Getting Started` section with setup instructions

## Added Sections

### 1. `# Project Configuration` (new)

Top-level heading appended after the existing content.

### 2. `## Repository Registry` (new)

Added table with 2 rows:
- backend | Rust backend service | serena_backend | /home/user/backend
- frontend-ui | TypeScript frontend | serena_ui | /home/user/frontend-ui

### 3. `## Jira Configuration` (new)

Added 5 fields:
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

Note: Jira Field Defaults subsection was not added (requires MCP discovery of available priorities and fixVersions, not available in simulation).

### 4. `## Code Intelligence` (new)

Added:
- Tool naming convention explanation with `mcp__<instance>__<tool>` pattern
- Concrete example using `serena_backend` instance
- `### Limitations` subsection noting no known limitations

### 5. `## Bug Configuration` (new)

Added 3 fields:
- Bug issue type ID: 10001
- Bug template: docs/bug-template.md (linked)
- Bug-to-Task link type: Blocks

### 6. `## Security Configuration` (new)

Added three subsections:

#### `### Product Lifecycle`
- Product pages URL: https://access.example.com/product-lifecycle
- Jira version prefix: MYPRODUCT
- Vulnerability issue type ID: 10200
- Component label pattern: pscomponent:
- VEX Justification custom field: customfield_12345
- Optional fields omitted (Upstream Affected Component, PS Component, Stream, ProdSec contact, ProdSec Jira account ID, Embargo policy URL) -- user did not provide values

#### `### Version Streams`
Table with 1 row:
- 2.1.x | git.downstream.example.com/my-org/product-release.2.1.z | /home/user/product-release.2.1.z | security-matrix.md

#### `### Source Repositories`
Table with 2 rows:
- backend | https://github.com/example/backend | upstream
- frontend-ui | https://github.com/example/frontend-ui | upstream

### 7. `## Hierarchy Configuration` (new)

Added 1 field:
- Default epic grouping strategy: by-sub-feature

## Skipped Steps

- **Step 4 (Jira Field Defaults)**: Requires MCP discovery, not available in simulation
- **Step 7 (Constraints template copy)**: Simulation mode
- **Step 8 (CONVENTIONS.md scaffold)**: Simulation mode
- **Step 9.4 (Bug template copy)**: Skipped per task instructions
- **Step 10.5 (security-matrix.md scaffolding)**: Skipped per task instructions
- **Step 10.6 (Supportability matrix population)**: User declined
