## Repository
trustify-backend

## Target Branch
main

## Description
Make `GET /api/v2/search` faster, addressing the TC-9002 MVP requirement "Search should be faster". Use the bottlenecks found by the baseline instrumentation from Task 1. The expected optimizations are: database indexes on the columns `SearchService` searches, pagination through the shared query helpers so unbounded result sets are never loaded, and response caching on the search route.

**Open question (blocking the final acceptance threshold):** TC-9002 has no quantitative target ("should be fast enough"). The Product Owner must give a target (for example, a p95 latency on the Task 1 representative query set) before this task is accepted. Until then, acceptance is measured as an improvement over the Task 1 baseline.

**Assumption:** the optimizations are applied only where the Task 1 spans show the time goes. If the baseline shows that a planned optimization is not needed (for example, DB execution is already fast), drop it and record that in the PR.

## Files to Modify
- `modules/search/src/service/mod.rs` — use the shared pagination/limit helpers so `SearchService` never loads an unbounded result set; restructure any per-entity query that the Task 1 spans identify as dominant
- `modules/search/src/endpoints/mod.rs` — add `offset`/`limit` query parameters (if not already present), return `PaginatedResults<T>`, and configure `tower-http` caching on the search route builder
- `migration/src/lib.rs` — register the new search index migration
- `tests/api/search.rs` — add pagination and caching tests, and turn the Task 1 timing harness into a regression check against the baseline

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — migration that adds full-text (GIN) or trigram indexes on the text columns `SearchService` searches in the `sbom`, `advisory`, and `package` tables

## API Changes
- `GET /api/v2/search` — MODIFY: accepts optional `offset` and `limit` query parameters (defaulting to the shared pagination defaults) and returns `PaginatedResults<T>` with `total`. This is backward compatible because existing callers that send no parameters get the first page with default size. Verify the current response shape at implementation time: if the endpoint already returns `PaginatedResults<T>`, this becomes a no-op.

## Implementation Notes
- Find the exact columns `SearchService` filters on in `modules/search/src/service/mod.rs` and index those. Do not guess column names: read the entity definitions in `entity/src/sbom.rs`, `entity/src/advisory.rs`, and `entity/src/package.rs`.
- The new migration follows the existing layout in `migration/src/m0001_initial/mod.rs` and must be registered in `migration/src/lib.rs`. The migration is purely additive (new indexes only), so it is safe to land on `main` on its own.
- Pagination: use the shared helpers in `common/src/db/query.rs` and the response wrapper `PaginatedResults<T>` in `common/src/model/paginated.rs`. Do not write a search-specific pagination implementation.
- Caching: the project uses `tower-http` caching middleware, configured in endpoint route builders. Follow the configuration used by the existing route builders in `modules/fundamental/src/sbom/endpoints/mod.rs` and `modules/fundamental/src/advisory/endpoints/mod.rs`. Choose a short cache TTL and document it, because newly ingested data must become searchable within a bounded time.
- Connection pool pressure may be part of the slowness. Check `common/src/db/limiter.rs` usage in the search path and note the findings in the PR. Changing limiter configuration is out of scope unless the Task 1 baseline shows it is the bottleneck.
- Per CONVENTIONS.md §Response Types: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`. See `modules/fundamental/src/sbom/endpoints/list.rs` for the established pattern.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's list endpoint (`endpoints/*.rs`) scope.
- Per CONVENTIONS.md §Query Helpers: filtering, pagination, and sorting go through `common/src/db/query.rs`. See `modules/fundamental/src/sbom/service/sbom.rs` for usage.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's service query (`service/*.rs`) scope.
- Per CONVENTIONS.md §Caching: cache configuration lives in the endpoint route builder. See `modules/fundamental/src/sbom/endpoints/mod.rs`.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's route builder (`endpoints/mod.rs`) scope.
- Per CONVENTIONS.md §Error Handling: handlers return `Result<T, AppError>` with `.context()` wrapping. See `common/src/error.rs`.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's Rust handler (`.rs`) scope.
- Per CONVENTIONS.md §Testing: integration tests hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)`. See `tests/api/sbom.rs`.
  Applies: task modifies `tests/api/search.rs` matching the convention's integration test (`tests/api/*.rs`) scope.
- Constraints (docs/constraints.md): §2.1–2.3 (commit rules); §3.1–3.3 (PR rules, `--base main`); §5.1–5.4 (scope, inspect first, follow patterns, no duplication).

## Reuse Candidates
- `common/src/db/query.rs` — shared filtering, pagination, and sorting helpers. Use these for search pagination.
- `common/src/model/paginated.rs::PaginatedResults` — the standard list response wrapper.
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference implementation of a paginated list endpoint.
- `modules/fundamental/src/advisory/service/advisory.rs` — `AdvisoryService` already has a `search` capability. Check whether its query logic overlaps with `SearchService` and reuse it rather than writing a second advisory search query.
- `migration/src/m0001_initial/mod.rs` — migration structure to follow.

## Acceptance Criteria
- [ ] Indexes exist for every text column `SearchService` searches, and `EXPLAIN` on the representative queries shows index usage instead of sequential scans
- [ ] `GET /api/v2/search` supports `offset`/`limit` and returns `PaginatedResults<T>` with an accurate `total`
- [ ] A request with no pagination parameters still succeeds and returns the default first page
- [ ] The search route is served through `tower-http` caching with a documented TTL
- [ ] Latency for the Task 1 representative query set is lower than the Task 1 baseline (the absolute target is pending Product Owner input on TC-9002 — see Description)
- [ ] Search results for the representative queries are the same set as before the change, apart from pagination (no functional regression, per the TC-9002 NFR "Don't break existing functionality")

## Test Requirements
- [ ] The migration applies and rolls back cleanly on the test database
- [ ] Pagination test: seeded data larger than one page returns the correct page sizes, `total`, and non-overlapping pages
- [ ] Default-parameters test: a request with no `offset`/`limit` returns 200 and the default page size
- [ ] Regression test: the representative queries return the same result set as before the change
- [ ] Timing regression test: the representative query set completes faster than the recorded Task 1 baseline

## Verification Commands
- `cargo test --test api search` — all search tests pass
- `cargo run -p migration -- up` — the new index migration applies without error

## Documentation Updates
- `README.md` — if the README documents the search API, add the new `offset`/`limit` parameters and the paginated response shape

## Dependencies
- Depends on: Task 1 — Add search performance baseline instrumentation
