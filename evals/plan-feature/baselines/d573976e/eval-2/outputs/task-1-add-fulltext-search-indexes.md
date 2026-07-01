# Task 1 — Add full-text search indexes via database migration

## Repository
trustify-backend

## Target Branch
main

## Description
Create a new database migration that adds full-text search indexes (GIN indexes on `tsvector` columns) to the searchable columns across SBOM, advisory, and package entities. This is the foundation for improving search performance and enabling weighted relevance ranking in subsequent tasks.

Currently, the `SearchService` in `modules/search/src/service/mod.rs` performs full-text search across entities, but without dedicated full-text indexes, queries must scan entire tables. Adding GIN indexes on `tsvector` columns for the key searchable fields will allow PostgreSQL to use index-backed full-text search, dramatically improving query performance.

## Files to Modify
- `migration/src/lib.rs` — register the new migration module

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — new migration adding GIN indexes for full-text search on SBOM (name, description), advisory (title, description), and package (name) columns

## Implementation Notes
- Follow the existing migration pattern established in `migration/src/m0001_initial/mod.rs` for migration module structure and registration.
- Use PostgreSQL `tsvector` columns with GIN indexes for full-text search. Create a generated `tsvector` column (e.g., `search_vector`) on each entity table that concatenates the searchable text fields with appropriate weights (A for title/name, B for description).
- Use `Index::create()` for each new index, following SeaORM migration conventions.
- The migration should be idempotent — use `IF NOT EXISTS` guards where supported.
- Reference the existing entity definitions in `entity/src/sbom.rs`, `entity/src/advisory.rs`, and `entity/src/package.rs` to identify the exact column names to index.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — existing migration pattern showing SeaORM migration structure and conventions
- `common/src/db/query.rs` — existing query helpers that will later consume these indexes

## Acceptance Criteria
- [ ] New migration creates GIN indexes on `tsvector` columns for SBOM (name, description), advisory (title, description), and package (name) tables
- [ ] Migration runs successfully against a PostgreSQL database without errors
- [ ] Migration is registered in `migration/src/lib.rs`
- [ ] Existing search functionality is not broken (backward compatible)

## Test Requirements
- [ ] Migration applies cleanly on a fresh database
- [ ] Migration applies cleanly on a database with existing data (upgrade path)
- [ ] Indexes are verified to exist after migration (query `pg_indexes` or equivalent)

## Verification Commands
- `cargo run --bin migration -- up` — migration applies without errors
- `psql -c "SELECT indexname FROM pg_indexes WHERE tablename IN ('sbom', 'advisory', 'package') AND indexdef LIKE '%gin%';"` — confirms GIN indexes exist

## Dependencies
- None (this is the first task)
