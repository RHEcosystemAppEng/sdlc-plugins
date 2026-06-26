# Changes Log

## Preserved (Existing Content)

The following sections from the original CLAUDE.md were preserved unchanged:

- `# my-project` heading and description
- `## Documentation` section with architecture and API links
- `## Getting Started` section with setup instructions

## Added (New Content)

The following sections were added as the `# Project Configuration` block:

1. **`## Repository Registry`** — new table with 2 entries:
   - `trustify-backend` (Rust backend service, serena_backend, /home/user/trustify-backend)
   - `trustify-ui` (TypeScript frontend, serena_ui, /home/user/trustify-ui)

2. **`## Jira Configuration`** — new section with 5 fields:
   - Project key: TC
   - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
   - Feature issue type ID: 10142
   - Git Pull Request custom field: customfield_10875
   - GitHub Issue custom field: customfield_10747

3. **`## Code Intelligence`** — new section with:
   - Tool naming convention documentation (`mcp__<instance>__<tool>`)
   - Example using `serena_backend` instance
   - Limitations subsection (no limitations for either instance)

4. **`## Bug Configuration`** — new section with 3 fields:
   - Bug issue type ID: 10001
   - Bug template: docs/bug-template.md
   - Bug-to-Task link type: Blocks

## Not Added

- **Security Configuration** — user declined to enable security triage
- **Hierarchy Configuration** — not part of setup scope for this run
- **Jira Field Defaults** — not configured during this setup
- **REST API Credentials** — not needed (Atlassian MCP is available)
