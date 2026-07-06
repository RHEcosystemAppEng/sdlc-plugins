# Repository Impact Map -- TC-9003: SBOM Comparison View

## Workflow Mode

**Selected mode:** `feature-branch`

**Rationale:** Atomicity indicator #4 (Tightly coupled feature components) is present -- the frontend comparison page (`/sbom/compare`) requires the new backend endpoint `GET /api/v2/sbom/compare` that does not yet exist. Merging the frontend without the backend would result in a broken page calling a non-existent endpoint. Additionally, atomicity indicator #2 (Breaking API changes) applies -- the new endpoint introduces a new API contract that the frontend depends on. Neither side functions independently on `main`.

**Interdependent tasks:** Backend tasks (comparison models, service, and endpoint) must land before frontend tasks (API types, client, hook, comparison page) can function. The frontend comparison page is non-functional without the backend diff endpoint.

The `workflow:feature-branch` label will be applied to the feature issue in Step 6a.

## Impact Map

```
trustify-backend:
  changes:
    - Add SBOM comparison diff model types (SbomComparison, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange) in modules/fundamental/src/sbom/model/
    - Add SBOM comparison service method to SbomService that computes on-the-fly diff between two SBOMs using existing package, advisory, and license data
    - Add GET /api/v2/sbom/compare?left={id1}&right={id2} endpoint in modules/fundamental/src/sbom/endpoints/
    - Register the comparison route in the SBOM endpoint module
    - Add integration tests for the comparison endpoint in tests/api/

trustify-ui:
  changes:
    - Add TypeScript interfaces for the SBOM comparison API response types in src/api/models.ts
    - Add fetchSbomComparison() client function in src/api/rest.ts
    - Add useSbomComparison React Query hook in src/hooks/
    - Add SbomComparePage component with header toolbar (SBOM selectors, Compare button, Export dropdown) and collapsible diff sections (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes) using PatternFly components
    - Add empty state and loading state for the comparison page
    - Add /sbom/compare route to src/routes.tsx
    - Add multi-select checkbox and "Compare selected" button to SbomListPage
    - Add MSW mock handlers and unit tests for the comparison page
```

## Epic Grouping (by-sub-feature)

- **TC-9003: Backend Comparison API** -- Tasks 2, 3 (model types, service + endpoint)
- **TC-9003: Frontend Comparison UI** -- Tasks 4, 5, 6 (API layer, comparison page, list page integration)
- **TC-9003: Documentation** -- Task 7 (endpoint and UI documentation)

## Priority and Fix Version

- **Priority:** Critical (inherited from TC-9003)
- **Fix Versions:** RHTPA 1.5.0 (inherited from TC-9003)
- **fixVersion scope:** not configured in Jira Field Defaults -- defaults to "both" (propagated to all tasks)

## Task additional_fields

All created tasks will include:
```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Critical"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

## Excluded Requirements

None -- all MVP and non-MVP requirements from the Feature description can be decomposed into actionable tasks. The non-MVP export requirement (Export diff as JSON or CSV) is included in Task 5 as client-side export functionality per the Figma design.
