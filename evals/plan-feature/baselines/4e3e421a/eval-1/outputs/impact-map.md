# Repository Impact Map — TC-9001: Add advisory severity aggregation endpoint

```
trustify-backend:
  changes:
    - Add AdvisorySeveritySummary model (critical, high, medium, low, total) to the SBOM module
    - Add SbomService aggregation that counts unique advisories per severity for an SBOM over the existing sbom_advisory join table (no new tables)
    - Add GET /api/v2/sbom/{id}/advisory-summary endpoint returning the summary, 404 for unknown SBOM
    - Cache the endpoint response for 5 minutes using the existing tower-http caching configuration
    - Invalidate the cached summary whenever advisory links for an SBOM are written (advisory correlation; SBOM ingestion if it writes links)
    - (Non-MVP) Add optional ?threshold=<severity> query parameter to filter counts
    - Add integration tests in tests/api/sbom.rs and tests/api/advisory.rs
    - Update REST API reference documentation for the new endpoint
    - Feature-level smoke tests and performance benchmarks per docs/testing-readiness.md
```

## Shared-artifact producer/consumer analysis

Artifact: the cached advisory severity summary per SBOM, which is derived from `entity/src/sbom_advisory.rs` rows and `entity/src/advisory.rs` severity.

| Role | Path | Coverage |
|---|---|---|
| Producer: populates the cache on a read miss | `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` (new), `modules/fundamental/src/sbom/endpoints/mod.rs` | Task 2, tests in `tests/api/sbom.rs` |
| Writer of the source data: advisory correlation | `modules/ingestor/src/graph/advisory/mod.rs` | Task 3 (invalidation), test in `tests/api/advisory.rs` |
| Writer of the source data: SBOM ingestion and re-ingestion (needs verification) | `modules/ingestor/src/graph/sbom/mod.rs` | Task 3. The implementer must confirm whether this path writes `sbom_advisory` rows, and add invalidation and a test if it does |
| Orchestration | `modules/ingestor/src/service/mod.rs` (`IngestorService`) | Task 3 |
| Consumer | Frontend dashboard widget (UC-1), external alerting integration (UC-2) | Not in a registered repository; see Excluded requirements |

No manual, on-demand, or recovery writers of `sbom_advisory` appear in the repository structure. Task 3 requires a workspace-wide grep for every write to `sbom_advisory`, and any additional writer it finds must be added before the cache-invalidation criterion counts as covered.

## Open questions / risks

1. **Cache invalidation vs. header-only caching.** The repository's caching uses `tower-http` middleware configured in route builders. If that configuration only emits HTTP `Cache-Control` headers, which means client- or proxy-side caching, the server cannot invalidate cached entries, and the NFR "ingestion must invalidate cached summaries" cannot be met. Task 2 must confirm that a server-side, invalidatable cache exists and escalate if it does not.
2. **Threshold semantics.** The requirement says "filter counts above a severity". UC-2, however, expects `threshold=critical` to return the critical count, which means "at or above". Task 4 must confirm the intended meaning with the feature owner.
3. **Null or unknown severities.** The feature does not say how to handle advisories without a recognized severity. Task 1 requires counting them in `total` and not in any named bucket, so that totals are never silently understated.

## Excluded requirements

| Requirement | Reason it cannot be planned |
|---|---|
| Add the new endpoint to the API latency Grafana dashboard (Customer Information/Supportability) | No monitoring or dashboard repository is listed in the Repository Registry, and `trustify-backend` contains no Grafana dashboard definitions. Missing input: the repository or location where Grafana dashboards are managed. |
| Alert if p95 exceeds 500ms (Customer Information/Supportability) | No alerting or monitoring configuration repository is in the Repository Registry. Missing input: the repository or location of the alerting rules. Task 7 measures latency against the threshold but does not create the alert. |
| Eliminate client-side counting logic from the dashboard (Goal) | The frontend dashboard repository is not in the Repository Registry for this plan. Missing input: the frontend repository and its Serena instance, so that a frontend task can be planned against the new endpoint. |

## Workflow mode decision

**Mode: `direct-to-main`**

Rationale: none of the atomicity indicators apply.
- No coordinated schema migrations, because the feature adds no new tables or migrations.
- No breaking API changes, because the endpoint is new and existing endpoints are unchanged. Task 4 adds an optional parameter that is backward compatible.
- No cross-cutting refactor, because all changes are additive.
- No tightly coupled frontend and backend components, because only the backend is planned and the endpoint works on its own.

Each task's PR leaves `main` in a working state. Task 2 adds the endpoint with caching; Task 3 then adds invalidation. Until Task 3 merges, summaries can be up to 5 minutes stale, but nothing breaks, and an unreleased endpoint has no existing consumers. All tasks target `main`, and no bookend tasks are generated.

## Hierarchy (Step 2.5)

The Jira project's issue types could not be discovered in this offline eval, because the Jira MCP is not available. Following the graceful-degradation rule: "No Epic-level type found in project — tasks will be created directly under the Feature." Feature → Task hierarchy is used. CLAUDE.md sets `Default epic grouping strategy: by-sub-feature`. If a level-1 type had been discovered, the suggested Epics would have been:
- `TC-9001: Severity summary endpoint`: Tasks 1, 2, 4
- `TC-9001: Cache invalidation`: Task 3
- `TC-9001: Docs and validation`: Tasks 5, 6, 7

Step 1.5 (parent link): the Feature has no parent set. In this non-interactive run the prompt was skipped, so no parent link was created.

## Task creation log (Step 6)

Inherited fields from TC-9001: priority `Major` (set, so propagated); fixVersions `RHTPA 1.5.0` (set, and `fixVersion scope: both`, so propagated).

`additional_fields` applied to every created task:

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Major"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

| # | File | Summary | Issue type | Parent | additional_fields |
|---|---|---|---|---|---|
| 1 | task-1-advisory-severity-summary-service.md | Add advisory severity summary model and service aggregation | Task | — (no Epic) | as above |
| 2 | task-2-advisory-summary-endpoint.md | Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching | Task | — | as above |
| 3 | task-3-cache-invalidation-on-ingestion.md | Invalidate cached advisory summaries on advisory ingestion | Task | — | as above |
| 4 | task-4-threshold-query-param.md | Add optional threshold query parameter to advisory-summary endpoint (non-MVP) | Task | — | as above |
| 5 | task-5-documentation.md | Document advisory-summary endpoint in REST API reference | Task | — | as above |
| 6 | task-6-smoke-tests.md | Smoke tests for advisory severity aggregation (TC-9001) | Task | — | as above |
| 7 | task-7-performance-benchmarks.md | Performance benchmarks for advisory severity aggregation (TC-9001) | Task | — | as above |

### Issue links (Step 6b)

Incorporates (Feature → Task, because there are no Epics): TC-9001 → Tasks 1, 2, 3, 4, 5, 6, 7

Depend (dependent → dependency):
- Task 2 → Task 1
- Task 3 → Task 2
- Task 4 → Task 2
- Task 5 → Task 2, Task 3, Task 4
- Task 6 → Task 1, Task 2, Task 3, Task 4
- Task 7 → Task 1, Task 2, Task 3, Task 4

### Description digests

A digest comment was written for each task as `task-N-digest.md`. In this offline run each digest was computed with `scripts/sha256-digest.py` over the local markdown description, because no Jira re-fetch was possible. A live run hashes the description as re-fetched from Jira.

---
This comment was AI-generated by [sdlc-workflow/plan-feature](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.10.
