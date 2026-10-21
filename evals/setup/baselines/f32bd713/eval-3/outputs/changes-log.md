# Changes Log

## Preserved

The following existing content from CLAUDE.md was preserved unchanged:
- Project heading (`# my-project`) and description
- `## Documentation` section (architecture.md, api.md links)
- `## Getting Started` section (clone, npm install, npm start steps)

## Added

All Project Configuration sections are new additions:

- `# Project Configuration` — top-level heading for all configuration
- `## Repository Registry` — table with headers but no data rows (no Serena instances discovered)
- `## Jira Configuration` — 3 fields: Project key (MYPROJ), Cloud ID (abc123), Feature issue type ID (10001). No custom fields included since the user did not provide any.
- `## Code Intelligence` — notes that no Serena MCP servers are configured and code intelligence is not available
- `## Bug Configuration` — 3 fields: Bug issue type ID (10001), Bug template (docs/bug-template.md), Bug-to-Task link type (Blocks)

## Declined

- `## Security Configuration` — user was prompted and opted out of enabling security triage. This section was not added.
