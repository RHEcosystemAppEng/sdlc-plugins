# Repository Impact Map — TC-9003: SBOM Comparison View

## Workflow Mode

**Mode:** `feature-branch`

**Rationale:** Atomicity indicator #4 (Tightly coupled feature components) is present. The frontend comparison page (`/sbom/compare`) requires the new backend endpoint `GET /api/v2/sbom/compare?left={id1}&right={id2}`. Neither side functions independently — the frontend cannot render comparison results without the backend diffing endpoint, and the backend endpoint has no value without the frontend UI. Additionally, atomicity indicator #2 (Breaking API changes) applies: the frontend consumes a new API contract that does not yet exist, so merging the frontend alone would result in a broken page.

**Interdependent tasks:** All backend tasks (comparison model, service, endpoint) must land before the frontend API layer and comparison page tasks can function. The feature branch `TC-9003` ensures all changes land together.

The `workflow:feature-branch` label will be applied to the feature issue.

## Impact Map

```
trustify-backend:
  changes:
    - Add SbomComparisonResult model with diff section structs (added/removed packages, version changes, new/resolved vulnerabilities, license changes)
    - Add comparison diffing logic in SbomService to compute structured diffs between two SBOMs
    - Add GET /api/v2/sbom/compare endpoint with left/right query parameters
    - Add integration tests for the comparison endpoint

trustify-ui:
  changes:
    - Add TypeScript interfaces for the comparison API response types
    - Add API client function for the comparison endpoint
    - Add React Query hook for the comparison query
    - Add SbomComparePage with header toolbar (SBOM selectors, Compare button, Export dropdown) and collapsible diff sections
    - Add route registration for /sbom/compare
    - Add checkbox selection support to SbomListPage for "Compare selected" workflow
    - Add unit tests and MSW mock handlers for the comparison page
```

## Priority and Fix Version Propagation

- **Priority:** Critical (will be propagated to all tasks)
- **Fix Versions:** RHTPA 1.5.0 (will be propagated to all tasks per default `fixVersion scope: "both"`)
