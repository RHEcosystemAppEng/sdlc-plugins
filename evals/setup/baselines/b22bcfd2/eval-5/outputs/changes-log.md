# Setup Changes Log

## Summary

Full Project Configuration created from scratch. The existing CLAUDE.md had no Project Configuration section.

## Changes Made

### 1. Repository Registry — CREATED

Added 2 repositories discovered from Serena MCP instances:

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| backend | Rust backend service | serena_backend | /home/user/backend |
| frontend-ui | TypeScript frontend | serena_ui | /home/user/frontend-ui |

### 2. Jira Configuration — CREATED

Added Jira configuration with user-provided values:

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### 3. Code Intelligence — CREATED

Added Code Intelligence section documenting:
- MCP tool naming convention: `mcp__<instance>__<tool>`
- Example using `serena_backend` instance
- Limitations subsection (no known limitations)

### 4. Bug Configuration — CREATED

Added Bug Configuration with:
- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

Note: Bug template file copy was skipped (simulation mode).

### 5. Security Configuration — CREATED

Added Security Configuration with:

**Product Lifecycle:**
- Product pages URL: https://access.example.com/product-lifecycle
- Jira version prefix: MYPRODUCT
- Vulnerability issue type ID: 10200
- Component label pattern: pscomponent:
- VEX Justification custom field: customfield_12345

**Version Streams (1 stream):**
- 2.1.x -> git.downstream.example.com/my-org/product-release.2.1.z

**Source Repositories (2 repositories):**
- backend (https://github.com/example/backend) — upstream
- frontend-ui (https://github.com/example/frontend-ui) — upstream

### 6. Hierarchy Configuration — CREATED

Added Hierarchy Configuration with:
- Default epic grouping strategy: by-sub-feature

## Files Not Modified (Simulation)

- `docs/constraints.md` — would have been created from constraints template
- `docs/bug-template.md` — would have been created from bug template
- `CONVENTIONS.md` in backend and frontend-ui — scaffolding not attempted in simulation
- `security-matrix.md` — scaffolding skipped per user request
