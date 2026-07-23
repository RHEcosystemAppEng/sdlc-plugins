# Changes Log

## Summary

All sections were newly created. The existing CLAUDE.md had no `# Project Configuration` section, so the entire configuration block was added.

## Preserved Content

- Original `# my-project` heading and description
- `## Documentation` section with architecture and API links
- `## Getting Started` section with setup instructions
- No existing Project Configuration content to preserve

## Added Sections

### 1. `# Project Configuration` (new)

Top-level heading added to contain all configuration subsections.

### 2. `## Repository Registry` (new)

Added table with two repositories:

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| trustify-backend | Rust backend service | serena_backend | /home/user/trustify-backend |
| trustify-ui | TypeScript frontend | serena_ui | /home/user/trustify-ui |

### 3. `## Jira Configuration` (new)

Added five configuration fields:
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

Note: `### Jira Field Defaults` subsection was not created because MCP discovery of available priorities and fixVersions was not performed (simulation mode) and no explicit user input was provided for these fields.

### 4. `## Code Intelligence` (new)

Added section documenting:
- Tool naming convention: `mcp__<instance>__<tool>`
- Example using `serena_backend` instance
- `### Limitations` subsection: no limitations reported

### 5. `## Bug Configuration` (new)

Added three configuration fields:
- Bug issue type ID: 10001
- Bug template: docs/bug-template.md (with markdown link)
- Bug-to-Task link type: Blocks

Note: Bug template file was not copied to the target project (simulation mode).

### 6. `## Hierarchy Configuration` (new)

Added one configuration field:
- Default epic grouping strategy: by-sub-feature

## Skipped Sections

### `### Jira Field Defaults`
- Reason: Requires MCP discovery of priorities and fixVersions; not available in simulation mode and not explicitly provided by user

### `## Security Configuration`
- Reason: User declined when asked whether to enable security triage

## Files Not Modified

- No actual project files were modified (all output written to outputs/ directory)
- Bug template file copy was skipped (simulation)
- Constraints template copy was skipped (simulation)
- CONVENTIONS.md scaffolding was skipped (simulation)
