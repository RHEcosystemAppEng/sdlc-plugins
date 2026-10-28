## Repository
trustify-backend

## Target Branch
main

## Description
Create a database migration that adds indexes on columns used for full-text search to improve search query performance. The current search implementation in `modules/search/src/service/mod.rs` executes queries that likely result in sequential scans on large tables. Adding GIN indexes for full-text search (tsvector) columns and B-tree indexes on commonly filtered columns will enable the database to use index scans, significantly reducing query latency.

**Assumptions pending clarification:**
- The primary performance bottleneck is missing database indexes (no profiling data was provided in the feature description)
- PostgreSQL GIN indexes on tsvector columns are the appropriate index type for the full-text search use case
- The columns to index are those referenced by SearchService queries in `modules/search/src/service/mod.rs`
- No specific performance targets were provided; the goal is to enable index-based query execution plans

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — New SeaORM migration that creates GIN indexes on full-text search columns and B-tree indexes on commonly queried columns (name, created date) across sbom, advisory, and package tables

## Files to Modify
- `migration/src/lib.rs` — Register the new m0002_search_indexes migration in the migration list

## Implementation Notes
- Follow the existing migration pattern established in `migration/src/m0001_initial/mod.rs` for migration structure and naming conventions.
- Use SeaORM's `Index::create()` API to define indexes within the migration's `up()` method.
- Create GIN indexes for tsvector columns used by full-text search. If tsvector columns do not yet exist, create them as generated columns using `tsvector_update_trigger` or equivalent.
- Create B-tree indexes on commonly filtered columns: `name`, `created_at`, `updated_at` on the sbom, advisory, and package tables.
- Ensure the migration's `down()` method drops all created indexes for reversibility.
- Reference entity definitions in `entity/src/sbom.rs`, `entity/src/advisory.rs`, and `entity/src/package.rs` to identify the exact column names.
- Per CONVENTIONS.md "Framework" convention: use SeaORM migration APIs consistently with the existing codebase patterns.
  Applies: task creates `migration/src/m0002_search_indexes/mod.rs` matching the convention's Rust/SeaORM scope.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — Existing migration that demonstrates the project's migration structure, naming, and SeaORM migration API usage patterns

## Acceptance Criteria
- [ ] A new migration `m0002_search_indexes` is created and registered in `migration/src/lib.rs`
- [ ] GIN indexes are created on full-text search columns for sbom, advisory, and package entities
- [ ] B-tree indexes are created on name and timestamp columns for sbom, advisory, and package entities
- [ ] Migration is reversible (down() drops all created indexes)
- [ ] Search queries show index scans in EXPLAIN output after migration

## Test Requirements
- [ ] Migration runs successfully on a clean database (forward migration)
- [ ] Migration rolls back cleanly (reverse migration)
- [ ] `EXPLAIN ANALYZE` on search queries confirms index usage after migration
- [ ] Existing search endpoint integration tests in `tests/api/search.rs` continue to pass after migration

## Verification Commands
- `cargo run --bin migration -- up` — Migration applies successfully
- `cargo run --bin migration -- down` — Migration reverts successfully

## Dependencies
- None (this is the first task and has no dependencies)
