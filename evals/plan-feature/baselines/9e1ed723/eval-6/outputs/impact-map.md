# TC-9006 — Repository Impact Map and Planning Record

Feature: **TC-9006 — Add vulnerability remediation tracking dashboard**
Priority: Major · Fix Versions: RHTPA 1.5.0 · Labels: ai-generated-jira

> Simulated Jira keys: Epics TC-9007 and TC-9008, Tasks TC-9009 to TC-9017. These are placeholders. Real keys would come back from `jira.create_issue`.

## Step 0 — Project Configuration check
Repository Registry, Jira Configuration (project key TC, Cloud ID, Feature type ID 10142), and Code Intelligence are all present. Validation passed.

## Step 1 — Feature extraction
- Priority: `Major`, propagated
- fixVersions: `[RHTPA 1.5.0]`, propagated (`fixVersion scope: both`)
- Documentation signals: **New Content**. Document the remediation dashboard and aggregation endpoints (user guide for security teams, endpoint reference for API consumers).
- Figma: no Figma link in the Feature or the arguments, so Step 2 was skipped.

## Step 1.5 — Parent linking
The Feature has no `parent`. The parent-link prompt was skipped (no parent key given), so no parent link was set.

## Step 2.5 — Issue type discovery (type-to-role mapping)
```
Type-to-role mapping:
  Feature: Feature (ID: 10142, level: 2)
  Epic:    Epic    (level: 1)    # level-1 type available, so Epic creation is enabled
  Task:    Task    (level: 0)
```
- Exactly one level-1 type exists ("Epic"), so no selection prompt was needed.
- Hierarchy Configuration: default Epic grouping strategy is **`by-repository`**. It was applied without prompting.

## Step 3 — Repository analysis (summary)
No Serena instances are configured, so the analysis used the repository structure fixtures (`repo-backend.md`, `repo-frontend.md`).

**trustify-backend**
- Domain module pattern `model/ + service/ + endpoints/` (e.g., `modules/fundamental/src/advisory/`). Routes are registered in `endpoints/mod.rs` and mounted in `server/src/main.rs`.
- Source data for aggregation (no new tables allowed): `entity/src/advisory.rs` (severity), `entity/src/sbom_advisory.rs` (SBOM↔vulnerability), `entity/src/sbom.rs`.
- Reuse: `common/src/db/query.rs` (filter/sort/paginate), `common/src/model/paginated.rs::PaginatedResults`, `common/src/error.rs::AppError`, `AdvisoryService`, `AdvisorySummary.severity`.
- Tests: `tests/api/*.rs` against PostgreSQL.
- Docs: `README.md`, `CONVENTIONS.md`. There is no `docs/testing-readiness.md`, so no testing tasks were generated.

**trustify-ui**
- API layer `src/api/client.ts` / `rest.ts` / `models.ts`, hooks in `src/hooks/`, pages in `src/pages/<Page>/` with `components/`, routes in `src/routes.tsx`.
- Reuse: `FilterToolbar.tsx`, `SeverityBadge.tsx`, `EmptyStateCard.tsx`, `LoadingSpinner.tsx`, `utils/severityUtils.ts`.
- Tests: Vitest + RTL + MSW (`tests/mocks/handlers.ts`, fixtures), Playwright (`tests/e2e/`).
- Docs: `README.md`, `CONVENTIONS.md`. There is no `docs/testing-readiness.md`.

**Backend API discovery (manual REST calls):** the remediation endpoints do not exist yet. They are defined by Tasks 2–4 and their contracts are copied into the frontend tasks' Implementation Notes:
- `GET /api/v2/remediation/summary` → `{ totals: {open, in_progress, resolved}, by_severity: [{severity, open, in_progress, resolved}] }`
- `GET /api/v2/remediation/by-product` → `PaginatedResults<{product, total, open, in_progress, resolved}>`
- `GET /api/v2/remediation/vulnerabilities` → `PaginatedResults<{advisory_id, identifier, title, severity, status, product, sbom_id}>`

**Shared-artifact analysis:** the endpoints only read existing advisory/SBOM correlation data. No new shared artifact is created or written. Producers of the correlation data (SBOM and advisory ingestion in `modules/ingestor/src/graph/`) are unchanged.

**Eval infrastructure:** none. No task modifies a skill `SKILL.md`.

## Step 4 — Repository Impact Map

```
trustify-backend:
  changes:
    - Add a new `remediation` domain module (model/service/endpoints) in modules/fundamental, mounted in server/src/main.rs
    - Add GET /api/v2/remediation/summary — counts by severity × status, computed from existing advisory/SBOM data
    - Add GET /api/v2/remediation/by-product — paginated per-product total/open/in_progress/resolved breakdown
    - Add GET /api/v2/remediation/vulnerabilities — paginated, filterable (severity/product/status) list for the dashboard table
    - Add integration tests in tests/api/remediation.rs
    - Document the remediation endpoints and dashboard (New Content)

trustify-ui:
  changes:
    - Add remediation API types, REST functions, React Query hooks, and MSW mocks
    - Add the /remediation dashboard page (lazy route) with Open/In Progress/Resolved summary cards and a status-by-severity progress chart
    - Add a filterable (severity, product, status), sortable, paginated vulnerability table on the dashboard
    - Add unit tests and a Playwright E2E test for UC-1/UC-2
```

### Excluded requirements
| Requirement | Reason / missing input |
|---|---|
| Progress chart "trend over the past 30 days" (requirement 3 / UC-1 step 3) | No historical remediation-status data source exists in the backend, and the NFR "No new database tables" rules out a status-history table. To plan the time-series, we need a decision on how history is derived (e.g., from timestamps on existing records, if any) or an approved exception to the NFR. The chart in Task 6 shows the current status-by-severity breakdown and can be extended later. |
| Export remediation report as CSV (non-MVP) | Not enough detail to break into tasks: report columns/scope and where it is generated (backend endpoint vs client-side) are not specified. Non-MVP. |

### Open questions (need confirmation before or during implementation)
1. **Remediation status source.** Open / In Progress / Resolved is not a documented attribute on the existing entities. Task 2 tells the implementer to check `entity/src/sbom_advisory.rs` and to stop and ask if no status column exists. The NFR forbids new tables, but a new column may also need approval.
2. **Inferred list endpoint.** `GET /api/v2/remediation/vulnerabilities` (Task 4) is not in the Feature requirements. It was added because the MVP filterable table needs a product/status-aware list that `GET /api/v2/advisory` does not provide.
3. **Product identity.** There is no product entity. Product is derived from SBOM metadata (Task 3).
4. **Counting unit.** Should a vulnerability that affects N SBOMs count once or N times? Tasks 2–4 must apply one rule consistently.
5. **Cross-repo feature branch.** Bookend tasks name a single repository (trustify-backend). The trustify-ui tasks also target `TC-9006`, so a `TC-9006` branch must also be created in trustify-ui and merged to trustify-ui `main` after the backend. Recommendation: confirm whether to add trustify-ui bookend tasks or have the Task 1/Task 9 implementer handle both repos.

## Step 4.5 — Workflow mode
**Mode: `feature-branch`**
- Atomicity indicator found: **#4 Tightly coupled feature components**. The new `/remediation` UI page (Tasks 5–7) needs new API endpoints (Tasks 2–4) that do not exist yet. Merging the frontend alone would ship a dashboard that calls missing endpoints.
- Indicators #1 (schema migrations), #2 (breaking API changes), and #3 (cross-cutting refactor) were not found. All backend changes are additive and add no tables.
- Interdependent tasks: Task 5 (API client/hooks) depends on Tasks 2, 3, 4. Tasks 6 and 7 depend on Task 5.
- The `workflow:feature-branch` label is applied to TC-9006 in Step 6a, keeping the existing `ai-generated-jira` label.
- Bookends: Task 1 (create-branch) and Task 9 (merge-branch) in trustify-backend, which has most of the tasks (6 of 9). Idempotency guard: TC-9006 has no linked issues, so there are no existing bookend tasks and both were generated.

## Step 5 — Epic grouping (strategy: by-repository)

| Epic group | Epic summary | Simulated key | Tasks |
|---|---|---|---|
| trustify-backend | TC-9006: trustify-backend | TC-9007 | 1, 2, 3, 4, 8, 9 |
| trustify-ui | TC-9006: trustify-ui | TC-9008 | 5, 6, 7 |

Hierarchy: **Feature TC-9006 → Epics (TC-9007, TC-9008) → Tasks**.

## Task list

| # | Summary | Repository | Target Branch | Parent Epic | Depends on | File |
|---|---|---|---|---|---|---|
| 1 | Create feature branch TC-9006 from main | trustify-backend | main | TC-9007 | — | task-1-create-feature-branch.md |
| 2 | Add remediation module and GET /api/v2/remediation/summary aggregation endpoint | trustify-backend | TC-9006 | TC-9007 | 1 | task-2-remediation-summary-endpoint.md |
| 3 | Add GET /api/v2/remediation/by-product per-product remediation breakdown endpoint | trustify-backend | TC-9006 | TC-9007 | 1, 2 | task-3-remediation-by-product-endpoint.md |
| 4 | Add filterable GET /api/v2/remediation/vulnerabilities endpoint | trustify-backend | TC-9006 | TC-9007 | 1, 2, 3 | task-4-remediation-vulnerability-list-endpoint.md |
| 5 | Add remediation API models, REST functions, and React Query hooks | trustify-ui | TC-9006 | TC-9008 | 1, 2, 3, 4 | task-5-remediation-api-client-and-hooks.md |
| 6 | Add /remediation dashboard page with summary cards and progress chart | trustify-ui | TC-9006 | TC-9008 | 1, 5 | task-6-remediation-dashboard-page.md |
| 7 | Add filterable outstanding-vulnerability table to /remediation | trustify-ui | TC-9006 | TC-9008 | 1, 5, 6 | task-7-remediation-vulnerability-table.md |
| 8 | Document the remediation tracking dashboard and remediation API endpoints | trustify-backend | TC-9006 | TC-9007 | 2–7 | task-8-remediation-documentation.md |
| 9 | Merge feature branch TC-9006 to main | trustify-backend | main | TC-9007 | 2–8 | task-9-merge-feature-branch.md |

No testing tasks were generated because neither repository has `docs/testing-readiness.md`.

## additional_fields for created issues
All Epics and Tasks get the same fields:
```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Major"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```
- Epics: `issueTypeName="Epic"`, `parent="TC-9006"`.
- Tasks: `issueTypeName="Task"`, `parent=<Epic key>` (see table above).
- Feature TC-9006 edit: `labels: ["ai-generated-jira", "workflow:feature-branch"]`.

See `task-creation-log.md` for the full ordered call log.
