# Task 1 — Add full-text search database migration

## Repository
trustify-backend

## Target Branch
main

## Description
Create a database migration that adds PostgreSQL full-text search infrastructure to the
sbom, advisory, and package tables. This migration adds `tsvector` columns with automatic
trigger-based population and GIN indexes to enable efficient full-text search with
relevance-based ranking. This replaces the implicit reliance on `LIKE`/`ILIKE` pattern
matching with a purpose-built search infrastructure.

This is the foundational task for TC-9002 (Improve search experience). The tsvector
columns and GIN indexes created here will be consumed by the SearchService refactor
in Task 2.

## Files to Create
- `migration/src/m0002_fulltext_search/mod.rs` — migration module that adds tsvector columns, trigger functions, and GIN indexes to sbom, advisory, and package tables

## Files to Modify
- `migration/src/lib.rs` — register the new m0002_fulltext_search migration module in the migration runner
- `entity/src/sbom.rs` — add `search_vector` tsvector column to the SBOM SeaORM entity definition
- `entity/src/advisory.rs` — add `search_vector` tsvector column to the advisory SeaORM entity definition
- `entity/src/package.rs` — add `search_vector` tsvector column to the package SeaORM entity definition

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for module structure, naming, and SeaORM migration API usage.
- The migration should:
  1. Add a `search_vector` column of type `tsvector` to each table (sbom, advisory, package)
  2. Create trigger functions that automatically update `search_vector` when relevant text columns are inserted or updated
  3. Create GIN indexes on each `search_vector` column using `CREATE INDEX ... USING gin(search_vector)`
  4. Backfill `search_vector` for any existing rows
- Text fields to index per entity:
  - **sbom**: name/title and description fields
  - **advisory**: title, description, and severity fields
  - **package**: name and license fields
- The migration must be idempotent — use `IF NOT EXISTS` guards where appropriate.
- Entity files (`entity/src/sbom.rs`, `entity/src/advisory.rs`, `entity/src/package.rs`) need a new `search_vector` field added to their SeaORM entity structs. Follow the existing field declaration patterns in those files.
- Per docs/constraints.md §2 (Commit Rules): commit messages must follow Conventional Commits format, reference TC-9002 in the footer, and include the `Assisted-by: Claude Code` trailer.
- Per docs/constraints.md §5 (Code Change Rules): inspect existing migration and entity code before modifying — do not guess the structure.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — existing migration module demonstrating the project's migration structure, SeaORM migration API usage, and up/down migration pattern
- `entity/src/sbom.rs` — existing entity definition showing the field declaration pattern to follow when adding the search_vector column
- `entity/src/advisory.rs` — existing entity definition with severity field showing the struct field pattern

## Acceptance Criteria
- [ ] Migration creates `search_vector` tsvector columns on sbom, advisory, and package tables
- [ ] GIN indexes are created on all three `search_vector` columns
- [ ] Trigger functions automatically populate `search_vector` on INSERT and UPDATE of text fields
- [ ] Existing rows are backfilled with tsvector values during migration
- [ ] Migration is registered in `migration/src/lib.rs`
- [ ] SeaORM entity structs in `entity/src/` are updated with the new `search_vector` field
- [ ] Migration runs successfully against a clean database and is idempotent

## Test Requirements
- [ ] Migration applies cleanly on a fresh database without errors
- [ ] Migration is reversible (down migration drops the tsvector columns, triggers, and GIN indexes)
- [ ] Inserting a record into sbom/advisory/package automatically populates the search_vector column via the trigger
- [ ] The GIN index is used by the query planner for tsquery searches (verify with EXPLAIN)

## Verification Commands
- `cargo run --bin migration -- up` — migration applies without errors
- `cargo run --bin migration -- down` — migration reverses cleanly

## Dependencies
- None (this is the foundational task)
