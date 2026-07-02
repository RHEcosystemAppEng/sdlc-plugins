# Epics for TC-9006: Vulnerability Remediation Tracking Dashboard

## Grouping Strategy

**by-repository** — one Epic per repository that contains tasks for this feature.

## Epics

### Epic 1: TC-9006: trustify-backend

- **Summary**: TC-9006: trustify-backend
- **Issue Type**: Epic (level 1)
- **Parent**: TC-9006
- **Priority**: Major
- **Fix Versions**: RHTPA 1.5.0
- **Labels**: ai-generated-jira
- **Description**: Backend implementation for the vulnerability remediation tracking dashboard. Adds a new remediation module under `modules/fundamental/` with aggregation models, a service that computes remediation statistics from existing SBOM and advisory data, and two REST endpoints: `GET /api/v2/remediation/summary` (counts by severity and status) and `GET /api/v2/remediation/by-product` (per-product breakdown). Includes integration tests and API reference documentation.
- **Tasks**: Task 1, Task 2, Task 3, Task 8

### Epic 2: TC-9006: trustify-ui

- **Summary**: TC-9006: trustify-ui
- **Issue Type**: Epic (level 1)
- **Parent**: TC-9006
- **Priority**: Major
- **Fix Versions**: RHTPA 1.5.0
- **Labels**: ai-generated-jira
- **Description**: Frontend implementation for the vulnerability remediation tracking dashboard. Adds TypeScript API types and client functions, React Query hooks, and a new dashboard page at `/remediation` with summary cards, a progress chart, and a filterable vulnerability table. Uses PatternFly 5 components and follows the existing page structure conventions. Includes unit tests with MSW mocking and a Playwright E2E test.
- **Tasks**: Task 4, Task 5, Task 6, Task 7

## Links

- TC-9006 **incorporates** Epic "TC-9006: trustify-backend"
- TC-9006 **incorporates** Epic "TC-9006: trustify-ui"

Note: Individual tasks are children of their respective Epic, not linked directly to Feature TC-9006.
