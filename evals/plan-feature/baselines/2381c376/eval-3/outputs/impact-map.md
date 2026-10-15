# Repository Impact Map

**Feature**: TC-9003 — SBOM comparison view
**Priority**: Critical
**Fix Versions**: RHTPA 1.5.0

## trustify-backend

changes:
  - Add SBOM comparison result model structs (SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange)
  - Add comparison diff service logic to compute structured diff between two SBOMs using existing package, advisory, and license data
  - Add GET /api/v2/sbom/compare?left={id1}&right={id2} endpoint handler with query parameter validation
  - Add integration tests for the comparison endpoint in tests/api/sbom.rs

## trustify-ui

changes:
  - Add TypeScript interfaces for the SBOM comparison API response shape
  - Add API client function (fetchSbomComparison) in src/api/rest.ts
  - Add React Query hook (useSbomComparison) for comparison data fetching
  - Add SbomComparePage component at src/pages/SbomComparePage/ with collapsible diff sections (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes)
  - Add route definition for /sbom/compare in src/routes.tsx
  - Add SBOM selection checkboxes and "Compare selected" button to SbomListPage
  - Add export dropdown (JSON/CSV) to comparison page header toolbar (non-MVP)

## Excluded requirements

None. All requirements from the Feature description can be planned with the available repositories and design context.

---

## Workflow Mode

**Selected mode**: feature-branch

**Rationale**: Atomicity indicator #4 (Tightly coupled feature components) applies. The frontend comparison page (`/sbom/compare`) depends on the new backend endpoint `GET /api/v2/sbom/compare`. Neither side functions independently — the frontend page cannot render without the backend endpoint, and the backend endpoint has no consumer until the frontend is deployed. Merging only the backend would leave a dead endpoint; merging only the frontend would produce a broken page.

**Interdependent tasks**:
- Backend endpoint (Task 3) must land before frontend API hook (Task 4) can be integrated
- Frontend comparison page (Task 5) depends on the React Query hook (Task 4), which depends on the backend API contract (Task 3)
- Frontend SBOM selection (Task 6) navigates to the comparison page (Task 5)

The `workflow:feature-branch` label will be applied to the feature issue TC-9003 in Step 6a.

---

## Epic Grouping

**Strategy**: by-sub-feature (from Hierarchy Configuration)

| Epic | Label | Tasks |
|---|---|---|
| TC-9003: Backend comparison API | Backend model, service, endpoint, tests | Task 2, Task 3 |
| TC-9003: Frontend comparison UI | Frontend API layer, comparison page, selection/routing | Task 4, Task 5, Task 6 |
| TC-9003: Documentation | Comparison endpoint and UI documentation | Task 7 |

Bookend tasks (Task 1: create-branch, Task 8: merge-branch) are linked directly to the Feature, not assigned to Epics.

---

## Task Creation Log — additional_fields

Every task and epic will be created with the following `additional_fields`:

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Critical"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

- **priority**: inherited from Feature TC-9003 (Critical; not "Undefined", so it is propagated)
- **fixVersions**: inherited from Feature TC-9003 (RHTPA 1.5.0; Jira Field Defaults section absent from CLAUDE.md, so fixVersion scope defaults to "both" and is propagated to tasks)
