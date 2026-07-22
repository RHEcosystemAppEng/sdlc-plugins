# Changes Log

## Preserved (existing content)

The following content from the original CLAUDE.md (`evals/setup/files/claude-md-empty.md`) is preserved unchanged:

- `# my-project` heading and project description
- `## Documentation` section with architecture and API links
- `## Getting Started` section with setup instructions

## Added (new sections)

All sections below are new — the original CLAUDE.md had no `# Project Configuration` section.

### 1. `# Project Configuration` heading
- **Status**: Added
- **Reason**: Required top-level heading for all sdlc-workflow skills

### 2. `## Repository Registry` table
- **Status**: Added
- **Entries added**:
  - trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend
  - trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui
- **Source**: Serena instances discovered from MCP tool listing, mapped by user

### 3. `## Jira Configuration` section
- **Status**: Added
- **Fields added**:
  - Project key: TC
  - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
  - Feature issue type ID: 10142
  - Git Pull Request custom field: customfield_10875
  - GitHub Issue custom field: customfield_10747
- **Source**: User-provided values

### 4. `## Code Intelligence` section
- **Status**: Added
- **Content**: Tool naming convention documentation with example using serena_backend
- **Subsection `### Limitations`**: Added with note that no limitations are known
- **Source**: Generated from discovered Serena instances

### 5. `## Bug Configuration` section
- **Status**: Added
- **Fields added**:
  - Bug issue type ID: 10001
  - Bug template: docs/bug-template.md
  - Bug-to-Task link type: Blocks
- **Source**: Bug issue type ID from Jira metadata; template path and link type accepted as defaults by user

## Not Added (skipped sections)

### `### Jira Field Defaults` subsection
- **Reason**: Requires MCP calls to discover available priorities and fixVersions (simulation does not permit MCP calls)

### `## Hierarchy Configuration` section
- **Reason**: Requires MCP calls to discover issue type hierarchy levels (simulation does not permit MCP calls)

### `## Security Configuration` section
- **Reason**: User declined to enable security triage for this project
