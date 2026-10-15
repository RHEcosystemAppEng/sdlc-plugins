## Repository
trustify-backend

## Target Branch
main

## Description
Create a database migration that adds PostgreSQL full-text search infrastructure (tsvector columns, GIN indexes, and trigger functions) to the searchable entity tables (sbom, advisory, package). This migration establishes the database-level foundation for search performance optimization and relevance ranking.

This addresses the "Search should be faster" requirement from TC-9002. The current search implementation lacks dedicated full-text search indexes, leading to sequential scans on text columns.

**Assumption pending clarification:** The performance bottleneck is at the database query level. PostgreSQL tsvector columns with GIN indexes are the appropriate optimization. No external search engine (e.g., Elasticsearch) is required for MVP.

## Files to Create
- `migration/src/m0002_search_performance/mod.rs` — SeaORM migration adding tsvector columns, GIN indexes, and trigger functions to sbom, advisory, and package tables

## Files to Modify
- `migration/src/lib.rs` — Register the new m0002_search_performance migration in the migration list

## Implementation Notes
- Per CONVENTIONS.md §Framework: implement database migration using SeaORM migration patterns.
  Applies: convention has no file-type restriction (broadly applicable).
  See `migration/src/m0001_initial/mod.rs` for the established migration pattern.
- Add a `search_vector` column of type `tsvector` to each searchable table (sbom, advisory, package)
- Create GIN indexes on each `search_vector` column for fast full-text search lookups
- Create trigger functions (`tsvector_update_trigger`) to automatically maintain the tsvector column when row data changes
- For the `sbom` table, the tsvector should index the name and description fields
- For the `advisory` table, the tsvector should index the title, description, and severity fields
- For the `package` table, the tsvector should index the name and namespace fields
- Use `setweight()` to assign different weights to fields (e.g., 'A' for name/title, 'B' for description) to support relevance ranking in Task 2
- Ensure the migration is idempotent and includes both `up()` and `down()` methods

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — Established SeaORM migration pattern showing table creation, column definitions, and index creation

## Acceptance Criteria
- [ ] Migration m0002_search_performance creates tsvector columns on sbom, advisory, and package tables
- [ ] GIN indexes are created on all tsvector columns
- [ ] Trigger functions automatically update tsvector columns when source fields change
- [ ] Tsvector columns use weighted concatenation (setweight) for relevance ranking support
- [ ] Migration is registered in migration/src/lib.rs
- [ ] Migration runs successfully against a clean database (up) and can be rolled back (down)
- [ ] Existing data is backfilled into the tsvector columns during migration

## Test Requirements
- [ ] Migration applies cleanly on a fresh PostgreSQL test database
- [ ] Migration rollback (down) removes all added columns, indexes, and triggers
- [ ] Inserting a new row in each table populates the tsvector column via the trigger
- [ ] Updating a searchable field in an existing row updates the tsvector column

## Verification Commands
- `cargo test -p migration` — migration tests pass
- `psql -c "\d sbom" | grep search_vector` — verify tsvector column exists on sbom table
- `psql -c "\di" | grep search_vector` — verify GIN indexes exist

## Dependencies
- None (this is the foundational task)
