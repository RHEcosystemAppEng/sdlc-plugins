# Changes Log

## Summary

All sections created from scratch — the source CLAUDE.md had no existing Project Configuration.

## Sections Added

### 1. Repository Registry (new)

Added table with 2 repositories:
- `backend` — Rust backend service, Serena instance `serena_backend`, path `/home/user/backend`
- `frontend-ui` — TypeScript frontend, Serena instance `serena_ui`, path `/home/user/frontend-ui`

### 2. Jira Configuration (new)

Added 5 fields:
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

Note: Jira Field Defaults subsection was not created (MCP unavailable for priority/fixVersion discovery in simulation mode).

### 3. Code Intelligence (new)

Added section documenting `mcp__<instance>__<tool>` naming convention with example using `serena_backend`. Added `### Limitations` subsection noting no known limitations.

### 4. Security Configuration (new)

Added complete Security Configuration section with:
- **Product Lifecycle**: 5 fields populated (Product pages URL, Jira version prefix, Vulnerability issue type ID, Component label pattern, VEX Justification custom field), 6 optional fields left blank
- **Version Streams**: 1 stream (2.1.x)
- **Source Repositories**: 2 repositories (backend, frontend-ui) with upstream deployment context

### 5. Bug Configuration (new)

Added 3 fields:
- Bug issue type ID: 10001
- Bug template: docs/bug-template.md (linked)
- Bug-to-Task link type: Blocks

Note: Bug template file copy skipped (simulation mode).

### 6. Hierarchy Configuration (new)

Added 1 field:
- Default epic grouping strategy: by-sub-feature

## Files Not Modified (simulation mode)

The following files would be created or modified in a live run but were skipped due to simulation constraints:

- `docs/constraints.md` — would be created from constraints.template.md
- `/home/user/backend/CONVENTIONS.md` — would be offered for scaffolding
- `/home/user/frontend-ui/CONVENTIONS.md` — would be offered for scaffolding
- `docs/bug-template.md` — would be copied from plugin template
- `security-matrix.md` — would be scaffolded for version stream 2.1.x
