# Repository Impact Map — TC-9003: SBOM Comparison View

## trustify-backend

changes:
  - Add SBOM comparison diff model types (SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange)
  - Add SBOM comparison service logic to compute structured diff between two SBOMs using existing PackageService and AdvisoryService
  - Add GET /api/v2/sbom/compare endpoint with left/right query parameters returning structured diff
  - Add integration tests for the comparison endpoint covering added/removed packages, version changes, vulnerability diff, and license changes

## trustify-ui

changes:
  - Add TypeScript interfaces for the SBOM comparison API response types
  - Add API client function to call GET /api/v2/sbom/compare
  - Add React Query hook (useSbomComparison) for the comparison endpoint
  - Add SbomComparePage with header toolbar (SBOM selectors, Compare button, Export dropdown) and collapsible diff sections
  - Add route definition for /sbom/compare
  - Add unit tests for the comparison page components
  - Add MSW mock handler and fixture data for comparison endpoint

## Workflow Mode

**Mode: feature-branch**

**Rationale:** Atomicity indicator #4 (Tightly coupled feature components) is present — the frontend comparison page requires the new backend GET /api/v2/sbom/compare endpoint that does not yet exist. Neither side functions independently: the frontend page cannot render without the backend endpoint, and the backend endpoint provides no user value without the frontend UI. Merging either side alone to main would leave dead code or a broken UI.

**Interdependent tasks:** All frontend tasks (API types, client, hook, page) depend on the backend endpoint task. The backend endpoint task depends on the comparison service and models.

sha256-md:1f484b4b208092601a109bb74fe4f5be373bb49840a296eba6a5facb35b08c81
