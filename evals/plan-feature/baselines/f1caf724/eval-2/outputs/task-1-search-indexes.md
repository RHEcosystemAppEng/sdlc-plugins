## Repository
trustify-backend

## Target Branch
main

## Description
Add database indexes to improve search query performance. The current search implementation lacks targeted indexes on text-searchable columns, resulting in sequential scans on large datasets. This task creates a SeaORM migration that adds GIN indexes on the columns used by the SearchService for full-text queries.

**Assumptions pending clarification:**
- The primary performance bottleneck is assumed to be at the database query level (missing indexes), not at the application or network layer. If profiling reveals the bottleneck is elsewhere, this migration alone will not resolve the "too slow" complaint.
- GIN indexes are chosen as the index type because they are optimized for full-text search operations in PostgreSQL. If the project uses a different search backend (e.g., Elasticsearch), this approach would need revision.
- The specific columns to index (sbom name/description, advisory title/description, package name) are assumed based on the entity model. The feature description does not specify which search fields are underperforming.

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` -- SeaORM migration adding GIN indexes on text-searchable columns (sbom name/description, advisory title/description, package name)

## Files to Modify
- `migration/src/lib.rs` -- register the new m0002_search_indexes migration module
- `tests/api/search.rs` -- add test verifying search queries perform correctly with indexes in place

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for the migration module structure.
- Use SeaORM's `Index::create()` API to define GIN indexes. Target columns: `sbom.name`, `sbom.description`, `advisory.title`, `advisory.description`, `package.name`.
- Add `tsvector` generated columns or GIN indexes on raw text columns depending on whether PostgreSQL full-text search is already configured (inspect `m0001_initial` for precedent).
- The migration must be reversible -- the down migration should drop all created indexes.
- Per CONVENTIONS.md §Framework: use SeaORM migration APIs for all database schema changes, consistent with the project's use of SeaORM for database operations.
  Applies: task creates `migration/src/m0002_search_indexes/mod.rs` matching the convention's Rust/SeaORM scope.
- Per CONVENTIONS.md §Testing: add integration test using the established pattern with `assert_eq!(resp.status(), StatusCode::OK)` in `tests/api/`.
  Applies: task modifies `tests/api/search.rs` matching the convention's test file scope.

## Acceptance Criteria
- [ ] Migration `m0002_search_indexes` creates GIN indexes on sbom name, sbom description, advisory title, advisory description, and package name columns
- [ ] Migration runs successfully against a clean database and an existing database
- [ ] Migration is reversible (down migration drops the indexes)
- [ ] `migration/src/lib.rs` registers the new migration in the correct order after m0001_initial
- [ ] Search query EXPLAIN plans show index usage instead of sequential scans for text search queries

## Test Requirements
- [ ] Integration test verifies the migration applies cleanly on a test database
- [ ] Integration test verifies search queries return results after index creation
- [ ] Verify migration is idempotent (running it twice does not produce errors)

## Verification Commands
- `cargo test -p migration` -- migration compiles and unit tests pass
- `cargo test -p tests --test search` -- search integration tests pass

## Dependencies
- None
