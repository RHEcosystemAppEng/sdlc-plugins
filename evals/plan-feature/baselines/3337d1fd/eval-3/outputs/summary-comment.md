# TC-9003: SBOM Comparison View — Planning Summary

## Tasks Created

| # | Task | Repository | Dependencies |
|---|---|---|---|
| 1 | Backend SBOM comparison model types | trustify-backend | — |
| 2 | Backend SBOM comparison service logic | trustify-backend | Task 1 |
| 3 | Backend SBOM comparison endpoint and integration tests | trustify-backend | Task 2 |
| 4 | Frontend SBOM comparison API types, client, and hook | trustify-ui | Task 3 |
| 5 | Frontend SBOM comparison page with diff section components | trustify-ui | Task 4 |
| 6 | Frontend route registration and SBOM list page integration | trustify-ui | Task 5 |

**Total: 6 tasks** (3 backend, 3 frontend)

## Repositories Affected

- **trustify-backend** — 3 new files, 3 modified files, 1 new API endpoint
- **trustify-ui** — 7 new files, 4 modified files, 1 new route

## Architecture Summary

The feature adds a structured SBOM diff capability with a clear separation across layers:

1. **Backend model layer** (Task 1): Rust structs defining the comparison response shape with six diff categories (added/removed packages, version changes, new/resolved vulnerabilities, license changes).
2. **Backend service layer** (Task 2): Comparison logic that fetches package and advisory data for two SBOMs and computes set differences. No new database tables — diff is computed on-the-fly.
3. **Backend endpoint layer** (Task 3): `GET /api/v2/sbom/compare?left={id1}&right={id2}` with query parameter validation and integration tests.
4. **Frontend API layer** (Task 4): TypeScript interfaces matching the backend response, Axios client function, and React Query hook with conditional fetching.
5. **Frontend UI layer** (Task 5): Comparison page with PatternFly components (Select for SBOM selection, ExpandableSection for diff categories, Table for data, EmptyState for initial load, Skeleton for loading).
6. **Frontend integration layer** (Task 6): Route registration and SBOM list page enhancement with row selection checkboxes and "Compare selected" action button.

## Workflow Mode

**Direct-to-main** — All changes are additive. The backend endpoint does not modify existing behavior. The frontend page is a new route. No database migrations, no breaking API changes. Cross-repo feature branches are impractical for separate repositories.

## Inherited Field Propagation

All 6 tasks inherit the following fields from feature TC-9003:

| Field | Value |
|---|---|
| Priority | Critical |
| Fix Versions | RHTPA 1.5.0 |

## Cross-Repository Dependency

Task 4 (frontend API layer) explicitly depends on Task 3 (backend endpoint). This establishes the cross-repo ordering: all backend tasks (1-3) must complete before frontend tasks (4-6) that consume the API can be implemented.
