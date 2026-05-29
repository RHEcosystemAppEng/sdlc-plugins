## Repository
trustify-backend

## Target Branch
main

## Description
Add PostgreSQL full-text search indexes (GIN indexes on tsvector columns) to the SBOM, advisory, and package entities to support efficient full-text search queries. This is a prerequisite for the search relevance improvements in subsequent tasks — without proper indexes, full-text search queries will perform sequential scans and degrade performance.

**Assumption (pending clarification):** The specific fields to index are inferred from the entity models since the feature description does not specify which fields users search by. SBOM name/description, advisory title/description, and package name/namespace are assumed to be the primary search fields based on the existing entity structure.

## Files to Modify
- `entity/src/sbom.rs` — add tsvector column definition to the SBOM entity
- `entity/src/advisory.rs` — add tsvector column definition to the advisory entity
- `entity/src/package.rs` — add tsvector column definition to the package entity

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — migration to add GIN indexes on tsvector columns for sbom, advisory, and package tables, and add a trigger to keep tsvector columns updated on INSERT/UPDATE

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for migration structure and registration
- Register the new migration in `migration/src/lib.rs`
- Use SeaORM's `ColumnDef` extension for tsvector column definitions, consistent with the entity pattern in `entity/src/sbom.rs`
- The tsvector columns should be populated via PostgreSQL triggers (using `tsvector_update_trigger` or a custom trigger function) to keep them in sync with the source text columns
- Use GIN index type for tsvector columns (standard PostgreSQL practice for full-text search)
- Per `common/src/db/query.rs`: the existing query builder helpers handle filtering and pagination — the new indexes will be consumed by the SearchService refactoring in Task 2

## Reuse Candidates
- `common/src/db/query.rs::query builder helpers` — existing query builder patterns for filtering and pagination that will work alongside the new indexes
- `migration/src/m0001_initial/mod.rs` — established migration structure to follow for the new migration module

## Acceptance Criteria
- [ ] A new SeaORM migration adds tsvector columns to sbom, advisory, and package tables
- [ ] GIN indexes are created on all tsvector columns
- [ ] PostgreSQL triggers keep tsvector columns in sync with source text columns on INSERT and UPDATE
- [ ] Migration runs successfully against a clean database and against an existing database (idempotent up migration)
- [ ] Existing integration tests in `tests/api/` continue to pass without modification

## Test Requirements
- [ ] Migration up/down executes without errors on a test PostgreSQL database
- [ ] Verify GIN indexes exist after migration via a SQL assertion or integration test
- [ ] Verify tsvector columns are populated correctly when inserting test data through existing SBOM/advisory/package endpoints
- [ ] All existing tests in `tests/api/sbom.rs`, `tests/api/advisory.rs`, and `tests/api/search.rs` pass (regression check)

## Documentation Updates
- `README.md` — document the new migration and any prerequisite PostgreSQL extensions (if pg_trgm or other extensions are needed)

[sdlc-workflow] Description digest: sha256:bc821cc57a6e39ea82db316a50bdcce414bbb26ff692ae3db095e600eb276dbe
