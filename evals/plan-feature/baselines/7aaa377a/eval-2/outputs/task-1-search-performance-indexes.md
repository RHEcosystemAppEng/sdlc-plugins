## Repository
trustify-backend

## Target Branch
main

## Description
Add a database migration to create indexes on frequently searched columns to improve full-text search query performance. The current search (TC-9002) is reported as slow, and adding targeted indexes on the columns used by `SearchService` for full-text search is the foundational step to address this.

The migration adds B-tree indexes on:
- `sbom.name` and `sbom.version` — used when searching SBOMs by name or version
- `advisory.title` — used when searching advisories by title
- `advisory.severity` — used when filtering/sorting advisories by severity
- `package.name` — used when searching packages by name
- `package_license.license` — used when filtering packages by license

These columns are the primary search targets based on the entity definitions in `entity/src/` and the full-text search implementation in `modules/search/src/service/mod.rs`.

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — new migration module defining `Index::create()` calls for all search-relevant columns

## Files to Modify
- `migration/src/lib.rs` — register the new `m0002_search_indexes` migration module in the migration list

## Implementation Notes
- Follow the SeaORM migration pattern established in `migration/src/m0001_initial/mod.rs` — the new migration module should implement the same `MigrationTrait` with `up` and `down` methods.
- Use `Index::create().table(Entity).col(Column)` syntax for each index definition. Create individual indexes rather than composite indexes, since the search queries target individual columns.
- The migration must be idempotent — use `IF NOT EXISTS` semantics or handle the case where the index already exists.
- Per Key Conventions (Module pattern): follow the existing directory structure under `migration/src/` with a dedicated subdirectory for this migration.
  Applies: task creates `migration/src/m0002_search_indexes/mod.rs` matching the convention's migration file scope.
- Per Key Conventions (Error handling): all migration operations should return `Result` with proper error context.
  Applies: task modifies `migration/src/lib.rs` matching the convention's `.rs` file scope.
- Reference `migration/src/m0001_initial/mod.rs` for the established migration pattern (struct layout, `MigrationTrait` implementation, `up`/`down` method signatures).

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — existing migration implementing `MigrationTrait`; use as the structural template for the new migration module
- `entity/src/sbom.rs` — SBOM entity definition; reference for column names to index
- `entity/src/advisory.rs` — Advisory entity definition; reference for column names to index
- `entity/src/package.rs` — Package entity definition; reference for column names to index

## Acceptance Criteria
- [ ] A new migration `m0002_search_indexes` exists and is registered in `migration/src/lib.rs`
- [ ] The migration creates B-tree indexes on `sbom.name`, `sbom.version`, `advisory.title`, `advisory.severity`, `package.name`, and `package_license.license`
- [ ] The migration includes a `down` method that drops all created indexes
- [ ] The migration runs successfully against a fresh database and against a database with existing data
- [ ] Existing search functionality is not broken by the migration

## Test Requirements
- [ ] Run the migration against the test PostgreSQL database and verify all indexes are created (check `pg_indexes` system catalog)
- [ ] Run the migration `down` and verify all indexes are dropped
- [ ] Run the migration `up` twice to verify idempotency
- [ ] Run existing search integration tests (`tests/api/search.rs`) to confirm no regressions

## Verification Commands
- `cargo run --bin migration -- up` — migration applies successfully
- `cargo run --bin migration -- down` — migration rolls back successfully
- `cargo test --test search` — existing search tests pass

## Dependencies
- None (this is the foundational task)
