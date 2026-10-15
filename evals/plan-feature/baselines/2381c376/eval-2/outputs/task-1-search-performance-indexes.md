## Repository
trustify-backend

## Target Branch
main

## Description
Add database indexes to improve search query performance. The current search implementation in `modules/search/src/service/mod.rs` performs full-text search across entities without dedicated indexes, resulting in sequential scans on large datasets. This task creates a database migration that adds GIN indexes on full-text search columns and optimizes the SearchService queries to leverage them.

**Ambiguity note:** The feature description states "search should be faster" and "currently too slow" without specifying a performance baseline or target SLA. This task assumes that adding appropriate indexes and optimizing queries will address the performance concern. The specific latency target remains an open question pending clarification from the product owner.

**Assumption (pending clarification):** "Faster" is interpreted as reducing query execution time through database-level indexing (PostgreSQL GIN indexes for full-text search vectors) and query-level optimization in the SeaORM query builder. Without a defined target, acceptance is based on verifiable use of indexes in query execution plans.

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — new migration adding GIN indexes on full-text search columns for SBOMs, advisories, and packages

## Files to Modify
- `migration/src/lib.rs` — register the new m0002_search_indexes migration module
- `modules/search/src/service/mod.rs` — optimize search queries to use indexed columns and to_tsvector/to_tsquery patterns
- `tests/api/search.rs` — add integration tests verifying search performance with indexed queries

## Implementation Notes
- Create the migration module following the established pattern in `migration/src/m0001_initial/mod.rs`. The migration should use SeaORM's migration API to add GIN indexes.
- Add GIN indexes on text columns used for full-text search in the `sbom`, `advisory`, and `package` entities (see entity definitions in `entity/src/sbom.rs`, `entity/src/advisory.rs`, `entity/src/package.rs`).
- In `modules/search/src/service/mod.rs`, update the SearchService to use `to_tsvector` and `to_tsquery` PostgreSQL functions for full-text search instead of LIKE/ILIKE patterns, enabling the GIN indexes to be used.
- Ensure all query modifications use the existing error handling pattern: `Result<T, AppError>` with `.context()` wrapping (see `common/src/error.rs`).
- Use the existing query builder helpers in `common/src/db/query.rs` for pagination and sorting of results.
- Per CONVENTIONS.md §Error Handling: all new or modified handlers must return `Result<T, AppError>` with `.context()` wrapping.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's `.rs` file scope.
- Per CONVENTIONS.md §Testing: add integration tests in `tests/api/` hitting a real PostgreSQL test database using the `assert_eq!(resp.status(), StatusCode::OK)` pattern. See `tests/api/search.rs` for the established test structure.
  Applies: task modifies `tests/api/search.rs` matching the convention's test `.rs` file scope.
- Per CONVENTIONS.md §Query Helpers: use shared filtering, pagination, and sorting via `common/src/db/query.rs`. See existing usage in `modules/fundamental/src/sbom/service/sbom.rs`.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's service `.rs` file scope.

## Reuse Candidates
- `common/src/db/query.rs::query builder helpers` — shared filtering, pagination, and sorting logic that should be reused for search query construction
- `migration/src/m0001_initial/mod.rs` — reference migration pattern for creating the new index migration

## Acceptance Criteria
- [ ] A new migration `m0002_search_indexes` exists and creates GIN indexes on full-text search columns
- [ ] The migration is registered in `migration/src/lib.rs`
- [ ] SearchService queries in `modules/search/src/service/mod.rs` use `to_tsvector`/`to_tsquery` patterns that leverage the new GIN indexes
- [ ] All existing search integration tests in `tests/api/search.rs` continue to pass (regression guard)
- [ ] New integration tests verify that search queries return correct results with the optimized query path
- [ ] Error handling follows the `Result<T, AppError>` pattern with `.context()` wrapping

## Test Requirements
- [ ] Integration test: verify search returns results after migration is applied
- [ ] Integration test: verify search with empty query returns paginated results
- [ ] Integration test: verify search with a specific term returns matching entities
- [ ] Regression: all existing tests in `tests/api/search.rs` pass without modification

## Verification Commands
- `cargo test --test search` — run search integration tests, expect all tests to pass
- `cargo run --bin migration` — run migrations, expect m0002_search_indexes to apply successfully
