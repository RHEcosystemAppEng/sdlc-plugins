# Changes Log

## Sections Added to CLAUDE.md

### `# Project Configuration`

New top-level section added to house all project configuration.

### `## Repository Registry`

Added repository registry table with two entries:
- backend (Rust backend service) via serena_backend at /home/user/backend
- frontend-ui (TypeScript frontend) via serena_ui at /home/user/frontend-ui

### `## Jira Configuration`

Added Jira configuration with all five fields:
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### `## Code Intelligence`

Added Code Intelligence section documenting the `mcp__<instance>__<tool>` naming convention with a concrete example using `serena_backend`. No limitations reported for any instance.

### `## Bug Configuration`

Added Bug Configuration section with all three fields:
- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

### `## Security Configuration`

Added Security Configuration section with three subsections:

- **Product Lifecycle**: Product pages URL, Jira version prefix (MYPRODUCT), Vulnerability issue type ID (10200), Component label pattern (pscomponent:), VEX Justification custom field (customfield_12345)
- **Version Streams**: One stream — 2.1.x mapped to Konflux release repo git.downstream.example.com/my-org/product-release.2.1.z with local path /home/user/product-release.2.1.z and security matrix at security-matrix.md
- **Source Repositories**: Two repositories — backend (https://github.com/example/backend) and frontend-ui (https://github.com/example/frontend-ui)
