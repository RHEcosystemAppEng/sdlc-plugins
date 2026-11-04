# Task 2 — Use indexed full-text queries and caching in SearchService

**Summary:** TC-9002: Use indexed full-text queries and caching in SearchService
**Issue type:** Task | **Labels:** ai-generated-jira | **Priority:** Normal | **Fix Versions:** RHTPA 1.6.0

## Repository
trustify-backend

## Target Branch
main

## Description
This task delivers the "Search should be faster" requirement of TC-9002. `SearchService` (`modules/search/src/service/mod.rs`) is rewritten to query the full-text indexes added in Task 1 (`@@ to_tsquery` / `websearch_to_tsquery` against the indexed tsvector) instead of un-indexed text matching. Response caching is also turned on for `GET /api/v2/search`, using the project's existing `tower-http` caching middleware.

**Planning assumption (A1/A4, still to be confirmed):** the target is p95 latency at or below 500 ms for `GET /api/v2/search` on a representative dataset. The Feature does not define "fast enough", so the Feature owner must confirm or replace this number.

## Files to Modify
- `modules/search/src/service/mod.rs` — replace text matching with indexed full-text queries and keep pagination
- `modules/search/src/endpoints/mod.rs` — add cache configuration to the search route builder
- `entity/src/sbom.rs` — add the generated tsvector field if Task 1 used generated columns (read-only and never set on insert)
- `entity/src/advisory.rs` — same as above
- `entity/src/package.rs` — same as above
- `tests/api/search.rs` — add performance and regression tests

## Implementation Notes
- Inspect `SearchService` first to find each query it builds per entity. Every per-entity query (SBOM, advisory, package) must use the indexed expression. A path left on the slow query defeats the change.
- Use `websearch_to_tsquery` (or `plainto_tsquery`) to parse user input, so special characters cannot cause query syntax errors. Never interpolate raw input into SQL. Use SeaORM `Expr::cust_with_values` or an equivalent bound-parameter API.
- Keep pagination and sorting going through the shared helpers in `common/src/db/query.rs`, and keep returning `PaginatedResults<T>` (`common/src/model/paginated.rs`).
- Caching: follow the repository convention "Uses `tower-http` caching middleware; cache configuration in endpoint route builders". Look at how existing route builders configure caching, for example `modules/fundamental/src/sbom/endpoints/mod.rs`, and apply the same pattern in `modules/search/src/endpoints/mod.rs`. Use a short TTL so newly ingested data shows up quickly.
- Error handling: return `Result<T, AppError>` with `.context()` wrapping (`common/src/error.rs`), as the repository conventions require.
- Constraints (docs/constraints.md): §5.1 scope only the files listed, §5.2 inspect before modifying, §5.4 no duplicated helpers, §5.8 parity with sibling services on error handling and logging, §2.1–2.3 commit rules, §3.2–3.3 PR targets `main`.

## Reuse Candidates
- `common/src/db/query.rs` — shared filtering, pagination and sorting helpers. Reuse them instead of writing new pagination code.
- `common/src/model/paginated.rs::PaginatedResults` — response wrapper for the search results
- `modules/fundamental/src/advisory/service/advisory.rs` — `AdvisoryService` already has a "search" operation. Check it for query-building patterns to reuse or align with, so two divergent search implementations do not exist.
- `modules/fundamental/src/sbom/endpoints/mod.rs` — example of route registration and cache configuration

## Acceptance Criteria
- [ ] The SBOM, advisory and package queries in `SearchService` all use the full-text indexes from Task 1. `EXPLAIN` shows an index scan (Bitmap Index Scan on the GIN index) and no sequential scan over text columns.
- [ ] `GET /api/v2/search` meets the latency target agreed with the Feature owner (assumed p95 at or below 500 ms on the seeded benchmark dataset)
- [ ] The search route sends cache headers, configured through the existing `tower-http` caching pattern
- [ ] The response shape (`PaginatedResults<T>`) and query parameters are unchanged (backward compatible)
- [ ] User input with tsquery special characters (`&`, `|`, `!`, `:`, `'`) returns 200 with results or an empty list. It never returns a 500.

## Test Requirements
- [ ] An integration test in `tests/api/search.rs` seeds data and asserts that matches are returned for each entity type, using the `assert_eq!(resp.status(), StatusCode::OK)` pattern
- [ ] An integration test sends special-character input and asserts 200 with no server error
- [ ] An integration test asserts the cache headers are present on `GET /api/v2/search`
- [ ] A test or benchmark records search latency on a seeded dataset and compares it with the pre-change baseline
- [ ] The existing search tests pass unchanged

## Verification Commands
- `cargo test --test api search` — all search tests pass
- `curl -s -o /dev/null -w '%{time_total}\n' 'http://localhost:8080/api/v2/search?q=openssl'` — response time within the agreed target

## Dependencies
- Depends on: Task 1 — Add full-text search indexes migration
