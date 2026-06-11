# Changes Log

All sections newly added (greenfield setup — no prior Project Configuration existed).

## Repository Registry

- Section newly added
- 2 entries added:
  - `backend` — Rust backend service, Serena instance `serena_backend`, path `/home/user/backend`
  - `frontend-ui` — TypeScript frontend, Serena instance `serena_ui`, path `/home/user/frontend-ui`

## Jira Configuration

- Section newly added
- All 5 fields added:
  - Project key: TC
  - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
  - Feature issue type ID: 10142
  - Git Pull Request custom field: customfield_10875
  - GitHub Issue custom field: customfield_10747

## Code Intelligence

- Section newly added
- Naming convention documented (`mcp__<instance>__<tool>` prefix pattern with example)
- Limitations subsection added for both Serena instances:
  - `serena_backend`: No known limitations
  - `serena_ui`: No known limitations

## Security Configuration

- Section newly added with 3 subsections:

### Product Lifecycle

- 5 fields added:
  - Product pages URL: https://access.example.com/product-lifecycle
  - Jira version prefix: MYPRODUCT
  - Vulnerability issue type ID: 10200
  - Component label pattern: pscomponent:
  - VEX Justification custom field: customfield_12345

### Version Streams

- 1 stream added:
  - 2.1.x — Konflux release repo `git.downstream.example.com/my-org/product-release.2.1.z`, local path `/home/user/product-release.2.1.z`, security matrix path `security-matrix.md`

### Source Repositories

- 2 repositories added:
  - backend — https://github.com/example/backend
  - frontend-ui — https://github.com/example/frontend-ui
