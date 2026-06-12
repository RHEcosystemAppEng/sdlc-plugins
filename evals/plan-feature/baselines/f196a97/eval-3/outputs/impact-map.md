# Repository Impact Map — TC-9003: SBOM Comparison View

## trustify-backend

changes:
  - Add SBOM comparison diff model structs (SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange)
  - Add comparison service method to SbomService that loads two SBOMs with their packages and advisories, computes the structured diff on-the-fly
  - Add GET /api/v2/sbom/compare endpoint with left/right query params, returning the structured diff response
  - Add integration tests for the comparison endpoint covering happy path, missing SBOM ID, same SBOM comparison, and large diff performance

## trustify-ui

changes:
  - Add TypeScript interfaces for the comparison API response types in api/models.ts
  - Add API client function fetchSbomComparison() in api/rest.ts
  - Add React Query hook useSbomComparison() in hooks/
  - Add SbomComparePage component with SBOM selectors, Compare button, diff sections (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes)
  - Add route definition for /sbom/compare in routes.tsx
  - Add checkbox selection support to SbomListPage with "Compare selected" action button
  - Add MSW mock handler and test fixtures for the comparison endpoint
  - Add unit tests for SbomComparePage
  - Add Playwright E2E test for the comparison workflow

## Workflow Mode

**Mode:** feature-branch

**Rationale:** Atomicity indicator 4 (tightly coupled feature components) is present. The frontend comparison page requires the new backend comparison endpoint (GET /api/v2/sbom/compare) that does not yet exist. Merging the frontend comparison page to main before the backend endpoint is available would expose a non-functional page to users. The frontend tasks (SbomComparePage, route, hooks) are interdependent with the backend task (comparison endpoint).

**Interdependent tasks:**
- Frontend tasks (comparison page, hooks, route) depend on backend task (comparison endpoint) being available
- The frontend comparison page cannot render meaningful results without the backend diff computation
- The SBOM list page selection UI depends on the comparison page route existing

**Bookend repository:** trustify-ui (majority of implementation tasks)
