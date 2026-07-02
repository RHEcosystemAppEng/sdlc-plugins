# Changes Log

## Summary

All Project Configuration sections were newly added. The existing CLAUDE.md had no `# Project Configuration` section, so the entire configuration block was appended.

## Sections Added

### 1. Repository Registry (NEW)

Added table with 2 repository entries:
- trustify-backend (serena_backend) -- Rust backend service at /home/user/trustify-backend
- trustify-ui (serena_ui) -- TypeScript frontend at /home/user/trustify-ui

### 2. Jira Configuration (NEW)

Added all 5 fields:
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### 3. Code Intelligence (NEW)

Added section with:
- Tool naming convention (`mcp__<instance>__<tool>`)
- Example using serena_backend instance
- Limitations subsection (no known limitations)

### 4. Bug Configuration (NEW)

Added all 3 fields:
- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

## Sections Declined

### Security Configuration -- DECLINED

User was asked whether to enable security triage for this project and declined. No Security Configuration section was created.

## Sections Preserved

The following content from the original CLAUDE.md was preserved unchanged:
- `# my-project` heading and description
- `## Documentation` section with architecture and API links
- `## Getting Started` section with setup instructions
