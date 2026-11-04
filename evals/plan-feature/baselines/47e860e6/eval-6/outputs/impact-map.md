# Repository Impact Map — TC-9006: Add vulnerability remediation tracking dashboard

(Would be posted as a comment on TC-9006 after user approval — Step 4.)

## Inputs and pre-checks

- **Step 0 — Project Configuration:** Repository Registry, Jira Configuration (project TC, Cloud ID, Feature type 10142) and Code Intelligence sections present. No Serena instances configured; repository analysis used the provided repository structure fixtures (`repo-backend.md`, `repo-frontend.md`).
- **Step 1 — Feature fields:** priority `Major`; fixVersions `[RHTPA 1.5.0]`; Documentation Considerations: **New Content**.
- **Step 1.5 — Parent link:** Feature has no parent; prompt skipped in eval mode (no parent link set).
- **Step 2 — Figma:** no Figma URL provided or present in the description; design-derived steps skipped.
- **Step 2.5 — Issue types:** `Feature` (ID 10142, level 2), `Epic` (level 1), `Task` (level 0). Exactly one level-1 type, named "Epic" → Epic hierarchy enabled.
- **Grouping strategy:** `by-repository` (Hierarchy Configuration default, as specified for this run) → one Epic per repository.
- **Testing readiness template:** no `docs/testing-readiness.md` in either repository → no testing tasks generated.
- **CONVENTIONS.md:** present at the root of both repositories; conventions applied per `shared/convention-applicability-rules.md`.

## Impact map

```
trustify-backend:
  changes:
    - Add new `remediation` domain module (model/service/endpoints) in modules/fundamental
    - Add GET /api/v2/remediation/summary — counts by severity × status, computed from existing sbom_advisory/advisory data
    - Add GET /api/v2/remediation/by-product — paginated per-product total/open/in-progress/resolved breakdown
    - Add GET /api/v2/remediation/vulnerabilities — paginated list filterable by severity, product, status (backs the dashboard table)
    - Mount remediation routes in server/src/main.rs
    - Add integration tests in tests/api/remediation.rs
    - Document the new endpoints and the dashboard (documentation task)

trustify-ui:
  changes:
    - Add remediation types, REST functions, and React Query hooks
    - Add /remediation route and RemediationDashboardPage with summary cards and progress chart
    - Add filterable/sortable/paginated vulnerability table with severity/product/status filters
    - Add MSW mocks, unit tests, and a Playwright E2E test for UC-1/UC-2
```

## Excluded / deferred requirements

- **Progress chart "trend over the past 30 days" (MVP, partially excluded):** the backend has no historical remediation-status data and the NFR forbids new tables, so a 30-day trend cannot be computed. **Missing input:** a data source for status history (e.g., status-change timestamps on existing tables, or approval for a new table/snapshot job). Task 5 renders the current status distribution per severity; the trend view is unresolved and needs clarification on TC-9006.
- **Export remediation report as CSV (non-MVP):** deferred, not planned in this iteration. It can be added later as a backend export endpoint plus a UI export button once MVP is delivered.

## Open assumptions (to verify at implementation time)

- Remediation status (Open/In Progress/Resolved) is stored on the SBOM–advisory relationship (`entity/src/sbom_advisory.rs`). If not, a schema change is needed, which conflicts with the "no new tables" NFR. Task 1 says to stop and escalate in that case.
- Product identity comes from the SBOM entity (`entity/src/sbom.rs`).

## Workflow mode (Step 4.5)

**Mode: `direct-to-main`**

Atomicity indicators:
1. Coordinated schema migrations: **none** (no migrations; aggregations use existing tables).
2. Breaking API changes: **none** (all three endpoints are new and additive; no existing contract changes).
3. Cross-cutting refactors: **none**.
4. Tightly coupled components: **not present**. The backend endpoints work and are useful on their own; the UI depends on them, and that ordering is enforced by task dependencies (Tasks 4–6 depend on Tasks 1–3), so every merge leaves `main` working.

All tasks target `main`. No bookend tasks and no `workflow:feature-branch` label.

## Jira hierarchy plan

```
TC-9006 (Feature)
├── Epic: "TC-9006: trustify-backend"  (Incorporates link from TC-9006)
│   ├── Task 1 — Add remediation module and GET /api/v2/remediation/summary endpoint
│   ├── Task 2 — Add GET /api/v2/remediation/by-product endpoint
│   ├── Task 3 — Add GET /api/v2/remediation/vulnerabilities filterable list endpoint
│   └── Task 7 — Document remediation dashboard and aggregation endpoints
└── Epic: "TC-9006: trustify-ui"  (Incorporates link from TC-9006)
    ├── Task 4 — Add remediation API client functions, types, and React Query hooks
    ├── Task 5 — Create remediation dashboard page with summary cards and progress chart
    └── Task 6 — Add filterable vulnerability table to remediation dashboard
```

### Epic creation (Step 6a.0)

| Epic | issueTypeName | summary | parent | additional_fields |
|---|---|---|---|---|
| Backend | `Epic` (level 1) | `TC-9006: trustify-backend` | `TC-9006` | `{"labels": ["ai-generated-jira"], "priority": {"name": "Major"}, "fixVersions": [{"name": "RHTPA 1.5.0"}]}` |
| Frontend | `Epic` (level 1) | `TC-9006: trustify-ui` | `TC-9006` | `{"labels": ["ai-generated-jira"], "priority": {"name": "Major"}, "fixVersions": [{"name": "RHTPA 1.5.0"}]}` |

Epic descriptions (plain text):
- **TC-9006: trustify-backend** — Backend remediation aggregation for the remediation dashboard: new remediation module with summary, by-product, and filterable vulnerability list endpoints computed from existing data, plus documentation of the endpoints and dashboard.
- **TC-9006: trustify-ui** — Frontend remediation dashboard at /remediation: API client and hooks, summary cards and progress chart, and a filterable vulnerability table.

### Task creation (Step 6a)

Every task is created with issue type `Task`, `parent` set to its Epic, and:

```
additional_fields: {
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Major"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

- **priority:** `Major` was inherited from TC-9006 and propagated (it is set, not "Undefined").
- **fixVersions:** `RHTPA 1.5.0` was inherited and propagated (the Feature has fixVersions and `fixVersion scope` is `both`).

| # | Task file | Repository | Parent Epic | Depends on |
|---|---|---|---|---|
| 1 | task-1-remediation-summary-endpoint.md | trustify-backend | TC-9006: trustify-backend | — |
| 2 | task-2-remediation-by-product-endpoint.md | trustify-backend | TC-9006: trustify-backend | 1 |
| 3 | task-3-remediation-vulnerability-list-endpoint.md | trustify-backend | TC-9006: trustify-backend | 1 |
| 4 | task-4-remediation-api-client-and-hooks.md | trustify-ui | TC-9006: trustify-ui | 1, 2, 3 |
| 5 | task-5-remediation-dashboard-page.md | trustify-ui | TC-9006: trustify-ui | 4 |
| 6 | task-6-remediation-vulnerability-table.md | trustify-ui | TC-9006: trustify-ui | 4, 5 |
| 7 | task-7-remediation-documentation.md (documentation) | trustify-backend | TC-9006: trustify-backend | 1, 2, 3, 5, 6 |

Each task gets a description digest comment immediately after creation (`task-N-digest.md`).

### Issue links (Step 6b)

- **Incorporates** (Feature → Epic only, not Feature → Task):
  - `TC-9006` incorporates `TC-9006: trustify-backend` Epic
  - `TC-9006` incorporates `TC-9006: trustify-ui` Epic
- **Depend** (dependent → dependency): 2→1, 3→1, 4→1, 4→2, 4→3, 5→4, 6→4, 6→5, 7→1, 7→2, 7→3, 7→5, 7→6

---
This comment was AI-generated by [sdlc-workflow/plan-feature](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.10.
