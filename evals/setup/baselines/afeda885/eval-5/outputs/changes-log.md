# Setup Changes Log

## Summary

The setup skill was executed against a CLAUDE.md with no existing Project Configuration section. All configuration sections were scaffolded from scratch.

## Changes Made

### 1. Repository Registry (NEW)

Added `## Repository Registry` table with two repositories discovered from Serena MCP instances:

| Repository | Role | Serena Instance | Path |
|---|---|---|---|
| backend | Rust backend service | serena_backend | /home/user/backend |
| frontend-ui | TypeScript frontend | serena_ui | /home/user/frontend-ui |

### 2. Jira Configuration (NEW)

Added `## Jira Configuration` with user-provided values:

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### 3. Jira Field Defaults (SKIPPED)

Not scaffolded. This subsection requires MCP or REST API discovery of available priorities and fixVersions, which is not available in simulation mode.

### 4. Code Intelligence (NEW)

Added `## Code Intelligence` section with:
- Tool naming convention: `mcp__<instance>__<tool>`
- Example using `serena_backend` instance
- `### Limitations` subsection: no limitations reported for either instance

### 5. Constraints Template (SIMULATED)

Would copy `constraints.template.md` to `docs/constraints.md` in the target project. Skipped in simulation mode.

### 6. CONVENTIONS.md Scaffolding (SIMULATED)

Would offer to scaffold CONVENTIONS.md for both repositories:
- `/home/user/backend/CONVENTIONS.md`
- `/home/user/frontend-ui/CONVENTIONS.md`
Skipped in simulation mode.

### 7. Bug Configuration (NEW)

Added `## Bug Configuration` with:
- Bug issue type ID: 10001 (discovered from Jira metadata)
- Bug template: docs/bug-template.md (user accepted default)
- Bug-to-Task link type: Blocks (user accepted default)

Bug template file copy skipped per simulation instructions.

### 8. Security Configuration (NEW)

Added `## Security Configuration` with three subsections:

#### Product Lifecycle
- Product pages URL: https://access.example.com/product-lifecycle
- Jira version prefix: MYPRODUCT
- Vulnerability issue type ID: 10200
- Component label pattern: pscomponent:
- VEX Justification custom field: customfield_12345
- Optional fields (Upstream Affected Component, PS Component, Stream, ProdSec contact email, ProdSec Jira account ID, Embargo policy URL): skipped by user

#### Version Streams
One stream configured:
- 2.1.x -> git.downstream.example.com/my-org/product-release.2.1.z

#### Source Repositories
Two repositories configured:
- backend (https://github.com/example/backend)
- frontend-ui (https://github.com/example/frontend-ui)

Supportability matrix population: declined by user.
security-matrix.md scaffolding: skipped by user.

### 9. Hierarchy Configuration (NEW)

Added `## Hierarchy Configuration` with:
- Default epic grouping strategy: by-sub-feature

## Files Written

| File | Action |
|---|---|
| outputs/claude-md-result.md | Created -- full CLAUDE.md with Project Configuration |
| outputs/discovery-log.md | Created -- step-by-step discovery log |
| outputs/changes-log.md | Created -- this file |

## Files Not Written (Simulation)

| File | Reason |
|---|---|
| docs/constraints.md | Simulation mode -- would be copied from constraints.template.md |
| docs/bug-template.md | Simulation mode -- would be copied from bug-template.md |
| /home/user/backend/CONVENTIONS.md | Simulation mode -- would be scaffolded from template |
| /home/user/frontend-ui/CONVENTIONS.md | Simulation mode -- would be scaffolded from template |
| security-matrix.md | User declined scaffolding |
