# Repository Impact Map — TC-9003: SBOM comparison view

## Impact Map

```
trustify-backend:
  changes:
    - Add SbomComparison model types (added/removed packages, version changes, new/resolved vulnerabilities, license changes)
    - Add comparison diff service method to SbomService that computes structured diff between two SBOMs
    - Add GET /api/v2/sbom/compare?left={id1}&right={id2} endpoint returning structured diff
    - Add integration tests for comparison endpoint covering normal diff, empty diff, and large SBOM cases

trustify-ui:
  changes:
    - Add SbomComparison TypeScript interfaces to API models
    - Add fetchSbomComparison() API client function in rest.ts
    - Add useSbomComparison React Query hook
    - Add SbomComparePage with header toolbar (SBOM selectors, Compare button), collapsible diff sections, empty state, and loading state
    - Add route definition for /sbom/compare
    - Add diff export functionality (JSON/CSV) for compliance documentation (non-MVP)
    - Add unit tests (Vitest + RTL) and MSW mock handlers for comparison page
```

## Excluded Requirements

None. All requirements (MVP and non-MVP) have been decomposed into actionable tasks.

## Workflow Mode Decision

**Selected mode:** `feature-branch`

**Rationale:** The following atomicity indicator was identified:

- **Tightly coupled feature components** — The frontend comparison page (`/sbom/compare`) requires the new backend endpoint (`GET /api/v2/sbom/compare`) that does not yet exist. Merging the frontend without the backend would result in a non-functional comparison page making API calls to a nonexistent endpoint. The backend can be merged independently (adds a new endpoint without breaking existing functionality), but the frontend cannot function without the backend.

**Interdependent tasks:**
- Task 5 (Create SBOM comparison page) depends on Task 3 (Add comparison endpoint) via Task 4 (API client/hook)
- Task 4 (API client and hook) depends on Task 3 (comparison endpoint) for the API contract

**Note:** The `workflow:feature-branch` label will be applied to the feature issue TC-9003 in Step 6a.

## Epic Grouping

**Strategy:** by-sub-feature (from CLAUDE.md Hierarchy Configuration default)

| Epic | Summary | Tasks |
|---|---|---|
| Epic 1 | TC-9003: Backend SBOM comparison service | Tasks 2, 3 |
| Epic 2 | TC-9003: Frontend comparison UI | Tasks 4, 5, 6 |

Documentation task (Task 7) depends on both Epics.

## Task Creation Fields

**Inherited from Feature TC-9003:**
- Priority: Critical (propagated to all tasks)
- fixVersions: RHTPA 1.5.0 (propagated to all tasks; fixVersion scope = "both" per Jira Field Defaults)

**additional_fields applied to each created task:**
```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Critical"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

**additional_fields applied to each created Epic:**
```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Critical"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

**Feature issue label update:**
Append `workflow:feature-branch` to TC-9003 labels (preserving existing labels including `ai-generated-jira`).

## Task Summary

| # | Summary | Repository | Target Branch | Dependencies |
|---|---|---|---|---|
| 1 | Create feature branch TC-9003 from main | trustify-backend | main | None |
| 2 | Add SBOM comparison model and diff service | trustify-backend | TC-9003 | Task 1 |
| 3 | Add SBOM comparison REST endpoint with integration tests | trustify-backend | TC-9003 | Task 1, Task 2 |
| 4 | Add API client and React Query hook for SBOM comparison | trustify-ui | TC-9003 | Task 1, Task 3 |
| 5 | Create SBOM comparison page with diff sections | trustify-ui | TC-9003 | Task 1, Task 4 |
| 6 | Add diff export for SBOM comparison | trustify-ui | TC-9003 | Task 1, Task 5 |
| 7 | Document SBOM comparison endpoint and UI | trustify-backend | TC-9003 | Tasks 2, 3, 4, 5, 6 |
| 8 | Merge feature branch TC-9003 to main | trustify-backend | main | Tasks 2, 3, 4, 5, 6 |
