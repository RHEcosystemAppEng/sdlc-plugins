# Setup Changes Log

## Preserved

The following existing content from CLAUDE.md was preserved unchanged:
- `# my-project` — project heading and description
- `## Documentation` — links to architecture and API docs
- `## Getting Started` — setup instructions (clone, npm install, npm start)

## Added

All Project Configuration sections are new (no prior `# Project Configuration` existed):

- **# Project Configuration** — new top-level heading appended after existing content
- **## Repository Registry** — new table with 2 rows:
  - trustify-backend (Rust backend service, serena_backend, /home/user/trustify-backend)
  - trustify-ui (TypeScript frontend, serena_ui, /home/user/trustify-ui)
- **## Jira Configuration** — new section with 5 fields:
  - Project key: TC
  - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
  - Feature issue type ID: 10142
  - Git Pull Request custom field: customfield_10875
  - GitHub Issue custom field: customfield_10747
- **## Code Intelligence** — new section documenting `mcp__<instance>__<tool>` naming convention with example using serena_backend, plus `### Limitations` subheading (no known limitations)
- **## Bug Configuration** — new section with 3 fields:
  - Bug issue type ID: 10001
  - Bug template: docs/bug-template.md
  - Bug-to-Task link type: Blocks

## Declined

- **## Security Configuration** — user was prompted and opted out of enabling security triage for this project. Section was not created.
