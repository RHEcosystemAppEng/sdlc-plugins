**Summary**: Add GET /api/v2/sbom/{id}/advisory-summary endpoint with 5-minute cache

## Repository
trustify-backend

## Target Branch
main

## Description
Expose the aggregation from Task 1 as `GET /api/v2/sbom/{id}/advisory-summary` (TC-9001). The endpoint returns `{ critical, high, medium, low, total }` for the SBOM, returns 404 when the SBOM does not exist (consistent with `GET /api/v2/sbom/{id}`), and caches responses for 5 minutes using the existing caching infrastructure. The cache must be keyed by SBOM ID and evictable so that Task 3 can invalidate it when new advisories are linked.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the `/api/v2/sbom/{id}/advisory-summary` route and attach the 5-minute cache configuration in the route builder
- `tests/api/sbom.rs` — integration tests for the new endpoint

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Axum handler calling `SbomService::advisory_severity_summary`

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `200 { "critical": N, "high": N, "medium": N, "low": N, "total": N }`; `404` if the SBOM ID does not exist

## Implementation Notes
- Handler: mirror `modules/fundamental/src/sbom/endpoints/get.rs` (path extraction of `{id}`, `SbomService` injection via state, `Result<Json<_>, AppError>` return, not-found → `AppError` 404 from `common/src/error.rs`). Do not return a 200 with zeros when the SBOM lookup fails — map the not-found result from Task 1 to 404.
- Route registration: add the route alongside existing routes in `modules/fundamental/src/sbom/endpoints/mod.rs`; `server/src/main.rs` already mounts the SBOM module, so no server change is expected (verify).
- Response is a single object, not `PaginatedResults<T>` (`common/src/model/paginated.rs` applies only to list endpoints).
- Caching: the repo uses `tower-http` caching middleware configured in endpoint route builders. Configure a 5-minute TTL for this route. Because TC-9001 requires invalidation on advisory ingestion, the cache must be a server-side entry keyed by SBOM ID that can be evicted programmatically (expose a small `invalidate_advisory_summary(sbom_id)` API on the existing cache infrastructure for Task 3). If the existing middleware only emits HTTP `Cache-Control` headers, do not rely on them alone — client/proxy copies cannot be invalidated; keep any `max-age` ≤ 300s and document this.
- Do not cache 404 responses (a newly ingested SBOM must become visible immediately).
- Register the handler in the OpenAPI spec if sibling handlers do (check `get.rs` for `utoipa` annotations).
- Per repository Key Conventions §Endpoint registration: each module's `endpoints/mod.rs` registers its routes. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint-registration scope. Example: existing `get` route registration in the same file.
- Per repository Key Conventions §Caching: cache configuration lives in the endpoint route builder. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's route-builder scope.
- Per repository Key Conventions §Testing: integration tests in `tests/api/` hit a real PostgreSQL test DB and use `assert_eq!(resp.status(), StatusCode::OK)`. Applies: task modifies `tests/api/sbom.rs` matching the convention's integration-test scope. Example: existing tests in `tests/api/sbom.rs`.
- Constraints (docs/constraints.md): §1.4/§5.1 scope to listed files; §5.2 inspect before modifying; §5.8 parity with sibling SBOM handlers on error handling/logging; §2.1–2.3 Conventional Commits with Jira footer and `Assisted-by: Claude Code` trailer; §3.1–3.3 branch per task ID, `--base main`, PR link posted to Jira.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — handler structure and 404 behaviour for `GET /api/v2/sbom/{id}`
- `common/src/error.rs::AppError` — NotFound mapping via `IntoResponse`
- Existing `tower-http` cache configuration in route builders — reuse rather than adding a new cache dependency

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with `{ critical, high, medium, low, total }` for an existing SBOM
- [ ] Counts reflect unique advisories (deduplicated by advisory ID)
- [ ] Returns 404 for a non-existent SBOM ID (never 200 with zeros)
- [ ] Successful responses are cached for 5 minutes, keyed by SBOM ID; 404s are not cached
- [ ] A programmatic invalidation entry point for a given SBOM ID exists for use by Task 3
- [ ] No new database tables or migrations

## Test Requirements
- [ ] Integration test: existing SBOM with seeded advisories of mixed severities returns 200 and the exact expected JSON body
- [ ] Integration test: duplicated SBOM–advisory links are counted once
- [ ] Integration test: unknown SBOM ID returns 404
- [ ] Integration test: SBOM with no advisories returns 200 with all zeros
- [ ] Test: second request within TTL is served from cache; after invalidation for that SBOM ID, a fresh value is returned

## Verification Commands
- `cargo test --test api sbom` — new and existing SBOM endpoint tests pass
- `curl -s -o /dev/null -w '%{http_code}' localhost:8080/api/v2/sbom/<unknown-id>/advisory-summary` — prints `404`

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model and SBOM aggregation service method
