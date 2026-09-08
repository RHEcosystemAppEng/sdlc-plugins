# Repository Impact Map — TC-9003: SBOM Comparison View

## trustify-backend

changes:
  - Add SBOM comparison diff model structs (SbomComparisonResult, PackageDiff, VersionChange, VulnerabilityDiff, LicenseChange) in modules/fundamental/src/sbom/model/
  - Implement SbomComparisonService with diff logic that compares two SBOMs by fetching their packages, advisories, and licenses, computing added/removed/changed sets
  - Add GET /api/v2/sbom/compare?left={id1}&right={id2} endpoint in modules/fundamental/src/sbom/endpoints/ with route registration
  - Add integration tests for the comparison endpoint in tests/api/sbom.rs

## trustify-ui

changes:
  - Add TypeScript interfaces for comparison API response types in src/api/models.ts
  - Add compareSboms() API client function in src/api/rest.ts
  - Add useSbomComparison React Query hook in src/hooks/
  - Create SbomComparePage page component at src/pages/SbomComparePage/ with header toolbar (SBOM selectors, Compare button, Export dropdown), six collapsible diff sections (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes), empty state, and loading state
  - Add /sbom/compare route to src/routes.tsx
  - Add multi-select checkboxes and "Compare selected" button to SbomListPage for navigation to comparison view
  - Add MSW mock handlers and test fixtures for comparison endpoint
  - Add unit tests for SbomComparePage and integration with comparison hook

## Excluded requirements

None. All MVP and non-MVP requirements can be planned with available inputs.

- The non-MVP requirement "Export diff as JSON or CSV" is included in the frontend comparison page task since the Figma design specifies the Export dropdown with JSON and CSV options. The export logic operates entirely on the client-side comparison result data.

---

## Workflow Mode Decision

**Selected mode:** `feature-branch`

**Rationale:** Atomicity indicator #4 (Tightly coupled feature components) applies. The frontend comparison page at `/sbom/compare` requires the new backend endpoint `GET /api/v2/sbom/compare` that does not yet exist. Merging only the frontend without the backend would result in a broken comparison view (API calls to a non-existent endpoint). Merging only the backend without the frontend would be harmless but incomplete. Coordinated delivery via feature branches ensures both sides land together.

**Interdependent tasks:**
- Task 3 (backend comparison endpoint) and Task 6 (frontend comparison page) are tightly coupled: the frontend calls the backend endpoint, and neither provides user value without the other.
- Task 5 (frontend API types/hook) depends on the backend API contract defined in Task 2/3.
- Task 7 (SbomListPage integration) depends on the comparison page existing (Task 6).

The `workflow:feature-branch` label will be applied to the TC-9003 feature issue.

---

## Epic Grouping (by-sub-feature)

Grouping strategy: `by-sub-feature` (from Hierarchy Configuration)

| Epic | Summary | Tasks |
|---|---|---|
| Epic A | TC-9003: Backend Comparison API | Task 1 (create-branch), Task 2, Task 3, Task 9 (merge-branch) |
| Epic B | TC-9003: Frontend Comparison UI | Task 4 (create-branch), Task 5, Task 6, Task 7, Task 8 (docs), Task 10 (merge-branch) |

---

## Field Inheritance

Inherited from parent Feature TC-9003:
- **Priority:** High — propagated to all created tasks and epics via `additional_fields.priority`
- **Fix Versions:** RHTPA 1.5.0 — propagated to all created tasks and epics via `additional_fields.fixVersions` (fixVersion scope defaults to "both" since no Jira Field Defaults section exists in CLAUDE.md)

All created issues will include:
```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "High"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```
