## TC-9003: SBOM Comparison View — Implementation Plan

### Tasks

| # | Title | Repository | Target Branch | Dependencies |
|---|---|---|---|---|
| 1 | create-branch | trustify-backend, trustify-ui | main | — |
| 2 | backend-comparison-model | trustify-backend | TC-9003 | Task 1 |
| 3 | backend-comparison-service | trustify-backend | TC-9003 | Task 1, Task 2 |
| 4 | backend-comparison-endpoint | trustify-backend | TC-9003 | Task 1, Task 3 |
| 5 | backend-integration-tests | trustify-backend | TC-9003 | Task 1, Task 4 |
| 6 | frontend-api-layer | trustify-ui | TC-9003 | Task 1, Task 4 |
| 7 | frontend-comparison-page | trustify-ui | TC-9003 | Task 1, Task 6 |
| 8 | frontend-tests-mocks | trustify-ui | TC-9003 | Task 1, Task 7 |
| 9 | merge-branch | trustify-backend, trustify-ui | main | Tasks 2-8 |

### Repositories Affected
- **trustify-backend** — Tasks 2, 3, 4, 5 (model, service, endpoint, integration tests)
- **trustify-ui** — Tasks 6, 7, 8 (API layer, comparison page, tests/mocks)

### Architecture Summary

This feature adds a structured SBOM comparison capability spanning both repositories:

**Backend (trustify-backend):**
- New `SbomComparison` model with six diff categories (added/removed packages, version changes, new/resolved vulnerabilities, license changes)
- `SbomComparisonService` that computes diffs on-the-fly from existing package and advisory data (no new database tables)
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` endpoint returning the comparison JSON
- Integration tests covering success, error, and edge cases

**Frontend (trustify-ui):**
- TypeScript interfaces matching the backend response contract
- `compareSboms()` API client function and `useSbomComparison` React Query hook
- `SbomComparePage` at `/sbom/compare` with PatternFly components: `Select` for SBOM selection, `ExpandableSection` for diff categories, composable `Table` for data display, `Badge` for counts, `EmptyState` for initial state
- MSW-based test mocks and comprehensive unit tests

### Workflow

**workflow:feature-branch** — This feature uses bookend tasks (create-branch / merge-branch) to isolate cross-repo development on the `TC-9003` feature branch before merging to `main`.

### Inherited Fields

Inherited fields propagated to tasks: priority=Critical, fixVersion=RHTPA 1.5.0
