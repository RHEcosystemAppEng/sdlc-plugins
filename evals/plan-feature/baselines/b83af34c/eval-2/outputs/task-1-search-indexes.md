## Repository
trustify-backend

## Target Branch
main

## Description
Add PostgreSQL database indexes to improve search query performance. The current search implementation lacks dedicated indexes for full-text search operations, contributing to slow query response times. This task creates a new SeaORM migration that adds GIN indexes on text columns used by the search service and B-tree indexes on commonly queried foreign key and filter columns.

**Assumption (pending clarification):** The feature states "search should be faster" but provides no baseline response time or target latency. This task assumes that adding database indexes is a necessary first step to improve search performance. Specific performance targets should be clarified with the product owner.

**Assumption (pending clarification):** The specific columns to index are inferred from the existing entity model (SBOM name/description fields, advisory title/description fields, package name fields). The exact set of indexed columns should be confirmed based on actual query patterns and slow-query analysis.

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — New migration module that creates GIN indexes for full-text search on SBOM, advisory, and package text columns, and B-tree indexes on foreign key columns used in join queries

## Files to Modify
- `migration/src/lib.rs` — Register the new m0002_search_indexes migration module in the migration registry

## Implementation Notes
The migration should follow the SeaORM migration pattern established in `migration/src/m0001_initial/mod.rs`. Create GIN indexes using `CREATE INDEX ... USING gin(to_tsvector('english', column))` for text search columns on the SBOM, advisory, and package entities defined in `entity/src/sbom.rs`, `entity/src/advisory.rs`, and `entity/src/package.rs`. Add B-tree indexes on foreign key columns in join tables (`entity/src/sbom_advisory.rs`, `entity/src/sbom_package.rs`) to speed up join operations used by the search service.

Per CONVENTIONS.md §Framework: use SeaORM migration API for index creation DDL. Applies: task creates `migration/src/m0002_search_indexes/mod.rs` matching the convention's Rust file scope.

## Acceptance Criteria
- [ ] New migration module `m0002_search_indexes` is created and registered
- [ ] GIN indexes are added on text columns used for full-text search on SBOM, advisory, and package tables
- [ ] B-tree indexes are added on foreign key columns in join tables (sbom_advisory, sbom_package)
- [ ] Migration runs successfully against a PostgreSQL test database
- [ ] Migration is idempotent (can be re-run without error via IF NOT EXISTS guards)
- [ ] Existing search functionality is not broken by the migration

## Test Requirements
- [ ] Migration applies cleanly on a fresh PostgreSQL database
- [ ] Migration rolls back cleanly without leaving orphaned indexes
- [ ] Existing search integration tests in `tests/api/search.rs` continue to pass after migration
- [ ] EXPLAIN ANALYZE on a representative search query shows index usage after migration

## Verification Commands
- `cargo test -p migration` — migration compiles and unit tests pass
- `cargo test -p tests --test search` — existing search integration tests pass
