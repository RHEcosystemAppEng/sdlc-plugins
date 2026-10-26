# Repository Impact Map — TC-9003: SBOM Comparison View

## trustify-backend

changes:
  - Add SBOM comparison result model types (SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange) in `modules/fundamental/src/sbom/model/`
  - Add comparison diff service method to SbomService that computes the structured diff between two SBOMs by comparing their linked packages, advisories, and licenses
  - Add `GET /api/v2/sbom/compare?left={id1}&right={id2}` endpoint handler in `modules/fundamental/src/sbom/endpoints/`
  - Register the new comparison route in `modules/fundamental/src/sbom/endpoints/mod.rs`
  - Add integration tests for the comparison endpoint in `tests/api/sbom.rs`

## trustify-ui

changes:
  - Add TypeScript interfaces for the comparison API response types in `src/api/models.ts`
  - Add REST client function `fetchSbomComparison()` in `src/api/rest.ts`
  - Add React Query hook `useSbomComparison` in `src/hooks/`
  - Create comparison page `SbomComparePage` under `src/pages/` with PatternFly ExpandableSection diff sections, Select dropdowns for SBOM selection, SeverityBadge for vulnerability display, and empty/loading states
  - Register `/sbom/compare` route in `src/routes.tsx`
  - Modify `SbomListPage` to add checkbox selection and "Compare selected" button that navigates to the comparison page with query params
  - Add export dropdown (JSON/CSV) on the comparison page (non-MVP requirement)

## Workflow Mode Decision

**Selected mode:** `feature-branch`

**Rationale:** Two atomicity indicators are present:

1. **Tightly coupled feature components (indicator #4):** The frontend comparison page (`/sbom/compare`) requires the new backend endpoint `GET /api/v2/sbom/compare` that does not yet exist. Neither side functions independently — merging only the backend adds an unused endpoint, and merging only the frontend creates a page that calls a nonexistent API.

2. **Breaking API changes (indicator #2):** The frontend tasks consume an API contract (request path, query parameters, response shape) that is created by a backend task. Merging only the frontend side would break the comparison page with failed API calls.

**Interdependent tasks:**
- Backend Task 3 (comparison endpoint) creates the API that Frontend Tasks 5-7 consume
- Frontend Task 5 (API client/hook) directly depends on Backend Task 3's endpoint contract
- Frontend Tasks 6-7 depend on Task 5's hook, which depends on the backend endpoint

The `workflow:feature-branch` label will be applied to the TC-9003 feature issue.

## Excluded Requirements

None. All requirements (MVP and non-MVP) have sufficient specification and target repositories for task decomposition. The non-MVP requirement (Export diff as JSON/CSV) is included as Task 8 and can be deprioritized if needed.
