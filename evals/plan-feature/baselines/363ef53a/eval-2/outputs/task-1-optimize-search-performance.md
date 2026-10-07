## Repository
trustify-backend

## Target Branch
main

## Description
Optimize search query performance in the SearchService to reduce response latency. The current full-text search across entities (SBOMs, advisories, packages) is reported as slow. This task adds database indexes on frequently searched columns and optimizes query execution patterns in the SearchService.

**Assumption (pending clarification):** No specific performance baseline or target latency has been defined in the feature description. This task assumes the goal is to reduce search response time to under 500ms for typical queries by adding appropriate database indexes and optimizing query patterns. The product owner should confirm specific performance SLAs.

**Assumption (pending clarification):** The feature description does not specify which search queries are slow or which entities are most impacted. This task assumes all entity types (SBOMs, advisories, packages) contribute to slow search performance and applies indexing broadly across searchable columns.

## Files to Modify
- `modules/search/src/service/mod.rs` -- Optimize SearchService query execution: reduce unnecessary joins, add query result limiting, and leverage database indexes
- `migration/src/lib.rs` -- Register the new migration module for search indexes
- `tests/api/search.rs` -- Add performance-related integration tests to verify search response times remain acceptable

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` -- Database migration to add indexes on frequently searched columns across sbom, advisory, and package entities

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for structuring the new migration module. Use SeaORM's `Index::create()` to define indexes on searchable text columns in the `sbom`, `advisory`, and `package` entities.
- Optimize the `SearchService` in `modules/search/src/service/mod.rs` by reviewing current query patterns: ensure queries use indexed columns, avoid full table scans, and apply pagination early in the query pipeline using helpers from `common/src/db/query.rs`.
- Consider adding a GIN or GiST index for PostgreSQL full-text search columns if the current implementation uses `LIKE` or `ILIKE` patterns.
- Per CONVENTIONS.md §Error handling: wrap all new database operations with `.context()` for descriptive error messages. Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's Rust handler scope.
- Per CONVENTIONS.md §Query helpers: use shared filtering, pagination, and sorting utilities from `common/src/db/query.rs` rather than building custom query logic. See `modules/fundamental/src/sbom/service/sbom.rs` for the established query pattern. Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's query builder scope.
- Per CONVENTIONS.md §Testing: add integration tests in `tests/api/search.rs` hitting a real PostgreSQL test database using the `assert_eq!(resp.status(), StatusCode::OK)` pattern. See `tests/api/sbom.rs` for an example. Applies: task modifies `tests/api/search.rs` matching the convention's test file scope.

## Reuse Candidates
- `common/src/db/query.rs` -- Shared query builder helpers for filtering, pagination, and sorting; use these to optimize search queries rather than writing custom pagination logic
- `migration/src/m0001_initial/mod.rs` -- Existing migration module showing the established pattern for SeaORM migrations
- `common/src/db/limiter.rs` -- Connection pool limiter that may be relevant for managing search query concurrency

## Acceptance Criteria
- [ ] Database indexes are added for searchable columns in the sbom, advisory, and package entities
- [ ] SearchService query execution is optimized to leverage the new indexes
- [ ] Migration runs successfully against a PostgreSQL test database
- [ ] Existing search endpoint integration tests continue to pass
- [ ] New integration tests verify that search queries execute within acceptable latency bounds

## Test Requirements
- [ ] Integration test: search endpoint returns results with status 200 after index migration
- [ ] Integration test: search across SBOMs with common terms returns results within expected time
- [ ] Integration test: search across advisories with common terms returns results within expected time
- [ ] Integration test: search with empty query returns paginated results correctly
- [ ] Verify that the migration is reversible (down migration drops the indexes)

## Verification Commands
- `cargo test -p tests --test search` -- verify all search integration tests pass
- `cargo run --bin migration -- up` -- verify migration applies cleanly

## Dependencies
- None
