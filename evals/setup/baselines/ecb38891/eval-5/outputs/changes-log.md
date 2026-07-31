# Changes Log

## Summary

Greenfield setup — no existing `# Project Configuration` section was found in CLAUDE.md. All sections were newly added.

## Sections Added

### Repository Registry (NEW)

Added table with 2 repository entries:
- backend (Rust backend service) mapped to serena_backend at /home/user/backend
- frontend-ui (TypeScript frontend) mapped to serena_ui at /home/user/frontend-ui

### Jira Configuration (NEW)

Added all 5 fields:
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### Code Intelligence (NEW)

Added tool naming convention documentation with `mcp__<instance>__<tool>` pattern and example using serena_backend. Added Limitations subheading noting no known limitations.

### Bug Configuration (NEW)

Added all 3 fields:
- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

### Security Configuration (NEW)

User opted in to security triage. Added complete section with three subsections:

#### Product Lifecycle
- Product pages URL: https://access.example.com/product-lifecycle
- Jira version prefix: MYPRODUCT
- Vulnerability issue type ID: 10200
- Component label pattern: pscomponent:
- VEX Justification custom field: customfield_12345

#### Version Streams
- 1 stream: 2.1.x

#### Source Repositories
- 2 repositories: backend, frontend-ui

## Sections Preserved

No existing sections to preserve — this was a greenfield setup. The existing CLAUDE.md content (project description, Documentation, Getting Started) was not modified.
