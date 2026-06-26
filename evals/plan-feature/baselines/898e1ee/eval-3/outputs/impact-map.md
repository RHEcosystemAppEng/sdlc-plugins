# Impact Map: TC-9003 — SBOM Comparison View

## Feature Overview
Add a side-by-side SBOM comparison view with a backend diffing endpoint and frontend comparison UI, enabling security analysts and compliance officers to see structured diffs between two SBOM versions.

## Repositories Impacted

### trustify-backend
| File Path | Action | Task(s) | Rationale |
|---|---|---|---|
| `modules/fundamental/src/sbom/model/comparison.rs` | Create | Task 2 | New model structs for the comparison response (SbomComparison, PackageDiff, VersionChange, VulnerabilityDiff, LicenseChange) |
| `modules/fundamental/src/sbom/model/mod.rs` | Modify | Task 2 | Re-export the new comparison module |
| `modules/fundamental/src/sbom/service/compare.rs` | Create | Task 3 | Comparison service with diff computation logic |
| `modules/fundamental/src/sbom/service/mod.rs` | Modify | Task 3 | Re-export the new compare service module |
| `modules/fundamental/src/sbom/endpoints/compare.rs` | Create | Task 4 | Axum handler for GET /api/v2/sbom/compare |
| `modules/fundamental/src/sbom/endpoints/mod.rs` | Modify | Task 4 | Register comparison route alongside existing SBOM routes |
| `tests/api/sbom_compare.rs` | Create | Task 5 | Integration tests for the comparison endpoint |

### trustify-ui
| File Path | Action | Task(s) | Rationale |
|---|---|---|---|
| `src/api/models.ts` | Modify | Task 6 | Add TypeScript interfaces for comparison response types |
| `src/api/rest.ts` | Modify | Task 6 | Add compareSboms() API client function |
| `src/hooks/useSbomComparison.ts` | Create | Task 7 | React Query hook for the comparison endpoint |
| `src/pages/SbomComparePage/SbomComparePage.tsx` | Create | Task 8 | Main comparison page component with toolbar and diff sections |
| `src/pages/SbomComparePage/components/DiffSection.tsx` | Create | Task 8 | Reusable collapsible diff section with ExpandableSection, Badge, and Table |
| `src/pages/SbomComparePage/components/SbomSelector.tsx` | Create | Task 8 | SBOM selector dropdown using PatternFly Select (typeahead) |
| `src/pages/SbomComparePage/components/ExportDropdown.tsx` | Create | Task 8 | Export dropdown with JSON/CSV options |
| `src/routes.tsx` | Modify | Task 8 | Add route for /sbom/compare |
| `src/App.tsx` | Modify | Task 8 | Add lazy import for SbomComparePage |
| `src/pages/SbomListPage/SbomListPage.tsx` | Modify | Task 9 | Add row selection checkboxes and "Compare selected" button |
| `tests/mocks/fixtures/sbom-comparison.json` | Create | Task 10 | Mock comparison response fixture |
| `tests/mocks/handlers.ts` | Modify | Task 10 | Add MSW handler for comparison endpoint |
| `tests/e2e/sbom-compare.spec.ts` | Create | Task 10 | Playwright E2E tests for comparison workflow |
| `src/pages/SbomComparePage/SbomComparePage.test.tsx` | Create | Task 10 | Unit tests for comparison page |

## API Changes

| Endpoint | Method | Action | Task(s) |
|---|---|---|---|
| `/api/v2/sbom/compare?left={id1}&right={id2}` | GET | NEW | Tasks 4, 5 (backend); Tasks 6, 7 (frontend client) |

## Dependency Graph

```
Task 1: Create feature branch (bookend: create-branch)
  |
  +---> Task 2: Backend comparison model
  |       |
  |       +---> Task 3: Backend comparison service
  |               |
  |               +---> Task 4: Backend comparison endpoint
  |                       |
  |                       +---> Task 5: Backend integration tests
  |
  +---> Task 6: Frontend API types and client
  |       |
  |       +---> Task 7: Frontend comparison hook
  |               |
  |               +---> Task 8: Frontend comparison page
  |                       |
  |                       +---> Task 9: Frontend SBOM list selection
  |                       |
  |                       +---> Task 10: Frontend E2E and MSW mocks
  |
  All Tasks 2-10 ---> Task 11: Merge feature branch (bookend: merge-branch)
```

## Task Summary

| Task | Repository | Title | Type |
|---|---|---|---|
| 1 | trustify-backend | Create feature branch | Bookend (create-branch) |
| 2 | trustify-backend | Backend comparison model structs | Implementation |
| 3 | trustify-backend | Backend comparison service | Implementation |
| 4 | trustify-backend | Backend comparison endpoint | Implementation |
| 5 | trustify-backend | Backend integration tests | Testing |
| 6 | trustify-ui | Frontend API types and client function | Implementation |
| 7 | trustify-ui | Frontend comparison hook | Implementation |
| 8 | trustify-ui | Frontend comparison page UI | Implementation |
| 9 | trustify-ui | Frontend SBOM list selection | Implementation |
| 10 | trustify-ui | Frontend E2E and MSW mocks | Testing |
| 11 | trustify-backend | Merge feature branch | Bookend (merge-branch) |

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Large SBOM diff computation exceeds p95 < 1s target | Medium | High | Task 3 uses HashMap-based O(n) algorithms; monitor with load tests against 2000-package SBOMs |
| Browser freezing on large diffs (>100 changed packages) | Medium | Medium | Task 8 implements virtualized lists for large sections |
| Version comparison direction detection inaccurate | Low | Low | Task 3 includes unit tests for upgrade/downgrade detection |
| Cross-repo integration issues between backend response and frontend types | Medium | Medium | Task 6 defines TypeScript interfaces matching exact backend JSON shape; Task 10 uses MSW mocks matching the contract |
