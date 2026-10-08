# Repository Impact Map -- TC-9003: SBOM Comparison View

## Workflow Mode

**Selected mode:** `feature-branch`

**Rationale:** Atomicity indicator #4 (Tightly coupled feature components) is present. The frontend comparison page requires the new backend `GET /api/v2/sbom/compare` endpoint, which does not yet exist. Merging the frontend without the backend would result in a broken comparison page (API calls would 404). Merging the backend without the frontend would leave a usable but undiscoverable endpoint. Both sides must land together for the feature to function.

**Interdependent tasks:**
- Task 4 (frontend API types/hook) depends on Task 3 (backend endpoint) -- the TypeScript interfaces and API client must match the backend response shape
- Task 5 (frontend comparison page) depends on Task 4 (frontend hook) -- the page consumes the comparison hook which calls the backend endpoint
- Task 6 (frontend list selection) depends on Task 5 (comparison page) -- the selection navigates to the comparison page

The `workflow:feature-branch` label will be applied to the TC-9003 feature issue.

## Impact Map

```
trustify-backend:
  changes:
    - Add SBOM comparison response model types (SbomComparison, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange)
    - Implement SBOM diff service that computes structured diff between two SBOMs from existing package, advisory, and license data (no new database tables)
    - Add REST endpoint GET /api/v2/sbom/compare?left={id1}&right={id2} returning the structured diff
    - Add integration tests for the comparison endpoint

trustify-ui:
  changes:
    - Add TypeScript interfaces for the SBOM comparison API response types
    - Add API client function fetchSbomComparison(leftId, rightId) calling the backend endpoint
    - Add React Query hook useSbomComparison for data fetching with caching
    - Implement SBOM comparison page at /sbom/compare with PatternFly components: Select dropdowns for SBOM selection, ExpandableSection for diff categories, Table for data display, Badge for count indicators, EmptyState for initial view, Skeleton for loading state
    - Add route definition for /sbom/compare in routes.tsx
    - Add checkbox selection and "Compare selected" button to the SBOM list page for navigating to the comparison view
    - Add mock comparison data fixture for tests
    - Document the comparison endpoint and UI (New Content doc impact)
```

## Epic Grouping (by-sub-feature)

- **Epic A: TC-9003: Backend comparison engine** -- Tasks 2, 3
- **Epic B: TC-9003: Frontend comparison UI** -- Tasks 4, 5, 6
- **Epic C: TC-9003: Documentation** -- Task 7

Bookend tasks (1, 8) are not assigned to Epics.

## Task Summary

| Task | Summary | Repository | Target Branch | Epic |
|---|---|---|---|---|
| 1 | Create feature branch TC-9003 from main | trustify-ui | main | -- |
| 2 | Add SBOM comparison model types and diff service | trustify-backend | TC-9003 | A |
| 3 | Add SBOM comparison endpoint with integration tests | trustify-backend | TC-9003 | A |
| 4 | Add SBOM comparison API types, client function, and React Query hook | trustify-ui | TC-9003 | B |
| 5 | Implement SBOM comparison page with diff sections | trustify-ui | TC-9003 | B |
| 6 | Add SBOM comparison selection to list page | trustify-ui | TC-9003 | B |
| 7 | Document SBOM comparison endpoint and UI | trustify-ui | TC-9003 | C |
| 8 | Merge feature branch TC-9003 to main | trustify-ui | main | -- |

## Cross-repo Dependencies

- Task 4 (trustify-ui: API types/hook) depends on Task 3 (trustify-backend: comparison endpoint) -- frontend types must match the backend API contract

## Inherited Field Values

The following field values are inherited from the parent Feature TC-9003 and propagated to all created tasks and Epics:

- **Priority:** Critical (inherited -- Feature priority is set and is not "Undefined")
- **Fix Versions:** RHTPA 1.5.0 (inherited -- Feature has fixVersions set; no `fixVersion scope` configuration found in Jira Field Defaults, defaulting to "both" which includes task-level propagation)
- **Labels:** ai-generated-jira (applied to all created issues)

### additional_fields for task/Epic creation

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Critical"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

## Feature Issue Label Update (feature-branch mode)

After all tasks are created, add `workflow:feature-branch` to the TC-9003 feature issue labels:
```
labels: ["ai-generated-jira", "workflow:feature-branch"]
```
