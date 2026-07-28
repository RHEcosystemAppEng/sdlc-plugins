# Changes Log

## Existing CLAUDE.md Content

Preserved all existing content:

- Project title and description (my-project)
- Documentation section (architecture.md, api.md)
- Getting Started section

## Sections Added

### Repository Registry

Added repository registry table with 2 entries:

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| backend | Rust backend service | serena_backend | /home/user/backend |
| frontend-ui | TypeScript frontend | serena_ui | /home/user/frontend-ui |

### Jira Configuration

Added Jira configuration with 5 fields:

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### Code Intelligence

Added Code Intelligence section with:

- Tool prefix usage instructions
- Example showing mcp__serena_backend__find_symbol usage
- Limitations subsection (no limitations reported)

### Bug Configuration

Added Bug Configuration section with 3 fields:

- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

### Security Configuration

Added Security Configuration section with 3 subsections:

**Product Lifecycle** - 5 fields configured:
- Product pages URL: https://access.example.com/product-lifecycle
- Jira version prefix: MYPRODUCT
- Vulnerability issue type ID: 10200
- Component label pattern: pscomponent:
- VEX Justification custom field: customfield_12345

**Version Streams** - 1 stream configured:
- 2.1.x stream with Konflux release repo, local path, and security matrix path

**Source Repositories** - 2 repositories configured:
- backend (https://github.com/example/backend)
- frontend-ui (https://github.com/example/frontend-ui)

## Files Not Modified

- No existing files were modified
- No MCP tools were called
- Bug template file copy was skipped (simulation mode)
- security-matrix.md scaffolding was skipped per user request
