# Repository Impact Map — TC-9003: SBOM Comparison View

## trustify-backend

changes:
  - Add SBOM comparison result model structs (added/removed packages, version changes, new/resolved vulnerabilities, license changes) in `modules/fundamental/src/sbom/model/`
  - Add comparison diff service method to SbomService that computes on-the-fly diff between two SBOMs using existing package, advisory, and license data
  - Add `GET /api/v2/sbom/compare?left={id1}&right={id2}` endpoint in `modules/fundamental/src/sbom/endpoints/`
  - Add integration tests for comparison endpoint in `tests/api/`

## trustify-ui

changes:
  - Add TypeScript interfaces for comparison API response types in `src/api/models.ts`
  - Add API client function for comparison endpoint in `src/api/rest.ts`
  - Add React Query hook `useSbomComparison` in `src/hooks/`
  - Add SbomComparePage with header toolbar (SBOM selectors, Compare button, Export dropdown), six collapsible diff sections (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes), empty state, and loading state
  - Add route for `/sbom/compare` in `src/routes.tsx`
  - Update SbomListPage to support multi-select via checkboxes and a "Compare selected" action button
  - Add unit tests for SbomComparePage components
  - Highlight packages with new critical vulnerabilities (red background on Critical severity rows in New Vulnerabilities section)

## Excluded requirements

None. All requirements (MVP and non-MVP) can be decomposed into actionable tasks:

- **Export diff as JSON or CSV** (non-MVP): planned as part of the frontend comparison page task. The Export dropdown UI is included in the Figma design and will be implemented alongside the comparison page, but wired to produce client-side downloads from the already-fetched comparison response.

## additional_fields for created issues

All tasks and epics will be created with the following `additional_fields`:

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Critical"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

- **Priority**: inherited from Feature TC-9003 (Critical)
- **fixVersions**: inherited from Feature TC-9003 (RHTPA 1.5.0). No `fixVersion scope` setting found in Jira Field Defaults — defaulting to "both" (propagate to tasks).
- **Labels**: `ai-generated-jira` applied to all created issues per skill rules.

## Workflow mode

**Selected mode**: `feature-branch`

**Rationale**: Atomicity indicator #4 (tightly coupled feature components) is present. The frontend comparison page (`/sbom/compare`) requires the new backend endpoint (`GET /api/v2/sbom/compare`) that does not yet exist. Neither side functions independently — the frontend page would show errors without the backend endpoint, and the backend endpoint serves no user-visible purpose without the frontend UI. Merging either side alone to `main` would leave an incomplete feature visible to users.

**Interdependent tasks**:
- Backend tasks (comparison model, service, endpoint) must exist before frontend tasks can function
- Frontend tasks (API types, hook, comparison page, route) depend on the backend endpoint being available
- All intermediate tasks target the `TC-9003` feature branch

The `workflow:feature-branch` label will be applied to the feature issue TC-9003 in Step 6a.

## Epic grouping

**Strategy**: by-sub-feature (from Hierarchy Configuration in CLAUDE.md)

| Epic | Tasks |
|---|---|
| TC-9003: Backend comparison API | Task 2, Task 3, Task 4 |
| TC-9003: Frontend comparison UI | Task 5, Task 6, Task 7, Task 8 |

Bookend tasks (Task 1 create-branch, Task 10 merge-branch) and the documentation task (Task 9) are not assigned to Epics.
