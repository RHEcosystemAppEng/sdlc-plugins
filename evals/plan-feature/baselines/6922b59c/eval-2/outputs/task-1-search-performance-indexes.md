## Repository
trustify-backend

## Target Branch
main

## Description
Add database indexes on commonly searched columns and optimize SearchService query patterns to improve search response times. The feature TC-9002 states search is "too slow" but provides no performance benchmarks or profiling data.

**Assumption (pending clarification):** The primary performance bottleneck is in database query execution due to missing full-text search indexes on name and description columns across searchable entities (sbom, advisory, package). This assumption should be validated with actual query profiling before implementation.

## Files to Modify
- `modules/search/src/service/mod.rs` -- Optimize SearchService query construction to leverage full-text search indexes and use parameterized queries
- `common/src/db/query.rs` -- Add search-optimized query builder helpers for full-text search predicates

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` -- Database migration to add GIN indexes on searchable text columns (name, description) across sbom, advisory, and package entities

## Implementation Notes
- Follow the existing migration structure in `migration/src/m0001_initial/mod.rs` for the new migration module. Register the migration in `migration/src/lib.rs`.
- Add GIN indexes on `name` and `description` columns for the `sbom`, `advisory`, and `package` entity tables to support full-text search via PostgreSQL `tsvector`/`tsquery`.
- Optimize SearchService in `modules/search/src/service/mod.rs` to use `to_tsvector` and `to_tsquery` for full-text matching instead of `LIKE`/`ILIKE` patterns.
- Leverage the connection pool limiter from `common/src/db/limiter.rs` if concurrent search queries are a concern.
- Per CONVENTIONS.md §Error Handling: all database operations in SearchService must return `Result<T, AppError>` and wrap errors with `.context()` for descriptive messages. See `modules/fundamental/src/sbom/service/sbom.rs` for the established error handling pattern.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's `.rs` error handling scope.
- Per CONVENTIONS.md §Query Helpers: use and extend shared query builder utilities from `common/src/db/query.rs` for search query construction rather than writing ad-hoc query logic.
  Applies: task modifies `common/src/db/query.rs` matching the convention's `.rs` query helper scope.

## Reuse Candidates
- `common/src/db/query.rs` -- Shared filtering, pagination, and sorting helpers; extend these for full-text search predicates rather than creating separate query utilities
- `common/src/db/limiter.rs` -- Connection pool limiter for managing concurrent search query load
- `migration/src/m0001_initial/mod.rs` -- Reference migration structure and SeaORM migration pattern

## Acceptance Criteria
- [ ] Database migration creates GIN indexes on searchable text columns (name, description) for sbom, advisory, and package entities
- [ ] Migration registered in `migration/src/lib.rs`
- [ ] SearchService query patterns optimized to use full-text search functions (tsvector/tsquery)
- [ ] Existing search functionality preserved -- all current search tests pass without modification
- [ ] Migration applies and rolls back cleanly against PostgreSQL

## Test Requirements
- [ ] Integration test verifying the migration applies successfully
- [ ] Integration test verifying search queries return correct results after optimization
- [ ] Verify existing tests in `tests/api/search.rs` continue to pass unchanged

## Verification Commands
- `cargo test --test search` -- existing search tests pass
- `cargo run --bin migration` -- migration applies successfully

## Dependencies
- None (this is the foundational performance task)
