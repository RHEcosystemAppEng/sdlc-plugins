# Task Creation Log — TC-9003

## Type-to-Role Mapping (Step 2.5)

Since Jira MCP is unavailable in this eval, the following mapping is assumed based on CLAUDE.md configuration:
- Feature: Feature (ID: 10142, level: 2)
- Epic: Epic (level: 1, if available)
- Task: Task (level: 0)

## Hierarchy Configuration

Default epic grouping strategy from CLAUDE.md: `by-sub-feature`

Since this is a multi-repo feature with clear repository boundaries, `by-repository` grouping is equally natural. Using `by-sub-feature` per configuration:

### Epic Groups (by-sub-feature)

| Epic | Summary | Tasks |
|---|---|---|
| Epic 1 | TC-9003: Backend comparison API | Tasks 1, 2, 3 |
| Epic 2 | TC-9003: Frontend comparison UI | Tasks 4, 5, 6, 7 |
| Epic 3 | TC-9003: Documentation | Task 8 |

## additional_fields for Each Task

All tasks receive the following `additional_fields`:

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Critical"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

### Field Propagation Rationale

- **labels**: `ai-generated-jira` is required on every AI-created issue (per Step 6a)
- **priority**: `Critical` inherited from TC-9003 (Feature priority is set and not "Undefined")
- **fixVersions**: `RHTPA 1.5.0` inherited from TC-9003 (Feature has non-empty fixVersions array; no `fixVersion scope` setting found in Jira Field Defaults, defaulting to "both" which propagates to tasks)

### Per-Task Creation Details

| Task # | Summary | Issue Type | Parent | additional_fields |
|---|---|---|---|---|
| 1 | Backend comparison models | Task | Epic 1 (TC-9003: Backend comparison API) | labels: [ai-generated-jira], priority: Critical, fixVersions: [RHTPA 1.5.0] |
| 2 | Backend comparison service | Task | Epic 1 | labels: [ai-generated-jira], priority: Critical, fixVersions: [RHTPA 1.5.0] |
| 3 | Backend comparison endpoint | Task | Epic 1 | labels: [ai-generated-jira], priority: Critical, fixVersions: [RHTPA 1.5.0] |
| 4 | Frontend API and hooks | Task | Epic 2 (TC-9003: Frontend comparison UI) | labels: [ai-generated-jira], priority: Critical, fixVersions: [RHTPA 1.5.0] |
| 5 | Frontend comparison page | Task | Epic 2 | labels: [ai-generated-jira], priority: Critical, fixVersions: [RHTPA 1.5.0] |
| 6 | Frontend SBOM list compare action | Task | Epic 2 | labels: [ai-generated-jira], priority: Critical, fixVersions: [RHTPA 1.5.0] |
| 7 | Frontend MSW mocks and E2E tests | Task | Epic 2 | labels: [ai-generated-jira], priority: Critical, fixVersions: [RHTPA 1.5.0] |
| 8 | Documentation — SBOM comparison | Task | Epic 3 (TC-9003: Documentation) | labels: [ai-generated-jira], priority: Critical, fixVersions: [RHTPA 1.5.0] |

### Epic Creation Details

| Epic # | Summary | Issue Type | Parent | additional_fields |
|---|---|---|---|---|
| Epic 1 | TC-9003: Backend comparison API | Epic | TC-9003 | labels: [ai-generated-jira], priority: Critical, fixVersions: [RHTPA 1.5.0] |
| Epic 2 | TC-9003: Frontend comparison UI | Epic | TC-9003 | labels: [ai-generated-jira], priority: Critical, fixVersions: [RHTPA 1.5.0] |
| Epic 3 | TC-9003: Documentation | Epic | TC-9003 | labels: [ai-generated-jira], priority: Critical, fixVersions: [RHTPA 1.5.0] |

## Issue Links (Step 6b)

### Feature "Incorporates" links (Epics available — link to Epics, not Tasks):
- TC-9003 incorporates Epic 1 (TC-9003: Backend comparison API)
- TC-9003 incorporates Epic 2 (TC-9003: Frontend comparison UI)
- TC-9003 incorporates Epic 3 (TC-9003: Documentation)

### Task "Depends on" links:
- Task 2 depends on Task 1 (models needed for service)
- Task 3 depends on Task 2 (service needed for endpoint)
- Task 4 depends on Task 3 (API contract must be finalized)
- Task 5 depends on Task 4 (hook must exist for page)
- Task 6 depends on Task 5 (page route must exist for navigation)
- Task 7 depends on Task 5 (page must exist for testing)
- Task 7 depends on Task 6 (list action must exist for E2E)
- Task 8 depends on Task 3 (API must be finalized for docs)
- Task 8 depends on Task 5 (UI must be finalized for docs)
