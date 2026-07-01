# Repository Impact Map — TC-9003: SBOM Comparison View

## trustify-backend

changes:
  - Add SBOM comparison diff model structs (SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange)
  - Add SBOM comparison service method to compute diff between two SBOMs using existing package, advisory, and license data
  - Add GET /api/v2/sbom/compare endpoint with left/right query parameters
  - Add integration tests for the comparison endpoint covering added/removed packages, version changes, vulnerability changes, and license changes

## trustify-ui

changes:
  - Add TypeScript interfaces for the SBOM comparison API response shape
  - Add API client function to call the comparison endpoint
  - Add React Query hook for the comparison API call
  - Add SbomComparePage with header toolbar (SBOM selectors, Compare button, Export dropdown) and collapsible diff sections per Figma design
  - Add diff section components (AddedPackagesTable, RemovedPackagesTable, VersionChangesTable, NewVulnerabilitiesTable, ResolvedVulnerabilitiesTable, LicenseChangesTable)
  - Add route definition for /sbom/compare
  - Add SBOM selection checkboxes and "Compare selected" action to the SbomListPage
  - Add unit tests for the comparison page and diff section components
  - Add MSW handlers and mock fixtures for the comparison endpoint

## Workflow Mode

**Selected mode: feature-branch**

**Rationale:** Atomicity indicator #4 (Tightly coupled feature components) is present — the frontend comparison page requires the new backend `GET /api/v2/sbom/compare` endpoint, which does not yet exist. Merging the frontend without the backend would result in a broken comparison page. The backend endpoint alone is non-functional without a consumer but is harmless; however, the frontend PR would break if merged to main before the backend endpoint is available.

**Interdependent tasks:**
- The frontend comparison page task depends on the backend comparison endpoint task — the frontend calls an endpoint that must exist for the feature to work.
- The SbomListPage selection UI task depends on the frontend comparison page task for the navigation target.

The `workflow:feature-branch` label will be applied to the TC-9003 feature issue.

## Epic Grouping

**Strategy: by-sub-feature** (from Hierarchy Configuration in CLAUDE.md)

**Epic groups:**
1. **TC-9003: Backend comparison engine** — Backend model, service, endpoint, and tests
2. **TC-9003: Frontend comparison UI** — Frontend API layer, comparison page, diff components, list page integration, and tests
