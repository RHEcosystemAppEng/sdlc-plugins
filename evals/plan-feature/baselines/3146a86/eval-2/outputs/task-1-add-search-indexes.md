# Task 1 — Add database indexes on searchable columns for search performance

## Repository
trustify-backend

## Target Branch
main

## Description
Add PostgreSQL indexes on text columns that are used for full-text search queries across
the SBOM, advisory, and package entity tables. The current search is slow because queries
perform sequential scans on unindexed text columns. Adding GIN indexes for full-text search
and B-tree indexes for filter columns will significantly improve query performance.

## Files to Modify
- `entity/src/sbom.rs` — verify searchable column definitions (name, description fields)
- `entity/src/advisory.rs` — verify searchable column definitions (title, description, severity fields)
- `entity/src/package.rs` — verify searchable column definitions (name, license fields)

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — new migration adding GIN indexes for full-text search columns and B-tree indexes for filter columns (entity type, severity, date fields)

## Implementation Notes
- Follow the existing migration pattern established in `migration/src/m0001_initial/mod.rs`
- Use SeaORM migration pattern: define the migration struct implementing `MigrationTrait`
- Add GIN indexes using `CREATE INDEX ... USING gin(to_tsvector('english', <column>))` for text search columns
- Add B-tree indexes for columns that will be used as filters (severity on advisory, date columns)
- Register the new migration in `migration/src/lib.rs`
- The migration must be idempotent — use `IF NOT EXISTS` for index creation

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — existing migration pattern showing the project's migration structure and conventions
- `common/src/db/query.rs` — query builder helpers that will consume these indexes; review to understand which columns are used in WHERE clauses

## Acceptance Criteria
- [ ] GIN indexes exist on all text columns used for full-text search (SBOM name/description, advisory title/description, package name)
- [ ] B-tree indexes exist on filter columns (advisory severity, date columns)
- [ ] Migration runs successfully against the PostgreSQL test database
- [ ] Migration is registered in `migration/src/lib.rs`
- [ ] Existing search queries execute without errors after migration

## Test Requirements
- [ ] Integration test verifying the migration applies cleanly to a fresh database
- [ ] Integration test verifying the migration is idempotent (can run twice without error)
- [ ] Verify existing search tests in `tests/api/search.rs` still pass after migration

## Verification Commands
- `cargo test -p migration` — migration tests pass
- `cargo test -p tests --test search` — existing search integration tests pass
