# Repository Impact Map — TC-9003: SBOM Comparison View

## Workflow Mode

**Mode:** `feature-branch`

**Rationale:** This feature exhibits the following atomicity indicators:

1. **Tightly coupled feature components** — The frontend comparison page (`/sbom/compare`) requires the new backend endpoint (`GET /api/v2/sbom/compare`). Neither side functions independently: the frontend page cannot render without the backend diff data, and the backend endpoint has no consumer without the frontend.
2. **Breaking API changes** — The frontend tasks consume a new API contract (`GET /api/v2/sbom/compare`) that does not yet exist. Merging the frontend without the backend (or vice versa) would leave `main` with a broken integration.

These indicators require all tasks to land together via a feature branch.

**Interdependent tasks:** All intermediate tasks are interdependent — the backend comparison endpoint (Tasks 2-3) must exist before the frontend comparison page (Tasks 4-6) can function, and the integration tests (Task 7) require both backend and frontend to be complete.

---

## Impact Map

```
trustify-backend:
  changes:
    - Add comparison model types (SbomComparisonResult, PackageDiff, VulnerabilityDiff, LicenseChange, VersionChange) to modules/fundamental/src/sbom/model/
    - Add SbomService::compare method that computes a structured diff between two SBOMs using existing package, advisory, and license data
    - Add GET /api/v2/sbom/compare endpoint with left/right query parameters in modules/fundamental/src/sbom/endpoints/
    - Register the comparison endpoint route in the SBOM endpoint module
    - Add integration tests for the comparison endpoint in tests/api/sbom.rs

trustify-ui:
  changes:
    - Add TypeScript interfaces for the comparison API response types in src/api/models.ts
    - Add compareSboms() API client function in src/api/rest.ts
    - Add useSbomComparison React Query hook in src/hooks/
    - Create SbomComparePage with header toolbar (SBOM selectors, Compare button, Export dropdown) and diff sections
    - Create page-specific components: DiffSection (expandable section with count badge and data table), SbomSelector (typeahead select)
    - Add /sbom/compare route to src/routes.tsx
    - Add MSW mock handler and fixture data for the comparison endpoint in tests/mocks/
    - Add unit tests for SbomComparePage
```
