## Repository
trustify-backend

## Target Branch
main

## Description
Add database migration to create full-text search indexes on searchable text columns across SBOM, advisory, and package entities. This migration adds `tsvector` columns and GIN indexes to support PostgreSQL full-text search, improving search query performance.

**Ambiguity flag:** The feature does not specify which fields should be indexed for search. This task assumes (Assumption A2, A5) that the following fields are searchable: SBOM name/description, advisory title/description/severity, and package name/namespace. This assumption is pending clarification with the product owner.

**Assumption:** Performance improvement targets p95 search latency under 500ms (Assumption A1). Index design is based on this target. Actual performance thresholds must be confirmed before implementation.

## Files to Modify
- `migration/src/lib.rs` — register new migration module

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — migration adding tsvector columns and GIN indexes to sbom, advisory, and package tables

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for module structure and registration
- Use SeaORM migration framework to add:
  - A `search_vector` column of type `tsvector` to the `sbom`, `advisory`, and `package` tables
  - GIN indexes on each `search_vector` column for fast full-text search
  - A trigger or update mechanism to populate `search_vector` from source text columns (e.g., `name`, `description`)
- Reference `common/src/db/query.rs` for existing query patterns used in the project
- Per docs/constraints.md §5.2: inspect existing migration code before modifying — do not guess structure
- Per docs/constraints.md §2.1-2.3: use Conventional Commits format with Jira reference and AI attribution trailer

## Reuse Candidates
- `common/src/db/query.rs::QueryBuilder` — existing query builder helpers for filtering and pagination; may need extension to support tsvector queries
- `migration/src/m0001_initial/mod.rs` — reference migration pattern for module structure

## Acceptance Criteria
- [ ] Migration creates `search_vector` tsvector columns on sbom, advisory, and package tables
- [ ] GIN indexes are created on all `search_vector` columns
- [ ] Migration runs successfully against a fresh database and against an existing database (up and down)
- [ ] Existing search functionality is not broken by the migration (backward compatible)

## Test Requirements
- [ ] Migration up: verify tsvector columns and GIN indexes exist after migration
- [ ] Migration down: verify tsvector columns and indexes are removed on rollback
- [ ] Verify existing integration tests in `tests/api/search.rs` still pass after migration

## Verification Commands
- `cargo test -p migration` — migration compiles and unit tests pass
- `cargo test --test search` — existing search integration tests pass

## Dependencies
- None (this is the foundational task)

---

[sdlc-workflow] Description digest: sha256-md:526625b271abfc4135fd7f0c08a66156e1051e7f74cef83828268e22ce021db2
