# Repository Impact Map

**Feature**: TC-9003 — SBOM comparison view
**Priority**: Critical
**Fix Versions**: RHTPA 1.5.0

## trustify-backend

changes:
  - Add SBOM comparison diff model types (SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange) in modules/fundamental/src/sbom/model/
  - Implement SBOM comparison service method in modules/fundamental/src/sbom/service/ that computes the diff between two SBOMs by querying existing package, advisory, and license data
  - Add GET /api/v2/sbom/compare?left={id1}&right={id2} endpoint in modules/fundamental/src/sbom/endpoints/
  - Add integration tests for the comparison endpoint in tests/api/

## trustify-ui

changes:
  - Add TypeScript interfaces for the comparison API response in src/api/models.ts
  - Add API client function fetchSbomComparison() in src/api/rest.ts
  - Add React Query hook useSbomComparison() in src/hooks/
  - Create SBOM comparison page at src/pages/SbomComparePage/ with header toolbar (SBOM selectors, Compare button) and collapsible diff sections (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes)
  - Register /sbom/compare route in src/routes.tsx with URL query parameter support for left/right SBOM IDs
  - Add export functionality (JSON/CSV) for comparison results on the comparison page
  - Add unit tests for the comparison page components using Vitest + React Testing Library with MSW handlers
  - Add mock comparison data fixtures in tests/mocks/fixtures/

## Excluded requirements

None. All requirements (MVP and non-MVP) have been decomposed into actionable tasks across the two repositories.

## Workflow Mode Decision

**Selected mode**: `feature-branch`

**Rationale**: Atomicity indicator #4 (Tightly coupled feature components) is present. The frontend SBOM comparison page at `/sbom/compare` requires the new backend endpoint `GET /api/v2/sbom/compare` that does not yet exist. If the frontend PR were merged to main before the backend endpoint was deployed, the comparison page would call a nonexistent endpoint, leaving main in a broken state. This matches the indicator description: "the feature consists of frontend and backend changes where neither side functions independently (e.g., a new UI page that requires a new API endpoint that does not yet exist)."

**Interdependent tasks**:
- Tasks 4, 5, 6, 7 (frontend) depend on Tasks 2, 3 (backend) because the frontend comparison page calls the `GET /api/v2/sbom/compare` endpoint implemented in the backend
- The `workflow:feature-branch` label will be applied to the feature issue TC-9003 in Step 6a
