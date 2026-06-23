## Repository
trustify-backend

## Target Branch
main

## Description
Create a database migration to add PostgreSQL full-text search indexes that will support relevance-ranked search across SBOMs, advisories, and packages. This migration adds tsvector columns and GIN indexes to enable efficient full-text search queries, replacing the current unoptimized search approach.

**Assumption pending clarification:** The specific fields to index for each entity are assumed based on the entity structure (name/title fields for SBOMs, title/description for advisories, name for packages). The product owner should confirm which fields are most important for search relevance.

**Assumption pending clarification:** The text search configuration is assumed to be `english`. If the platform serves multilingual content, the search configuration may need to be adjusted.

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — Migration to add tsvector columns and GIN indexes for full-text search on sbom, advisory, and package tables

## Files to Modify
- `migration/src/lib.rs` — Register the new migration module m0002_search_indexes

## Implementation Notes
- Follow the existing migration pattern established in `migration/src/m0001_initial/mod.rs`
- Use SeaORM migration framework to create the migration
- Add a `search_vector` column of type `tsvector` to the sbom, advisory, and package tables
- Create GIN indexes on the tsvector columns for efficient full-text search
- Add a trigger to automatically update the tsvector column when rows are inserted or updated
- The migration should be idempotent — use `IF NOT EXISTS` guards where appropriate

Per CONVENTIONS.md §Module pattern: follow the established migration directory structure.
Applies: task creates `migration/src/m0002_search_indexes/mod.rs` matching the convention's migration file scope.

## Acceptance Criteria
- [ ] Migration creates tsvector columns on sbom, advisory, and package tables
- [ ] GIN indexes are created on all tsvector columns
- [ ] Triggers are in place to auto-populate tsvector columns on insert/update
- [ ] Migration runs successfully against a clean database
- [ ] Migration is registered in `migration/src/lib.rs`
- [ ] Existing data is not lost or corrupted by the migration

## Test Requirements
- [ ] Migration applies cleanly to an empty database (forward migration)
- [ ] Migration applies cleanly to a database with existing data (existing rows get tsvector populated)

## Verification Commands
- `cargo run --bin migration -- up` — migration applies without errors

## Dependencies
None

[sdlc-workflow] Description digest: sha256-md:82c28ab53ddc88ebd5af1bfc6f402d881d3a6f5984dd982b52a49f4912cb5f12
