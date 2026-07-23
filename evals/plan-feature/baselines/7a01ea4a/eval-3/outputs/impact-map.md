# Repository Impact Map -- TC-9003: SBOM Comparison View

## trustify-backend

changes:
  - Add SBOM comparison model types (SbomComparisonResult with sub-structs for added/removed packages, version changes, new/resolved vulnerabilities, license changes) in modules/fundamental/src/sbom/model/
  - Add SBOM comparison service logic to compute diff on-the-fly from existing package, advisory, and license data in modules/fundamental/src/sbom/service/
  - Add GET /api/v2/sbom/compare?left={id1}&right={id2} endpoint in modules/fundamental/src/sbom/endpoints/ returning structured diff
  - Add integration tests for the comparison endpoint in tests/api/

## trustify-ui

changes:
  - Add TypeScript interfaces for the comparison API response types in src/api/models.ts
  - Add API client function fetchSbomComparison() in src/api/rest.ts
  - Add React Query hook useSbomComparison in src/hooks/
  - Add SbomComparePage with header toolbar (SBOM selectors, Compare button, Export dropdown) and collapsible diff sections (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes) in src/pages/SbomComparePage/
  - Add /sbom/compare route in src/routes.tsx with lazy loading
  - Add checkbox selection and "Compare selected" button to SbomListPage for two-SBOM selection
  - Add unit tests (Vitest + RTL), MSW mock handlers, fixtures, and E2E tests (Playwright) for the comparison feature
  - Support URL-shareable comparisons via query parameters left and right
  - Use virtualized lists for diff sections with >100 items (per NFR)
  - Highlight packages with Critical severity in New Vulnerabilities section

## Excluded requirements

- **Export diff as JSON or CSV** (non-MVP) -- The Figma design includes an Export dropdown with JSON and CSV options. The UI scaffolding (disabled Export button) is included in the comparison page task, but the actual export logic is deferred as non-MVP per the feature requirements. No missing inputs prevent planning; this is a prioritization decision documented in the feature.

## Workflow mode

**Selected mode:** `feature-branch`

**Rationale:** Atomicity indicator 4 (tightly coupled feature components) is present. The frontend SBOM comparison page at /sbom/compare requires the new backend endpoint GET /api/v2/sbom/compare which does not yet exist. Merging the frontend page to main before the backend endpoint is deployed would result in a page that calls a non-existent API endpoint, producing runtime errors for any user who navigates to the comparison URL. The backend and frontend changes are interdependent -- neither side provides standalone user value without the other.

**Interdependent tasks:**
- Backend Tasks 2-3 (model/service + endpoint) must land before Frontend Tasks 4-7 can function
- Frontend Tasks 4-7 depend on the backend endpoint being available
- The `workflow:feature-branch` label will be applied to the TC-9003 feature issue

## Epic grouping

**Strategy:** by-sub-feature (from Hierarchy Configuration in CLAUDE.md)

| Epic | Tasks |
|---|---|
| TC-9003: Backend Comparison API | Task 2, Task 3 |
| TC-9003: Frontend Comparison UI | Task 4, Task 5, Task 6, Task 7 |
| TC-9003: Documentation | Task 8 |

Bookend tasks (Task 1: create-branch, Task 9: merge-branch) are created directly under the Feature, not under Epics.

## Task creation field values (additional_fields)

Inherited from Feature TC-9003:
- **Priority:** Critical (propagated to all tasks and epics)
- **Fix Versions:** RHTPA 1.5.0 (propagated to all tasks and epics; fixVersion scope defaults to "both" since no Jira Field Defaults section exists in CLAUDE.md)
- **Labels:** ["ai-generated-jira"] (applied to all created issues)

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Critical"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```
