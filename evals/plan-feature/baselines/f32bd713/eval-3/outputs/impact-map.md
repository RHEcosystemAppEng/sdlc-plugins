# Repository Impact Map — TC-9003: SBOM Comparison View

## Impact Map

```
trustify-backend:
  changes:
    - Add SBOM comparison model types (SbomComparisonResult with diff sections for added/removed packages, version changes, new/resolved vulnerabilities, license changes)
    - Add comparison service logic to compute structured diffs between two SBOMs using existing package, advisory, and license data
    - Add GET /api/v2/sbom/compare?left={id1}&right={id2} endpoint returning structured diff response
    - Add integration tests for the comparison endpoint in tests/api/sbom.rs

trustify-ui:
  changes:
    - Add TypeScript interfaces for the comparison API response shape (SbomComparisonResult and per-section types)
    - Add API client function compareSboms(leftId, rightId) in src/api/rest.ts
    - Add React Query hook useSbomComparison for the comparison endpoint
    - Add SbomComparePage with header toolbar (SBOM selectors, Compare button, Export dropdown), collapsible diff sections (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes), empty state, and loading state per Figma design
    - Add SBOM selection checkboxes and "Compare selected" button to SbomListPage
    - Register /sbom/compare route in src/routes.tsx
    - Add MSW mock handlers, test fixtures, unit tests, and Playwright E2E test for comparison features
```

## Excluded Requirements

None. All requirements (MVP and non-MVP) are covered:
- MVP requirements (comparison endpoint, comparison page, URL-shareable comparison, critical vulnerability highlighting) are covered in the implementation tasks.
- Non-MVP requirement (export diff as JSON/CSV) is included in the comparison page UI task, as the Figma design includes the Export dropdown and the data is available client-side from the comparison API response.

## Workflow Mode Decision

**Selected mode:** `feature-branch`

**Rationale:** Atomicity indicator #4 — **Tightly coupled feature components** — is present. The feature consists of a new backend comparison endpoint (`GET /api/v2/sbom/compare`) and a new frontend comparison page that consumes it. Neither side functions independently:
- The frontend comparison page cannot render without the backend comparison endpoint
- The backend comparison endpoint has no consumer until the frontend page exists
- Merging either side independently to `main` would leave dead code or a broken UI

Additionally, atomicity indicator #2 — **Breaking API changes** — applies: the frontend tasks depend on a new API endpoint that does not yet exist in `main`. Merging the frontend first would result in API calls to a nonexistent endpoint.

**Interdependent tasks:**
- Tasks 2-3 (backend) create the comparison endpoint
- Tasks 4-6 (frontend) consume the comparison endpoint
- Task 4 directly depends on Task 3's API being available

The `workflow:feature-branch` label will be applied to the feature issue TC-9003 in Step 6a.

## Epic Grouping

**Strategy:** by-sub-feature (from Hierarchy Configuration)

| Epic | Label | Tasks |
|---|---|---|
| TC-9003: Backend SBOM comparison engine | Backend diff computation and REST endpoint | Tasks 2, 3 |
| TC-9003: Frontend comparison UI | API integration, comparison page, and list page enhancements | Tasks 4, 5, 6 |

Bookend tasks (Tasks 1, 8) and the documentation task (Task 7) are not assigned to sub-feature epics.

## Inherited Field Values

- **Priority:** Critical (inherited from TC-9003, will be propagated to all created tasks and epics)
- **fixVersions:** RHTPA 1.5.0 (inherited from TC-9003; no `fixVersion scope` setting found in Jira Field Defaults, defaulting to "both" — will be propagated to all created tasks and epics)

## additional_fields for created issues

Every task and epic will be created with:
```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Critical"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

## Documentation Signals

- **Doc impact type:** New Content
- **Details:** Document the comparison endpoint and comparison UI. API consumers need endpoint reference; UI users need a guide for the comparison workflow.
- **Reference material:** Existing SBOM detail page documentation, package/advisory data model docs.
