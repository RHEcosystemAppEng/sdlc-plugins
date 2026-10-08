# Task 1: Optimize search query performance with full-text indexes

## Repository
trustify-backend

## Target Branch
main

## Description
Improve the performance of the SearchService full-text search by adding PostgreSQL full-text search indexes and optimizing the query implementation. The current search is reported as "too slow" (TC-9002) but no specific performance targets have been provided.

**Assumption pending clarification:** "Faster" is interpreted as reducing query response time through database indexing and query optimization. No quantitative performance target has been defined -- measure improvement relative to the current implementation and document baseline vs optimized timings in the PR description.

**Assumption pending clarification:** The performance bottleneck is assumed to be in the database query layer (missing indexes, unoptimized full-text search queries) rather than in application-level processing or network latency. Verify this assumption by profiling the current search path before implementing changes.

## Files to Modify
- `modules/search/src/service/mod.rs` -- optimize SearchService full-text search query construction to use indexed columns and efficient query plans
- `common/src/db/query.rs` -- add or extend query builder helpers to support full-text search index utilization (e.g., GIN index-compatible query construction)
- `migration/src/lib.rs` -- register the new migration module
- `tests/api/search.rs` -- add performance-oriented integration tests validating that search returns results within acceptable time bounds

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` -- database migration to add GIN indexes on full-text search columns for SBOMs, advisories, and packages

## Implementation Notes
- Per CONVENTIONS.md [Error handling]: all modified handlers and service methods must return `Result<T, AppError>` with `.context()` wrapping for error propagation.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's `.rs` handler file scope.
- Per CONVENTIONS.md [Query helpers]: use the shared query builder in `common/src/db/query.rs` for filtering, pagination, and sorting rather than writing ad-hoc query logic.
  Applies: task modifies `common/src/db/query.rs` matching the convention's query builder scope.
- Per CONVENTIONS.md [Testing]: integration tests must follow the pattern in `tests/api/search.rs` -- hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)` assertions.
  Applies: task modifies `tests/api/search.rs` matching the convention's `tests/api/` test file scope.
- The new migration should follow the structure of `migration/src/m0001_initial/mod.rs` as the reference pattern for SeaORM migrations.
- Profile the current search query before and after changes to quantify improvement. Include timing comparisons in the PR description.
- Use PostgreSQL GIN indexes on `tsvector` columns for full-text search acceleration. If `tsvector` columns do not yet exist, the migration should add them as generated columns.

## Reuse Candidates
- `common/src/db/query.rs::query` -- existing query builder helpers for filtering, pagination, and sorting that should be extended rather than duplicated
- `migration/src/m0001_initial/mod.rs` -- reference migration pattern showing SeaORM migration structure

## Acceptance Criteria
- [ ] GIN indexes are created on full-text search columns via a new database migration
- [ ] SearchService queries utilize the new indexes (verified via EXPLAIN ANALYZE)
- [ ] Search response times are measurably improved compared to the pre-change baseline
- [ ] All existing search integration tests continue to pass (no regressions)
- [ ] New integration tests verify search returns results for known data

## Test Requirements
- [ ] Integration test: search endpoint returns results within reasonable time for a dataset with known entries
- [ ] Integration test: search returns correct results after index creation (functional correctness preserved)
- [ ] Integration test: verify existing search functionality is not broken (regression check against current tests/api/search.rs patterns)
- [ ] Migration test: verify the migration applies cleanly and indexes are created

## Verification Commands
- `cargo test --test search` -- run search integration tests, expect all tests to pass
- `cargo build` -- verify the project compiles without errors after changes

## Dependencies
- None (this is a standalone performance improvement)
