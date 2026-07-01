# Repository Impact Map — TC-9003: SBOM Comparison View

## trustify-backend

changes:
  - Add SBOM comparison diff model types (SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange)
  - Add SbomService method to compute the structured diff between two SBOMs by querying existing package, advisory, and license data
  - Add GET /api/v2/sbom/compare endpoint with query parameters left and right returning the structured diff response
  - Add integration tests for the comparison endpoint covering added/removed packages, version changes, vulnerability changes, and license changes

## trustify-ui

changes:
  - Add TypeScript interfaces for the comparison API response shape (SbomComparisonResult and nested types)
  - Add API client function fetchSbomComparison(leftId, rightId) in rest.ts
  - Add React Query hook useSbomComparison for the comparison endpoint
  - Add SbomComparePage component at /sbom/compare with header toolbar (SBOM selectors, Compare button, Export dropdown) and collapsible diff sections (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes)
  - Add route definition for /sbom/compare in routes.tsx
  - Add checkbox selection and "Compare selected" button to SbomListPage for triggering comparison navigation
  - Add unit tests for SbomComparePage component and E2E test for the comparison workflow

## Workflow Mode

**Mode**: feature-branch

**Rationale**: This feature exhibits atomicity indicator #4 (tightly coupled feature components) — the frontend comparison page requires the new backend `GET /api/v2/sbom/compare` endpoint that does not exist on main. Merging the frontend without the backend would result in a broken comparison page. Additionally, atomicity indicator #2 (breaking API changes) applies — the frontend consumes a new API contract that must exist before the UI can function.

**Interdependent tasks**: All frontend tasks (API client, comparison page, list page selection) depend on the backend comparison endpoint task. The backend endpoint task depends on the backend service task.

The `workflow:feature-branch` label will be applied to the TC-9003 feature issue. Intermediate tasks will target the TC-9003 branch.
