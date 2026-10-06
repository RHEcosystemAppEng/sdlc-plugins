# Repository Impact Map — TC-9003: SBOM Comparison View

## trustify-backend

Changes:
- Add `SbomComparisonResult` model with diff category structs (added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes)
- Add comparison service method to `SbomService` that fetches both SBOMs' packages and advisories and computes a structured diff
- Add `GET /api/v2/sbom/compare?left={id1}&right={id2}` endpoint handler with query parameter validation
- Add integration tests for the comparison endpoint covering normal diff, empty diff, invalid IDs, and large SBOM performance

## trustify-ui

Changes:
- Add TypeScript interfaces for the comparison API response types (`SbomComparisonResult`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`)
- Add API client function `fetchSbomComparison(leftId, rightId)` in `src/api/rest.ts`
- Add React Query hook `useSbomComparison` in `src/hooks/`
- Add `SbomComparisonPage` with header toolbar (SBOM selectors, Compare button, Export dropdown) and six collapsible diff sections per Figma design
- Add route definition for `/sbom/compare` in `src/routes.tsx`
- Add checkbox selection and "Compare selected" button to `SbomListPage` for list-page entry point
- Add unit tests (Vitest + React Testing Library) and E2E tests (Playwright) for the comparison page
- Add MSW mock handler and fixture data for the comparison endpoint

## Excluded Requirements

- **Export diff as JSON or CSV** (non-MVP): The Figma design includes an Export dropdown, so the UI shell (disabled button) will be included in the comparison page task. However, the backend export endpoint and full export functionality are not planned in this iteration because the feature description marks this as non-MVP and no backend export endpoint is specified. The frontend Export dropdown will be rendered but disabled until a future iteration implements the backend support.

---

## Workflow Mode Decision

**Selected mode:** `feature-branch`

**Rationale:** Atomicity indicator 4 (Tightly coupled feature components) is present. The frontend comparison page (`/sbom/compare`) requires the new backend endpoint `GET /api/v2/sbom/compare` that does not yet exist. If the frontend PR merged to `main` before the backend PR, the comparison page would make API calls to a nonexistent endpoint, resulting in runtime errors for users who navigate to the comparison page. Neither side functions independently in a user-facing sense: the backend endpoint without the frontend provides no user-accessible value, and the frontend without the backend produces errors.

**Interdependent tasks:**
- Task 5 (comparison page) and Task 6 (route integration) depend on Task 3 (backend endpoint) being available
- Task 4 (API types and hook) codifies the API contract that Task 3 implements

**Note:** The `workflow:feature-branch` label will be applied to the TC-9003 feature issue.

---

## Epic Grouping

**Strategy:** by-sub-feature (from CLAUDE.md Hierarchy Configuration)

### Epic 1: TC-9003: Backend comparison engine
- Task 2: Add SBOM comparison model and diff service
- Task 3: Add SBOM comparison endpoint with integration tests

### Epic 2: TC-9003: Frontend comparison UI
- Task 4: Add comparison API types, client function, and React Query hook
- Task 5: Add SBOM comparison page with diff sections
- Task 6: Add comparison route and SBOM list page compare action
- Task 7: Add comparison page unit and E2E tests

### Documentation
- Task 8: Document comparison endpoint and comparison UI workflow (assigned to Epic 2)

### Bookend Tasks (not assigned to Epics)
- Task 1: Create feature branch TC-9003 from main
- Task 9: Merge feature branch TC-9003 to main

---

## Task Creation Log — additional_fields

### Feature issue update
- **TC-9003**: Add label `workflow:feature-branch` (appended to existing labels: `["ai-generated-jira", "workflow:feature-branch"]`)

### Epics
Each Epic is created with:
```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Critical"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```
- Parent: `{"key": "TC-9003"}`

### Tasks (Tasks 1-9)
Each Task is created with:
```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Critical"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```
- Tasks 2-3: `parent` set to Epic 1 key
- Tasks 4-8: `parent` set to Epic 2 key
- Tasks 1, 9 (bookends): no Epic parent

**Priority propagation:** Included — Feature priority is "Critical" (not "Undefined").
**fixVersions propagation:** Included — Feature has fixVersions `["RHTPA 1.5.0"]` and no `fixVersion scope` setting in Jira Field Defaults (defaults to "both").

---

## Issue Links

### Feature "Incorporates" links (Feature to Epics)
- TC-9003 incorporates Epic 1 (Backend comparison engine)
- TC-9003 incorporates Epic 2 (Frontend comparison UI)

### Task dependency links
- Task 2 depends on Task 1
- Task 3 depends on Task 1, Task 2
- Task 4 depends on Task 1
- Task 5 depends on Task 1, Task 4
- Task 6 depends on Task 1, Task 5
- Task 7 depends on Task 1, Task 6
- Task 8 depends on Task 3, Task 7
- Task 9 depends on Tasks 2, 3, 4, 5, 6, 7, 8
