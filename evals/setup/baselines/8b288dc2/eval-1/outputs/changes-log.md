# Changes Log

## Preserved (from existing CLAUDE.md)

- `# my-project` heading and project description.
- `## Documentation` section with architecture and API links.
- `## Getting Started` section with setup instructions.

## Added

### `# Project Configuration` (new section, appended after existing content)

- **`## Repository Registry`** — new table with 2 rows:
  - trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend
  - trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui

- **`## Jira Configuration`** — new section with 5 fields:
  - Project key: TC
  - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
  - Feature issue type ID: 10142
  - Git Pull Request custom field: customfield_10875
  - GitHub Issue custom field: customfield_10747

- **`## Code Intelligence`** — new section documenting tool naming convention (`mcp__<instance>__<tool>`), with example using `serena_backend`.
  - **`### Limitations`** — no limitations reported for either instance.

- **`## Bug Configuration`** — new section with 3 fields:
  - Bug issue type ID: 10001
  - Bug template: docs/bug-template.md
  - Bug-to-Task link type: Blocks

## Not Added (skipped per task instructions)

- **`### Jira Field Defaults`** — skipped (requires MCP discovery of priorities/fixVersions, not available in simulation).
- **`## Hierarchy Configuration`** — skipped (no hierarchy data provided in simulation).
- **`## Security Configuration`** — skipped (user declined security triage enablement).
- **Bug template file** — copy skipped per simulation instructions.
- **`docs/constraints.md`** — copy skipped (simulation mode, no filesystem writes outside outputs/).
- **`CONVENTIONS.md`** — scaffolding skipped (simulation mode, no filesystem writes outside outputs/).
