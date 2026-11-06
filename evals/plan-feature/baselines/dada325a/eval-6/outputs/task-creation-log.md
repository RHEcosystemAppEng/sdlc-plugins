# TC-9006 — Task Creation Log (simulated)

No Jira calls were made. Keys are simulated placeholders, in creation order.

## Type-to-role mapping
- Feature: Feature (ID 10142, level 2)
- Epic: Epic (level 1)
- Task: Task (level 0)

Grouping strategy: `by-repository` (CLAUDE.md Hierarchy Configuration).
Workflow mode: `direct-to-main` (all Target Branch = `main`; no bookend tasks).

## Inherited fields
| Field | Feature value | Propagated? | Reason |
|---|---|---|---|
| priority | Major | Yes — Epics and Tasks | Set and not "Undefined" |
| fixVersions | RHTPA 1.5.0 | Yes — Epics and Tasks | Non-empty and `fixVersion scope: both` |

## 6a.0 — Epics

| Order | Key | Issue type | Summary | parent | additional_fields |
|---|---|---|---|---|---|
| 1 | TC-9101 | Epic | TC-9006: trustify-backend | TC-9006 | `{"labels": ["ai-generated-jira"], "priority": {"name": "Major"}, "fixVersions": [{"name": "RHTPA 1.5.0"}]}` |
| 2 | TC-9102 | Epic | TC-9006: trustify-ui | TC-9006 | `{"labels": ["ai-generated-jira"], "priority": {"name": "Major"}, "fixVersions": [{"name": "RHTPA 1.5.0"}]}` |

Epic group mapping: `trustify-backend → TC-9101`, `trustify-ui → TC-9102`.

## 6a — Tasks

All tasks: issue type `Task`, `additional_fields = {"labels": ["ai-generated-jira"], "priority": {"name": "Major"}, "fixVersions": [{"name": "RHTPA 1.5.0"}]}`.

| Task | Key | Summary | Repository | parent (Epic) | File | Description digest |
|---|---|---|---|---|---|---|
| 1 | TC-9103 | Add remediation module with summary aggregation endpoint | trustify-backend | TC-9101 | task-1-backend-remediation-summary-endpoint.md | `sha256-md:457730645911442694020b5d362d28a111bf8979bf9a2a81fd02388e08b2902e` |
| 2 | TC-9104 | Add per-product remediation breakdown endpoint | trustify-backend | TC-9101 | task-2-backend-remediation-by-product-endpoint.md | `sha256-md:93223d3ff6300611da557bd54d3b1787603f4e8870e9af2ceb9d778af59b0122` |
| 3 | TC-9105 | Add filterable remediation vulnerability list endpoint | trustify-backend | TC-9101 | task-3-backend-remediation-vulnerability-list-endpoint.md | `sha256-md:668ceb0059e8d1550507e6b62fc9196b15ed444db0ab50747f1a2119168641c2` |
| 4 | TC-9106 | Add remediation API models, client functions, and React Query hooks | trustify-ui | TC-9102 | task-4-ui-remediation-api-hooks.md | `sha256-md:b3eb70e5dcd79e5ba12e020325fa092d799c0226ab985896f5cf4e375f7c66f6` |
| 5 | TC-9107 | Add remediation dashboard page with summary cards and progress chart | trustify-ui | TC-9102 | task-5-ui-remediation-dashboard-page.md | `sha256-md:66ba74a627753445f2e15f9033c5046cadf4794722630c6140ccc00d5ac19536` |
| 6 | TC-9108 | Add filterable vulnerability table to remediation dashboard | trustify-ui | TC-9102 | task-6-ui-remediation-vulnerability-table.md | `sha256-md:5a7dada3293cfdd58ce69877d9232a25dbc97c5a485f96d1457949b299db8f26` |
| 7 | TC-9109 | Document the remediation dashboard and aggregation endpoints | trustify-ui | TC-9102 | task-7-docs-remediation-dashboard.md | `sha256-md:de4f4a961e5c1e1bc143e485e82cd2236cbe95b6dc101ffb6197b5091c5228b5` |

Digests were computed with `scripts/sha256-digest.py` over each task's description body (the content below the metadata comment in each task file). In a live run the description would be re-fetched from Jira after creation and hashed as persisted. Each digest is posted as a standalone comment (`task-N-digest.md`) immediately after the task is created, before links.

## 6b — Links

Incorporates (Feature → Epic):
- TC-9006 incorporates TC-9101
- TC-9006 incorporates TC-9102

Depend (dependent → dependency):
- TC-9104 → TC-9103
- TC-9105 → TC-9103
- TC-9106 → TC-9103, TC-9104, TC-9105
- TC-9107 → TC-9106
- TC-9108 → TC-9106, TC-9107
- TC-9109 → TC-9103, TC-9104, TC-9105, TC-9106, TC-9107, TC-9108

## Feature label
Not modified (direct-to-main mode — no `workflow:feature-branch` label).
