# Setup Changes Log

## Sections Added

The following Project Configuration sections were newly added to CLAUDE.md:

1. **`# Project Configuration`** — Top-level heading added after existing content
2. **`## Repository Registry`** — Added with table headers (Repository, Role, Serena Instance, Path) and no data rows; note that no repositories are configured
3. **`## Jira Configuration`** — Added with three fields:
   - Project key: MYPROJ
   - Cloud ID: abc123
   - Feature issue type ID: 10001
4. **`## Code Intelligence`** — Added noting no Serena MCP servers are configured, with `mcp__<instance>__<tool>` naming convention documented for future reference, and `### Limitations` subsection noting no Serena instances
5. **`## Bug Configuration`** — Added with three fields:
   - Bug issue type ID: 10001
   - Bug template: docs/bug-template.md
   - Bug-to-Task link type: Blocks

## Sections Declined / Skipped

- **Security Configuration** — User declined when offered the optional Security Configuration step
- **Hierarchy Configuration** — Skipped per user instruction
- **Jira Field Defaults** — Skipped per user instruction

## Pre-existing Content Preserved

The following existing sections were preserved unchanged:

- `# my-project` heading and description
- `## Documentation` section with architecture and API links
- `## Getting Started` section with setup instructions
