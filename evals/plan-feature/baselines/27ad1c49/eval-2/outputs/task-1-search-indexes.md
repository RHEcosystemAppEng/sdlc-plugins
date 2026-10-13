## Repository
trustify-backend

## Target Branch
main

## Description
Add a database migration that creates full-text search indexes on key searchable columns across SBOM, advisory, and package entities. This addresses the "search should be faster" requirement by ensuring the database can efficiently serve full-text search queries without sequential scans.

**Assumptions pending clarification:**
- Assumes PostgreSQL `tsvector` / GIN indexes are the appropriate indexing strategy, since the repository uses PostgreSQL and SeaORM
- Assumes indexes should cover the primary searchable text columns on sbom, advisory, and package tables (e.g., name, description, identifier fields)
- Assumes no schema changes to existing tables beyond adding indexes (non-breaking migration)

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — New migration module adding GIN indexes for full-text search on sbom, advisory, and package tables

## Files to Modify
- `migration/src/lib.rs` — Register the new migration module in the migration runner

## Implementation Notes
Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for migration module structure.

Use SeaORM migration API to create GIN indexes on `tsvector` columns. The migration should:
1. Add a generated `tsvector` column (or create a GIN index on existing text columns) for each searchable entity
2. Create GIN indexes using `Index::create()` for each searchable column
3. Include a `down()` migration that drops the indexes

Reference the entity definitions in `entity/src/sbom.rs`, `entity/src/advisory.rs`, and `entity/src/package.rs` to identify the columns that should be indexed for search.

## Acceptance Criteria
- [ ] Migration creates GIN indexes on searchable columns for sbom, advisory, and package tables
- [ ] Migration is registered in `migration/src/lib.rs` and runs successfully
- [ ] Migration includes a reversible `down()` function that drops the created indexes
- [ ] Existing search queries benefit from the new indexes (no sequential scans on indexed columns)

## Test Requirements
- [ ] Migration applies cleanly on a fresh database
- [ ] Migration rolls back cleanly via `down()`
- [ ] Existing search integration tests in `tests/api/search.rs` continue to pass after migration
