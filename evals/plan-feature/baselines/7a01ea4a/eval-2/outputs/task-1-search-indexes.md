## Repository
trustify-backend

## Target Branch
main

## Description
Add database indexes on frequently searched columns in the entity tables used by the SearchService's full-text search. The current search queries scan entity tables without dedicated indexes on searchable columns, contributing to slow query performance. This addresses TC-9002 requirement: "Search should be faster." Adding B-tree indexes on name/title columns and timestamp columns will reduce query execution time for common search and filter patterns. If the SearchService uses PostgreSQL full-text search (`tsvector`), add GIN indexes on the corresponding `tsvector` columns for efficient full-text queries.

## Files to Modify
- `migration/src/lib.rs` -- register the new migration module in the migration runner

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` -- new SeaORM migration adding indexes on searchable columns: `sbom.name`, `advisory.title`, `package.name`, and timestamp columns used for date-range filtering

## Implementation Notes
- Inspect `migration/src/m0001_initial/mod.rs` to understand the existing SeaORM migration structure before creating the new migration
- Use `Index::create()` from `sea_orm_migration::prelude` to define each index
- Add B-tree indexes on: `sbom` table `name` column, `advisory` table `title` column, `package` table `name` column
- Add B-tree indexes on timestamp columns (e.g., `created_at`, `updated_at`) that will support date-range filter queries planned in Task 3
- If the SearchService in `modules/search/src/service/mod.rs` uses `tsvector` columns for full-text search, add GIN indexes on those columns (`CREATE INDEX ... USING GIN (column)`)
- Implement the `down()` migration to drop all created indexes for reversibility
- Per CONVENTIONS.md section "Framework": use SeaORM for database migration definitions. Applies: task creates `migration/src/m0002_search_indexes/mod.rs` matching the convention's Rust migration file scope.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` -- existing migration module demonstrating the SeaORM migration API pattern (`MigrationTrait` implementation, `up`/`down` methods, table/index operations)
- `entity/src/sbom.rs` -- SBOM entity definition with column names to identify the exact column identifiers for index creation
- `entity/src/advisory.rs` -- Advisory entity definition with column names for index targets
- `entity/src/package.rs` -- Package entity definition with column names for index targets

## Acceptance Criteria
- [ ] New migration creates B-tree indexes on `sbom.name`, `advisory.title`, and `package.name` columns
- [ ] New migration creates indexes on timestamp columns used for date-range queries
- [ ] Migration `up()` runs successfully against the PostgreSQL test database without errors
- [ ] Migration `down()` removes all created indexes cleanly
- [ ] Existing search endpoint behavior is unchanged (indexes are additive DDL, not behavioral changes)
- [ ] Existing integration tests continue to pass

## Test Requirements
- [ ] Migration `up()` and `down()` operations execute without errors against the test database
- [ ] Verify indexes exist after running `up()` by querying the `pg_indexes` system catalog
- [ ] Verify indexes are removed after running `down()` by querying the `pg_indexes` system catalog
- [ ] All existing search integration tests in `tests/api/search.rs` continue to pass after migration

## Verification Commands
- `cargo test -p migration` -- verify the migration module compiles and migration operations succeed
- `cargo test -p tests --test search` -- verify existing search integration tests still pass after index creation

## Dependencies
- None
