# Setup Changes Log

## Sections Added to CLAUDE.md

All sections below were newly added under `# Project Configuration`.

### 1. Repository Registry (added)

- Added `## Repository Registry` section with table headers (Repository, Role, Serena Instance, Path)
- Table contains no data rows — no Serena instances were discovered

### 2. Jira Configuration (added)

- Added `## Jira Configuration` section with manually entered values:
  - Project key: MYPROJ
  - Cloud ID: abc123
  - Feature issue type ID: 10001
- No optional custom fields configured (Git Pull Request, GitHub Issue)

### 3. Code Intelligence (added)

- Added `## Code Intelligence` section noting no Serena MCP servers are configured
- Added `### Limitations` subsection noting no limitations known due to no Serena instances

### 4. Bug Configuration (added)

- Added `## Bug Configuration` section with:
  - Bug issue type ID: 10001
  - Bug template: docs/bug-template.md
  - Bug-to-Task link type: Blocks

## Sections Not Added

### Security Configuration (skipped)

- User declined security triage configuration — section not added

### Hierarchy Configuration (not prompted)

- No level-1 issue type (Epic) discovery was performed — section not added
