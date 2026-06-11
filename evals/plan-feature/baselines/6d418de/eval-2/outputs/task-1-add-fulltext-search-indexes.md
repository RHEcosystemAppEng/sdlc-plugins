# Task 1 — Add full-text search indexes via database migration

## Repository
trustify-backend

## Target Branch
main

## Description
Create a new SeaORM database migration that adds GIN indexes for full-text search on the key searchable columns across the sbom, advisory, and package tables. This migration lays the groundwork for ranked full-text search by adding `tsvector` generated columns and corresponding GIN indexes, enabling PostgreSQL's built-in full-text search capabilities to be used efficiently by the SearchService.

Currently, the `SearchService` in `modules/search/src/service/mod.rs` performs full-text search across entities, but without dedicated full-text indexes the queries rely on sequential scans or basic LIKE/ILIKE patterns, which degrade as data grows.

## Files to Modify
- `migration/src/lib.rs` — Register the new migration module in the migration runner

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — Migration that adds tsvector columns and GIN indexes to sbom, advisory, and package tables

## Implementation Notes
- Follow the existing migration pattern established in `migration/src/m0001_initial/mod.rs` for module structure and naming convention
- The migration should add `tsvector` generated columns on searchable text fields:
  - `sbom` table: index on name/description fields
  - `advisory` table: index on title/description/identifier fields
  - `package` table: index on name/namespace fields
- Use `CREATE INDEX ... USING gin(...)` for each tsvector column
- The migration should be idempotent (use `IF NOT EXISTS` guards)
- Framework: SeaORM migrations — use the `sea_orm_migration::prelude::*` imports
- Per docs/constraints.md section 2 (Commit Rules): commit must reference TC-9002 and follow Conventional Commits format
- Per docs/constraints.md section 5 (Code Change Rules): inspect the existing migration code before writing new code

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — Existing migration module demonstrating the SeaORM migration pattern, table creation approach, and module registration

## Acceptance Criteria
- [ ] New migration module `m0002_search_indexes` exists and is registered in `migration/src/lib.rs`
- [ ] GIN indexes are created on tsvector columns for sbom, advisory, and package tables
- [ ] Migration runs successfully against a PostgreSQL database without errors
- [ ] Migration is idempotent — running it twice does not fail
- [ ] Existing data and queries are not affected (backward compatible)

## Test Requirements
- [ ] Migration applies cleanly on a fresh database (full migration run from scratch)
- [ ] Migration applies cleanly on a database that already has m0001_initial applied
- [ ] Rollback/down migration drops the indexes and tsvector columns cleanly

## Verification Commands
- `cargo run -p migration -- up` — migration completes without errors
- `psql -c "\di" | grep search` — GIN indexes appear in the index listing

## Dependencies
- None
