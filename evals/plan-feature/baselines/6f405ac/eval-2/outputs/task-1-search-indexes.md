## Repository
trustify-backend

## Target Branch
main

## Description
Add a database migration to create full-text search indexes on searchable text columns across SBOM, advisory, and package entities. This addresses the "search should be faster" requirement from TC-9002 by ensuring the database can efficiently execute text search queries without full table scans.

**Ambiguity note:** The feature does not specify which columns are searched or what "too slow" means quantitatively. This task assumes the SearchService queries against name/title/description fields on the primary entities, and that adding GIN indexes for PostgreSQL full-text search (`tsvector`) will address the performance complaint. This assumption is pending clarification.

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — New migration that adds GIN indexes on `tsvector` columns for SBOM, advisory, and package tables to support full-text search

## Files to Modify
- `migration/src/lib.rs` — Register the new m0002 migration module in the migration runner

## Implementation Notes
Follow the existing migration pattern established in `migration/src/m0001_initial/mod.rs`. The new migration should:
- Add a `search_vector` column of type `tsvector` to the SBOM, advisory, and package tables (or create GIN indexes on existing text columns used by the search service)
- Create GIN indexes on the `tsvector` columns for efficient full-text search
- Add a trigger to auto-update the `tsvector` column when rows are inserted or updated

Reference `modules/search/src/service/mod.rs` to determine which entity fields the SearchService currently queries, and ensure indexes cover those fields.

Per CONVENTIONS.md §Framework: use SeaORM migration patterns for schema changes. Applies: task modifies `migration/src/m0002_search_indexes/mod.rs` matching the convention's `.rs` scope.

Per CONVENTIONS.md §Module pattern: the migration follows the existing `migration/src/m0001_initial/mod.rs` structure. Applies: task creates `migration/src/m0002_search_indexes/mod.rs` matching the convention's `.rs` scope.

## Acceptance Criteria
- [ ] A new migration `m0002_search_indexes` exists and is registered in `migration/src/lib.rs`
- [ ] The migration creates GIN indexes on text-searchable columns for SBOM, advisory, and package entities
- [ ] The migration is reversible (has a down/rollback implementation)
- [ ] The migration runs successfully against a clean database and an existing database with data

## Test Requirements
- [ ] Migration applies cleanly on a fresh database (tested via migration runner)
- [ ] Migration applies cleanly on a database with existing data from m0001
- [ ] Rollback removes the indexes and columns without data loss
