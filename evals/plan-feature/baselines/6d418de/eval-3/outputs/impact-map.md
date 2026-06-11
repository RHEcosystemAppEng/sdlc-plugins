# Repository Impact Map — TC-9003: SBOM Comparison View

## trustify-backend

changes:
  - Add comparison model structs (SbomComparisonResult with added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes)
  - Add comparison service logic in sbom module to compute structured diff between two SBOMs on-the-fly using existing package, advisory, and license data
  - Add GET /api/v2/sbom/compare endpoint with left and right query parameters returning SbomComparisonResult
  - Register the new comparison endpoint route in the sbom endpoints module
  - Add integration tests for the comparison endpoint covering added/removed packages, version changes, vulnerability diffs, and license changes

## trustify-ui

changes:
  - Add TypeScript interfaces for the SBOM comparison API response types in the API models
  - Add API client function for the comparison endpoint in the REST client
  - Add React Query hook for fetching comparison data
  - Add SbomComparePage with header toolbar (SBOM selectors, Compare button, Export dropdown) and collapsible diff sections per Figma design
  - Add page-specific components: diff section tables for each category (AddedPackages, RemovedPackages, VersionChanges, NewVulnerabilities, ResolvedVulnerabilities, LicenseChanges)
  - Add route definition for /sbom/compare with URL query parameter support for left and right SBOM IDs
  - Add checkbox selection and "Compare selected" button to existing SbomListPage
  - Add unit tests for the comparison page and its components
  - Add MSW mock handlers and fixtures for the comparison endpoint

---

## Workflow Mode

**Selected mode:** `feature-branch`

**Rationale:** Atomicity indicator #4 (tightly coupled feature components) is present. The frontend comparison page at `/sbom/compare` requires the new backend endpoint `GET /api/v2/sbom/compare` which does not yet exist. Merging the frontend without the backend would result in a broken page that cannot fetch comparison data. Merging the backend without the frontend provides no user-facing value and leaves an untested API surface. Both sides must land together.

**Interdependent tasks:**
- The backend comparison endpoint task and the frontend comparison page task are directly coupled: the frontend calls an endpoint that only exists after the backend task is merged.
- The frontend API client/hook task depends on the backend endpoint's response shape being available.
