# Changes Log

## Summary

The existing CLAUDE.md had no Project Configuration section. All configuration sections were created from scratch.

## Added

### `# Project Configuration` (new top-level section)

The entire Project Configuration section was created, including:

### `## Repository Registry` (new)
- Added table with 2 repositories:
  - `backend` (Rust backend service) linked to `serena_backend` at `/home/user/backend`
  - `frontend-ui` (TypeScript frontend) linked to `serena_ui` at `/home/user/frontend-ui`

### `## Jira Configuration` (new)
- Added Project key: TC
- Added Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Added Feature issue type ID: 10142
- Added Git Pull Request custom field: customfield_10875
- Added GitHub Issue custom field: customfield_10747

### `## Code Intelligence` (new)
- Added tool naming convention documentation (`mcp__<instance>__<tool>`)
- Added example using `serena_backend` instance
- Added `### Limitations` subsection (no limitations known)

### `## Bug Configuration` (new)
- Added Bug issue type ID: 10001
- Added Bug template: docs/bug-template.md
- Added Bug-to-Task link type: Blocks

### `## Security Configuration` (new)
- Added `### Product Lifecycle` with:
  - Product pages URL: https://access.example.com/product-lifecycle
  - Jira version prefix: MYPRODUCT
  - Vulnerability issue type ID: 10200
  - Component label pattern: pscomponent:
  - VEX Justification custom field: customfield_12345
  - Optional fields left blank: Upstream Affected Component, PS Component, Stream, ProdSec contact email, ProdSec Jira account ID, Embargo policy URL
- Added `### Version Streams` table with 1 stream:
  - 2.1.x stream with Konflux release repo, local path, and security matrix path
- Added `### Source Repositories` table with 2 repositories:
  - backend (https://github.com/example/backend, upstream)
  - frontend-ui (https://github.com/example/frontend-ui, upstream)

## Preserved

- All existing content in CLAUDE.md was preserved:
  - `# my-project` heading and description
  - `## Documentation` section with architecture and API links
  - `## Getting Started` section with setup instructions

## Skipped

- Jira Field Defaults: MCP discovery not available in simulation; subsection not created
- Hierarchy Configuration: MCP discovery not available in simulation; subsection not created
- Bug template file copy: Skipped per simulation instructions
- security-matrix.md scaffolding: User skipped
- Supportability matrix population: User declined
- CONVENTIONS.md scaffolding: Not addressed in simulation scope
- docs/constraints.md copy: Not addressed in simulation scope
