## TC-9003: SBOM Comparison View -- Implementation Plan

### Architecture Summary

This feature adds a side-by-side SBOM comparison capability across two repositories. The **trustify-backend** provides a new `GET /api/v2/sbom/compare` endpoint that computes a structured diff between two SBOMs on-the-fly (no new database tables), covering added/removed packages, version changes, new/resolved vulnerabilities, and license changes. The **trustify-ui** provides a Figma-driven comparison page at `/sbom/compare` with PatternFly components (Select dropdowns, ExpandableSection diffs, composable Tables, Badge counts), plus a "Compare selected" action on the existing SBOM list page.

### Task Breakdown

| # | Task | Repository | Dependencies |
|---|---|---|---|
| 1 | SBOM comparison data model (SbomComparisonResult struct) | trustify-backend | -- |
| 2 | SBOM comparison service (diff logic in SbomService) | trustify-backend | Task 1 |
| 3 | SBOM comparison endpoint (GET /api/v2/sbom/compare) | trustify-backend | Task 1, Task 2 |
| 4 | Backend integration tests | trustify-backend | Task 3 |
| 5 | Frontend API types, client function, and React Query hook | trustify-ui | Task 3 |
| 6 | SBOM comparison page UI (Figma design, PatternFly components) | trustify-ui | Task 5 |
| 7 | MSW mocks and comprehensive unit tests | trustify-ui | Task 5, Task 6 |
| 8 | SBOM list selection with "Compare selected" action | trustify-ui | Task 6 |

### Cross-repo Dependencies

- Task 5 (frontend API types/hook) depends on Task 3 (backend endpoint) -- the frontend data layer requires the backend comparison endpoint to exist.
- Backend tasks (1-4) have lower task numbers than all frontend tasks (5-8), ensuring the API contract is established before UI integration begins.

### Repositories Affected

- **trustify-backend** (Rust, Axum, SeaORM): Tasks 1-4
- **trustify-ui** (React, TypeScript, PatternFly 5, React Query): Tasks 5-8

### Field Propagation

- **Priority:** Critical (inherited from Feature TC-9003, propagated to all tasks)
- **Fix Versions:** RHTPA 1.5.0 (inherited from Feature TC-9003, propagated to all tasks -- default scope "both" applies)
