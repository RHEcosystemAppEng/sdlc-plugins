# Plan Summary: TC-9006 — Add vulnerability remediation tracking dashboard

## Tasks Created
- **10 tasks** total across 2 repositories
- **4 backend tasks** (Tasks 1-4) in trustify-backend
- **6 frontend tasks** (Tasks 5-10) in trustify-ui

## Epics Created
- **Epic 1**: TC-9006: trustify-backend (Issue Type: Epic, level-1; Parent: TC-9006)
  - Contains Tasks 1, 2, 3, 4
- **Epic 2**: TC-9006: trustify-ui (Issue Type: Epic, level-1; Parent: TC-9006)
  - Contains Tasks 5, 6, 7, 8, 9, 10

## Repositories Affected
1. **trustify-backend** — Rust backend (Axum, SeaORM, PostgreSQL)
2. **trustify-ui** — React/TypeScript frontend (PatternFly 5, React Query, Vite)

## Architecture Summary

**Backend**: A new `remediation` module is added under `modules/fundamental/src/` following the existing model/service/endpoints pattern. The service aggregates vulnerability remediation data from existing entity tables (advisory, sbom_advisory, sbom, package) without creating new database tables. Two REST endpoints are exposed: `GET /api/v2/remediation/summary` returns severity-by-status counts, and `GET /api/v2/remediation/by-product` returns paginated per-product remediation breakdowns.

**Frontend**: A new `RemediationDashboardPage` is created under `src/pages/` with summary cards (Open/In Progress/Resolved by severity), a progress chart (remediation trend over time), and a filterable vulnerability table (filter by severity, product, status). The page is accessible at `/remediation` with a navigation menu entry. Data fetching uses React Query hooks wrapping Axios API client functions.

## Incorporates Link Decisions
- Feature TC-9006 --Incorporates--> Epic 1 (TC-9006: trustify-backend)
- Feature TC-9006 --Incorporates--> Epic 2 (TC-9006: trustify-ui)
- Links are from Feature to Epics only. Tasks are children of their respective Epics, not directly linked to the Feature.
- Grouping strategy: by-repository (one Epic per repository)

## Inherited Field Propagation
- **Priority**: Major — inherited from Feature TC-9006, propagated to both Epics and all 10 Tasks
- **Fix Versions**: RHTPA 1.5.0 — inherited from Feature TC-9006, propagated to both Epics and all 10 Tasks

## Documentation Task
- Task 10 addresses the "New Content" documentation impact identified in the Feature description
- Covers user guide for the dashboard and API reference for aggregation endpoints

## Dependency Ordering
- Backend tasks (1-4) have lower task numbers than frontend tasks (5-10)
- Frontend tasks depend on backend API endpoints being defined (Task 5 depends on Task 3)
- Testing and documentation tasks depend on implementation tasks being complete
