# Repository Impact Map — TC-9003: SBOM Comparison View

## trustify-backend

changes:
  - Add comparison response model types (SbomComparisonResult, PackageDiff, VersionChange, VulnerabilityDiff, LicenseChange) in the sbom model module
  - Add comparison service method to SbomService that computes structured diffs between two SBOMs by comparing their package sets, advisory associations, and license mappings
  - Add `GET /api/v2/sbom/compare?left={id1}&right={id2}` endpoint that accepts two SBOM IDs, invokes the comparison service, and returns the structured diff response
  - Add integration tests for the comparison endpoint covering: valid comparison, identical SBOMs, non-existent SBOM IDs, and large package sets

## trustify-ui

changes:
  - Add TypeScript interfaces for the comparison API response types (SbomComparisonResult, PackageDiff, VersionChange, VulnerabilityDiff, LicenseChange)
  - Add API client function `compareSboms(leftId, rightId)` in rest.ts
  - Add React Query hook `useSbomComparison(leftId, rightId)` for data fetching
  - Add SbomComparePage component with header toolbar (SBOM selectors, Compare button, Export dropdown) and collapsible diff sections (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes)
  - Add route `/sbom/compare` with URL query parameter support for `left` and `right` SBOM IDs
  - Add "Compare selected" action to SbomListPage for selecting two SBOMs and navigating to comparison
  - Add unit tests for comparison page components and E2E test for the comparison workflow

## Workflow Mode

**Mode**: feature-branch
**Rationale**: Atomicity indicator #4 (tightly coupled feature components) — the frontend comparison UI requires the new backend `GET /api/v2/sbom/compare` endpoint. Neither side functions independently; merging the frontend without the backend would result in a broken comparison page, and the backend endpoint has no consumers until the frontend lands. Additionally, atomicity indicator #2 applies — the frontend depends on a new API contract that does not yet exist.
**Interdependent tasks**: All frontend tasks depend on the backend comparison endpoint being available. The backend endpoint has no existing consumers, so it provides no value until the frontend is merged.
