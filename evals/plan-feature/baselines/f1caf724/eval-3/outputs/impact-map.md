# Repository Impact Map — TC-9003: SBOM comparison view

## Workflow Mode

**Selected mode:** `feature-branch`

**Rationale:** Atomicity indicator #4 (tightly coupled feature components) is present. The frontend comparison page (`/sbom/compare`) requires the new backend `GET /api/v2/sbom/compare` endpoint, which does not yet exist. Neither the frontend page nor the backend endpoint delivers user-visible value independently — the comparison page cannot function without the comparison endpoint, and the endpoint has no consumer without the comparison page. Merging either side alone to `main` would leave a partially visible, non-functional feature.

**Interdependent tasks:**
- Task 3 (backend comparison endpoint) and Task 5 (frontend comparison page) are directly coupled — the frontend calls the backend endpoint.
- Task 4 (frontend API types/hook) depends on Task 3's API contract.
- Task 6 (SBOM list multi-select) navigates to the comparison page, which depends on the endpoint.

The `workflow:feature-branch` label will be applied to the feature issue TC-9003.

---

## Impact Map

### trustify-backend
  changes:
    - Add SBOM comparison model types (SbomComparisonResult and sub-types) in `modules/fundamental/src/sbom/model/`
    - Add comparison service logic to compute structured diff between two SBOMs in `modules/fundamental/src/sbom/service/`
    - Add `GET /api/v2/sbom/compare?left={id1}&right={id2}` endpoint in `modules/fundamental/src/sbom/endpoints/`
    - Add integration tests for the comparison endpoint in `tests/api/`

### trustify-ui
  changes:
    - Add TypeScript interfaces for comparison response types in `src/api/models.ts`
    - Add `compareSboms()` API client function in `src/api/rest.ts`
    - Create `useSbomComparison` React Query hook in `src/hooks/`
    - Create SBOM comparison page at `/sbom/compare` with header toolbar and six collapsible diff sections in `src/pages/SbomComparePage/`
    - Add route for `/sbom/compare` in `src/routes.tsx`
    - Add checkbox multi-selection and "Compare selected" action to `src/pages/SbomListPage/SbomListPage.tsx`
    - Add unit and integration tests for comparison page and list page changes

---

## Excluded Requirements

- **Export diff as JSON or CSV** — marked as non-MVP in the feature requirements. The Export dropdown UI element is included in the comparison page per the Figma design, but full export functionality (generating and downloading JSON/CSV files) is deferred to a follow-up feature. The UI button is rendered but can be connected to client-side export logic if desired during implementation.

---

## Priority and fixVersion Inheritance

- **Priority:** Critical (inherited from Feature TC-9003, will be propagated to all created tasks)
- **fixVersions:** RHTPA 1.5.0 (inherited from Feature TC-9003, will be propagated to all created tasks — no `fixVersion scope` setting found in CLAUDE.md Jira Field Defaults, defaulting to "both")

---

## Task Summary

| Task | Summary | Repository | Epic Group |
|---|---|---|---|
| 1 | Create feature branch TC-9003 from main | trustify-ui | (bookend) |
| 2 | Add SBOM comparison diff model and service | trustify-backend | Backend comparison engine |
| 3 | Add SBOM comparison endpoint with integration tests | trustify-backend | Backend comparison engine |
| 4 | Add SBOM comparison API types and React Query hook | trustify-ui | Frontend comparison UI |
| 5 | Create SBOM comparison page with diff sections | trustify-ui | Frontend comparison UI |
| 6 | Add multi-select and compare action to SBOM list page | trustify-ui | Frontend comparison UI |
| 7 | Document SBOM comparison endpoint and UI workflow | trustify-ui | (documentation) |
| 8 | Merge feature branch TC-9003 to main | trustify-ui | (bookend) |

## Type-to-Role Mapping

```
Type-to-role mapping:
  Feature: Feature (ID: 10142, level: 2)
  Epic:    (not discovered — no Jira project metadata available in eval mode)
  Task:    (not discovered — no Jira project metadata available in eval mode)
```

Note: In eval mode, issue types cannot be dynamically discovered from Jira. If a level-1 Epic type were available, tasks would be grouped into Epics using the `by-sub-feature` strategy (per CLAUDE.md Hierarchy Configuration) with two Epics: "TC-9003: Backend comparison engine" and "TC-9003: Frontend comparison UI".
