## Repository
trustify-backend

## Target Branch
main

## Description
Optimize the SearchService's full-text search query performance. The feature description states search is "currently too slow" but provides no quantitative performance targets (see Ambiguity A1 in the impact map). This task focuses on database-level optimizations: adding appropriate indexes for full-text search columns, optimizing query structure to leverage indexes effectively, and evaluating caching strategies for frequently executed queries.

**Ambiguity note:** No performance baseline or target latency has been specified. The implementer should measure current search query latency before and after changes to quantify improvement. Consider adding query instrumentation if not already present.

## Files to Modify
- `modules/search/src/service/mod.rs` -- optimize search query construction in SearchService for better index utilization
- `common/src/db/query.rs` -- review and optimize shared query builder helpers used by search queries

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` -- database migration to add full-text search indexes (GIN indexes on tsvector columns)

## Implementation Notes
- Analyze current search query execution plans using `EXPLAIN ANALYZE` to identify bottlenecks
- Add GIN indexes on tsvector columns used by full-text search (if not already present)
- Review SearchService query construction for N+1 query patterns or unnecessary joins
- Evaluate `tower-http` caching middleware applicability for search results with short TTL
- Per CONVENTIONS.md §Error Handling: all service methods must return `Result<T, AppError>` with `.context()` wrapping for any new error paths.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's .rs handler/service scope.
- Per CONVENTIONS.md §Query Helpers: use shared filtering, pagination, and sorting helpers from `common/src/db/query.rs` -- do not duplicate query-building logic. See `modules/fundamental/src/sbom/service/sbom.rs` for established pattern.
  Applies: task modifies `common/src/db/query.rs` matching the convention's .rs query helper scope.
- Per CONVENTIONS.md §Testing: integration tests must follow the pattern in `tests/api/search.rs` using a real PostgreSQL test database with `assert_eq!(resp.status(), StatusCode::OK)`.
  Applies: convention has no file-type restriction (broadly applicable).

**Constraints (docs/constraints.md):**
- §2 Commit Rules: every commit must reference the Jira task ID in the footer, follow Conventional Commits, and include `--trailer="Assisted-by: Claude Code"`
- §3 PR Rules: branch must be named after the Jira task ID; after opening PR, post link as Jira comment; `gh pr create` must specify `--base main`
- §5 Code Change Rules: changes scoped to listed files; inspect code before modifying; follow patterns in Implementation Notes; do not duplicate existing functionality

## Reuse Candidates
- `common/src/db/query.rs` -- shared query builder helpers for filtering, pagination, and sorting; extend rather than rebuild for search optimization
- `common/src/db/limiter.rs` -- connection pool limiter; may be relevant if search queries need concurrency management

## Acceptance Criteria
- [ ] Full-text search indexes are added via a new database migration
- [ ] SearchService query construction is optimized to leverage indexes (verified via EXPLAIN ANALYZE showing index scan usage)
- [ ] Search endpoint response times show measurable improvement over baseline (note: no specific target defined -- see Ambiguity A1)
- [ ] Existing search integration tests in `tests/api/search.rs` continue to pass
- [ ] No regressions in other endpoint functionality

## Test Requirements
- [ ] Add integration test verifying search queries return results within acceptable latency bounds
- [ ] Verify existing search tests pass with new indexes in place
- [ ] Test search performance with representative data volume

## Verification Commands
- `cargo test --test search` -- verify search integration tests pass
- `cargo build` -- verify compilation succeeds

## Dependencies
- None
