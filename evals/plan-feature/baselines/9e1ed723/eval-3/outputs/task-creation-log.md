# Task Creation Log — TC-9003 (simulated; no Jira calls made)

Placeholder keys (`EPIC-A`, `TASK-1`, …) stand in for the Jira keys that would be returned by `jira.create_issue`.

## 6a.0 — Epics

All Epics: `issueTypeName=Epic` (level 1, from Step 2.5), `parent=TC-9003`.

| Placeholder | Summary | Description (plain text) |
|---|---|---|
| EPIC-A | TC-9003: SBOM diff API | Backend work for the SBOM comparison: on-the-fly diff model/service and the GET /api/v2/sbom/compare endpoint with integration tests (Tasks 2, 3). |
| EPIC-B | TC-9003: SBOM comparison UI | Frontend comparison experience: API client/hook, /sbom/compare page, diff sections with critical highlighting, list-page "Compare selected", JSON/CSV export (Tasks 4–8). |
| EPIC-C | TC-9003: Delivery and documentation | Feature-branch bookends and documentation for the comparison endpoint and UI (Tasks 1, 9, 10). |

`additional_fields` for each Epic:
```json
{ "labels": ["ai-generated-jira"], "priority": {"name": "Critical"}, "fixVersions": [{"name": "RHTPA 1.5.0"}] }
```

## 6a — Tasks

Every Task: `issueTypeName=Task`, description = body of the corresponding `task-N-*.md` file, and:
```json
{ "labels": ["ai-generated-jira"], "priority": {"name": "Critical"}, "fixVersions": [{"name": "RHTPA 1.5.0"}] }
```

| # | Placeholder | Summary | Repository | parent | Digest comment file |
|---|---|---|---|---|---|
| 1 | TASK-1 | Create feature branch TC-9003 from main | trustify-ui | EPIC-C | task-1-digest.md |
| 2 | TASK-2 | Add SBOM comparison response model and on-the-fly diff service | trustify-backend | EPIC-A | task-2-digest.md |
| 3 | TASK-3 | Add GET /api/v2/sbom/compare endpoint with integration tests | trustify-backend | EPIC-A | task-3-digest.md |
| 4 | TASK-4 | Add SBOM comparison API client and useSbomComparison hook | trustify-ui | EPIC-B | task-4-digest.md |
| 5 | TASK-5 | Add /sbom/compare page shell with SBOM selectors and URL-shareable state | trustify-ui | EPIC-B | task-5-digest.md |
| 6 | TASK-6 | Render the six SBOM diff sections with count badges, sortable tables, and critical-vulnerability highlighting | trustify-ui | EPIC-B | task-6-digest.md |
| 7 | TASK-7 | Add two-SBOM checkbox selection and "Compare selected" action on the SBOM list page | trustify-ui | EPIC-B | task-7-digest.md |
| 8 | TASK-8 | Add Export dropdown to download the SBOM diff as JSON or CSV | trustify-ui | EPIC-B | task-8-digest.md |
| 9 | TASK-9 | Document the SBOM comparison API endpoint and comparison UI workflow | trustify-backend | EPIC-C | task-9-digest.md |
| 10 | TASK-10 | Merge feature branch TC-9003 to main | trustify-ui | EPIC-C | task-10-digest.md |

Each task's digest comment is posted immediately after creation, before links/other comments.

Feature label update (feature-branch mode):
```
jira.edit_issue(TC-9003, fields={"labels": ["ai-generated-jira", "workflow:feature-branch"]})
```

## 6b — Links

Incorporates (Feature → Epics, since Epics exist):
- TC-9003 incorporates EPIC-A
- TC-9003 incorporates EPIC-B
- TC-9003 incorporates EPIC-C

Depend (`inward` = dependent, `outward` = dependency):
| Dependent | Depends on |
|---|---|
| TASK-2 | TASK-1 |
| TASK-3 | TASK-1, TASK-2 |
| TASK-4 | TASK-1, TASK-3 |
| TASK-5 | TASK-1, TASK-4 |
| TASK-6 | TASK-1, TASK-5 |
| TASK-7 | TASK-1, TASK-5 |
| TASK-8 | TASK-1, TASK-5, TASK-6 |
| TASK-9 | TASK-1, TASK-2, TASK-3, TASK-4, TASK-5, TASK-6, TASK-7, TASK-8 |
| TASK-10 | TASK-2, TASK-3, TASK-4, TASK-5, TASK-6, TASK-7, TASK-8, TASK-9 |

## Bookend idempotency guard

TC-9003 "Linked Issues: None" → no existing "Create feature branch" / "Merge feature branch" tasks → bookends generated.
