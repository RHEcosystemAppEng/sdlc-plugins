# Changes Log

## Summary

The existing CLAUDE.md (`claude-md-empty.md`) contained no `# Project Configuration` section. All configuration sections were created new.

## Preserved Content

- The existing CLAUDE.md content (project title, Documentation section, Getting Started section) was preserved unchanged
- No existing configuration was overwritten (there was none to preserve)

## Added Sections

### 1. `# Project Configuration` (new)

Top-level heading added to contain all configuration subsections.

### 2. `## Repository Registry` (new)

Added table with 2 repositories discovered from Serena MCP tool listing:

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| backend | Rust backend service | serena_backend | /home/user/backend |
| frontend-ui | TypeScript frontend | serena_ui | /home/user/frontend-ui |

### 3. `## Jira Configuration` (new)

Added 5 fields from user-provided values:
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

Note: `### Jira Field Defaults` subsection was not created — MCP discovery of priorities and fixVersions was not available in simulation mode.

### 4. `## Code Intelligence` (new)

Added section documenting:
- Tool naming convention: `mcp__<instance>__<tool>`
- Concrete example using serena_backend instance
- `### Limitations` subsection noting no known limitations

### 5. `## Security Configuration` (new)

Added full security configuration with three subsections:

#### `### Product Lifecycle`
- 5 fields populated from user input (Product pages URL, Jira version prefix, Vulnerability issue type ID, Component label pattern, VEX Justification custom field)
- 6 optional fields left blank (Upstream Affected Component, PS Component, Stream, ProdSec contact email, ProdSec Jira account ID, Embargo policy URL)

#### `### Version Streams`
- 1 stream added: 2.1.x

#### `### Source Repositories`
- 2 repositories added: backend, frontend-ui (both with deployment context: upstream)

### 6. `## Bug Configuration` (new)

Added 3 fields:
- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

### 7. `## Hierarchy Configuration` (new)

Added 1 field:
- Default epic grouping strategy: by-sub-feature

## Skipped Steps

- **Jira Field Defaults**: MCP not available for priority/fixVersion discovery; no user inputs provided
- **Constraints template copy**: Simulation mode — no file operations
- **CONVENTIONS.md scaffolding**: Simulation mode — no file operations
- **Bug template file copy**: Skipped per simulation instructions
- **security-matrix.md scaffolding**: User skipped
- **Supportability matrix population**: User declined
