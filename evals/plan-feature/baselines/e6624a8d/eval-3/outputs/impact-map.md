# Repository Impact Map -- TC-9003: SBOM Comparison View

## Impact Map

```
trustify-backend:
  changes:
    - Add SBOM comparison diff models (SbomComparisonResult, PackageDiff, VersionChange, VulnerabilityDiff, LicenseChange) in modules/fundamental/src/sbom/model/
    - Add comparison diff logic to SbomService in modules/fundamental/src/sbom/service/
    - Add GET /api/v2/sbom/compare endpoint with left/right query parameters in modules/fundamental/src/sbom/endpoints/
    - Register comparison route in sbom endpoints module (modules/fundamental/src/sbom/endpoints/mod.rs)
    - Add integration tests for comparison endpoint in tests/api/sbom.rs
    - Document comparison endpoint and comparison UI workflow

trustify-ui:
  changes:
    - Add TypeScript interfaces for comparison API response types in src/api/models.ts
    - Add fetchSbomComparison() client function in src/api/rest.ts
    - Add useSbomComparison React Query hook in src/hooks/
    - Create SbomComparePage with header toolbar (SBOM selectors, Compare button, Export dropdown) per Figma design
    - Create diff section components (AddedPackagesSection, RemovedPackagesSection, VersionChangesSection, NewVulnerabilitiesSection, ResolvedVulnerabilitiesSection, LicenseChangesSection) using PatternFly ExpandableSection, Badge, and Table
    - Add empty state and loading state per Figma design
    - Add client-side export functionality (JSON and CSV) for comparison results
    - Register /sbom/compare route in src/routes.tsx
    - Add checkbox selection and "Compare selected" button to SbomListPage
    - Add tests for comparison page and components
```

## Excluded Requirements

None -- all requirements (MVP and non-MVP) from the Feature description are covered by the planned tasks. The non-MVP "Export diff as JSON or CSV" requirement is included in the frontend comparison page task as client-side export.

## Workflow Mode Decision

**Selected mode:** `feature-branch`

**Rationale:** Atomicity indicator identified -- tightly coupled feature components. The frontend comparison page (`/sbom/compare`) requires the new backend endpoint (`GET /api/v2/sbom/compare`). Neither side functions independently:
- Merging only the backend changes leaves `main` with an unused, untested-from-UI endpoint
- Merging only the frontend changes would break because the comparison endpoint does not exist yet

The `workflow:feature-branch` label will be applied to the TC-9003 feature issue after task creation.

**Interdependent tasks:**
- Frontend Task 4 (API types and hook) depends on Backend Task 3 (comparison endpoint) for the API contract
- Frontend Task 5 (comparison page) depends on Task 4 (API layer)
- Frontend Task 6 (route and integration) depends on Task 5 (comparison page)

## Epic Grouping (by-sub-feature)

Per Hierarchy Configuration default `by-sub-feature`:

| Epic | Label | Tasks |
|---|---|---|
| TC-9003: Backend comparison engine | Backend diff models, service, endpoint, and tests | Tasks 2, 3 |
| TC-9003: Frontend comparison UI | API types, hook, comparison page, routing | Tasks 4, 5, 6 |
| TC-9003: Documentation | Comparison endpoint and UI documentation | Task 7 |

Bookend tasks (1, 8) are not grouped into Epics.

## Inherited Field Propagation

The following fields are inherited from the Feature issue (TC-9003) and will be propagated to all created tasks and Epics:

| Field | Value | Propagation |
|---|---|---|
| `priority` | Critical | Propagated -- Feature priority is "Critical" (not "Undefined") |
| `fixVersions` | RHTPA 1.5.0 | Propagated -- Feature has fixVersions set, and fixVersion scope defaults to "both" (no Jira Field Defaults section in CLAUDE.md) |
| `labels` | ai-generated-jira | Applied to all created issues |

### additional_fields for created issues

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Critical"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

## Task Summary

| # | Summary | Repository | Target Branch | Type |
|---|---|---|---|---|
| 1 | Create feature branch TC-9003 from main | trustify-backend | main | bookend (create-branch) |
| 2 | Add SBOM comparison diff models and service | trustify-backend | TC-9003 | implementation |
| 3 | Add SBOM comparison REST endpoint with integration tests | trustify-backend | TC-9003 | implementation |
| 4 | Add comparison API types, client function, and React Query hook | trustify-ui | TC-9003 | implementation |
| 5 | Implement SBOM comparison page with diff sections | trustify-ui | TC-9003 | implementation |
| 6 | Add comparison route and SBOM list page selection integration | trustify-ui | TC-9003 | implementation |
| 7 | Document SBOM comparison endpoint and UI | trustify-backend | TC-9003 | documentation |
| 8 | Merge feature branch TC-9003 to main | trustify-backend | main | bookend (merge-branch) |
