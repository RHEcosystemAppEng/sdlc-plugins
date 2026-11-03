## Repository
trustify-backend

## Target Branch
main

## Description
Part of TC-9002 (Improve search experience), requirement "Search should be faster" (MVP).

The Feature gives no latency target, so this task covers only low-regret performance improvements that follow existing repository conventions:
1. Bound the size of `GET /api/v2/search` responses by paginating with the shared `PaginatedResults<T>` wrapper and the shared pagination helpers. This matches every other list endpoint.
2. Add response caching to the search route builder using the existing `tower-http` caching middleware convention.
3. Add a latency baseline test, so later optimizations can be measured once the Feature owner gives a target.

**Assumption to verify first:** repository analysis could not inspect the body of `SearchService`. Before changing anything, check whether search results are already paginated or cached. If they are, record that on the PR and keep only the parts that are still missing. Meeting the requirement in full ("search is fast") is still unresolved until a latency target is given (see the TC-9002 impact map, clarification question 1).

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — accept pagination query parameters (offset/limit), return `PaginatedResults<T>`, and configure the caching middleware on the search route builder
- `modules/search/src/service/mod.rs` — apply pagination to the search query with the shared query helpers instead of loading all matches
- `tests/api/search.rs` — add pagination, cache-header, backward-compatibility, and latency-baseline tests

## API Changes
- `GET /api/v2/search` — MODIFY: accepts optional `offset` and `limit` query parameters. The response is wrapped in `PaginatedResults<T>` (`items`, `total`). Requests without these parameters get the default page size used by the other list endpoints.

## Implementation Notes
- Pagination: reuse the shared helpers in `common/src/db/query.rs` (filtering, pagination, sorting) and the `PaginatedResults<T>` wrapper in `common/src/model/paginated.rs`. Follow the pattern of `modules/fundamental/src/sbom/endpoints/list.rs` (`GET /api/v2/sbom`) and `modules/fundamental/src/advisory/endpoints/list.rs` (`GET /api/v2/advisory`), which already return paginated results.
- Caching: the repository configures `tower-http` caching middleware in endpoint route builders. Apply the same configuration in the search route registration in `modules/search/src/endpoints/mod.rs`. Copy the cache settings from an existing module's `endpoints/mod.rs` (e.g., `modules/fundamental/src/sbom/endpoints/mod.rs`) rather than inventing new values.
- Error handling: handlers return `Result<T, AppError>` (`common/src/error.rs`) with `.context()` wrapping. Reject an invalid `limit` (e.g., negative or non-numeric) with a 400 through `AppError` instead of silently falling back to an unbounded query.
- Route mounting is done in `server/src/main.rs`. It needs no change unless the route builder signature changes.
- Per CONVENTIONS.md §Response types (as summarized in the repository Key Conventions): list endpoints return `PaginatedResults<T>`. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint handler scope. Example: `modules/fundamental/src/sbom/endpoints/list.rs`.
- Per CONVENTIONS.md §Query helpers: use the shared pagination from `common/src/db/query.rs`. Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's service/query scope. Example: `modules/fundamental/src/sbom/service/sbom.rs` (`SbomService::list`).
- Per CONVENTIONS.md §Testing: integration tests hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task modifies `tests/api/search.rs` matching the convention's integration test scope. Example: `tests/api/sbom.rs`.
- Constraints (docs/constraints.md):
  - §2 commits: Conventional Commits, `Implements <task-key>` footer, `--trailer="Assisted-by: Claude Code"`.
  - §3 PRs: `--base main`, and post the PR link on the Jira task.
  - §5 code changes: change only the listed files, inspect code before modifying it, reuse the existing helpers, and check parity with sibling list endpoints (error handling, caching).

## Reuse Candidates
- `common/src/db/query.rs` — shared pagination, filtering, and sorting helpers. Use these instead of writing new offset/limit logic.
- `common/src/model/paginated.rs::PaginatedResults` — standard paginated response wrapper.
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference paginated list handler.
- `modules/fundamental/src/sbom/endpoints/mod.rs` — reference route builder with caching middleware configuration.

## Acceptance Criteria
- [ ] `GET /api/v2/search` accepts optional `offset` and `limit` and returns `PaginatedResults<T>` with the correct `total`
- [ ] A request without `offset`/`limit` returns the first page using the same default page size as the other list endpoints
- [ ] An invalid `limit` or `offset` returns 400 via `AppError`. It never falls back to an unbounded query.
- [ ] The search route has `tower-http` caching configured the same way as the other modules' route builders
- [ ] A latency baseline for representative search queries is measured and recorded in the PR description, before and after the change
- [ ] All existing tests in `tests/api/search.rs` pass (or are updated only for the `PaginatedResults` response shape, with the change explained in the PR)

## Test Requirements
- [ ] Integration test: search with `limit=N` returns at most N items, and `total` reflects all matches
- [ ] Integration test: search with `offset` returns the next page without overlap
- [ ] Integration test: search without pagination parameters returns the default page
- [ ] Integration test: invalid `limit` (negative or non-numeric) returns 400
- [ ] Integration test: the search response includes the cache headers set by the caching middleware
- [ ] Latency baseline test (or `#[ignore]`d benchmark test) in `tests/api/search.rs` that times representative queries against a seeded test database

## Verification Commands
- `cargo test -p tests search` — all search integration tests pass
- `curl -s "http://localhost:8080/api/v2/search?q=openssl&limit=5"` — returns JSON with `items` (at most 5 entries) and `total`

## Documentation Updates
- `README.md` — document the `offset`/`limit` parameters and the paginated response shape of `GET /api/v2/search`, if the README documents the API
