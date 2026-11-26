# Repository Impact Map — TC-9001: Add advisory severity aggregation endpoint

## Feature summary (from Step 1)

| Field | Value |
|---|---|
| Key | TC-9001 |
| Title | Add advisory severity aggregation endpoint |
| Priority | Major (set, propagated to tasks) |
| Fix Versions | RHTPA 1.5.0 (set, propagated to tasks; `fixVersion scope: both`) |
| Figma | None (no Figma link in the feature and none provided as an argument, so Step 2 was skipped) |
| Parent link (Step 1.5) | None set. Offline eval, so the interactive prompt was skipped |
| Documentation signals | Doc impact = **Updates** (add endpoint to the REST API reference). Reference material: existing SBOM advisory endpoint docs |
| Testing readiness template | Found at `docs/testing-readiness.md`. Categories: **Smoke Tests**, **Performance Benchmarks** |
| CONVENTIONS.md | Present at the repo root. Conventions applied: Module pattern, Error handling, Endpoint registration, Response types, Query helpers, Testing, Caching |

## Impact map

```
trustify-backend:
  changes:
    - Add AdvisorySeveritySummary response model { critical, high, medium, low, total } under the SBOM module
    - Add an SbomService aggregation that counts unique advisories (deduplicated by advisory ID) per severity for an SBOM, using the existing sbom_advisory join table (no new tables)
    - Add GET /api/v2/sbom/{id}/advisory-summary endpoint, registered in the SBOM endpoints router
    - Return 404 for unknown SBOM IDs, consistent with GET /api/v2/sbom/{id}
    - Cache advisory-summary responses for 5 minutes per SBOM ID using the existing tower-http cache configuration, and expose per-SBOM invalidation
    - Invalidate cached summaries from every ingestion path that links advisories to SBOMs (advisory correlation, plus SBOM ingestion if it correlates)
    - (Non-MVP) Support an optional ?threshold=<severity> query parameter returning only counts at or above the threshold
    - Add integration tests in tests/api/sbom.rs
    - Update the REST API reference documentation for the new endpoint
    - Run feature-level Smoke Tests and Performance Benchmarks from docs/testing-readiness.md
```

## Shared-artifact producer/consumer analysis (Step 3)

Artifact: **cached per-SBOM advisory severity summary**, derived from the `sbom_advisory` join table (`entity/src/sbom_advisory.rs`).

| Role | Path | Covered by |
|---|---|---|
| Consumer / cache populator | `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` (new) | Task 2 (tests in `tests/api/sbom.rs`) |
| Computation | `modules/fundamental/src/sbom/service/sbom.rs` | Task 1 |
| Writer: advisory ingestion (primary: parse, store, correlate) | `modules/ingestor/src/graph/advisory/mod.rs` | Task 3 |
| Writer: SBOM ingestion (parse, store, link). Writes `sbom_advisory` if it correlates new SBOMs against existing advisories | `modules/ingestor/src/graph/sbom/mod.rs` | Task 3 (implementer must confirm with grep) |
| Orchestration / on-demand ingest path | `modules/ingestor/src/service/mod.rs` (`IngestorService`) | Task 3 |

Coverage gap note: no Serena instance or source checkout was available, so only the repository structure was inspected and the full set of `sbom_advisory` writers could not be confirmed from code. Task 3 requires a `grep -rn "sbom_advisory"` sweep, and any extra writer (for example an unlink or delete path) must be added to the task. No scope exclusion conflicts with this criterion.

## Discrepancies / open questions

1. **Cache invalidation vs `tower-http` caching.** The repo's caching is `tower-http` middleware configured in route builders. If it is purely HTTP `Cache-Control` header caching, the server cannot invalidate it from the ingestion pipeline, so the NFR "advisory ingestion pipeline must invalidate cached summaries" cannot be met using "existing cache infrastructure" alone. Task 2 must check this first and escalate on TC-9001 if the cache is header-only.
2. **`GET /api/v2/sbom/{id}/advisories`.** The feature says this endpoint exists today, but it does not appear in `modules/fundamental/src/sbom/endpoints/` (only `list.rs` and `get.rs`). Task 1 asks the implementer to locate its query and reuse it.
3. **Threshold semantics (non-MVP).** "Filter counts above a severity" vs UC-2's "only critical count is returned". The plan reads this as *at or above* the threshold, with lower buckets omitted. This needs stakeholder confirmation.
4. **Severity values outside the four buckets.** These count toward `total` only. Confirm on TC-9001.

## Excluded requirements

| Requirement | Reason excluded (missing input) |
|---|---|
| Add the new endpoint to the API latency Grafana dashboard (Customer Information/Supportability) | No observability/dashboards repository is in the Repository Registry, and the backend repo structure has no Grafana dashboard definitions. Needs the target repository for dashboard configuration. |
| Alert if p95 exceeds 500ms (Customer Information/Supportability) | Same reason: no alerting/monitoring configuration repository is available. Needs the target repository for alert rules. (The 500ms threshold is still checked in Task 7's benchmarks.) |
| Eliminate client-side counting logic from the dashboard (Goal) / dashboard widget rendering the severity bar chart (UC-1 step 3) | No frontend repository is in the Repository Registry and no Figma design was provided. Needs the frontend repo (and design, if the widget changes) to plan the consumer-side change. |

## Workflow mode (Step 4.5)

**Selected mode: `direct-to-main`**

Rationale. None of the atomicity indicators apply:
1. Coordinated schema migrations: none. No new tables or migrations; the existing `sbom_advisory` table is reused.
2. Breaking API changes: none. The endpoint is new and additive. The `threshold` param is optional and backward compatible.
3. Cross-cutting refactors: none. No renames or shared type changes.
4. Tightly coupled frontend/backend components: none in scope. Only the backend is planned, and the endpoint is usable on its own.

Each task merges to `main` without breaking it. Task 1 adds an unused service method, Task 2 exposes it, Task 3 adds invalidation, and Task 4 adds an optional parameter. Ordering is handled through task dependencies. No bookend tasks are generated, and every task targets `main`.

## Issue type discovery and hierarchy (Steps 2.5, 5, 6a.0)

Jira could not be queried (offline eval), so `get_project_issue_types` was not called. Configured values: Feature type ID 10142; `Default epic grouping strategy: by-sub-feature` (from Hierarchy Configuration).

- **If a level-1 (Epic) type is discovered**, these are the proposed by-sub-feature Epics (Epics get `parent = TC-9001`, labels `ai-generated-jira`, priority Major, fixVersions RHTPA 1.5.0; Feature "Incorporates" each Epic):
  - `TC-9001: Advisory summary endpoint (MVP)`: Tasks 1, 2, 3
  - `TC-9001: Severity threshold filter`: Task 4
  - `TC-9001: Documentation and validation`: Tasks 5, 6, 7
- **If no level-1 type exists** (graceful degradation): tasks are created directly under the Feature, and the Feature "Incorporates" each Task.

## Task list

| # | Title | Type | Depends on |
|---|---|---|---|
| 1 | Add advisory severity summary model and SbomService aggregation query | Implementation | — |
| 2 | Add GET /api/v2/sbom/{id}/advisory-summary endpoint with 404 handling and 5-minute caching | Implementation | 1 |
| 3 | Invalidate cached SBOM advisory summaries from the ingestion pipeline | Implementation | 2 |
| 4 | Add optional ?threshold= severity filter (non-MVP) | Implementation | 2 |
| 5 | Document GET /api/v2/sbom/{id}/advisory-summary in the REST API reference | Documentation | 1, 2, 3, 4 |
| 6 | Smoke Tests | Testing | 1, 2, 3, 4 |
| 7 | Performance Benchmarks | Testing | 1, 2, 3, 4 |

## `additional_fields` for every created issue (Step 6a)

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Major"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

- `priority`: included. The Feature priority is "Major", which is not "Undefined".
- `fixVersions`: included. The Feature has `RHTPA 1.5.0` and CLAUDE.md `fixVersion scope` = `both`.
- Applies to all 7 tasks (and to Epics, if created).

---
This comment was AI-generated by [sdlc-workflow/plan-feature](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.14.0.
