# Repository Impact Map — TC-9003: SBOM Comparison View

## Workflow Mode

**Mode:** `feature-branch`

**Rationale:** Atomicity indicator #4 (Tightly coupled feature components) is present. The frontend comparison page at `/sbom/compare` requires the new backend endpoint `GET /api/v2/sbom/compare` that does not yet exist. Merging the frontend without the backend would result in a broken comparison page. Merging the backend without the frontend delivers no user value but is not broken — however, the tight coupling between the UI design (which drives the response shape) and the backend response structure means coordinated delivery is required.

**Interdependent tasks:**
- The backend comparison endpoint task (Task 2) must be completed before the frontend comparison page task (Task 4) can be integration-tested.
- The frontend SBOM list page modifications (Task 3) and the comparison page (Task 4) share the same route setup and must coordinate on URL parameter conventions.

---

## Impact Map

```
trustify-backend:
  changes:
    - Add comparison diff model structs (SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange)
    - Add comparison service method to SbomService that computes the diff between two SBOMs using existing package, advisory, and license data
    - Add GET /api/v2/sbom/compare endpoint with left and right query parameters
    - Add integration tests for the comparison endpoint covering added/removed packages, version changes, vulnerability diffs, and license changes

trustify-ui:
  changes:
    - Add TypeScript interfaces for the comparison API response types in api/models.ts
    - Add API client function for the comparison endpoint in api/rest.ts
    - Add React Query hook for the comparison API call
    - Modify SbomListPage to support multi-select checkboxes and a "Compare selected" button
    - Add new SbomComparePage with header toolbar (SBOM selectors, Compare button, Export dropdown) and collapsible diff sections per Figma design
    - Add route definition for /sbom/compare in routes.tsx
    - Add MSW mock handler and fixture data for the comparison endpoint
    - Add unit tests for the comparison page
```
