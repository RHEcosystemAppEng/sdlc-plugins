# Repository Impact Map — TC-9003: SBOM Comparison View

## Workflow Mode

**Mode:** `feature-branch`
**Feature branch:** `TC-9003`

**Rationale:** Feature-branch mode is required because two atomicity indicators are present:
- **Tightly coupled feature components (indicator #4):** The frontend comparison page (`/sbom/compare`) requires the new backend `GET /api/v2/sbom/compare` endpoint. Neither side functions independently — the frontend cannot render without the backend diff response, and the backend endpoint has no value without the frontend UI.
- **Breaking API changes (indicator #2):** The frontend consumes a new API contract (`SbomComparisonResult`) that does not yet exist. Merging the frontend without the backend would result in runtime errors against `main`.

**Interdependent tasks:** All backend tasks (comparison model/service, comparison endpoint) must land before the frontend tasks (API types/hook, comparison page) can function.

## Impact Map

```
trustify-backend:
  changes:
    - Add SbomComparisonResult model with diff categories (added/removed packages, version changes, new/resolved vulnerabilities, license changes)
    - Add comparison service method to SbomService that computes a structured diff between two SBOMs
    - Add GET /api/v2/sbom/compare?left={id1}&right={id2} endpoint
    - Add integration tests for the comparison endpoint

trustify-ui:
  changes:
    - Add TypeScript interfaces for the comparison API response
    - Add API client function for the comparison endpoint
    - Add React Query hook for SBOM comparison
    - Add SbomComparePage with header toolbar (SBOM selectors, Compare button, Export dropdown)
    - Add diff section components (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes) using PatternFly ExpandableSection and Table
    - Add route definition for /sbom/compare
    - Add unit tests for comparison page and components
```
