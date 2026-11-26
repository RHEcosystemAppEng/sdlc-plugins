# TC-9006 — Repository Impact Map and Planning Log

**Feature:** TC-9006 — Add vulnerability remediation tracking dashboard
**Feature priority:** Major (id not provided in fixture) — propagated
**Feature fixVersions:** RHTPA 1.5.0 — propagated (`fixVersion scope: both`)

---

## Step 0 — Project Configuration validation

- Repository Registry: present
- Jira Configuration: present (Project key TC, Cloud ID 2b9e35e3-6bd3-4cec-b838-f4249ee02432, Feature issue type ID 10142)
- Code Intelligence: present (no Serena instances, so analysis fell back to the repository structure fixtures `repo-backend.md` and `repo-frontend.md`)

Result: passed.

## Step 1 — Feature extraction

- Title: Add vulnerability remediation tracking dashboard
- Priority: `Major`. This is not "Undefined", so it is propagated.
- fixVersions: `[RHTPA 1.5.0]`. The list is not empty, so it is propagated.
- Documentation signals: **New Content**. Document the remediation dashboard (user guide) and the aggregation endpoints (API reference).
- Figma links: none found in the description, and no Figma URL was passed as an argument.

## Step 1.5 — Parent link

The Feature has no existing parent. In the eval, the parent-link prompt was skipped ("press Enter"), so no `edit_issue` call was made.

## Step 2 — Figma

No Figma URL is available, so Step 2 was skipped. The UI tasks use standard PatternFly 5 components (Card, Chart, Table, Toolbar). No custom sub-component specifications were extracted. No display-text-vs-API comparison could be done against mockups. API status/severity values are listed in the frontend task notes instead.

## Step 2.5 — Issue type discovery

`jira.get_project_issue_types(cloudId=2b9e35e3-6bd3-4cec-b838-f4249ee02432, projectKey=TC)` (simulated from the eval statement)

Type-to-role mapping:

```
Feature: Feature (ID: 10142, level: 2)
Epic:    Epic    (level: 1)          # level-1 type named "Epic" is available
Task:    Task    (level: 0)
```

- Epic support is **enabled** because a level-1 type exists. Only one level-1 type was found, and it is named "Epic".
- Hierarchy Configuration: the eval sets the default Epic grouping strategy to **`by-repository`**, so it was applied without prompting.

## Step 3 — Repository analysis summary

### trustify-backend (Rust, Axum, SeaORM)
- Module pattern is `model/ + service/ + endpoints/` (see `modules/fundamental/src/advisory/`, `modules/fundamental/src/sbom/`).
- Data sources for aggregation (no new tables, per the NFR):
  - `entity/src/sbom_advisory.rs` is the SBOM–Advisory join table and represents a vulnerability affecting an SBOM.
  - `entity/src/advisory.rs` with `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` (has a `severity` field).
  - `entity/src/sbom.rs` (SBOM, used as the product dimension).
- Shared helpers:
  - `common/src/db/query.rs` (filtering, pagination, sorting)
  - `common/src/model/paginated.rs::PaginatedResults<T>`
  - `common/src/error.rs::AppError`
- Route mounting: `server/src/main.rs`
- Tests: `tests/api/*.rs`, run against real PostgreSQL
- Docs: `README.md`, `CONVENTIONS.md`
- No `docs/testing-readiness.md` exists, so **no testing tasks** are generated.

### trustify-ui (React 18, TS, PatternFly 5, React Query)
- API layer: `src/api/client.ts`, `src/api/models.ts`, `src/api/rest.ts`. Hooks live in `src/hooks/`.
- Routing is in `src/routes.tsx` (lazy-loaded pages). The page pattern is `src/pages/<Page>/` with a `components/` subdirectory.
- Reusable components:
  - `src/components/SeverityBadge.tsx`
  - `src/components/FilterToolbar.tsx`
  - `src/components/EmptyStateCard.tsx`
  - `src/components/LoadingSpinner.tsx`
  - `src/utils/severityUtils.ts`
- Tests: Vitest + RTL (`*.test.tsx`), MSW (`tests/mocks/handlers.ts`, `tests/mocks/fixtures/`), Playwright (`tests/e2e/`)
- Docs: `README.md`, `CONVENTIONS.md`
- No `docs/testing-readiness.md` exists, so **no testing tasks** are generated.
- The UI has no generated API client for the new endpoints, so manual REST calls are needed. Backend API contracts are recorded in tasks 6–8.

### Shared-artifact producer/consumer analysis — `sbom_advisory` correlation data
Remediation counts are only correct if SBOM–advisory correlation data is accurate (see Customer Considerations).
- **Producers:**
  - `modules/ingestor/src/graph/advisory/mod.rs` creates rows during advisory ingestion and correlation.
  - `modules/ingestor/src/graph/sbom/mod.rs` creates rows during SBOM ingestion and package linking.
  - `modules/ingestor/src/service/mod.rs::IngestorService` is the entry point for on-demand and API-triggered ingestion.
- **Consumers (existing):**
  - `modules/fundamental/src/sbom/service/sbom.rs::SbomService`
  - `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService`
- **Consumer (new):** the `RemediationService` (tasks 2–4).
- **Coverage:** this feature does not change any producer. Producer coverage stays in the existing ingestion tests. The new consumer tests (tasks 2–4) seed the join table through the same ingestion path used by `tests/api/advisory.rs` and `tests/api/sbom.rs`.

### Open questions (need clarification before implementation)
1. **Remediation status source.** The status values Open / In Progress / Resolved must come from existing data, because no new tables are allowed. The fixture does not show a status column on `sbom_advisory`. Task 2 requires the implementer to confirm which column holds this status before writing the aggregation. If no such column exists, the "no new tables" NFR conflicts with the status requirement, and the user must decide how to resolve it.
2. **Product dimension.** There is no `product` entity in the repository. The plan treats the SBOM (its name/product metadata in `entity/src/sbom.rs`) as the product. This needs confirmation.

## Repository Impact Map

```
trustify-backend:
  changes:
    - Add a new `remediation` domain module (model/service/endpoints) that aggregates existing sbom_advisory + advisory + sbom data
    - Add GET /api/v2/remediation/summary — counts grouped by severity (Critical/High/Medium/Low) × status (Open/In Progress/Resolved)
    - Add GET /api/v2/remediation/by-product — paginated per-product breakdown (total, open, resolved)
    - Add GET /api/v2/remediation/vulnerabilities — paginated, filterable (severity, product, status) list of tracked vulnerabilities backing the dashboard table (derived requirement: the MVP "filterable vulnerability table" needs a data source)
    - Mount the remediation routes in server/src/main.rs
    - Add integration tests in tests/api/remediation.rs
    - Document the new endpoints and the dashboard (README.md)

trustify-ui:
  changes:
    - Add TypeScript models, REST functions and React Query hooks for the three remediation endpoints
    - Add the /remediation dashboard page with summary cards (Open / In Progress / Resolved) and a remediation progress chart
    - Add a filterable (severity, product, status), sortable vulnerability table to the dashboard
    - Add MSW handlers/fixtures, unit tests and a Playwright E2E spec for the dashboard
```

### Excluded requirements
| Requirement | Reason / missing input |
|---|---|
| Progress chart "trend over the past 30 days" (part of an MVP requirement) | **Missing input:** there is no historical remediation-status data source. Combined with the "no new database tables" NFR, the backend cannot compute a 30-day time series unless status-change timestamps already exist (Open question 1). The chart is planned as a **current-state** progress chart (status breakdown per severity) built from `/summary`. The time-series trend will be planned once a historical data source is confirmed. |
| Export remediation report as CSV (non-MVP) | **Missing input:** non-MVP, and no CSV column or format specification. Deferred. It can be planned later as a backend `text/csv` variant of `/vulnerabilities` plus a UI export button. |
| Figma-driven visual specification | **Missing input:** no Figma design is linked. UI tasks fall back to PatternFly 5 defaults. |

## Step 4.5 — Workflow mode decision

**Selected mode: `feature-branch`**

Atomicity indicators found:
- **(4) Tightly coupled feature components.** The new `/remediation` UI page (tasks 6–8) calls three new backend endpoints (tasks 2–4) that do not exist yet. If the UI tasks merged to `main` before the backend tasks, `main` would ship a page that fails on every request.
- Indicators 1–3 were not found: there are no schema migrations, existing API contracts are not changed (endpoints are additive only), and there is no cross-cutting refactor.

Interdependent tasks:
- Task 6 depends on Tasks 2, 3, and 4 (API contracts).
- Tasks 7 and 8 depend on Task 6.

The `workflow:feature-branch` label will be added to TC-9006 in Step 6a. The labels after the update will be `["ai-generated-jira", "workflow:feature-branch"]`.

Bookend tasks (Task 1 create-branch, Task 10 merge-branch) target **trustify-backend**, where most implementation tasks land (backend: tasks 2, 3, 4, 5, 9; UI: tasks 6, 7, 8).
**Note for user:** the frontend tasks also target branch `TC-9006` in trustify-ui. The skill requires each bookend to name a single repository, so a `TC-9006` branch must also be created in trustify-ui (and merged at the end). Please confirm whether to handle the UI branch manually or to add UI bookend tasks.

Bookend idempotency guard: TC-9006 has no linked issues ("Linked Issues: None"), so no existing bookends were found and bookends were generated.

## Step 5 — Epic grouping (by-repository)

| Epic group | Summary | Tasks |
|---|---|---|
| trustify-backend | `TC-9006: trustify-backend` | 1, 2, 3, 4, 5, 9, 10 |
| trustify-ui | `TC-9006: trustify-ui` | 6, 7, 8 |

## Task list

| # | File | Summary | Repository | Parent Epic | Target Branch | Depends on |
|---|---|---|---|---|---|---|
| 1 | task-1-create-feature-branch.md | Create feature branch TC-9006 from main | trustify-backend | TC-9006: trustify-backend | main | — |
| 2 | task-2-remediation-summary-endpoint.md | Add remediation module and GET /api/v2/remediation/summary | trustify-backend | TC-9006: trustify-backend | TC-9006 | 1 |
| 3 | task-3-remediation-by-product-endpoint.md | Add GET /api/v2/remediation/by-product | trustify-backend | TC-9006: trustify-backend | TC-9006 | 1, 2 |
| 4 | task-4-remediation-vulnerabilities-endpoint.md | Add GET /api/v2/remediation/vulnerabilities (filterable list) | trustify-backend | TC-9006: trustify-backend | TC-9006 | 1, 2 |
| 5 | task-5-remediation-backend-perf-validation.md | Validate remediation aggregation performance (p95 < 500ms at 10k vulns) | trustify-backend | TC-9006: trustify-backend | TC-9006 | 1, 2, 3, 4 |
| 6 | task-6-remediation-api-client-hooks.md | Add remediation API models, REST functions and hooks | trustify-ui | TC-9006: trustify-ui | TC-9006 | 1, 2, 3, 4 |
| 7 | task-7-remediation-dashboard-page.md | Add /remediation dashboard page with summary cards and progress chart | trustify-ui | TC-9006: trustify-ui | TC-9006 | 1, 6 |
| 8 | task-8-remediation-vulnerability-table.md | Add filterable vulnerability table to remediation dashboard | trustify-ui | TC-9006: trustify-ui | TC-9006 | 1, 6, 7 |
| 9 | task-9-remediation-documentation.md | Document remediation dashboard and aggregation endpoints | trustify-backend | TC-9006: trustify-backend | TC-9006 | 2, 3, 4, 6, 7, 8 |
| 10 | task-10-merge-feature-branch.md | Merge feature branch TC-9006 to main | trustify-backend | TC-9006: trustify-backend | main | 1–9 |

Backend implementation tasks (2–5) are numbered before the frontend tasks that depend on them (6–8).

---

## Step 6 — Jira creation log (simulated; no external calls made)

Simulated keys are shown in angle brackets. Real keys would be assigned by Jira.

### 6a.0 — Epic creation

```
jira.create_issue(
  projectKey="TC",
  issueTypeName="Epic",                # level-1 type discovered in Step 2.5
  summary="TC-9006: trustify-backend",
  description="Backend work for TC-9006: new remediation module providing GET /api/v2/remediation/summary, /by-product and /vulnerabilities aggregation endpoints computed from existing sbom_advisory/advisory/sbom data, performance validation, documentation, plus the feature-branch bookend tasks.",
  parent="TC-9006",
  additional_fields={
    "labels": ["ai-generated-jira"],
    "priority": {"name": "Major"},
    "fixVersions": [{"name": "RHTPA 1.5.0"}]
  }
)  -> <EPIC-BE>

jira.create_issue(
  projectKey="TC",
  issueTypeName="Epic",
  summary="TC-9006: trustify-ui",
  description="Frontend work for TC-9006: remediation API client and hooks, /remediation dashboard page with summary cards and progress chart, and filterable vulnerability table.",
  parent="TC-9006",
  additional_fields={
    "labels": ["ai-generated-jira"],
    "priority": {"name": "Major"},
    "fixVersions": [{"name": "RHTPA 1.5.0"}]
  }
)  -> <EPIC-UI>
```

Epic mapping: `trustify-backend → <EPIC-BE>`, `trustify-ui → <EPIC-UI>`

### 6a — Task creation

Every task is created with `issueTypeName="Task"` and `projectKey="TC"`, and uses these `additional_fields`:

```
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Major"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

| # | Summary | parent | Simulated key |
|---|---|---|---|
| 1 | Create feature branch TC-9006 from main | <EPIC-BE> | <T1> |
| 2 | Add remediation module and GET /api/v2/remediation/summary | <EPIC-BE> | <T2> |
| 3 | Add GET /api/v2/remediation/by-product | <EPIC-BE> | <T3> |
| 4 | Add GET /api/v2/remediation/vulnerabilities | <EPIC-BE> | <T4> |
| 5 | Validate remediation aggregation performance | <EPIC-BE> | <T5> |
| 6 | Add remediation API models, REST functions and hooks | <EPIC-UI> | <T6> |
| 7 | Add /remediation dashboard page with summary cards and progress chart | <EPIC-UI> | <T7> |
| 8 | Add filterable vulnerability table to remediation dashboard | <EPIC-UI> | <T8> |
| 9 | Document remediation dashboard and aggregation endpoints | <EPIC-BE> | <T9> |
| 10 | Merge feature branch TC-9006 to main | <EPIC-BE> | <T10> |

Each task creation is immediately followed by `jira.get_issue(<Tn>)`, then `python3 scripts/sha256-digest.py`, and then a standalone digest comment (see `task-N-digest.md`).

Feature label update (feature-branch mode):

```
jira.edit_issue("TC-9006", fields={"labels": ["ai-generated-jira", "workflow:feature-branch"]})
```

### 6b — Issue links

**Incorporates links go from the Feature to the Epics only, not to individual tasks:**

```
jira.create_issue_link(link_type="Incorporates", inward_issue_key="TC-9006", outward_issue_key=<EPIC-BE>)
jira.create_issue_link(link_type="Incorporates", inward_issue_key="TC-9006", outward_issue_key=<EPIC-UI>)
```

**Depend links** use the form `inward = dependent task`, `outward = dependency`:

| Dependent | Depends on |
|---|---|
| T2 | T1 |
| T3 | T1, T2 |
| T4 | T1, T2 |
| T5 | T1, T2, T3, T4 |
| T6 | T1, T2, T3, T4 |
| T7 | T1, T6 |
| T8 | T1, T6, T7 |
| T9 | T2, T3, T4, T6, T7, T8 |
| T10 | T1, T2, T3, T4, T5, T6, T7, T8, T9 |

### 6c — Feature summary comment

See `summary-comment.md`. The impact map comment (Step 4) and the workflow mode comment (Step 4.5) are in `impact-map-comment.md` and `workflow-mode-comment.md`.
