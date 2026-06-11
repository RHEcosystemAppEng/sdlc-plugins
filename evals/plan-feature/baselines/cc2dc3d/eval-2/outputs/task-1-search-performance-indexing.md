## Repository
trustify-backend

## Target Branch
main

## Description
Add database indexes on searchable text columns to improve search query performance. The current search is reported as "too slow" (TC-9002). This task adds GIN indexes for full-text search vectors on the primary searchable entities (sbom, advisory, package) and a B-tree index on commonly filtered columns. This lays the groundwork for the full-text search implementation in Task 2.

**Assumption (pending clarification):** Target search response time is under 500ms at p95. No explicit performance SLA was provided in the feature description.

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — new migration adding GIN indexes on tsvector columns and B-tree indexes on frequently filtered columns (severity, created_at) for sbom, advisory, and package entities

## Files to Modify
- `migration/src/lib.rs` — register the new m0002_search_indexes migration module
- `entity/src/sbom.rs` — add a `search_vector` column (tsvector type) to the SBOM entity for full-text search indexing
- `entity/src/advisory.rs` — add a `search_vector` column (tsvector type) to the Advisory entity
- `entity/src/package.rs` — add a `search_vector` column (tsvector type) to the Package entity

## Implementation Notes
- Follow the existing migration pattern established in `migration/src/m0001_initial/mod.rs`. Create a new migration module `m0002_search_indexes` under `migration/src/`.
- Use SeaORM's migration API to add `tsvector` columns and GIN indexes. The tsvector columns should be populated via a trigger or a generated column that concatenates the relevant text fields (e.g., for SBOMs: name, document_id; for advisories: title, synopsis; for packages: name, version).
- Add B-tree indexes on `advisory.severity` and timestamp columns used for date range filtering.
- Register the migration in `migration/src/lib.rs` following the pattern used for `m0001_initial`.
- The entity definitions in `entity/src/` use SeaORM derive macros. Add the `search_vector` field with appropriate SeaORM column type annotation.
- Per the repository's error handling convention: all fallible operations should return `Result<T, AppError>` with `.context()` wrapping.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — demonstrates the established migration pattern (table creation, column definitions, index creation) to follow for the new migration
- `common/src/db/query.rs` — contains shared query builder helpers; review for any existing index-related utilities

## Acceptance Criteria
- [ ] A new migration `m0002_search_indexes` exists and runs successfully against a clean database
- [ ] GIN indexes are created on `search_vector` columns for sbom, advisory, and package tables
- [ ] B-tree indexes are created on severity and timestamp columns
- [ ] Entity structs include the `search_vector` field
- [ ] Existing tests continue to pass (no regression)

## Test Requirements
- [ ] Migration runs forward successfully on a clean database
- [ ] Migration runs forward successfully on an existing database (incremental)
- [ ] Verify indexes exist after migration using a SQL query against `pg_indexes`
- [ ] Existing integration tests in `tests/api/search.rs`, `tests/api/sbom.rs`, and `tests/api/advisory.rs` still pass

## Verification Commands
- `cargo test` — all existing tests pass without regression
- `sea-orm-cli migrate up` — migration applies successfully

## Dependencies
- None
