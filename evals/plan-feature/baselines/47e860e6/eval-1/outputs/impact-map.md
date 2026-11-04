# Repository Impact Map — TC-9001: Add advisory severity aggregation endpoint

> This is the content of the Jira comment posted on TC-9001 after the user approved the map (Step 4), with the workflow mode decision (Step 4.5) appended.

## Feature summary

- **Feature**: TC-9001 — Add advisory severity aggregation endpoint
- **Priority**: Major (inherited by all tasks)
- **Fix Versions**: RHTPA 1.5.0 (inherited by all tasks; `fixVersion scope: both`)
- **Doc signals**: Doc Impact = **Updates** — add endpoint to REST API reference
- **Testing readiness template**: found at `docs/testing-readiness.md` in trustify-backend — categories: **Smoke Tests**, **Performance Benchmarks**
- **Figma**: none linked — no UI analysis performed (backend-only feature)

## Repository Impact Map

```
trustify-backend:
  changes:
    - Add an AdvisorySeveritySummary response model { critical, high, medium, low, total }
    - Add a service method that counts unique advisories (deduplicated by advisory ID) per severity for an SBOM, using the existing sbom_advisory join table (no new tables / migrations)
    - Add GET /api/v2/sbom/{id}/advisory-summary endpoint, returning 404 for an unknown SBOM ID
    - Cache the advisory-summary response for 5 minutes using the existing caching infrastructure
    - Invalidate cached summaries for an SBOM when the advisory ingestion pipeline links new advisories to it
    - (Non-MVP) Support optional ?threshold=<severity> query parameter to restrict counts to severities at/above the threshold
    - Update the REST API reference documentation with the new endpoint
    - Validate the feature against the repository's testing readiness template (Smoke Tests, Performance Benchmarks)
```

## Analysis basis

Analysis performed via Glob/Read fallback (no Serena instance configured for this repository — see CLAUDE.md Code Intelligence).

Relevant code locations discovered:

| Area | Path | Relevance |
|---|---|---|
| SBOM routes | `modules/fundamental/src/sbom/endpoints/mod.rs` | Route registration for `/api/v2/sbom`; new route + cache layer goes here |
| SBOM get handler | `modules/fundamental/src/sbom/endpoints/get.rs` | Existing `GET /api/v2/sbom/{id}` — 404 pattern to mirror |
| SBOM service | `modules/fundamental/src/sbom/service/sbom.rs` | `SbomService` — host for the aggregation method |
| SBOM models | `modules/fundamental/src/sbom/model/mod.rs`, `summary.rs`, `details.rs` | Model module pattern |
| Advisory model | `modules/fundamental/src/advisory/model/summary.rs` | `AdvisorySummary` — includes the `severity` field (source of severity values) |
| Advisory service | `modules/fundamental/src/advisory/service/advisory.rs` | `AdvisoryService` — existing advisory fetch/list/search queries (reuse candidate for SBOM→advisory join logic) |
| Join entity | `entity/src/sbom_advisory.rs` | SBOM–Advisory join table (data source; satisfies "no new tables") |
| Entities | `entity/src/sbom.rs`, `entity/src/advisory.rs` | SBOM existence check; advisory severity column |
| Query helpers | `common/src/db/query.rs` | Shared filtering helpers |
| Errors | `common/src/error.rs` | `AppError` (NotFound → 404) |
| Advisory ingestion | `modules/ingestor/src/graph/advisory/mod.rs` | Parses, stores, **correlates** advisories to SBOMs → writes `sbom_advisory`; invalidation hook point |
| Ingestor service | `modules/ingestor/src/service/mod.rs` | `IngestorService` orchestration |
| Server | `server/src/main.rs` | Mounts module routes (sbom module already mounted — no change expected) |
| Tests | `tests/api/sbom.rs`, `tests/api/advisory.rs` | Integration test location/pattern (`assert_eq!(resp.status(), StatusCode::OK)`) |
| Docs | `README.md`, `CONVENTIONS.md`, `docs/testing-readiness.md` | Documentation discovery |

**CONVENTIONS.md**: listed at the repository root, but its contents were not available to this planning run. The repository's documented Key Conventions (Axum + SeaORM, `model/ + service/ + endpoints/` module pattern, `Result<T, AppError>` with `.context()`, per-module route registration, `tower-http` caching configured in route builders, integration tests in `tests/api/`) were used for convention enrichment. Implementers should re-check `CONVENTIONS.md` at implementation time.

## Shared-artifact producer/consumer analysis

The cached advisory summary is a shared artifact derived from `sbom_advisory` + `advisory.severity`.

| Role | Path | Covered by |
|---|---|---|
| Producer (cache populate) | `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` (new) | Task 2 |
| Writer of source data (correlation → `sbom_advisory`) | `modules/ingestor/src/graph/advisory/mod.rs` | Task 3 (invalidation) |
| Writer of source data (SBOM ingestion) | `modules/ingestor/src/graph/sbom/mod.rs` | **Unresolved — see below** |
| Consumer | Dashboard widget / alerting integrations via `GET /api/v2/sbom/{id}/advisory-summary` | Tasks 2, 4 |

**Unresolved path — needs user confirmation:** `modules/ingestor/src/graph/sbom/mod.rs` is documented as "parse, store, link packages" — there is no repository evidence that it writes `sbom_advisory` rows, so it is not included in task Files to Modify. However, if SBOM re-ingestion (or any advisory update/re-score or deletion path) changes correlations or severities for an existing SBOM ID, the cached summary would be stale for up to 5 minutes. The NFR names only the advisory ingestion pipeline. **Please confirm whether SBOM re-ingestion and advisory severity updates must also invalidate the cache**; until confirmed, the "cache invalidated when advisories are linked" criterion is covered only for the advisory-correlation path.

**Caching mechanism caveat:** the repo's caching is `tower-http` middleware configured in route builders. If that amounts to HTTP `Cache-Control` headers, server-side invalidation cannot evict client/proxy copies. Task 2 therefore requires a server-side, SBOM-ID-keyed cache entry (TTL 5 min) that Task 3 can evict; any HTTP cache headers must not exceed this behaviour silently.

## Excluded requirements

| Requirement | Reason excluded / missing input |
|---|---|
| Add the new endpoint to the API latency Grafana dashboard | No monitoring/dashboard repository in the Repository Registry; Grafana dashboard definitions are not in trustify-backend. Provide the dashboard repo/location to plan this. |
| Alert if p95 exceeds 500ms | Same — alerting rules live outside the registered repository. Provide the alerting config location to plan this. |

## Open questions (do not block planning)

1. **Threshold semantics** (non-MVP): requirement says "filter counts above a severity", UC-2 says "only critical count is returned" for `threshold=critical`. Task 4 plans "at or above threshold, other levels omitted/zeroed" — confirm inclusive semantics and response shape.
2. **Advisories with no/unknown severity**: should they be counted in `total`? Task 1 plans `total` = number of unique advisories with a recognised severity (= critical+high+medium+low) and requires the choice to be documented and tested; confirm.

---

## Workflow Mode Decision

**Selected mode: `direct-to-main`**

Atomicity indicators evaluated:

1. Coordinated schema migrations — **none** (NFR: no new tables; no migration).
2. Breaking API changes — **none** (new endpoint is purely additive; no existing contract changes).
3. Cross-cutting refactors — **none**.
4. Tightly coupled feature components — **none** (single backend repository; no frontend task in scope).

Each task merges independently without breaking `main`: Task 1 adds unused service/model code; Task 2 exposes the endpoint; Task 3 adds invalidation (before it lands, summaries are at most 5 minutes stale, which is the cache TTL); Task 4 is an additive optional parameter. All tasks target `main`; no bookend tasks generated.

## Hierarchy

Epic-level (level-1) issue type: not discovered in this run (no Jira access; Step 2.5 treated as "no level-1 type"). Message: "No Epic-level type found in project — tasks will be created directly under the Feature." CLAUDE.md `Default epic grouping strategy: by-sub-feature` is therefore not applied. Feature → Task hierarchy with "Incorporates" links from TC-9001 to each task.

## Planned tasks

| # | Title | Type | Depends on |
|---|---|---|---|
| 1 | Add advisory severity summary model and SBOM aggregation service method | Implementation | — |
| 2 | Add GET /api/v2/sbom/{id}/advisory-summary endpoint with 5-minute cache | Implementation | 1 |
| 3 | Invalidate cached advisory summaries on advisory ingestion | Implementation | 2 |
| 4 | Support optional threshold query parameter on advisory-summary (non-MVP) | Implementation | 2 |
| 5 | Document advisory-summary endpoint in REST API reference | Documentation | 1, 2, 3, 4 |
| 6 | Smoke tests for advisory severity aggregation | Testing | 1, 2, 3, 4 |
| 7 | Performance benchmarks for advisory severity aggregation | Testing | 1, 2, 3, 4 |

## Fields set on created issues (`additional_fields`)

All 7 tasks:

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Major"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

- priority: inherited from Feature ("Major" — set, not "Undefined") → propagated
- fixVersions: Feature has `RHTPA 1.5.0`; `fixVersion scope: both` → propagated
- parent: omitted (no Epics)

See `task-creation-log.md` for per-task creation and link calls.

---

This comment was AI-generated by [sdlc-workflow/plan-feature](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.10.
