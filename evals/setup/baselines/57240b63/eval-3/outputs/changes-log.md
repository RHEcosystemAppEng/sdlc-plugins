# Changes Log

## Sections Added

All Project Configuration sections were **newly added** to CLAUDE.md (no prior `# Project Configuration` section existed):

1. **# Project Configuration** — top-level heading added
2. **## Repository Registry** — added with table headers (Repository, Role, Serena Instance, Path) and no data rows, since no Serena MCP servers were discovered
3. **## Jira Configuration** — added with three required fields:
   - Project key: MYPROJ
   - Cloud ID: abc123
   - Feature issue type ID: 10001
   - No Git Pull Request or GitHub Issue custom fields (not provided)
4. **## Code Intelligence** — added with note that no Serena MCP servers are configured and code intelligence is not available; includes ### Limitations subsection noting no limitations known
5. **## Bug Configuration** — added with three fields:
   - Bug issue type ID: 10001
   - Bug template: docs/bug-template.md
   - Bug-to-Task link type: Blocks

## Sections Not Added

- **## Security Configuration** — user declined the opt-in prompt; section was not created
- **### Jira Field Defaults** — not added (no MCP or REST API available to discover available priorities and fixVersions)
- **## Hierarchy Configuration** — not added (no MCP or REST API available to discover issue type hierarchy)

## Preserved Content

- All pre-existing non-configuration content was preserved unchanged:
  - HTML comment at top of file
  - `# my-project` heading and description
  - `## Documentation` section with links
  - `## Getting Started` section with steps
- Project Configuration was appended after the existing content
