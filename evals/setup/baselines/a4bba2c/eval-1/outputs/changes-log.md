# Changes Log

## Preserved (existing content)

The following sections from the existing CLAUDE.md were preserved unchanged:

- `# my-project` -- project title and description
- `## Documentation` -- links to architecture.md and api.md
- `## Getting Started` -- setup instructions (clone, npm install, npm start)

## Added (new content)

The following section was appended to CLAUDE.md:

- `# Project Configuration` -- new top-level section containing:
  - `## Repository Registry` -- table with 2 entries (trustify-backend via serena_backend, trustify-ui via serena_ui)
  - `## Jira Configuration` -- 5 fields (project key, cloud ID, feature issue type ID, git PR custom field, GitHub issue custom field)
  - `## Code Intelligence` -- documents the `mcp__<instance>__<tool>` naming convention with examples for both serena_backend and serena_ui
  - `### Limitations` -- notes that no limitations are known for either Serena instance
