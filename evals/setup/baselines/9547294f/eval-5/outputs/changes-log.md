# Changes Log

## Summary

All sections were newly created since the existing CLAUDE.md had no Project Configuration.

## Sections Added

### 1. Repository Registry (NEW)

Added Repository Registry table with two repositories:
- `backend` -- Rust backend service, Serena instance: serena_backend, path: /home/user/backend
- `frontend-ui` -- TypeScript frontend, Serena instance: serena_ui, path: /home/user/frontend-ui

### 2. Jira Configuration (NEW)

Added Jira Configuration with all fields:
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### 3. Code Intelligence (NEW)

Added Code Intelligence section with:
- Tool naming convention explanation
- Example using serena_backend instance
- Limitations subsection (no limitations known)

### 4. Bug Configuration (NEW)

Added Bug Configuration section with:
- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

Note: Bug template file copy was skipped (simulation mode).

### 5. Security Configuration (NEW)

User opted in to security triage. Added Security Configuration section with:

**Product Lifecycle:**
- Product pages URL: https://access.example.com/product-lifecycle
- Jira version prefix: MYPRODUCT
- Vulnerability issue type ID: 10200
- Component label pattern: pscomponent:
- VEX Justification custom field: customfield_12345

**Version Streams:**
- 2.1.x: git.downstream.example.com/my-org/product-release.2.1.z (local: /home/user/product-release.2.1.z, matrix: security-matrix.md)

**Source Repositories:**
- backend: https://github.com/example/backend
- frontend-ui: https://github.com/example/frontend-ui

security-matrix.md scaffolding was skipped (user declined).
Supportability matrix population was skipped (user declined).

## Sections Not Modified

No existing sections were modified -- this was a greenfield setup.
