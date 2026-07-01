# Task 1 — Add full-text search indexes via database migration

## Repository
trustify-backend

## Target Branch
main

## Description
Create a SeaORM database migration that adds GIN indexes on tsvector columns for the SBOM, advisory, and package entities. This is the foundational performance improvement for TC-9002: without proper full-text search indexes, PostgreSQL falls back to sequential scans for text search queries, which is the most likely cause of the reported slow search performance.

The migration should add tsvector columns (if not already present) to the `sbom`, `advisory`, and `package` tables and create GIN indexes on those columns to enable efficient full-text search. A trigger or generated column should keep the tsvector in sync with the source text fields.

## Files to Modify
- `migration/src/lib.rs` — register the new migration module

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — migration that adds tsvector columns and GIN indexes to sbom, advisory, and package tables

## API Changes
- No API changes in this task (infrastructure only)

## Implementation Notes
- Follow the existing migration pattern established in `migration/src/m0001_initial/mod.rs` for migration structure and naming.
- Use SeaORM's migration framework (`sea_orm_migration::prelude::*`) for schema changes.
- Add GIN indexes using `Index::create().table(...).col(...).index_type(IndexType::Gin)` pattern.
- The tsvector columns should be generated columns or maintained via triggers that concatenate relevant text fields for each entity:
  - `sbom`: name, version, supplier fields from `entity/src/sbom.rs`
  - `advisory`: title, description, identifier fields from `entity/src/advisory.rs`
  - `package`: name, version, license fields from `entity/src/package.rs`
- Per CONVENTIONS.md: follow the established migration naming and structure conventions.
  Applies: task creates `migration/src/m0002_search_indexes/mod.rs` matching the convention's migration file scope.
- Per CONVENTIONS.md: if any foreign key columns are added, add corresponding indexes (per established migration patterns).
  Applies: task creates `migration/src/m0002_search_indexes/mod.rs` matching the convention's migration file scope.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — existing migration demonstrating the established migration pattern and SeaORM migration API usage
- `entity/src/sbom.rs` — SBOM entity definition showing the text fields available for tsvector generation
- `entity/src/advisory.rs` — Advisory entity definition showing available text fields
- `entity/src/package.rs` — Package entity definition showing available text fields

## Acceptance Criteria
- [ ] A new migration exists that adds tsvector columns to sbom, advisory, and package tables
- [ ] GIN indexes are created on all tsvector columns
- [ ] The tsvector columns are populated from relevant text fields in each entity
- [ ] The migration runs successfully against a clean database
- [ ] The migration runs successfully against an existing database (upgrade path)
- [ ] The migration is registered in `migration/src/lib.rs`

## Test Requirements
- [ ] Migration applies cleanly on a fresh PostgreSQL database
- [ ] Migration applies cleanly on a database with existing data (tsvector columns populated for existing rows)
- [ ] Migration rollback works correctly (down migration drops indexes and columns)

## Verification Commands
- `cargo test -p migration` — migration compiles and any migration tests pass

## Dependencies
- None (this is the first task)
