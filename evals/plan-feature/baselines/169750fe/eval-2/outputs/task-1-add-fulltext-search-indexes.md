## Repository
trustify-backend

## Target Branch
main

## Description
Add PostgreSQL full-text search indexes to SBOM, advisory, and package entities to support faster and more relevant search queries. This replaces the current implicit LIKE/ILIKE pattern matching with GIN-indexed `tsvector` columns, enabling PostgreSQL's built-in full-text search engine.

**Assumption (pending clarification):** Indexes are created on name/title, description, and identifier fields for each entity type. Exact fields may need adjustment after stakeholder review.

## Files to Modify
- `entity/src/sbom.rs` — add `search_vector` tsvector column to SBOM entity
- `entity/src/advisory.rs` — add `search_vector` tsvector column to Advisory entity
- `entity/src/package.rs` — add `search_vector` tsvector column to Package entity

## Files to Create
- `migration/src/m0002_fulltext_search_indexes/mod.rs` — migration to add tsvector columns, GIN indexes, and trigger functions for automatic tsvector population

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` — register the new migration in `migration/src/lib.rs`.
- Use SeaORM's `ColumnDef` to define the new `tsvector` column type on each entity. Reference the existing entity definitions in `entity/src/sbom.rs`, `entity/src/advisory.rs`, and `entity/src/package.rs` for the established column definition pattern.
- Create a GIN index on each `search_vector` column for fast full-text search lookups.
- Add a PostgreSQL trigger function to automatically update the `search_vector` column on INSERT and UPDATE using `tsvector_update_trigger` or a custom function with field weighting (`setweight`).
- **Assumption (pending clarification):** Use 'english' text search configuration. Field weights: title/name = A, description = B, identifiers = C.
- Per CONVENTIONS.md §Migration Patterns: add `Index::create()` for all FK columns.
  Applies: task modifies `migration/src/m0002_fulltext_search_indexes/mod.rs` matching the convention's migration file scope.

## Acceptance Criteria
- [ ] A new migration creates `search_vector` tsvector columns on SBOM, advisory, and package tables
- [ ] GIN indexes are created on all `search_vector` columns
- [ ] Trigger functions automatically populate `search_vector` on INSERT and UPDATE
- [ ] Migration runs successfully against a clean database and an existing database with data
- [ ] Existing SBOM, advisory, and package entity definitions compile with the new column

## Test Requirements
- [ ] Migration applies cleanly on an empty test database
- [ ] Migration applies cleanly on a database with existing data (backfill populates search vectors)
- [ ] Inserting a new SBOM/advisory/package automatically populates the search_vector column
- [ ] Updating a searchable field on an existing record updates the search_vector column

## Dependencies
- None (this is the foundational task)
