# Repository Impact Map -- TC-9003: SBOM comparison view

## trustify-backend

changes:
  - Add SBOM comparison model types (SbomComparisonResult with sub-structs for each diff category: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, license changes)
  - Add comparison diff service logic to compute structured diff from existing package, advisory, and license data for two SBOMs
  - Add GET /api/v2/sbom/compare?left={id1}&right={id2} endpoint with query parameter validation
  - Register comparison route in sbom endpoints module and server route mounting
  - Add integration tests for the comparison endpoint covering normal diff, empty diff, invalid IDs, and performance with large SBOMs

## trustify-ui

changes:
  - Add TypeScript interfaces for the comparison API response types in src/api/models.ts
  - Add fetchSbomComparison() API client function in src/api/rest.ts
  - Add useSbomComparison() React Query hook in src/hooks/
  - Create SbomComparePage with header toolbar (SBOM selectors, Compare button, Export dropdown), six collapsible diff sections (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes), empty state, and loading state
  - Add /sbom/compare route definition in src/routes.tsx
  - Modify SbomListPage to add checkbox selection and "Compare selected" button that navigates to /sbom/compare?left={id1}&right={id2}
  - Add MSW mock handlers and fixtures for the comparison endpoint
  - Add unit tests for the comparison page and list page integration
  - Implement virtualized lists for diff sections with >100 rows (NFR: no browser freezing on large diffs)

## Excluded requirements

None. All MVP and non-MVP requirements can be planned with the available inputs. The non-MVP requirement "Export diff as JSON or CSV" is included in the frontend comparison page task as a UI element per the Figma design; the actual export logic is noted as non-MVP scope.

## Workflow mode

**Mode:** `feature-branch`

**Rationale:** Atomicity indicator 4 (tightly coupled feature components) is present -- the frontend comparison page requires the backend comparison endpoint (`GET /api/v2/sbom/compare`) which does not yet exist. Merging the frontend comparison page to main before the backend endpoint is deployed would result in a broken comparison page that calls a non-existent API endpoint.

**Interdependent tasks:**
- Frontend Tasks 4-6 (comparison API layer, comparison page, list page integration) depend on Backend Tasks 2-3 (comparison model/service, comparison endpoint)
- The `workflow:feature-branch` label will be applied to the TC-9003 feature issue

## Epic grouping (by-sub-feature)

| Epic | Group label | Tasks |
|---|---|---|
| TC-9003: Backend comparison API | Backend comparison API | Task 2, Task 3 |
| TC-9003: Frontend comparison UI | Frontend comparison UI | Task 4, Task 5, Task 6 |
| TC-9003: Documentation | Documentation | Task 7 |

Bookend tasks (Task 1: create-branch, Task 8: merge-branch) are not assigned to Epics.

## Task creation additional_fields

All created tasks will include:

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Critical"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

- **priority**: inherited from Feature TC-9003 (Critical)
- **fixVersions**: inherited from Feature TC-9003 (RHTPA 1.5.0); no `fixVersion scope` setting in CLAUDE.md Jira Field Defaults, so default to "both" (propagate to tasks)

All created Epics will include the same additional_fields with labels, priority, and fixVersions.
