## Repository
trustify-backend

## Target Branch
main

## Description
Add a database migration to create PostgreSQL full-text search indexes on searchable entity columns, improving search query performance. The current search implementation in `modules/search/src/service/mod.rs` (SearchService) performs full-text search across entities but lacks dedicated indexes, leading to sequential scans on large datasets.

This task addresses the TC-9002 requirement "Search should be faster" by adding GIN indexes for full-text search on the `sbom`, `advisory`, and `package` tables.

**Assumption (pending clarification):** The performance bottleneck is database query execution time during full-text search, not application-level processing or network latency. No current baseline metrics or target latency thresholds were specified in the feature description. If the bottleneck is elsewhere, this migration may be insufficient and additional optimization approaches would need to be evaluated.

## Files to Modify
- `migration/src/lib.rs` — Register the new migration module in the migration runner

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — New migration: create GIN indexes on searchable text columns in `sbom`, `advisory`, and `package` tables for full-text search

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for migration module structure and SeaORM migration trait implementation.
- Per CONVENTIONS.md §Framework: use SeaORM migration API for index creation (e.g., `Index::create().table(...).col(...).index_type(IndexType::Gin)`).
  Applies: task creates `migration/src/m0002_search_indexes/mod.rs` matching the convention's .rs file scope.
- Create GIN indexes using `to_tsvector()` on text columns that the SearchService queries. Inspect `entity/src/sbom.rs`, `entity/src/advisory.rs`, and `entity/src/package.rs` to identify the exact column names used for search (likely name/title and description fields).
- Register the new migration in `migration/src/lib.rs` following the pattern used for `m0001_initial`.
- The migration should be idempotent — use `IF NOT EXISTS` semantics where supported by SeaORM, or handle the case where indexes already exist.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — Existing migration module demonstrating the SeaORM migration trait pattern and index creation approach
- `entity/src/sbom.rs` — SBOM entity definition with column names to index
- `entity/src/advisory.rs` — Advisory entity definition with column names to index
- `entity/src/package.rs` — Package entity definition with column names to index

## Acceptance Criteria
- [ ] A new migration module `m0002_search_indexes` exists and is registered in `migration/src/lib.rs`
- [ ] GIN indexes are created on searchable text columns in `sbom`, `advisory`, and `package` tables
- [ ] The migration runs successfully against a PostgreSQL database without errors
- [ ] The migration is idempotent — running it twice does not cause errors
- [ ] Existing search functionality continues to work after the migration (backward compatible)

## Test Requirements
- [ ] Verify the migration applies cleanly to a fresh PostgreSQL database
- [ ] Verify the migration applies cleanly to a database with existing data
- [ ] Verify that `EXPLAIN ANALYZE` on a search query shows index usage (GIN index scan) rather than sequential scan after migration

## Verification Commands
- `cargo run --bin migration -- up` — migration applies without errors
- `psql -c "\di" | grep search` — verify indexes exist in the database

## Dependencies
- None (this is the first task and has no dependencies)
