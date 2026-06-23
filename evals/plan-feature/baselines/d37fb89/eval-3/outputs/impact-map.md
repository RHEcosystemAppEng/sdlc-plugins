# Repository Impact Map — TC-9003: SBOM Comparison View

## Workflow Mode Decision

**Mode**: Feature-branch workflow
**Branch name**: TC-9003

**Rationale**: This is a tightly coupled cross-repo feature. The frontend comparison UI at `/sbom/compare` depends on a new backend API endpoint (`GET /api/v2/sbom/compare`) that does not exist yet. Frontend tasks cannot be developed or tested against `main` until the backend endpoint is merged. Feature-branch mode allows intermediate tasks to target a shared branch (`TC-9003`) in each repository, with bookend tasks to create and merge the branch.

## trustify-backend

| Area | Files | Change Type | Notes |
|---|---|---|---|
| Comparison model | `modules/fundamental/src/sbom/model/compare.rs` | Create | New `SbomComparison` response struct with diff categories |
| Comparison service | `modules/fundamental/src/sbom/service/compare.rs` | Create | Diff logic: load two SBOMs, compute added/removed packages, version changes, vulnerability diff, license changes |
| SBOM model module | `modules/fundamental/src/sbom/model/mod.rs` | Modify | Re-export `compare` module |
| SBOM service module | `modules/fundamental/src/sbom/service/mod.rs` | Modify | Re-export `compare` module |
| Comparison endpoint | `modules/fundamental/src/sbom/endpoints/compare.rs` | Create | `GET /api/v2/sbom/compare?left={id}&right={id}` handler |
| Endpoint registration | `modules/fundamental/src/sbom/endpoints/mod.rs` | Modify | Register comparison route |
| Integration tests | `tests/api/sbom_compare.rs` | Create | Tests for comparison endpoint: valid diff, missing SBOM, empty diff, large SBOM handling |

## trustify-ui

| Area | Files | Change Type | Notes |
|---|---|---|---|
| API types | `src/api/models.ts` | Modify | Add `SbomComparison` interface and related sub-types |
| API client | `src/api/rest.ts` | Modify | Add `fetchSbomComparison()` function |
| React Query hook | `src/hooks/useSbomComparison.ts` | Create | `useSbomComparison(leftId, rightId)` hook |
| Comparison page | `src/pages/SbomComparePage/SbomComparePage.tsx` | Create | Main comparison page with header toolbar and diff sections |
| Comparison page components | `src/pages/SbomComparePage/components/DiffSection.tsx` | Create | Reusable collapsible diff section with count badge and data table |
| Comparison page components | `src/pages/SbomComparePage/components/ComparisonToolbar.tsx` | Create | Header toolbar with SBOM selectors, Compare button, Export dropdown |
| Route registration | `src/routes.tsx` | Modify | Add `/sbom/compare` route |
| Unit tests | `src/pages/SbomComparePage/SbomComparePage.test.tsx` | Create | Tests for comparison page rendering, empty state, loading state, diff sections |
| Mock handlers | `tests/mocks/handlers.ts` | Modify | Add MSW handler for comparison endpoint |
| Mock fixtures | `tests/mocks/fixtures/sbom-comparison.json` | Create | Mock comparison response data |
| E2E tests | `tests/e2e/sbom-compare.spec.ts` | Create | Playwright E2E test for comparison workflow |

## Task Summary

| Task | Repository | Title | Depends On |
|---|---|---|---|
| 1 | — | Create feature branch TC-9003 from main | — |
| 2 | trustify-backend | SBOM comparison model and diff service | Task 1 |
| 3 | trustify-backend | SBOM comparison REST endpoint | Tasks 1, 2 |
| 4 | trustify-backend | Integration tests for SBOM comparison endpoint | Tasks 1, 3 |
| 5 | trustify-ui | API types and client function for SBOM comparison | Tasks 1, 3 |
| 6 | trustify-ui | SBOM comparison page with diff sections | Tasks 1, 5 |
| 7 | trustify-ui | Tests for SBOM comparison page | Tasks 1, 6 |
| 8 | — | Merge feature branch TC-9003 to main | Tasks 2, 3, 4, 5, 6, 7 |
