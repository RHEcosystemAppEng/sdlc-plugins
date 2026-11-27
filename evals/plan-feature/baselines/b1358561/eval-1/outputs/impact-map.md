# Repository Impact Map — TC-9001: Add advisory severity aggregation endpoint

## Run Context and Documented Choices

This run was executed offline (eval mode). No Jira, Figma, or Serena calls were made; all
outputs that would have gone to Jira are written as files in this directory.

| Step | Decision / Assumption |
|---|---|
| Step 0 — Project Configuration | CLAUDE.md has Repository Registry, Jira Configuration (Project key TC, Cloud ID, Feature issue type ID 10142) and Code Intelligence. Validation passed. |
| Step 1 — Fetch issue | Feature read from `feature-standard.md`. Priority: **Major**. fixVersions: **RHTPA 1.5.0**. |
| Step 1 — Documentation signals | "Documentation Considerations" present. Doc impact type: **Updates** — add endpoint to REST API reference. User purpose: API consumers need endpoint path, parameters, response shape. Reference material: existing SBOM advisory endpoints documentation. |
| Step 1.5 — Parent link | Feature has no parent. Prompt skipped (non-interactive) — no parent link set. |
| Step 2 — Figma | No Figma URL in arguments or description. Step skipped (backend-only feature). |
| Step 2.5 — Issue types | Could not call `get_project_issue_types`. Assumed the TC project exposes the standard hierarchy: Feature (ID 10142, level 2), **Epic** (level 1), Task (level 0). Epic creation therefore enabled. If discovery at run time finds no level-1 type, tasks would be created directly under the Feature with Feature → Task "Incorporates" links. |
| Step 2.5 — Hierarchy Configuration | CLAUDE.md `Default epic grouping strategy: by-sub-feature` → used without prompting. Suggested sub-feature groupings were auto-approved (non-interactive). |
| Step 3 — Repository analysis | Target repo `trustify-backend` analyzed from `repo-backend.md` (no Serena instance; directory tree used as Glob/Read evidence). |
| Step 3 — CONVENTIONS.md | `CONVENTIONS.md` exists at repo root. Its content was not provided separately; the "Key Conventions" section of the repo description is used as its content (sections: Framework, Module pattern, Error handling, Endpoint registration, Response types, Query helpers, Testing, Caching). |
| Step 3 — Testing readiness template | `docs/testing-readiness.md` found. Categories: **Smoke Tests**, **Performance Benchmarks** → one testing task per category. |
| Step 3 — Documentation files | `README.md`, `CONVENTIONS.md`. No `docs/api/` or OpenAPI spec file appears in the tree. |
| Step 3 — Eval infrastructure | Not applicable — no task modifies a skill `SKILL.md`. |
| Step 4 — Map approval | Auto-approved (non-interactive). |
| Prompt for priority / fixVersion (Jira Field Defaults) | No prompt possible; Feature values inherited as-is (Major / RHTPA 1.5.0). |

## Repository Analysis Findings

- **SBOM module** (`modules/fundamental/src/sbom/`): follows `model/ + service/ + endpoints/`.
  Routes registered in `endpoints/mod.rs` (`/api/v2/sbom`); `get.rs` implements
  `GET /api/v2/sbom/{id}` (the 404 behavior to mirror). `SbomService` in `service/sbom.rs`.
- **Advisory module** (`modules/fundamental/src/advisory/`): `AdvisorySummary`
  (`model/summary.rs`) carries the `severity` field; `AdvisoryService` (`service/advisory.rs`)
  provides fetch/list/search.
- **Entities**: `entity/src/sbom_advisory.rs` (SBOM–Advisory join table), `entity/src/advisory.rs`,
  `entity/src/sbom.rs`. Satisfies the "no new tables" NFR — aggregation is a `GROUP BY severity`
  over `sbom_advisory` joined to `advisory` with `COUNT(DISTINCT advisory.id)`.
- **Shared helpers**: `common/src/db/query.rs` (filtering helpers), `common/src/error.rs`
  (`AppError`, implements `IntoResponse`).
- **Caching**: `tower-http` caching middleware configured in endpoint route builders.
- **Server**: `server/src/main.rs` mounts module routers (no change expected — the new route is
  registered inside the existing SBOM router).
- **Tests**: `tests/api/sbom.rs` (SBOM endpoint integration tests, real PostgreSQL).
- **Discrepancy noted**: the Feature references an existing `GET /api/v2/sbom/{id}/advisories`
  endpoint, but no corresponding handler file appears under `sbom/endpoints/` (only `list.rs`,
  `get.rs`). The implementer must locate its actual handler (possibly inside `endpoints/mod.rs` or
  the advisory module) and reuse its SBOM→advisory join logic rather than duplicating it.

### Shared-artifact producer / consumer analysis — cached advisory summary

The cached per-SBOM severity summary is a shared artifact whose correctness depends on the
`sbom_advisory` relationship.

| Role | Path | Evidence | Coverage |
|---|---|---|---|
| Producer (cache populate) | `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` (new) via `SbomService` | Requirement: cached 5 min | Task 2 tests |
| Writer of underlying data — primary | `modules/ingestor/src/graph/advisory/mod.rs` (advisory ingestion: parse, store, **correlate**) | Creates `sbom_advisory` links | Task 3 invalidation + test |
| Writer of underlying data — alternate | `modules/ingestor/src/graph/sbom/mod.rs` (SBOM ingestion / re-ingestion: parse, store, link packages) | Re-ingesting an SBOM can change which advisories correlate to it | Task 3 invalidation + test |
| Orchestration / on-demand ingest | `modules/ingestor/src/service/mod.rs` (`IngestorService`) | Entry point for both ingestion paths (incl. API-triggered upload) | Task 3 — invalidation hook wired here |
| Consumer | `GET /api/v2/sbom/{id}/advisory-summary` (dashboard widget, alerting integrations) | UC-1, UC-2 | Tasks 2, 4, 6, 7 |

No stakeholder scope exclusion conflicts with these paths; all are included in task scope.

## Impact Map

```
trustify-backend:
  changes:
    - Add an AdvisorySeveritySummary response model ({ critical, high, medium, low, total })
    - Add a service method that aggregates unique advisory counts by severity for an SBOM using the existing sbom_advisory join table, returning not-found for unknown SBOM IDs
    - Add GET /api/v2/sbom/{id}/advisory-summary endpoint registered in the SBOM router, returning 404 for unknown SBOMs
    - Cache advisory-summary responses for 5 minutes using the existing tower-http caching infrastructure
    - Invalidate cached advisory summaries when advisory ingestion (correlation) or SBOM (re-)ingestion links advisories to an SBOM
    - Add optional ?threshold=<severity> query parameter that filters counts to severities at or above the threshold (non-MVP)
    - Integration tests for the new endpoint, 404 path, deduplication, caching, invalidation and threshold filter
    - Update REST API reference documentation with the new endpoint
    - Smoke-test and performance-benchmark validation per docs/testing-readiness.md
```

## Excluded Requirements

| Requirement | Missing input preventing planning |
|---|---|
| "Add the new endpoint to the API latency Grafana dashboard" (Customer Information/Supportability) | No observability/dashboards repository in the Repository Registry; Grafana dashboard definitions are not part of `trustify-backend`. Provide the dashboard repo (or owning team) to plan this. |
| "Alert if p95 exceeds 500ms" (Customer Information/Supportability) | No alerting-rules repository (e.g., Prometheus rules) in the Repository Registry. Provide the target repo to plan this. |

Note: the non-MVP `?threshold` requirement **is** planned (Task 4) because it is sufficiently
specified. Ambiguity documented in Task 4: the use case says "Only critical count is returned"
— interpreted as "severities below the threshold are reported as 0 and `total` reflects only
the included severities", keeping the response shape stable.

## Workflow Mode Decision (Step 4.5)

**Mode: `direct-to-main`**

Atomicity indicators evaluated:

1. Coordinated schema migrations — **none** (NFR forbids new tables; no migration).
2. Breaking API changes — **none** (purely additive endpoint; no existing contract modified).
3. Cross-cutting refactors — **none**.
4. Tightly coupled feature components — **none**. Single repository; each task leaves `main`
   working: the service method (Task 1) is unused-but-valid until Task 2; cache invalidation
   (Task 3) is additive; the threshold param (Task 4) is additive.

No bookend tasks are generated. All tasks use Target Branch `main`. The
`workflow:feature-branch` label is NOT applied.

## Epic Grouping (strategy: by-sub-feature)

| Epic | Summary | Tasks |
|---|---|---|
| Epic A | TC-9001: Advisory severity summary endpoint | Task 1, Task 2, Task 4 |
| Epic B | TC-9001: Advisory summary cache invalidation | Task 3 |
| Epic C | TC-9001: Documentation and feature validation | Task 5, Task 6, Task 7 |

Epic descriptions are in `epic-a.md`, `epic-b.md`, `epic-c.md`.

## Task List

| # | File | Summary | Epic | Depends on |
|---|---|---|---|---|
| 1 | task-1-advisory-summary-model-service.md | Add advisory severity aggregation model and service method | A | — |
| 2 | task-2-advisory-summary-endpoint.md | Add GET /api/v2/sbom/{id}/advisory-summary endpoint with 5-minute caching | A | Task 1 |
| 3 | task-3-cache-invalidation.md | Invalidate cached advisory summaries on advisory/SBOM ingestion | B | Task 2 |
| 4 | task-4-threshold-filter.md | Support optional ?threshold query parameter on advisory-summary (non-MVP) | A | Task 2 |
| 5 | task-5-api-docs.md | Document advisory-summary endpoint in REST API reference | C | Tasks 1–4 |
| 6 | task-6-smoke-tests.md | Smoke tests for advisory severity aggregation | C | Tasks 1–4 |
| 7 | task-7-performance-benchmarks.md | Performance benchmarks for advisory severity aggregation | C | Tasks 1–4 |

## Task Creation Log — `additional_fields` (Step 6a / 6a.0)

Inherited values: priority **Major** (set on Feature, not "Undefined" → propagated);
fixVersions **RHTPA 1.5.0** (Feature non-empty, `fixVersion scope: both` → propagated).

Applied identically to all 3 Epics and all 7 Tasks:

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Major"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

| Issue | Type | parent | Summary |
|---|---|---|---|
| Epic A | Epic | TC-9001 | TC-9001: Advisory severity summary endpoint |
| Epic B | Epic | TC-9001 | TC-9001: Advisory summary cache invalidation |
| Epic C | Epic | TC-9001 | TC-9001: Documentation and feature validation |
| Task 1 | Task | Epic A | Add advisory severity aggregation model and service method |
| Task 2 | Task | Epic A | Add GET /api/v2/sbom/{id}/advisory-summary endpoint with 5-minute caching |
| Task 3 | Task | Epic B | Invalidate cached advisory summaries on advisory and SBOM ingestion |
| Task 4 | Task | Epic A | Support optional ?threshold query parameter on advisory-summary |
| Task 5 | Task | Epic C | Document advisory-summary endpoint in REST API reference |
| Task 6 | Task | Epic C | Smoke tests for advisory severity aggregation |
| Task 7 | Task | Epic C | Performance benchmarks for advisory severity aggregation |

After each task is created, a description digest comment is posted (`task-N-digest.md`).

### Issue links (Step 6b)

Incorporates (Feature → Epic, since Epics are available):
- TC-9001 incorporates Epic A, Epic B, Epic C

Depend (dependent → dependency):
- Task 2 → Task 1
- Task 3 → Task 2
- Task 4 → Task 2
- Task 5 → Task 1, Task 2, Task 3, Task 4
- Task 6 → Task 1, Task 2, Task 3, Task 4
- Task 7 → Task 1, Task 2, Task 3, Task 4
