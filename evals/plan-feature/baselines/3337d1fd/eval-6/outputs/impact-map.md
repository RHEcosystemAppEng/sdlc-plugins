# Impact Map: TC-9006 — Add vulnerability remediation tracking dashboard

## Feature
- **Key**: TC-9006
- **Summary**: Add vulnerability remediation tracking dashboard
- **Priority**: Major (inherited by all tasks)
- **Fix Versions**: RHTPA 1.5.0 (inherited by all tasks)

## Workflow Mode
direct-to-main

## Epic Hierarchy

Epic 1: TC-9006: trustify-backend
  Issue Type: Epic (level-1)
  Parent: TC-9006
  Tasks: [Task 1, Task 2, Task 3, Task 4]
  Link: Feature TC-9006 --Incorporates--> this Epic

Epic 2: TC-9006: trustify-ui
  Issue Type: Epic (level-1)
  Parent: TC-9006
  Tasks: [Task 5, Task 6, Task 7, Task 8, Task 9, Task 10]
  Link: Feature TC-9006 --Incorporates--> this Epic

## Field Inheritance
- **Priority**: Major — inherited from Feature TC-9006, propagated to all Epics and Tasks
- **Fix Versions**: RHTPA 1.5.0 — inherited from Feature TC-9006, propagated to all Epics and Tasks

## Repositories Affected
1. **trustify-backend** — Rust backend service (Axum + SeaORM)
2. **trustify-ui** — React/TypeScript frontend (PatternFly 5 + React Query)

## Task Summary

### Epic 1: TC-9006: trustify-backend

| Task | Summary | Repository | Dependencies |
|------|---------|------------|--------------|
| Task 1 | Create remediation module with model types | trustify-backend | None |
| Task 2 | Implement remediation service with aggregation queries | trustify-backend | Task 1 |
| Task 3 | Create remediation API endpoints | trustify-backend | Task 2 |
| Task 4 | Add integration tests for remediation endpoints | trustify-backend | Task 3 |

### Epic 2: TC-9006: trustify-ui

| Task | Summary | Repository | Dependencies |
|------|---------|------------|--------------|
| Task 5 | Add remediation API types, client functions, and React Query hooks | trustify-ui | Task 3 |
| Task 6 | Create remediation dashboard page with summary cards and progress chart | trustify-ui | Task 5 |
| Task 7 | Create filterable vulnerability table component | trustify-ui | Task 5 |
| Task 8 | Integrate dashboard routing and navigation | trustify-ui | Task 6, Task 7 |
| Task 9 | Add unit and E2E tests for remediation dashboard | trustify-ui | Task 8 |
| Task 10 | Documentation for remediation dashboard and API endpoints | trustify-ui | Task 8 |

## Dependency Graph

```
Task 1 (models)
  └─> Task 2 (service)
        └─> Task 3 (endpoints)
              ├─> Task 4 (backend tests)
              └─> Task 5 (API types + hooks)
                    ├─> Task 6 (dashboard page)
                    │     └─> Task 8 (routing)
                    └─> Task 7 (vulnerability table)
                          └─> Task 8 (routing)
                                ├─> Task 9 (frontend tests)
                                └─> Task 10 (documentation)
```

## Incorporates Links
- Feature TC-9006 --Incorporates--> Epic 1 (TC-9006: trustify-backend)
- Feature TC-9006 --Incorporates--> Epic 2 (TC-9006: trustify-ui)

Note: Incorporates links are from Feature to Epics only, NOT from Feature directly to Tasks. Tasks are children of their respective Epics.

## Architecture Summary

### Backend (trustify-backend)
- New `remediation` module under `modules/fundamental/src/` following the model/service/endpoints pattern
- Aggregation service computes counts from existing entity tables (advisory, sbom_advisory, sbom) — no new database tables
- Two new REST endpoints: GET /api/v2/remediation/summary and GET /api/v2/remediation/by-product
- Paginated responses using existing PaginatedResults<T> wrapper

### Frontend (trustify-ui)
- New page directory `src/pages/RemediationDashboardPage/` with dashboard component and subcomponents
- Summary cards showing Open/In Progress/Resolved counts by severity
- Progress chart showing remediation trend over time
- Filterable vulnerability table with severity, product, and status filters
- Route at /remediation with lazy loading, navigation menu entry
- React Query hooks for data fetching, MSW mocks for testing

## Non-Functional Requirements Addressed
- Summary endpoint p95 < 500ms (Task 2 service design, Task 4 performance testing)
- Dashboard handles up to 10,000 tracked vulnerabilities (Task 6 rendering, Task 7 pagination)
- No new database tables (Task 2 aggregation from existing entities)
