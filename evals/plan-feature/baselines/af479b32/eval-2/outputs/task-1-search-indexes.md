# Task 1: Add full-text search indexes for query performance optimization

## Repository
trustify-backend

## Target Branch
main

## Description
Add PostgreSQL GIN indexes on searchable text columns across SBOM, advisory, and package entities to improve full-text search query performance. The current search implementation performs unindexed full-text scans, which degrades as data volume grows. This task creates a new database migration with GIN indexes and updates the SearchService to leverage indexed `tsvector` columns for efficient full-text search.

This addresses the MVP requirement "Search should be faster" from TC-9002. Note: no specific latency SLA was defined in the feature; the improvement is structural (indexed vs. unindexed queries) and should be validated against a pre-index baseline.

## Files to Modify
- `modules/search/src/service/mod.rs` -- optimize search query builder to use tsvector columns with GIN-indexed full-text search operators instead of LIKE/ILIKE patterns
- `tests/api/search.rs` -- add integration tests verifying search performance with indexes and correctness of indexed search results

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` -- new SeaORM migration adding GIN indexes on tsvector columns for SBOM (name, description), advisory (title, description), and package (name) entities

## Implementation Notes
- Create a new migration module following the established pattern in `migration/src/m0001_initial/mod.rs`. Register it in `migration/src/lib.rs`.
- Add `tsvector` generated columns (or use `to_tsvector()` in queries) for the searchable text fields. Create GIN indexes on these columns.
- Update `SearchService` in `modules/search/src/service/mod.rs` to use the `@@` (matches) operator with `to_tsquery()` instead of LIKE/ILIKE patterns for full-text search.
- Per CONVENTIONS.md §Query helpers: use shared query builder helpers from `common/src/db/query.rs` for constructing search predicates. Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's service query file scope.
- Per CONVENTIONS.md §Error handling: service methods should return `Result<T, AppError>` with `.context()` wrapping for database errors. Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's `.rs` service file scope.
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` use a real PostgreSQL test database with `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task modifies `tests/api/search.rs` matching the convention's test file scope.

## Reuse Candidates
- `common/src/db/query.rs` -- shared query builder helpers for filtering, pagination, and sorting; extend for full-text search predicate construction
- `migration/src/m0001_initial/mod.rs` -- existing migration structure to follow for the new migration module
- `common/src/db/limiter.rs` -- connection pool limiter, relevant if search queries need resource-aware execution

## Acceptance Criteria
- [ ] GIN indexes are created on searchable text columns for SBOM, advisory, and package entities via a new migration
- [ ] SearchService uses indexed full-text search operators (`@@` with `to_tsquery`) instead of LIKE/ILIKE
- [ ] Search endpoint returns the same correct results as before (backward-compatible)
- [ ] Search query execution time improves compared to pre-index baseline on the test dataset

## Test Requirements
- [ ] Migration applies successfully and creates expected GIN indexes (verify via test database schema inspection)
- [ ] Search endpoint returns correct results for single-word and multi-word queries after migration
- [ ] Existing search integration tests in `tests/api/search.rs` continue to pass without modification
- [ ] New test verifies that search queries hit the GIN index (explain plan or timing assertion)

## Verification Commands
- `cargo test --test api search` -- verify all search integration tests pass
- `cargo run --bin migration` -- verify migration applies cleanly

## Dependencies
- None
