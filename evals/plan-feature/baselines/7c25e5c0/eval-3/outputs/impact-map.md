# Repository Impact Map — TC-9003: SBOM Comparison View

## Workflow Mode Decision

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators are present. The backend comparison endpoint is independently functional (API consumers can use it without the frontend). The frontend comparison page depends on the backend endpoint existing, but this is enforced via task dependency ordering — backend tasks land first, then frontend tasks. No coordinated schema migrations, breaking API changes, or cross-cutting refactors require all-or-nothing delivery.

## Inherited Field Propagation

- **Priority:** Critical — inherited from Feature TC-9003, propagated to all created tasks
- **fixVersions:** RHTPA 1.5.0 — inherited from Feature TC-9003, propagated to all created tasks (fixVersion scope defaults to "both" per Jira Field Defaults)

## trustify-backend

Changes:
- Create `SbomComparisonResult` response model with diff sections: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, license changes
- Add `compare` method to `SbomService` that computes on-the-fly diff between two SBOMs using existing package, advisory, and license data
- Add `GET /api/v2/sbom/compare?left={id1}&right={id2}` endpoint handler with route registration
- Add integration tests for the comparison endpoint covering: successful diff, 404 for missing SBOM, empty diff (identical SBOMs), large SBOM performance

## trustify-ui

Changes:
- Add TypeScript interfaces for the comparison API response (`SbomComparisonResult`, section item types) and API client function `compareSboms(leftId, rightId)`
- Add `useSbomComparison` React Query hook wrapping the comparison API call
- Create comparison page at `/sbom/compare` with PatternFly layout: header toolbar with SBOM selectors, expandable diff sections with data tables, empty state, loading skeletons (per Figma design)
- Add "Compare selected" action to existing SBOM list page — selection checkboxes and action button that navigates to comparison page with selected IDs as URL params
- Add MSW mock handlers and component tests for the comparison page and list page selection
- Register `/sbom/compare` route in `src/routes.tsx`

## Excluded Requirements

- **Export diff as JSON or CSV:** marked as non-MVP in the feature requirements. The Export dropdown is shown in the Figma mockups but export functionality is excluded from this plan. Can be planned as a follow-up feature once the core comparison view ships.

## Task Summary

| # | Task | Repository | Dependencies |
|---|------|-----------|-------------|
| 1 | Backend comparison model | trustify-backend | — |
| 2 | Backend comparison service | trustify-backend | Task 1 |
| 3 | Backend comparison endpoint | trustify-backend | Task 2 |
| 4 | Backend integration tests | trustify-backend | Task 3 |
| 5 | Frontend API types and client | trustify-ui | Task 3 |
| 6 | Frontend comparison hook | trustify-ui | Task 5 |
| 7 | Frontend comparison page | trustify-ui | Task 6 |
| 8 | Frontend SBOM list compare action | trustify-ui | Task 7 |
| 9 | Frontend MSW mocks and tests | trustify-ui | Task 7, Task 8 |
| 10 | Documentation | trustify-backend | Task 3, Task 7 |

## Discovered Backend API Contracts

- `GET /api/v2/sbom` — returns `PaginatedResults<SbomSummary>` (see `modules/fundamental/src/sbom/endpoints/list.rs`)
- `GET /api/v2/sbom/{id}` — returns `SbomDetails` (see `modules/fundamental/src/sbom/endpoints/get.rs`)
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: returns `SbomComparisonResult` with sections for added/removed packages, version changes, new/resolved vulnerabilities, license changes

## additional_fields for Created Issues

All tasks will be created with:
```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Critical"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

## Issue Links

- Feature TC-9003 "Incorporates" → each created task
- Task dependency links as per the Dependencies column above
