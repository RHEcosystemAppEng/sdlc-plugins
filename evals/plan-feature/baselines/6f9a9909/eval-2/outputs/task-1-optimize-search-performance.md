## Repository
trustify-backend

## Target Branch
main

## Description
Optimize the search query performance in the `SearchService` to reduce response times for full-text search operations across SBOMs, advisories, and packages. The current search implementation in `modules/search/src/service/mod.rs` performs full-text search across entities but users report it is too slow.

**Assumption (pending clarification):** In the absence of specified performance targets, this task assumes a target of p95 query response time under 500ms for searches returning up to 100 results. This assumption should be validated with the product owner before implementation begins.

**Assumption (pending clarification):** The current search bottleneck is assumed to be at the database query level (missing indexes, unoptimized query plans) rather than at the application layer. The implementer should profile actual query execution to confirm this assumption.

## Files to Modify
- `modules/search/src/service/mod.rs` — optimize search query construction, add query plan hints, reduce unnecessary joins
- `modules/search/src/endpoints/mod.rs` — add caching configuration for search results using tower-http caching middleware
- `common/src/db/query.rs` — extend shared query builder helpers to support optimized full-text search patterns

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — add database indexes for full-text search columns across SBOM, advisory, and package entities

## Implementation Notes
- The existing `SearchService` in `modules/search/src/service/mod.rs` performs full-text search across entities. Profile the current query execution plan and identify missing indexes on frequently searched columns.
- Use the shared query builder helpers in `common/src/db/query.rs` for pagination and sorting — extend them to support optimized full-text search patterns rather than duplicating query construction logic.
- Add `tower-http` caching middleware configuration to the search endpoint route builder in `modules/search/src/endpoints/mod.rs`, following the caching pattern established in other endpoint modules.
- For the migration, follow the module pattern established in `migration/src/m0001_initial/mod.rs` — create a new migration module under `migration/src/` that adds GIN or GiST indexes for full-text search columns.
- The search endpoint at `GET /api/v2/search` returns results via `PaginatedResults<T>` from `common/src/model/paginated.rs` — ensure any query optimizations preserve this response shape.
- Per docs/constraints.md §2 (Commit Rules): every commit must reference TC-9002 in the footer, follow Conventional Commits, and include the `Assisted-by: Claude Code` trailer.
- Per docs/constraints.md §3 (PR Rules): the feature branch must be named after the Jira issue ID, and the PR link must be posted as a comment on the Jira task.
- Per docs/constraints.md §5 (Code Change Rules): changes must be scoped to the files listed above, code must be inspected before modification, and implementation must follow referenced patterns.

**Convention-aware enrichment:**

- Per CONVENTIONS.md §Error Handling: all new or modified handlers must return `Result<T, AppError>` with `.context()` wrapping for error propagation.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's Rust handler file scope.

- Per CONVENTIONS.md §Response Types: list endpoints must return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's Rust endpoint file scope.

- Per CONVENTIONS.md §Query Helpers: use shared filtering, pagination, and sorting via `common/src/db/query.rs`.
  Applies: task modifies `common/src/db/query.rs` matching the convention's query helper file scope.

- Per CONVENTIONS.md §Caching: use `tower-http` caching middleware with cache configuration in endpoint route builders.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's Rust endpoint file scope.

- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task modifies `tests/api/search.rs` matching the convention's Rust test file scope.

## Reuse Candidates
- `common/src/db/query.rs::query builder helpers` — shared filtering, pagination, and sorting utilities that should be extended rather than duplicated for optimized search queries
- `common/src/db/limiter.rs::connection pool limiter` — connection pool management that may need tuning for search query workloads
- `common/src/model/paginated.rs::PaginatedResults<T>` — response wrapper already used by list endpoints; search results must use this same type

## Acceptance Criteria
- [ ] Search queries execute with improved performance (target: p95 < 500ms for searches returning up to 100 results — pending clarification of actual targets)
- [ ] Database indexes are added for full-text search columns via a new migration
- [ ] Search endpoint has appropriate caching configuration via tower-http middleware
- [ ] Query builder helpers in `common/src/db/query.rs` support optimized full-text search patterns
- [ ] Existing search API contract (`GET /api/v2/search`) is preserved — no breaking changes to response shape
- [ ] All existing search integration tests continue to pass

## Test Requirements
- [ ] Add performance-focused integration tests in `tests/api/search.rs` that verify search queries return results within acceptable time bounds
- [ ] Add integration tests verifying that search indexes are created by the new migration
- [ ] Verify existing search integration tests in `tests/api/search.rs` continue to pass without modification
- [ ] Test caching behavior: verify that repeated identical search queries benefit from caching

## Verification Commands
- `cargo test --test search` — run search integration tests and verify all pass
- `cargo build` — verify the project compiles without errors after changes

## Dependencies
- None
