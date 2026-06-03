# Task 1 — Add full-text search migration for SBOM, advisory, and package entities

## Repository
trustify-backend

## Target Branch
main

## Description
Create a database migration that adds PostgreSQL full-text search support to the SBOM,
advisory, and package entities. This migration adds `tsvector` columns and GIN indexes
to enable efficient full-text search with relevance ranking, replacing the current
approach that likely uses LIKE/ILIKE pattern matching.

This is the foundational task for TC-9002 (Improve search experience). The indexes and
tsvector columns created here will be consumed by the SearchService refactor in Task 2.

## Files to Create
- `migration/src/m0002_fulltext_search/mod.rs` — migration module that adds tsvector columns and GIN indexes to sbom, advisory, and package tables

## Files to Modify
- `migration/src/lib.rs` — register the new migration module in the migration runner
- `entity/src/sbom.rs` — add the `search_vector` tsvector column to the SBOM SeaORM entity
- `entity/src/advisory.rs` — add the `search_vector` tsvector column to the advisory SeaORM entity
- `entity/src/package.rs` — add the `search_vector` tsvector column to the package SeaORM entity

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for structure and conventions.
- Use SeaORM's migration API to create the migration. The migration should:
  1. Add a `search_vector` column of type `tsvector` to each table (sbom, advisory, package)
  2. Create GIN indexes on each `search_vector` column for fast full-text search
  3. Create trigger functions that automatically update the `search_vector` column when relevant text columns are inserted or updated
- For SBOMs: index the name/title and description fields
- For advisories: index the title, description, and severity fields
- For packages: index the name and license fields
- Use `CREATE INDEX ... USING gin(search_vector)` for the GIN indexes
- The migration must be idempotent — use `IF NOT EXISTS` where appropriate
- Entity files (`entity/src/sbom.rs`, `entity/src/advisory.rs`, `entity/src/package.rs`) need a new field added to the SeaORM entity struct to represent the `search_vector` column. Follow the existing field patterns in those files.
- Per docs/constraints.md §2 (Commit Rules): commit messages must follow Conventional Commits, reference TC-9002, and include the Assisted-by trailer.
- Per docs/constraints.md §5 (Code Change Rules): inspect existing migration and entity code before modifying — do not guess the structure.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — existing migration module demonstrating the project's migration structure and SeaORM migration API usage
- `entity/src/sbom.rs` — existing entity definition showing the field declaration pattern to follow when adding the search_vector column

## Acceptance Criteria
- [ ] Migration creates `search_vector` tsvector columns on sbom, advisory, and package tables
- [ ] GIN indexes are created on all three `search_vector` columns
- [ ] Trigger functions automatically populate `search_vector` on INSERT and UPDATE
- [ ] Migration is registered in `migration/src/lib.rs`
- [ ] SeaORM entity structs are updated with the new `search_vector` field
- [ ] Migration runs successfully against a clean database and is idempotent

## Test Requirements
- [ ] Migration applies cleanly on a fresh database
- [ ] Migration is reversible (down migration drops the columns and indexes)
- [ ] Inserting a record into sbom/advisory/package automatically populates the search_vector column
- [ ] The GIN index is used by the query planner for tsquery searches (verify with EXPLAIN)

## Verification Commands
- `cargo run --bin migration -- up` — migration applies without errors
- `cargo run --bin migration -- down` — migration reverses cleanly

## Dependencies
- None (this is the foundational task)
