# Changes Log

## Preserved (existing CLAUDE.md content)

The following existing sections were preserved unchanged:

- `# my-project` — project heading and description
- `## Documentation` — links to architecture.md and api.md
- `## Getting Started` — setup instructions (clone, npm install, npm start)

## Added (new Project Configuration section)

The following `# Project Configuration` section was appended to the existing CLAUDE.md:

### Repository Registry
- Added table with headers (Repository, Role, Serena Instance, Path) but **no data rows** — no Serena MCP servers were discovered

### Jira Configuration
- Added Project key: MYPROJ (manual entry)
- Added Cloud ID: abc123 (manual entry)
- Added Feature issue type ID: 10001 (manual entry)
- No Git Pull Request custom field (user had none)
- No GitHub Issue custom field (user had none)
- No Jira Field Defaults subsection (not configured)
- No REST API Credentials subsection (not needed)

### Code Intelligence
- Added section documenting that no Serena MCP servers are configured
- Added Limitations subsection noting no limitations known

### Bug Configuration
- Added Bug issue type ID: 10001 (manual entry)
- Added Bug template: docs/bug-template.md (default path accepted)
- Added Bug-to-Task link type: Blocks (default accepted)

## Not Added

- **Security Configuration** — user declined when offered the opt-in
- **Hierarchy Configuration** — not scaffolded (no issue type discovery available without Atlassian MCP)
- **Jira Field Defaults** — not configured during this setup
- **CONVENTIONS.md** — not part of Project Configuration scaffolding scope
