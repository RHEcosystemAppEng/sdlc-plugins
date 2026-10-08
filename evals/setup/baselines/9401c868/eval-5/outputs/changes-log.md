# Setup Changes Log

## Summary

All sections were created from scratch -- the existing CLAUDE.md had no Project Configuration.

## Changes Made

### 1. Appended `# Project Configuration` heading

- Location: end of existing CLAUDE.md content
- Action: created new top-level heading

### 2. Created `## Repository Registry`

- Action: created table with 2 repository rows
- Rows added:
  - `backend | Rust backend service | serena_backend | /home/user/backend`
  - `frontend-ui | TypeScript frontend | serena_ui | /home/user/frontend-ui`

### 3. Created `## Jira Configuration`

- Action: created section with 5 fields
- Fields set:
  - Project key: TC
  - Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
  - Feature issue type ID: 10142
  - Git Pull Request custom field: customfield_10875
  - GitHub Issue custom field: customfield_10747

### 4. Created `## Code Intelligence`

- Action: created section with naming convention, example, and Limitations subsection
- Example uses `serena_backend` instance
- Limitations: none reported

### 5. Created `## Bug Configuration`

- Action: created section with 3 fields
- Fields set:
  - Bug issue type ID: 10001
  - Bug template: docs/bug-template.md
  - Bug-to-Task link type: Blocks

### 6. Created `## Security Configuration`

- Action: created section with 3 subsections

#### 6a. `### Product Lifecycle`

- Fields set:
  - Product pages URL: https://access.example.com/product-lifecycle
  - Jira version prefix: MYPRODUCT
  - Vulnerability issue type ID: 10200
  - Component label pattern: pscomponent:
  - VEX Justification custom field: customfield_12345
- Optional fields left empty: Upstream Affected Component, PS Component, Stream, ProdSec contact email, ProdSec Jira account ID, Embargo policy URL

#### 6b. `### Version Streams`

- Rows added:
  - `2.1.x | git.downstream.example.com/my-org/product-release.2.1.z | /home/user/product-release.2.1.z | security-matrix.md`

#### 6c. `### Source Repositories`

- Rows added:
  - `backend | https://github.com/example/backend | upstream`
  - `frontend-ui | https://github.com/example/frontend-ui | upstream`

### 7. Created `## Hierarchy Configuration`

- Action: created section with 1 field
- Fields set:
  - Default epic grouping strategy: by-sub-feature

## Files NOT Modified (Simulation Mode)

- `docs/constraints.md` -- would have been created from constraints.template.md
- `docs/bug-template.md` -- would have been created from bug-template.md template
- `CONVENTIONS.md` in backend -- would have been offered for scaffolding
- `CONVENTIONS.md` in frontend-ui -- would have been offered for scaffolding
- `security-matrix.md` -- scaffolding skipped per user request
