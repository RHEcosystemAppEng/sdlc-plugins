# Task creation log — TC-9003 (simulated Step 6)

No Jira calls were made (eval mode). Placeholder keys `TC-9003-E*` / `TC-9003-T*` stand in for the keys Jira would assign.

## Type-to-role mapping (Step 2.5, assumed)

```
Feature: Feature (ID: 10142, level: 2)
Epic:    Epic    (ID: resolved via get_project_issue_types, level: 1)   # assumed present — CLAUDE.md has Hierarchy Configuration
Task:    Task    (ID: resolved via get_project_issue_types, level: 0)
```

## Inherited field values

- Priority: **Critical** (set on Feature, not "Undefined") → propagated to all Epics and Tasks
- fixVersions: **RHTPA 1.5.0** (non-empty) and `fixVersion scope: both` → propagated to all Epics and Tasks
- Prompt for priority / fixVersion (both `true` in Jira Field Defaults): non-interactive default = accept inherited values

Common `additional_fields` for every Epic and Task:

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Critical"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

## 6a.0 — Epics (by-sub-feature)

| # | Placeholder key | issueTypeName | Summary | parent | Description (plain text) |
|---|---|---|---|---|---|
| A | TC-9003-EA | Epic | TC-9003: SBOM diff API | TC-9003 | Backend comparison model, diff service and GET /api/v2/sbom/compare endpoint in trustify-backend (Tasks 2, 3). |
| B | TC-9003-EB | Epic | TC-9003: Comparison UI and navigation | TC-9003 | Frontend API client/hook, /sbom/compare page and "Compare selected" entry point in trustify-ui (Tasks 4, 5, 6). |
| C | TC-9003-EC | Epic | TC-9003: Compliance export and documentation | TC-9003 | JSON/CSV export of the diff (non-MVP) and user/API documentation (Tasks 7, 8). |
| D | TC-9003-ED | Epic | TC-9003: Feature branch lifecycle | TC-9003 | Bookend tasks that create and merge the TC-9003 feature branch (Tasks 1, 9). |

## 6a — Tasks

| Task | Placeholder key | Summary | Repository | Target Branch | parent (Epic) | Digest file |
|---|---|---|---|---|---|---|
| 1 | TC-9003-T1 | Create feature branch TC-9003 from main | trustify-ui | main | TC-9003-ED | task-1-digest.md |
| 2 | TC-9003-T2 | Add SBOM comparison model and diff computation in SbomService | trustify-backend | TC-9003 | TC-9003-EA | task-2-digest.md |
| 3 | TC-9003-T3 | Add GET /api/v2/sbom/compare endpoint with integration tests | trustify-backend | TC-9003 | TC-9003-EA | task-3-digest.md |
| 4 | TC-9003-T4 | Add SBOM comparison API client, types and useSbomComparison hook | trustify-ui | TC-9003 | TC-9003-EB | task-4-digest.md |
| 5 | TC-9003-T5 | Add /sbom/compare comparison page with collapsible diff sections and shareable URL | trustify-ui | TC-9003 | TC-9003-EB | task-5-digest.md |
| 6 | TC-9003-T6 | Add SBOM multi-select and "Compare selected" action to SbomListPage | trustify-ui | TC-9003 | TC-9003-EB | task-6-digest.md |
| 7 | TC-9003-T7 | Implement "Export JSON" / "Export CSV" for the SBOM comparison (non-MVP) | trustify-ui | TC-9003 | TC-9003-EC | task-7-digest.md |
| 8 | TC-9003-T8 | Document the SBOM comparison endpoint and comparison UI workflow | trustify-ui | TC-9003 | TC-9003-EC | task-8-digest.md |
| 9 | TC-9003-T9 | Merge feature branch TC-9003 to main | trustify-ui | main | TC-9003-ED | task-9-digest.md |

After all tasks are created: `jira.edit_issue(TC-9003, fields={"labels": ["ai-generated-jira", "workflow:feature-branch"]})` (existing label preserved).

## 6b — Issue links

**Incorporates (Feature → Epic):**
- TC-9003 incorporates TC-9003-EA, TC-9003-EB, TC-9003-EC, TC-9003-ED

**Depend (inward = dependent, outward = dependency):**

| Dependent | Depends on |
|---|---|
| T2 | T1 |
| T3 | T1, T2 |
| T4 | T1, T3 |
| T5 | T1, T4 |
| T6 | T1, T5 |
| T7 | T1, T5 |
| T8 | T1, T3, T5, T6, T7 |
| T9 | T2, T3, T4, T5, T6, T7, T8 |

## 6c — Feature comment

See `summary-comment.md`. Workflow-mode decision comment: `workflow-mode-comment.md`. Impact map comment: `impact-map.md`.
