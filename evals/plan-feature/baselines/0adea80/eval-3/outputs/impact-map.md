# Repository Impact Map — TC-9003: SBOM Comparison View

## trustify-backend

changes:
  - Add SBOM comparison diff model structs (SbomComparisonResult with added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes)
  - Add SBOM comparison service logic to compute structured diff between two SBOMs on-the-fly from existing package/advisory data
  - Add GET /api/v2/sbom/compare endpoint with left/right query parameters returning the structured diff
  - Add integration tests for the comparison endpoint covering normal diff, empty diff, large SBOM performance, and invalid SBOM IDs

## trustify-ui

changes:
  - Add TypeScript interfaces for the SBOM comparison API response shape
  - Add API client function to call GET /api/v2/sbom/compare
  - Add React Query hook (useSbomComparison) for the comparison endpoint
  - Add SbomComparePage component with SBOM selectors, compare button, and diff sections per Figma design
  - Add diff section components (AddedPackagesTable, RemovedPackagesTable, VersionChangesTable, NewVulnerabilitiesTable, ResolvedVulnerabilitiesTable, LicenseChangesTable) using PatternFly ExpandableSection and Table
  - Add route definition for /sbom/compare with URL query parameter support for left/right SBOM IDs
  - Add unit tests for the comparison page and diff section components
  - Add MSW mock handlers and fixtures for the comparison endpoint

## Workflow Mode

**Selected mode:** `feature-branch`

**Rationale:** Atomicity indicator #4 (tightly coupled feature components) applies. The frontend comparison page requires the new backend `GET /api/v2/sbom/compare` endpoint, which does not yet exist. Merging only the frontend would produce a non-functional page calling a missing endpoint; merging only the backend provides no user-facing value. Both sides must land together for the feature to function.

**Interdependent tasks:** All backend and frontend implementation tasks are interdependent. The frontend API client, hook, and page components depend on the backend endpoint existing. The merge-branch task depends on all intermediate tasks.
