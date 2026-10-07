# Repository Impact Map — TC-9003: SBOM comparison view

## Workflow Mode

**Selected mode:** `feature-branch`

**Rationale:** Atomicity indicator #4 (Tightly coupled feature components) is present. The frontend comparison page at `/sbom/compare` requires the new backend endpoint `GET /api/v2/sbom/compare` — neither side functions independently. The frontend cannot render comparison results without the backend diff endpoint, and the backend endpoint has no consumer until the frontend comparison page exists. Merging either side alone leaves `main` with dead code or a broken UI.

**Interdependent tasks:**
- Task 3 (backend comparison endpoint) and Task 4 (frontend API types/client/hook) are tightly coupled: Task 4 defines TypeScript types matching Task 3's response shape.
- Task 5 (frontend comparison page) depends on Task 3 (backend endpoint) for live data.
- Task 6 (list page selection) depends on Task 5 (comparison page) for navigation target.

The `workflow:feature-branch` label will be applied to TC-9003 in Step 6a.

## Inherited Field Values from TC-9003

- **Priority:** Critical (will be propagated to all created tasks and epics)
- **Fix Versions:** RHTPA 1.5.0 (will be propagated to all created tasks and epics; no `fixVersion scope` setting found in Jira Field Defaults — defaults to "both")

## `additional_fields` for Created Issues

All tasks and epics will be created with:

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Critical"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

## Epic Grouping Strategy

**Strategy:** `by-sub-feature` (from Hierarchy Configuration in CLAUDE.md)

| Epic | Label | Tasks |
|---|---|---|
| Epic A | TC-9003: Backend comparison service | Task 2, Task 3 |
| Epic B | TC-9003: Frontend comparison UI | Task 4, Task 5, Task 6 |
| Epic C | TC-9003: Documentation | Task 7 |

Bookend tasks (Task 1, Task 8) are linked directly to the Feature, not assigned to Epics.

## Repository Changes

### trustify-backend

changes:
  - Add SBOM comparison diff model structs (SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange) in modules/fundamental/src/sbom/model/
  - Add SBOM comparison diff service logic in modules/fundamental/src/sbom/service/ that computes the diff between two SBOMs by comparing their package sets, advisory associations, and license mappings
  - Add GET /api/v2/sbom/compare?left={id1}&right={id2} endpoint in modules/fundamental/src/sbom/endpoints/ that accepts two SBOM IDs and returns the structured diff
  - Add integration tests for the comparison endpoint in tests/api/

### trustify-ui

changes:
  - Add TypeScript interfaces for the comparison API response in src/api/models.ts
  - Add fetchSbomComparison client function in src/api/rest.ts
  - Add useSbomComparison React Query hook in src/hooks/
  - Add SbomComparePage with header toolbar (dual SBOM selectors, Compare button, Export dropdown), collapsible diff sections (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes), empty state, and loading state
  - Add /sbom/compare route in src/routes.tsx
  - Add checkbox selection and "Compare selected" button to SbomListPage for navigation to comparison view
  - Add tests for comparison page and list page selection

## Excluded Requirements

| Requirement | Reason |
|---|---|
| Add comparison endpoint to the API latency Grafana dashboard | Requires Grafana dashboard configuration access — not within trustify-backend or trustify-ui repository scope |
| Monitor for timeouts on large SBOM comparisons (>2000 packages per SBOM) | Requires monitoring infrastructure configuration — not within trustify-backend or trustify-ui repository scope |

## Task Summary

| # | Summary | Repository | Type |
|---|---|---|---|
| 1 | Create feature branch TC-9003 from main | trustify-backend | Bookend (create-branch) |
| 2 | Add SBOM comparison model and diff service | trustify-backend | Implementation |
| 3 | Add SBOM comparison REST endpoint with integration tests | trustify-backend | Implementation |
| 4 | Add SBOM comparison API types, client function, and hook | trustify-ui | Implementation |
| 5 | Add SBOM comparison page with diff sections and export | trustify-ui | Implementation |
| 6 | Add SBOM selection and compare navigation to list page | trustify-ui | Implementation |
| 7 | Document SBOM comparison endpoint and UI | trustify-backend | Documentation |
| 8 | Merge feature branch TC-9003 to main | trustify-backend | Bookend (merge-branch) |
