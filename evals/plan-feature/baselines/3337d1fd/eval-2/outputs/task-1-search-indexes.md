## Repository
trustify-backend

## Target Branch
main

## Description
Add PostgreSQL full-text search indexes to optimize search query performance. The current search implementation in `modules/search/src/service/mod.rs` performs full-text search across entities (SBOMs, advisories, packages) but lacks database-level indexes to accelerate text matching. This task creates a new SeaORM migration that adds GIN indexes on text-searchable columns and introduces `tsvector` generated columns for efficient full-text search, directly addressing the "search should be faster" requirement.

**Assumption (pending clarification):** No performance baseline or target SLA has been provided. This task assumes that adding GIN indexes on `tsvector` columns is the appropriate optimization. If profiling reveals the bottleneck is elsewhere (e.g., response serialization, connection pool exhaustion), the approach may need revision.

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — New migration adding GIN indexes and tsvector generated columns for SBOM, advisory, and package tables

## Files to Modify
- `migration/src/lib.rs` — Register the new migration module `m0002_search_indexes`

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for migration module structure and registration.
  Applies: task creates `migration/src/m0002_search_indexes/mod.rs` matching the convention's migration module scope.
- Add `tsvector` generated columns to the `sbom`, `advisory`, and `package` tables. Use `to_tsvector('english', coalesce(name, '') || ' ' || coalesce(description, ''))` or equivalent column concatenation based on the actual column names in the entity definitions at `entity/src/sbom.rs`, `entity/src/advisory.rs`, and `entity/src/package.rs`.
- Create GIN indexes on each `tsvector` column using `CREATE INDEX ... USING gin(...)`.
- Use raw SQL in the migration via SeaORM's `manager.get_connection().execute_unprepared()` for PostgreSQL-specific DDL (GIN indexes, generated columns).
- The migration must be idempotent — use `IF NOT EXISTS` on index creation.

## Acceptance Criteria
- [ ] A new migration `m0002_search_indexes` exists and is registered in `migration/src/lib.rs`
- [ ] The migration adds `tsvector` generated columns to sbom, advisory, and package tables
- [ ] GIN indexes are created on each `tsvector` column
- [ ] The migration runs successfully against a PostgreSQL test database without errors
- [ ] The migration is reversible (down migration drops the indexes and columns)
- [ ] Existing data is not lost or corrupted by the migration

## Test Requirements
- [ ] Integration test verifying the migration applies cleanly on a fresh database
- [ ] Integration test verifying the migration rolls back cleanly
- [ ] Verify via `EXPLAIN ANALYZE` (manual or test assertion) that search queries use the new GIN indexes after migration

## Dependencies
- None — this is the foundational task
