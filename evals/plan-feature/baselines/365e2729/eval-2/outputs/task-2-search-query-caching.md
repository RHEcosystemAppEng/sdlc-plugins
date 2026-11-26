## Repository
trustify-backend

## Target Branch
main

## Description
Reduce latency of `GET /api/v2/search` by optimizing the queries issued by `SearchService` (pagination pushed into SQL, no N+1 lookups, bounded result size) and enabling response caching on the search route using the project's existing `tower-http` caching middleware. This addresses the TC-9002 MVP requirement "Search should be faster".

**Assumptions pending clarification (TC-9002):**
- ASSUMPTION: Short-lived caching of search responses is acceptable. Search results can include newly ingested SBOMs/advisories; the acceptable staleness window has not been specified. A conservative default (e.g., 60 seconds) is used until the Feature owner confirms.
- ASSUMPTION: Search results must remain paginated through `PaginatedResults<T>`; no change to the response shape is intended.
- ASSUMPTION: No numeric latency target exists; improvements are demonstrated by before/after measurements recorded in the PR.

## Files to Modify
- `modules/search/src/service/mod.rs` — push offset/limit into SQL, remove per-row follow-up queries, apply a maximum page size
- `modules/search/src/endpoints/mod.rs` — add caching configuration to the search route builder
- `tests/api/search.rs` — add tests for pagination bounds and cache headers

## API Changes
- `GET /api/v2/search` — MODIFY: response now carries cache-control headers; `limit` is capped at a maximum page size. Response body shape is unchanged.

## Implementation Notes
- `SearchService` in `modules/search/src/service/mod.rs` performs the full-text search across entities. Review it for (a) loading all matches and paginating in memory, and (b) per-result follow-up queries; replace both with single paginated SQL queries.
- Use the shared pagination helpers in `common/src/db/query.rs` instead of hand-rolled offset/limit logic, and return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
- Caching: the project configures `tower-http` caching in each endpoint route builder. Mirror the existing configuration used in `modules/fundamental/src/sbom/endpoints/mod.rs` / `modules/fundamental/src/advisory/endpoints/mod.rs` when adding caching to `modules/search/src/endpoints/mod.rs`.
- Handlers must keep returning `Result<T, AppError>` (`common/src/error.rs`) with `.context()` wrapping on fallible calls.
- Per CONVENTIONS.md §Caching: configure caching via `tower-http` middleware in the endpoint route builder, not inside the service. See `modules/fundamental/src/sbom/endpoints/mod.rs` for an existing route builder.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint route builder scope.
- Per CONVENTIONS.md §Query helpers: use the shared filtering, pagination, and sorting helpers from `common/src/db/query.rs`.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's Rust database query scope.
- Per CONVENTIONS.md §Response types: list-style responses return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint handler scope.
- Per CONVENTIONS.md §Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's Rust handler scope.
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` against the PostgreSQL test database, using `assert_eq!(resp.status(), StatusCode::OK)`.
  Applies: task modifies `tests/api/search.rs` matching the convention's `tests/api/` scope.

Constraints (docs/constraints.md):
- §2 Commit rules: Conventional Commits format, Jira task ID in footer, `Assisted-by:` trailer.
- §3 PR rules: `gh pr create --base main`; post the PR link on the Jira task.
- §5 Code change rules: scope changes to the listed files; inspect before modifying; reuse `common/src/db/query.rs` rather than duplicating pagination logic.

## Reuse Candidates
- `common/src/db/query.rs` — shared pagination/filtering/sorting query builder helpers
- `common/src/model/paginated.rs::PaginatedResults` — standard paginated response wrapper
- `modules/fundamental/src/sbom/endpoints/mod.rs` — existing route builder with `tower-http` caching configuration to mirror
- `common/src/db/limiter.rs` — connection pool limiter; confirm search queries go through it rather than bypassing it

## Acceptance Criteria
- [ ] `SearchService` issues paginated SQL queries (offset/limit applied in the database), with no per-result follow-up queries
- [ ] Requests with `limit` above the maximum page size are capped (or rejected with 400, per existing list endpoint behavior) rather than returning unbounded results
- [ ] `GET /api/v2/search` responses include cache headers configured through `tower-http` in `modules/search/src/endpoints/mod.rs`
- [ ] Response body shape (`PaginatedResults<T>`) is unchanged for existing clients
- [ ] Before/after latency for a representative query is recorded in the PR description

## Test Requirements
- [ ] Integration test: paginated search returns the correct `total` and the requested page of results
- [ ] Integration test: a `limit` above the maximum page size does not return more than the maximum
- [ ] Integration test: search response contains the expected cache-control header
- [ ] Existing tests in `tests/api/search.rs`, `tests/api/sbom.rs`, and `tests/api/advisory.rs` continue to pass

## Verification Commands
- `cargo test --test api search` — search integration tests pass
- `curl -i "http://localhost:8080/api/v2/search?q=openssl"` — returns 200 with a `cache-control` header

## Dependencies
- Depends on: Task 1 — Add full-text search indexes (migration)
