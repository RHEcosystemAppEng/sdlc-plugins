# Repository Impact Map -- TC-9003: SBOM comparison view

## trustify-backend

changes:
- Add SBOM comparison response model types (SbomComparisonResult with added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes)
- Add comparison service logic in SbomService to compute diff between two SBOMs using existing package, advisory, and license data (no new database tables)
- Add GET /api/v2/sbom/compare?left={id1}&right={id2} endpoint with query parameter validation
- Add integration tests for the comparison endpoint covering all diff categories and error cases
- Document the comparison endpoint and UI workflow (New Content)

## trustify-ui

changes:
- Add TypeScript interfaces for the comparison API response types in src/api/models.ts
- Add API client function fetchSbomComparison in src/api/rest.ts
- Add React Query hook useSbomComparison in src/hooks/
- Create SbomComparePage component at /sbom/compare with header toolbar (SBOM selectors, Compare button, Export dropdown) and 6 collapsible diff sections (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes)
- Add route definition for /sbom/compare in src/routes.tsx
- Modify SbomListPage to add checkbox selection and "Compare selected" navigation button
- Implement client-side export of comparison results as JSON and CSV (non-MVP)
- Add MSW handlers, test fixtures, and unit tests for comparison feature

## Excluded requirements

None -- all requirements (MVP and non-MVP) are plannable with the available design context and repository information.

---

## Workflow Mode Decision

**Selected mode:** `feature-branch`

**Rationale:** The feature introduces tightly coupled frontend and backend components. Specifically, a new UI page at `/sbom/compare` requires a new backend API endpoint `GET /api/v2/sbom/compare` that does not yet exist. This matches the atomicity indicator "tightly coupled feature components -- the feature consists of frontend and backend changes where neither side functions independently."

**Interdependent tasks:**
- Frontend tasks (5-9) depend on backend tasks (2-4): the frontend comparison page calls the backend comparison endpoint; merging only the frontend would result in API calls to a non-existent endpoint.
- The `workflow:feature-branch` label will be applied to feature issue TC-9003.

---

## Inherited Field Values

- **Priority:** Critical (inherited from TC-9003, propagated to all created tasks and epics)
- **Fix Version:** RHTPA 1.5.0 (inherited from TC-9003, propagated to all created tasks and epics -- fixVersion scope defaults to "both" since no Jira Field Defaults section exists)

## Epic Grouping (by-sub-feature)

| Epic | Summary | Tasks |
|---|---|---|
| Epic 1 | TC-9003: Backend Comparison API | Tasks 2, 3, 4 |
| Epic 2 | TC-9003: Frontend Comparison UI | Tasks 5, 6, 7, 8, 9 |

Task 1 (create-branch bookend), Task 10 (documentation), and Task 11 (merge-branch bookend) are linked directly to the Feature.

## Task Creation Log

| Task # | Summary | Type | Repository | Epic | Labels | Priority | Fix Versions |
|---|---|---|---|---|---|---|---|
| 1 | Create feature branch TC-9003 from main | Task | trustify-ui | -- | ai-generated-jira | Critical | RHTPA 1.5.0 |
| 2 | Add SBOM comparison response model types | Task | trustify-backend | TC-9003: Backend Comparison API | ai-generated-jira | Critical | RHTPA 1.5.0 |
| 3 | Add SBOM comparison service and REST endpoint | Task | trustify-backend | TC-9003: Backend Comparison API | ai-generated-jira | Critical | RHTPA 1.5.0 |
| 4 | Add SBOM comparison integration tests | Task | trustify-backend | TC-9003: Backend Comparison API | ai-generated-jira | Critical | RHTPA 1.5.0 |
| 5 | Add SBOM comparison API types and React Query hook | Task | trustify-ui | TC-9003: Frontend Comparison UI | ai-generated-jira | Critical | RHTPA 1.5.0 |
| 6 | Implement SBOM comparison page with diff sections | Task | trustify-ui | TC-9003: Frontend Comparison UI | ai-generated-jira | Critical | RHTPA 1.5.0 |
| 7 | Add comparison selection to SBOM list page | Task | trustify-ui | TC-9003: Frontend Comparison UI | ai-generated-jira | Critical | RHTPA 1.5.0 |
| 8 | Implement comparison diff export as JSON and CSV | Task | trustify-ui | TC-9003: Frontend Comparison UI | ai-generated-jira | Critical | RHTPA 1.5.0 |
| 9 | Add comparison page tests and mock fixtures | Task | trustify-ui | TC-9003: Frontend Comparison UI | ai-generated-jira | Critical | RHTPA 1.5.0 |
| 10 | Document SBOM comparison endpoint and UI | Task | trustify-backend | -- | ai-generated-jira | Critical | RHTPA 1.5.0 |
| 11 | Merge feature branch TC-9003 to main | Task | trustify-ui | -- | ai-generated-jira | Critical | RHTPA 1.5.0 |

Feature issue TC-9003 labels updated to include `workflow:feature-branch`.

## Issue Links

**Feature "Incorporates" links:**
- TC-9003 "Incorporates" Epic: TC-9003: Backend Comparison API
- TC-9003 "Incorporates" Epic: TC-9003: Frontend Comparison UI
- TC-9003 "Incorporates" Task 1 (create-branch bookend)
- TC-9003 "Incorporates" Task 10 (documentation)
- TC-9003 "Incorporates" Task 11 (merge-branch bookend)

**Task "Depends" links:**
- Task 2 depends on Task 1 (create-branch)
- Task 3 depends on Task 1, Task 2
- Task 4 depends on Task 1, Task 3
- Task 5 depends on Task 1
- Task 6 depends on Task 1, Task 5
- Task 7 depends on Task 1
- Task 8 depends on Task 1, Task 6
- Task 9 depends on Task 1, Task 6, Task 7
- Task 10 depends on Task 4, Task 9
- Task 11 depends on Tasks 2, 3, 4, 5, 6, 7, 8, 9, 10

---

This comment was AI-generated by [sdlc-workflow/plan-feature](https://github.com/mrizzi/sdlc-plugins) v0.12.1.
