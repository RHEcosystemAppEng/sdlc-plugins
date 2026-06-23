# Task 1 — Add full-text search database migration

## Repository
trustify-backend

## Target Branch
main

## Description
Create a database migration that adds PostgreSQL full-text search infrastructure to the searchable entity tables (sbom, advisory, package). This migration adds tsvector columns and GIN indexes to support efficient full-text search with relevance ranking, replacing any existing naive text matching. This is a prerequisite for the search service optimization in Task 2.

**Ambiguity note (assumption pending clarification):** The feature description does not specify which entity fields should be searchable or how they should be weighted. We assume: SBOM name/description, Advisory title/description/severity, and Package name/license are the searchable fields. Stakeholders should confirm the field set before implementation.

## Files to Modify
- `migration/src/lib.rs` — register the new migration module

## Files to Create
- `migration/src/m0002_search_fulltext/mod.rs` — migration that adds tsvector columns and GIN indexes to sbom, advisory, and package tables; adds trigger functions to keep tsvector columns in sync on INSERT/UPDATE

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for module structure and SeaORM migration trait implementation.
- Add a `search_vector` column of type `tsvector` to the `sbom`, `advisory`, and `package` tables.
- Create GIN indexes on each `search_vector` column for efficient full-text search (e.g., `CREATE INDEX idx_sbom_search ON sbom USING GIN(search_vector)`).
- Add PostgreSQL trigger functions that automatically populate `search_vector` on INSERT and UPDATE using `to_tsvector('english', coalesce(field1, '') || ' ' || coalesce(field2, ''))`.
- Include a backfill statement to populate `search_vector` for existing rows.
- Per `docs/constraints.md` §2 (Commit Rules): commit must reference TC-9002 in the footer, use Conventional Commits format, and include `--trailer="Assisted-by: Claude Code"`.
- Per `docs/constraints.md` §5.1 (Code Change Rules): changes must be scoped to the files listed above.

### Convention applicability
- Per CONVENTIONS.md §Module pattern: follow `model/ + service/ + endpoints/` structure for any new domain modules.
  Applies: task creates `migration/src/m0002_search_fulltext/mod.rs` matching the convention's migration file scope.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — existing migration module demonstrating SeaORM migration structure, naming conventions, and registration pattern

## Acceptance Criteria
- [ ] A new migration module `m0002_search_fulltext` is created and registered in `migration/src/lib.rs`
- [ ] The migration adds `search_vector` (tsvector) columns to `sbom`, `advisory`, and `package` tables
- [ ] GIN indexes are created on all `search_vector` columns
- [ ] Trigger functions are defined to keep `search_vector` in sync on INSERT/UPDATE
- [ ] Existing rows are backfilled with tsvector data
- [ ] The migration runs successfully against a PostgreSQL test database (forward migration)

## Test Requirements
- [ ] Verify the migration applies cleanly to a fresh database using the project's migration tooling
- [ ] Verify that inserting a row into each table populates the `search_vector` column via the trigger
- [ ] Verify that updating a searchable field on an existing row updates the `search_vector` column

## Verification Commands
- `cargo test -p migration` — migration tests pass
- `sea-orm-cli migrate up` — migration applies without errors

## Dependencies
- None (this is the first task)

[sdlc-workflow] Description digest: sha256-md:9243a71c2b3214cc0098dc5bd64a7cb81a32b4a85d20952977128d10f9a03ca8
