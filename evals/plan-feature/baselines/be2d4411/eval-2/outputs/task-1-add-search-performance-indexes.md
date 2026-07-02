## Repository
trustify-backend

## Target Branch
main

## Description
Add a database migration that creates indexes to improve search query performance. This
addresses the "search should be faster" requirement by adding GIN indexes for PostgreSQL
full-text search on text columns across SBOM, advisory, and package entities, and B-tree
indexes on commonly filtered columns (severity, timestamps). These indexes are a
prerequisite for the full-text search relevance scoring in the subsequent task.

**Ambiguity note:** No performance baseline or target latency was specified in the feature
description. This task assumes current slowness is due to missing indexes. Performance
targets are pending clarification from stakeholders (assumed sub-500ms p95).

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — SeaORM migration to add GIN indexes on tsvector columns for full-text search and B-tree indexes on severity and timestamp columns

## Files to Modify
- `migration/src/lib.rs` — register the new migration module `m0002_search_indexes` in the migration list

## Implementation Notes
- Follow the existing migration pattern established in `migration/src/m0001_initial/mod.rs` — use SeaORM's `MigrationTrait` with `up` and `down` methods.
- Create GIN indexes on text-searchable columns across SBOM, advisory, and package entities. Use `to_tsvector('english', column)` expressions for columns like advisory title/description, SBOM name, and package name.
- Create B-tree indexes on `severity` (advisory entity) and `created`/`modified` timestamp columns to support filter queries.
- Use `Index::create()` from SeaORM for all index definitions — follow the SeaORM index creation pattern.
- Reference entity definitions in `entity/src/sbom.rs`, `entity/src/advisory.rs`, and `entity/src/package.rs` to identify the correct column names.
- All handlers in this codebase return `Result<T, AppError>` — ensure the migration's error handling follows the same pattern using `.context()` wrapping from `common/src/error.rs`.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — established migration pattern showing SeaORM MigrationTrait implementation with up/down methods
- `entity/src/advisory.rs` — advisory entity definition with column names for severity and timestamp fields
- `entity/src/sbom.rs` — SBOM entity definition with searchable text columns

## Acceptance Criteria
- [ ] A new migration `m0002_search_indexes` exists and is registered in `migration/src/lib.rs`
- [ ] GIN indexes are created on tsvector expressions for text-searchable columns (advisory title/description, SBOM name, package name)
- [ ] B-tree indexes are created on advisory severity and entity timestamp columns
- [ ] Migration runs successfully against a PostgreSQL test database (both up and down)
- [ ] Existing search endpoint `GET /api/v2/search` continues to function without changes

## Test Requirements
- [ ] Migration `up` runs without errors on a clean database and on a database with existing data
- [ ] Migration `down` removes all created indexes without errors
- [ ] Verify indexes exist after migration using `\di` or equivalent query against the test database
- [ ] Existing integration tests in `tests/api/search.rs` continue to pass after migration

## Verification Commands
- `cargo test -p migration` — migration compiles and unit tests pass
- `cargo test -p tests --test search` — existing search integration tests pass

## Dependencies
- None

## additional_fields
- priority: Normal
- fixVersions: RHTPA 1.6.0
- labels: ai-generated-jira

[sdlc-workflow] Description digest: sha256-md:fd38b1c3907cf02969c980d12f8bef834bf9ff1da7a5b626452f4dbecc25f797
