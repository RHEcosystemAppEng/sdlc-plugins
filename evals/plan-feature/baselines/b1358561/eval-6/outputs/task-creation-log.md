# Task Creation Log — TC-9006

Simulated Jira operations in execution order. Keys are placeholders.

## 6a.0 – Epics
| Order | Key | Type | Summary | parent | additional_fields |
|---|---|---|---|---|---|
| 1 | TC-9101 | Epic | TC-9006: trustify-backend | TC-9006 | `{"labels": ["ai-generated-jira"], "priority": {"name": "Major"}, "fixVersions": [{"name": "RHTPA 1.5.0"}]}` |
| 2 | TC-9102 | Epic | TC-9006: trustify-ui | TC-9006 | `{"labels": ["ai-generated-jira"], "priority": {"name": "Major"}, "fixVersions": [{"name": "RHTPA 1.5.0"}]}` |

Epic group mapping: `trustify-backend` → TC-9101, `trustify-ui` → TC-9102

## 6a – Tasks (each followed immediately by its digest comment)
All tasks use issue type `Task` and `additional_fields = {"labels": ["ai-generated-jira"], "priority": {"name": "Major"}, "fixVersions": [{"name": "RHTPA 1.5.0"}]}`.

| # | Key | parent (Epic) | Summary | Digest comment |
|---|---|---|---|---|
| 1 | TC-9103 | TC-9101 | Add remediation domain module with summary and per-product aggregation service | `task-1-digest.md` (sha256-md:82198eaeb59d8a6070e92983a950515e538db1a7676109a4d5ac5d5fa72e6ae3) |
| 2 | TC-9104 | TC-9101 | Add GET /api/v2/remediation/summary and /api/v2/remediation/by-product endpoints | `task-2-digest.md` (sha256-md:e050b82645efd5953889b3d09cb55386edac40c8300de9161503e12f3f43c053) |
| 3 | TC-9105 | TC-9101 | Add filterable remediation vulnerability list and 30-day trend endpoints | `task-3-digest.md` (sha256-md:dfa122c0855a48f7c8bffb261ceedf489230cd03f4a060bffdf65f0e8f448927) |
| 4 | TC-9106 | TC-9102 | Add remediation API types, REST client functions, React Query hooks and MSW mocks | `task-4-digest.md` (sha256-md:194050c5bf999d169952e84a45cf46c55912320604c9d6245b9d728b4f6776be) |
| 5 | TC-9107 | TC-9102 | Add /remediation dashboard page with summary cards and remediation trend chart | `task-5-digest.md` (sha256-md:68c7739e2f48aceee9dc99982342a0fdfb05f04320dc5789ac6866038f770294) |
| 6 | TC-9108 | TC-9102 | Add filterable outstanding-vulnerability table to the remediation dashboard | `task-6-digest.md` (sha256-md:39b363e610791cd6ae04672198939da7662aa1321897d0a9a50aecadb4d81efc) |
| 7 | TC-9109 | TC-9101 | Document the remediation tracking dashboard and remediation aggregation endpoints | `task-7-digest.md` (sha256-md:923bfef1cfa5e064b7e985568b7012c010bd8df39027e636db003bd8737b51e9) |

The workflow mode is direct-to-main, so the Feature gets no `workflow:feature-branch` label.

## 6b – Links
Incorporates (Feature → Epic):
- `create_issue_link(link_type="Incorporates", inward_issue_key="TC-9006", outward_issue_key="TC-9101")`
- `create_issue_link(link_type="Incorporates", inward_issue_key="TC-9006", outward_issue_key="TC-9102")`

Depend (dependent → dependency):
- TC-9104 → TC-9103
- TC-9105 → TC-9103; TC-9105 → TC-9104
- TC-9106 → TC-9104; TC-9106 → TC-9105
- TC-9107 → TC-9106
- TC-9108 → TC-9106; TC-9108 → TC-9107
- TC-9109 → TC-9103, TC-9104, TC-9105, TC-9106, TC-9107, TC-9108

## Comments on TC-9006
- `impact-map-comment.md` — Repository Impact Map and workflow mode decision (Step 4 / 4.5)
- `summary-comment.md` — plan summary (Step 6c)
