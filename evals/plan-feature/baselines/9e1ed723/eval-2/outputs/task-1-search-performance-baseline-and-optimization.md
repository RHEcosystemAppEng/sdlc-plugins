## Repository
trustify-backend

## Target Branch
main

## Description
Improve the response time of the unified search endpoint `GET /api/v2/search` (TC-9002 requirement "Search should be faster", MVP).

The Feature states search is "too slow" and should be "fast enough" but gives no latency target, no slow query examples, and no dataset size. This task therefore has two parts: first, measure current latency and find the bottlenecks in `SearchService`. Second, apply targeted optimizations (query shape, pagination, response caching) within the existing search module.

**Assumptions (pending clarification on TC-9002):**
- ASSUMPTION A1: "Search" means the unified search endpoint `GET /api/v2/search` (`modules/search/`), not the per-entity list endpoints (`GET /api/v2/sbom`, `/api/v2/advisory`, `/api/v2/package`). If the slowness reports are about list endpoints, the scope of this task changes.
- ASSUMPTION A2: With no latency target in the Feature, the provisional target is a measurable improvement over the recorded baseline (for example, p95 latency reduced, with the number agreed once the baseline is known). The product owner must confirm the actual target (for example, "p95 < 500 ms on dataset size N").
- ASSUMPTION A3: Optimizations stay inside the existing search module and the shared query helpers. Schema changes such as new database indexes are out of scope until profiling shows they are needed. If they are needed, they will be raised as a follow-up task, not added silently.

## Files to Modify
- `modules/search/src/service/mod.rs` — optimize `SearchService` full-text query execution (avoid unbounded result sets, push pagination and limits into the database query, remove redundant per-entity round trips found during profiling)
- `modules/search/src/endpoints/mod.rs` — apply `tower-http` response caching to the `GET /api/v2/search` route builder, and enforce default and maximum page size
- `tests/api/search.rs` — add regression and latency-guard tests for the search endpoint

## Implementation Notes
- Start by profiling `SearchService` in `modules/search/src/service/mod.rs`. Record baseline latency for representative queries against the integration-test PostgreSQL database and put the numbers in the PR description. That baseline is the evidence for ASSUMPTION A2.
- Use the shared pagination helpers in `common/src/db/query.rs` instead of building pagination by hand in the search service. Apply limit and offset at the database level so the service never loads the full match set into memory.
- Results must keep using the `PaginatedResults<T>` wrapper from `common/src/model/paginated.rs`. The response shape must not change (Feature NFR: "Don't break existing functionality").
- Caching: the repository already uses `tower-http` caching middleware, configured in endpoint route builders. Configure it on the search route in `modules/search/src/endpoints/mod.rs`, following how the other modules' `endpoints/mod.rs` files configure their routes (for example `modules/fundamental/src/sbom/endpoints/mod.rs`). Keep the cache TTL short, because newly ingested SBOMs and advisories must show up in search results.
- Per CONVENTIONS.md §Error handling: every handler returns `Result<T, AppError>` (`common/src/error.rs`) and wraps fallible calls with `.context()`.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's Rust handler (`.rs`) scope.
- Per CONVENTIONS.md §Query helpers: use the shared filtering, pagination, and sorting helpers in `common/src/db/query.rs`.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's Rust database-query (`.rs`) scope.
- Per CONVENTIONS.md §Caching: cache configuration belongs in the endpoint route builder.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint route builder (`.rs`) scope.
- Per CONVENTIONS.md §Testing: integration tests go in `tests/api/`, run against the real PostgreSQL test database, and use the `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task modifies `tests/api/search.rs` matching the convention's integration test (`tests/api/*.rs`) scope.
- Constraints (docs/constraints.md): changes stay within the files listed above (§5.1). Inspect code before modifying it (§5.2). Reuse the existing helpers rather than duplicating them (§5.4). Commits use Conventional Commits, reference TC-9002's task key in the footer, and include an `Assisted-by:` trailer (§2.1–2.3). The PR targets `main` via `--base main` and its link is posted to the Jira task (§3.2, §3.3).

## Reuse Candidates
- `common/src/db/query.rs` — shared filtering, pagination, and sorting helpers. Use them for database-level pagination in the search query.
- `common/src/model/paginated.rs::PaginatedResults` — the standard list response wrapper. Keep it as the search response type.
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — already has a `search` operation. Check it for query patterns that could be shared or that duplicate what `SearchService` does.
- `common/src/db/limiter.rs` — connection pool limiter. Check whether search queries wait on pool contention while profiling.

## Acceptance Criteria
- [ ] Baseline latency (p50/p95) for representative `GET /api/v2/search` queries is measured and recorded in the PR description
- [ ] p95 latency of `GET /api/v2/search` improves measurably over the recorded baseline (the exact target is pending clarification, see ASSUMPTION A2)
- [ ] Search pagination is applied at the database query level through `common/src/db/query.rs` helpers, and a maximum page size is enforced
- [ ] `tower-http` response caching is configured on the search route
- [ ] The `GET /api/v2/search` request parameters and response shape (`PaginatedResults<T>`) are unchanged and backward compatible

## Test Requirements
- [ ] Integration test in `tests/api/search.rs`: an existing-style search query still returns `StatusCode::OK` with the same response shape as before (regression guard)
- [ ] Integration test: requesting a page size above the maximum is clamped (or rejected per the chosen behavior) and does not return an unbounded result set
- [ ] Integration test: paginated results (offset/limit) return the correct `total` and item slice
- [ ] All existing tests in `tests/api/search.rs`, `tests/api/sbom.rs`, and `tests/api/advisory.rs` keep passing

## Verification Commands
- `cargo test --test search` (run from `tests/`) — all search integration tests pass
- `cargo build` — workspace builds without errors

## Dependencies
- None
