# Setup Changes Log

## Summary

Created the full `# Project Configuration` section in CLAUDE.md. The existing file had no Project Configuration, so all sections were created from scratch.

## Changes Made

### 1. Repository Registry (NEW)

Added `## Repository Registry` table with 2 entries:

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| backend | Rust backend service | serena_backend | /home/user/backend |
| frontend-ui | TypeScript frontend | serena_ui | /home/user/frontend-ui |

### 2. Jira Configuration (NEW)

Added `## Jira Configuration` with the following fields:

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### 3. Code Intelligence (NEW)

Added `## Code Intelligence` section with:
- Tool naming convention explanation (`mcp__<instance>__<tool>`)
- Example using `serena_backend` instance
- `### Limitations` subsection (no limitations known)

### 4. Bug Configuration (NEW)

Added `## Bug Configuration` section with:
- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

### 5. Hierarchy Configuration (NEW)

Added `## Hierarchy Configuration` section with:
- Default epic grouping strategy: by-sub-feature

### 6. Security Configuration (NEW)

Added `## Security Configuration` section with:

#### Product Lifecycle
- Product pages URL: https://access.example.com/product-lifecycle
- Jira version prefix: MYPRODUCT
- Vulnerability issue type ID: 10200
- Component label pattern: pscomponent:
- VEX Justification custom field: customfield_12345
- Upstream Affected Component custom field: (not configured)
- PS Component custom field: (not configured)
- Stream custom field: (not configured)
- ProdSec contact email: (not configured)
- ProdSec Jira account ID: (not configured)

#### Version Streams
| Stream | Konflux Release Repo | Local Path | Security Matrix Path |
|---|---|---|---|
| 2.1.x | git.downstream.example.com/my-org/product-release.2.1.z | /home/user/product-release.2.1.z | security-matrix.md |

#### Source Repositories
| Repository | URL |
|---|---|
| backend | https://github.com/example/backend |
| frontend-ui | https://github.com/example/frontend-ui |

## Files Not Modified (Simulation)

- `docs/constraints.md` — would be created from constraints template (skipped in simulation)
- `docs/bug-template.md` — would be created from bug template (skipped in simulation)
- `security-matrix.md` — user declined scaffolding
- `CONVENTIONS.md` — not scaffolded in this simulation
