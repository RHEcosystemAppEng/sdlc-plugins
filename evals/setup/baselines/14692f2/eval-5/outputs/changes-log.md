# Setup Changes Log

## Summary

All Project Configuration sections were created from scratch. The existing CLAUDE.md had no Project Configuration section.

## Changes Made

### 1. Repository Registry — CREATED

Added `## Repository Registry` table with 2 repositories:

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| backend | Rust backend service | serena_backend | /home/user/backend |
| frontend-ui | TypeScript frontend | serena_ui | /home/user/frontend-ui |

### 2. Jira Configuration — CREATED

Added `## Jira Configuration` with:

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### 3. Jira Field Defaults — SKIPPED

Not created. Requires MCP or REST API connection to discover available priorities and fixVersions. This can be configured in a future setup run when MCP connectivity is available.

### 4. Code Intelligence — CREATED

Added `## Code Intelligence` section with:

- Tool naming convention documentation (`mcp__<instance>__<tool>`)
- Example using `serena_backend` instance
- `### Limitations` subsection (no limitations reported)

### 5. Bug Configuration — CREATED

Added `## Bug Configuration` with:

- Bug issue type ID: 10001
- Bug template: docs/bug-template.md
- Bug-to-Task link type: Blocks

Note: Bug template file copy was skipped (simulation mode).

### 6. Security Configuration — CREATED

Added `## Security Configuration` with:

#### Product Lifecycle
- Product pages URL: https://access.example.com/product-lifecycle
- Jira version prefix: MYPRODUCT
- Vulnerability issue type ID: 10200
- Component label pattern: pscomponent:
- VEX Justification custom field: customfield_12345
- Upstream Affected Component custom field: (empty — user skipped)
- PS Component custom field: (empty — user skipped)
- Stream custom field: (empty — user skipped)

#### Version Streams (1 stream)
| Stream | Konflux Release Repo | Local Path | Security Matrix Path |
|---|---|---|---|
| 2.1.x | git.downstream.example.com/my-org/product-release.2.1.z | /home/user/product-release.2.1.z | security-matrix.md |

#### Source Repositories (2 repos)
| Repository | URL |
|---|---|
| backend | https://github.com/example/backend |
| frontend-ui | https://github.com/example/frontend-ui |

### 7. Hierarchy Configuration — CREATED

Added `## Hierarchy Configuration` with:

- Default epic grouping strategy: by-sub-feature

### 8. Constraints Template — SKIPPED

Not copied to `docs/constraints.md` (simulation mode — no filesystem writes outside outputs/).

### 9. CONVENTIONS.md Scaffolding — SKIPPED

Not scaffolded for any repository (simulation mode — no filesystem writes outside outputs/).

### 10. Security Matrix Scaffolding — SKIPPED

User declined security-matrix.md scaffolding.

### 11. Supportability Matrix Population — SKIPPED

User declined supportability matrix population.

## Files Modified

- `CLAUDE.md` — Appended `# Project Configuration` section with all subsections (written to outputs/claude-md-result.md in simulation)

## Files Not Modified (Simulation)

- `docs/constraints.md` — Would have been created from constraints template
- `docs/bug-template.md` — Would have been created from bug template
- `CONVENTIONS.md` — Would have been scaffolded for each repository
- `security-matrix.md` — User declined scaffolding
