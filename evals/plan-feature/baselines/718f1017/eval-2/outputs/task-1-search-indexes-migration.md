## Repository
trustify-backend

## Target Branch
main

## Description
Add a database migration that creates PostgreSQL full-text search indexes (GIN indexes on tsvector columns) for the primary searchable entity fields. This migration enables the SearchService to use efficient full-text search queries with ranking instead of naive LIKE/ILIKE pattern matching, addressing the "search should be faster" requirement from TC-9002.

**Ambiguity note:** The feature does not specify which fields should be indexed for search. Assumption (pending clarification): index the most user-visible text fields — SBOM name, advisory title/summary, and package name — as these are the fields most likely searched by users.

## Files to Modify
- `migration/src/lib.rs` — register the new migration module in the migration runner

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — migration that adds GIN indexes on tsvector-generated columns for SBOM (name), advisory (title), and package (name) entities

## Implementation Notes
- Follow the existing migration pattern established in `migration/src/m0001_initial/mod.rs` for module structure and SeaORM migration trait implementation.
- Use PostgreSQL `to_tsvector('english', column_name)` to generate tsvector values and create GIN indexes on the result.
- The migration should add a GIN index for each searchable column rather than a single combined index, to allow flexible query composition.
- Consider adding a stored generated tsvector column to each entity table if performance testing shows runtime tsvector generation is too slow, but start with expression indexes as the simpler approach.
- Per CONVENTIONS.md (repo-level): the project uses SeaORM for database operations. Follow the SeaORM migration pattern with `MigrationTrait` implementation.
  Applies: task creates `migration/src/m0002_search_indexes/mod.rs` matching the convention's migration file scope.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — existing migration module demonstrating the SeaORM MigrationTrait pattern, table creation, and index creation syntax to follow
- `common/src/db/query.rs` — shared query builder helpers; review to understand existing query patterns that the new indexes must support

## Acceptance Criteria
- [ ] A new migration module `m0002_search_indexes` exists and is registered in `migration/src/lib.rs`
- [ ] The migration creates GIN indexes on tsvector expressions for SBOM name, advisory title, and package name fields
- [ ] The migration is reversible (implements `down` to drop the indexes)
- [ ] The migration runs successfully against a PostgreSQL test database without errors

## Test Requirements
- [ ] Migration applies cleanly on a fresh database (run full migration suite)
- [ ] Migration rolls back cleanly (test `down` migration)
- [ ] Verify GIN indexes exist after migration by querying `pg_indexes` system catalog

## Verification Commands
- `cargo test -p migration` — migration compiles and tests pass
- `psql -c "SELECT indexname FROM pg_indexes WHERE indexname LIKE '%search%';"` — verify indexes created after migration

## Dependencies
- None (this is the foundational task)

<!-- [sdlc-workflow] Description digest: sha256-md:a83af7a0bdab29f0225329bf9eb0183d87b439ea6c4c288881bcc34b89f8d7d3 -->
