# Repository Impact Map — TC-9003: SBOM Comparison View

## Impact Map

```
trustify-backend:
  changes:
    - Add SBOM comparison result model types (SbomComparisonResult with sub-types for added/removed packages, version changes, new/resolved vulnerabilities, license changes)
    - Implement SBOM comparison service logic to compute structured diffs between two SBOMs by ID using existing package, advisory, and license data
    - Add GET /api/v2/sbom/compare endpoint with left and right query parameters returning structured diff
    - Add integration tests for the comparison endpoint covering all diff categories and error cases

trustify-ui:
  changes:
    - Add TypeScript interfaces for the SBOM comparison API response types
    - Add fetchSbomComparison() REST client function and useSbomComparison React Query hook
    - Create SbomComparePage with header toolbar (SBOM selectors, Compare button, Export dropdown) and collapsible diff sections using PatternFly ExpandableSection, Table, Badge, and EmptyState components per Figma design
    - Add /sbom/compare route with URL query parameter support for shareable comparison links
    - Update SbomListPage to support multi-row selection and "Compare selected" action button
    - Add unit tests, MSW mock handlers, and Playwright E2E test for the comparison workflow
```

## Workflow Mode Decision

**Mode:** `feature-branch`

**Rationale:** Atomicity indicator #4 (Tightly coupled feature components) is present — the frontend comparison page requires the new `GET /api/v2/sbom/compare` backend endpoint that does not yet exist. Neither side functions independently: merging only the backend adds a dead endpoint with no consumer; merging only the frontend results in API calls to a non-existent endpoint. Atomicity indicator #2 (Breaking API changes) is also present — the frontend consumes a new API contract that must exist before the frontend can function.

**Interdependent tasks:**
- Backend Tasks 2-3 (model/service and endpoint) must land before Frontend Tasks 4-6 can function
- Frontend Task 4 (API types/hook) depends on the exact response shape from Backend Task 3
- Frontend Tasks 5-6 depend on Task 4 for data fetching

All intermediate tasks target branch `TC-9003`. The `workflow:feature-branch` label will be applied to the feature issue.

## Inherited Fields

- **Priority:** Critical (propagated to all tasks)
- **Fix Versions:** RHTPA 1.5.0 (propagated to all tasks — no fixVersion scope restriction configured)
- **Labels:** ai-generated-jira (on all tasks)
